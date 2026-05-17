"""Lid (anketa) handlerlari."""
import logging
import re

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.db import get_session
from bot.db.repository import (
    create_lead,
    get_apartment,
    get_or_create_user,
    get_user_language,
)
from bot.keyboards.common import main_menu, remove_kb, share_phone_kb
from bot.keyboards.lead import payment_kb, rooms_interest_kb, skip_kb
from bot.locales import t
from bot.states.states import LeadStates
from bot.utils.formatter import format_money

router = Router(name="lead")
logger = logging.getLogger(__name__)


PHONE_REGEX = re.compile(r"^\+?\d[\d\s\-()]{7,20}$")


def _normalize_phone(raw: str) -> str | None:
    cleaned = raw.strip()
    digits = "".join(c for c in cleaned if c.isdigit() or c == "+")
    if not digits:
        return None
    only_digits = digits.lstrip("+")
    if len(only_digits) < 9 or len(only_digits) > 15:
        return None
    if digits.startswith("+"):
        return "+" + only_digits
    if only_digits.startswith("998"):
        return "+" + only_digits
    if len(only_digits) == 9:
        return "+998" + only_digits
    return "+" + only_digits


@router.callback_query(F.data.startswith("lead:start"))
async def cb_lead_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Anketani boshlash."""
    await state.clear()

    parts = callback.data.split(":")
    source = parts[2] if len(parts) > 2 else "manual"
    apartment_id = None
    if source == "apt" and len(parts) > 3:
        try:
            apartment_id = int(parts[3])
        except ValueError:
            apartment_id = None
    elif source == "calc" and len(parts) > 3:
        try:
            apartment_id = int(parts[3]) or None
        except ValueError:
            apartment_id = None

    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)

    await state.update_data(apartment_id=apartment_id, source=source)
    await state.set_state(LeadStates.waiting_name)

    try:
        await callback.message.answer(
            t("lead_collect_intro", language), parse_mode="HTML"
        )
    except TelegramBadRequest:
        pass

    await callback.message.answer(t("lead_ask_name", language), reply_markup=remove_kb())
    await callback.answer()


@router.message(LeadStates.waiting_name)
async def lead_name(message: Message, state: FSMContext) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)

    name = (message.text or "").strip()
    if len(name) < 2:
        await message.answer(t("lead_ask_name", language))
        return

    await state.update_data(full_name=name)
    await state.set_state(LeadStates.waiting_phone)
    await message.answer(
        t("lead_ask_phone", language),
        reply_markup=share_phone_kb(language),
        parse_mode="HTML",
    )


@router.message(LeadStates.waiting_phone, F.contact)
async def lead_phone_contact(message: Message, state: FSMContext) -> None:
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone
    await _continue_after_phone(message, state, phone)


@router.message(LeadStates.waiting_phone)
async def lead_phone_text(message: Message, state: FSMContext) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)

    normalized = _normalize_phone(message.text or "")
    if normalized is None:
        await message.answer(t("lead_invalid_phone", language), parse_mode="HTML")
        return

    await _continue_after_phone(message, state, normalized)


async def _continue_after_phone(
    message: Message, state: FSMContext, phone: str
) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)

    await state.update_data(phone=phone)

    data = await state.get_data()
    if data.get("apartment_id"):
        await state.update_data(rooms_interest=None)
        await state.set_state(LeadStates.waiting_payment)
        await message.answer(
            t("lead_ask_payment", language),
            reply_markup=payment_kb(language),
            parse_mode="HTML",
        )
    else:
        await state.set_state(LeadStates.waiting_rooms)
        await message.answer(
            t("lead_ask_rooms", language),
            reply_markup=rooms_interest_kb(language),
            parse_mode="HTML",
        )


@router.callback_query(LeadStates.waiting_rooms, F.data.startswith("lead:rooms:"))
async def lead_rooms(callback: CallbackQuery, state: FSMContext) -> None:
    rooms_value = int(callback.data.split(":")[2])
    rooms = rooms_value if rooms_value > 0 else None

    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)

    await state.update_data(rooms_interest=rooms)
    await state.set_state(LeadStates.waiting_payment)

    try:
        await callback.message.edit_text(
            t("lead_ask_payment", language),
            reply_markup=payment_kb(language),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        await callback.message.answer(
            t("lead_ask_payment", language),
            reply_markup=payment_kb(language),
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(LeadStates.waiting_payment, F.data.startswith("lead:pay:"))
async def lead_payment(callback: CallbackQuery, state: FSMContext) -> None:
    payment_type = callback.data.split(":")[2]

    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)

    await state.update_data(payment_type=payment_type)
    await state.set_state(LeadStates.waiting_notes)

    try:
        await callback.message.edit_text(
            t("lead_ask_notes", language),
            reply_markup=skip_kb(language),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        await callback.message.answer(
            t("lead_ask_notes", language),
            reply_markup=skip_kb(language),
            parse_mode="HTML",
        )
    await callback.answer()


@router.callback_query(LeadStates.waiting_notes, F.data == "lead:skip")
async def lead_skip_notes(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await state.update_data(notes=None)
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        pass
    await _finalize_lead(callback.from_user, state, bot, callback.message)
    await callback.answer()


@router.message(LeadStates.waiting_notes)
async def lead_notes(message: Message, state: FSMContext, bot: Bot) -> None:
    notes = (message.text or "").strip()
    if len(notes) > 1000:
        notes = notes[:1000]
    await state.update_data(notes=notes)
    await _finalize_lead(message.from_user, state, bot, message)


async def _finalize_lead(tg_user, state: FSMContext, bot: Bot, message) -> None:
    data = await state.get_data()
    await state.clear()

    async with get_session() as session:
        language = await get_user_language(session, tg_user.id)
        user = await get_or_create_user(
            session,
            tg_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
        )
        user.phone = data.get("phone") or user.phone

        lead = await create_lead(
            session,
            user_id=user.id,
            apartment_id=data.get("apartment_id"),
            full_name=data.get("full_name"),
            phone=data.get("phone"),
            rooms_interest=data.get("rooms_interest"),
            payment_type=data.get("payment_type"),
            notes=data.get("notes"),
            source=data.get("source") or "bot",
        )

        # Xonadon ma'lumotini olamiz (notification uchun)
        apartment = None
        if lead.apartment_id:
            apartment = await get_apartment(session, lead.apartment_id)

    # Mijozga tasdiq
    await message.answer(
        t(
            "lead_success",
            language,
            name=data.get("full_name", ""),
            phone=data.get("phone", ""),
        ),
        reply_markup=main_menu(language),
        parse_mode="HTML",
    )

    # Adminlarga xabar yuborish
    await _notify_managers(bot, lead, user, apartment, data)


async def _notify_managers(bot: Bot, lead, user, apartment, data: dict) -> None:
    payment_map = {
        "cash": "💵 100% naqd",
        "installment": "📅 Bo'lib-bo'lib (foizsiz)",
        "mortgage": "🏦 Bank ipotekasi",
        "undecided": "🤔 Hali aniq emas",
    }

    text_parts = [
        "🔔 <b>YANGI LID!</b>",
        "",
        f"👤 Ism: <b>{lead.full_name or '—'}</b>",
        f"📱 Telefon: <code>{lead.phone or '—'}</code>",
    ]

    if user.username:
        text_parts.append(f"💬 Telegram: @{user.username}")
    text_parts.append(f"🆔 TG ID: <code>{user.tg_id}</code>")

    if apartment:
        text_parts.extend(
            [
                "",
                f"🏡 <b>Xonadon:</b> {apartment.title}",
                f"📐 Maydon: {apartment.area:.1f} m²",
                f"🚪 Xonalar: {apartment.rooms}",
                f"💰 Narx: {format_money(apartment.price_total)}",
            ]
        )
    elif lead.rooms_interest:
        text_parts.append(f"🚪 Qiziqayotgan: {lead.rooms_interest} xonali")
    else:
        text_parts.append("🚪 Qiziqayotgan: aniqlanmagan")

    if lead.payment_type:
        text_parts.append(f"💳 To'lov turi: {payment_map.get(lead.payment_type, lead.payment_type)}")

    if lead.notes:
        text_parts.extend(["", f"📝 Izoh: <i>{lead.notes}</i>"])

    text_parts.extend(
        [
            "",
            f"📅 Sana: {lead.created_at.strftime('%d.%m.%Y %H:%M')}",
            f"🔢 Lid #{lead.id}",
        ]
    )

    text = "\n".join(text_parts)

    recipients = set(settings.admin_ids_list)
    if settings.manager_id:
        recipients.add(settings.manager_id)

    for chat_id in recipients:
        try:
            await bot.send_message(chat_id, text, parse_mode="HTML")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Lid xabarini yuborib bo'lmadi (%s): %s", chat_id, exc)
