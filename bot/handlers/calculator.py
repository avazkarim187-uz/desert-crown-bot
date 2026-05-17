"""Kalkulyator handlerlari."""
import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.db import get_session
from bot.db.repository import (
    get_apartment,
    get_or_create_user,
    get_user_language,
    list_apartments,
    log_calculator_use,
)
from bot.keyboards.calculator import (
    calc_apartments_kb,
    calc_result_kb,
    down_payment_kb,
    term_kb,
)
from bot.locales import t
from bot.states.states import CalculatorStates
from bot.utils.formatter import (
    calculate_monthly_payment_zero_interest,
    format_area,
    format_money,
)

router = Router(name="calculator")
logger = logging.getLogger(__name__)


async def _start_calc(message_or_cb, language) -> None:
    """Kalkulyatorni boshlash — xonadon tanlash yoki narx kiritish."""
    async with get_session() as session:
        apartments = await list_apartments(session)

    target = (
        message_or_cb if isinstance(message_or_cb, Message) else message_or_cb.message
    )

    if apartments:
        kb = calc_apartments_kb(list(apartments), language)
        text = t("calc_intro", language) + "\n\n" + t("calc_choose_apartment", language)
        try:
            if isinstance(message_or_cb, Message):
                await target.answer(text, reply_markup=kb, parse_mode="HTML")
            else:
                await target.edit_text(text, reply_markup=kb, parse_mode="HTML")
        except TelegramBadRequest:
            await target.answer(text, reply_markup=kb, parse_mode="HTML")
    else:
        # To'g'ridan-to'g'ri narx kiritishni so'raymiz
        await target.answer(t("calc_enter_price", language), parse_mode="HTML")


@router.message(F.text.in_({"💰 To'lov kalkulyatori", "💰 Калькулятор"}))
async def menu_calculator(message: Message, state: FSMContext) -> None:
    await state.clear()
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)
    await _start_calc(message, language)


@router.callback_query(F.data == "calc:restart")
async def cb_calc_restart(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)
    await _start_calc(callback, language)
    await callback.answer()


@router.callback_query(F.data.startswith("calc:apt:"))
async def cb_choose_apartment(callback: CallbackQuery, state: FSMContext) -> None:
    apt_value = callback.data.split(":")[2]

    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)

    if apt_value == "custom":
        await state.set_state(CalculatorStates.waiting_price)
        try:
            await callback.message.edit_text(
                t("calc_enter_price", language), parse_mode="HTML"
            )
        except TelegramBadRequest:
            await callback.message.answer(t("calc_enter_price", language), parse_mode="HTML")
        await callback.answer()
        return

    apartment_id = int(apt_value)
    async with get_session() as session:
        apartment = await get_apartment(session, apartment_id)

    if apartment is None:
        await callback.answer(t("error", language), show_alert=True)
        return

    await state.update_data(
        apartment_id=apartment.id,
        price=apartment.price_total,
        area=apartment.area,
    )

    try:
        await callback.message.edit_text(
            t("calc_choose_down_payment", language),
            reply_markup=down_payment_kb(language),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        await callback.message.answer(
            t("calc_choose_down_payment", language),
            reply_markup=down_payment_kb(language),
            parse_mode="HTML",
        )
    await callback.answer()


@router.message(CalculatorStates.waiting_price)
async def calc_input_price(message: Message, state: FSMContext) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)

    cleaned = "".join(c for c in (message.text or "") if c.isdigit())
    if not cleaned:
        await message.answer(t("calc_invalid_number", language))
        return

    price = int(cleaned)
    if price < 1_000_000 or price > 100_000_000_000:
        await message.answer(t("calc_invalid_range", language))
        return

    await state.update_data(apartment_id=None, price=price, area=None)
    await message.answer(
        t("calc_choose_down_payment", language),
        reply_markup=down_payment_kb(language),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("calc:dp:"))
async def cb_choose_down_payment(callback: CallbackQuery, state: FSMContext) -> None:
    dp_value = callback.data.split(":")[2]

    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)

    if dp_value == "custom":
        await state.set_state(CalculatorStates.waiting_custom_dp)
        try:
            await callback.message.edit_text(
                t("calc_enter_custom_percent", language)
            )
        except TelegramBadRequest:
            await callback.message.answer(t("calc_enter_custom_percent", language))
        await callback.answer()
        return

    await state.update_data(down_payment_percent=int(dp_value))

    try:
        await callback.message.edit_text(
            t("calc_choose_term", language),
            reply_markup=term_kb(language),
            parse_mode="HTML",
        )
    except TelegramBadRequest:
        await callback.message.answer(
            t("calc_choose_term", language),
            reply_markup=term_kb(language),
            parse_mode="HTML",
        )
    await callback.answer()


@router.message(CalculatorStates.waiting_custom_dp)
async def calc_input_custom_dp(message: Message, state: FSMContext) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)

    text = (message.text or "").strip().rstrip("%")
    try:
        pct = int(text)
    except ValueError:
        await message.answer(t("calc_invalid_number", language))
        return

    if not 0 <= pct <= 100:
        await message.answer(t("calc_invalid_range", language))
        return

    await state.update_data(down_payment_percent=pct)
    await message.answer(
        t("calc_choose_term", language),
        reply_markup=term_kb(language),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("calc:term:"))
async def cb_choose_term(callback: CallbackQuery, state: FSMContext) -> None:
    term_value = callback.data.split(":")[2]

    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)

    if term_value == "custom":
        await state.set_state(CalculatorStates.waiting_custom_term)
        try:
            await callback.message.edit_text(
                t("calc_enter_custom_term", language)
            )
        except TelegramBadRequest:
            await callback.message.answer(t("calc_enter_custom_term", language))
        await callback.answer()
        return

    await state.update_data(term_months=int(term_value))
    await _send_result(callback, state, language, edit=True)
    await callback.answer()


@router.message(CalculatorStates.waiting_custom_term)
async def calc_input_custom_term(message: Message, state: FSMContext) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)

    text = (message.text or "").strip()
    try:
        months = int(text)
    except ValueError:
        await message.answer(t("calc_invalid_number", language))
        return

    if not 1 <= months <= 240:
        await message.answer(t("calc_invalid_range", language))
        return

    await state.update_data(term_months=months)
    await _send_result(message, state, language, edit=False)


async def _send_result(
    message_or_cb, state: FSMContext, language, edit: bool
) -> None:
    data = await state.get_data()
    price = data.get("price")
    dp_pct = data.get("down_payment_percent", 0)
    term = data.get("term_months", 60)
    apartment_id = data.get("apartment_id")
    area = data.get("area")

    if not price or not term:
        return

    calc = calculate_monthly_payment_zero_interest(price, dp_pct, term)

    async with get_session() as session:
        user = await get_or_create_user(
            session,
            tg_id=message_or_cb.from_user.id,
            username=message_or_cb.from_user.username,
            first_name=message_or_cb.from_user.first_name,
            last_name=message_or_cb.from_user.last_name,
        )
        await log_calculator_use(
            session,
            user_id=user.id,
            price=price,
            down_payment_percent=dp_pct,
            term_months=term,
            monthly_payment=calc["monthly_payment"],
            apartment_id=apartment_id,
        )

    result_text = t(
        "calc_result",
        language,
        price=format_money(price),
        area=format_area(area) if area else "—",
        down_pct=dp_pct,
        down_payment=format_money(calc["down_payment"]),
        term=term,
        monthly=format_money(calc["monthly_payment"]),
        total=format_money(calc["total_paid"]),
    )

    target = (
        message_or_cb if isinstance(message_or_cb, Message) else message_or_cb.message
    )
    kb = calc_result_kb(apartment_id, language)

    if edit and not isinstance(message_or_cb, Message):
        try:
            await target.edit_text(result_text, reply_markup=kb, parse_mode="HTML")
        except TelegramBadRequest:
            await target.answer(result_text, reply_markup=kb, parse_mode="HTML")
    else:
        await target.answer(result_text, reply_markup=kb, parse_mode="HTML")

    await state.clear()
