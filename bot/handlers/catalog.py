"""Katalog handlerlari."""
import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message
from aiogram.exceptions import TelegramBadRequest

from bot.db import get_session
from bot.db.repository import get_apartment, get_user_language, list_apartments
from bot.keyboards.catalog import (
    apartment_card_kb,
    apartment_list_kb,
    rooms_filter_kb,
)
from bot.locales import t
from bot.utils.formatter import (
    calculate_monthly_payment_zero_interest,
    format_area,
    format_money,
)

router = Router(name="catalog")
logger = logging.getLogger(__name__)


@router.message(F.text.in_({"🏢 Xonadonlarni ko'rish", "🏢 Посмотреть квартиры"}))
async def menu_catalog(message: Message) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)
    await message.answer(
        t("catalog_choose_rooms", language),
        reply_markup=rooms_filter_kb(language),
    )


@router.callback_query(F.data.startswith("cat:rooms:"))
async def cb_filter_rooms(callback: CallbackQuery) -> None:
    rooms_value = int(callback.data.split(":")[2])
    rooms = rooms_value if rooms_value > 0 else None

    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)
        apartments = await list_apartments(session, rooms=rooms)

    if not apartments:
        await callback.message.edit_text(
            t("catalog_empty", language),
            reply_markup=rooms_filter_kb(language),
        )
        await callback.answer()
        return

    title = (
        f"<b>{len(apartments)} ta xonadon topildi</b>\n\n"
        f"Quyidagi ro'yxatdan tanlang:"
    )
    await callback.message.edit_text(
        title,
        reply_markup=apartment_list_kb(list(apartments), language),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cat:show:"))
async def cb_show_apartment(callback: CallbackQuery) -> None:
    apartment_id = int(callback.data.split(":")[2])

    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)
        apartment = await get_apartment(session, apartment_id)

    if apartment is None:
        await callback.answer(t("error", language), show_alert=True)
        return

    # Hisoblar (20% boshlang'ich + 60 oy)
    calc = calculate_monthly_payment_zero_interest(
        apartment.price_total, 20, 60
    )
    floors = "—"
    if apartment.floor_min and apartment.floor_max:
        floors = f"{apartment.floor_min}-{apartment.floor_max}"
    elif apartment.floor_min:
        floors = str(apartment.floor_min)

    description = (
        apartment.description_uz if language.value == "uz" else apartment.description_ru
    ) or ""

    card_text = t(
        "apartment_card",
        language,
        title=apartment.title,
        area=f"{apartment.area:.1f}",
        rooms=apartment.rooms,
        floors=floors,
        price=format_money(apartment.price_total),
        price_per_m2=format_money(
            apartment.price_per_m2 or int(apartment.price_total / apartment.area)
        ),
        down_payment_20=format_money(calc["down_payment"]),
        monthly_60_20=format_money(calc["monthly_payment"]),
        description=description,
    )

    keyboard = apartment_card_kb(apartment, language)

    if apartment.plan_image:
        from pathlib import Path

        plan_path = Path(apartment.plan_image)
        if plan_path.exists():
            try:
                await callback.message.delete()
            except TelegramBadRequest:
                pass
            await callback.message.answer_photo(
                photo=FSInputFile(plan_path),
                caption=card_text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:
            await callback.message.edit_text(
                card_text, reply_markup=keyboard, parse_mode="HTML"
            )
    else:
        try:
            await callback.message.edit_text(
                card_text, reply_markup=keyboard, parse_mode="HTML"
            )
        except TelegramBadRequest:
            await callback.message.answer(
                card_text, reply_markup=keyboard, parse_mode="HTML"
            )

    await callback.answer()


@router.callback_query(F.data == "cat:back")
async def cb_back_to_filter(callback: CallbackQuery) -> None:
    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)
    try:
        await callback.message.edit_text(
            t("catalog_choose_rooms", language),
            reply_markup=rooms_filter_kb(language),
        )
    except TelegramBadRequest:
        await callback.message.answer(
            t("catalog_choose_rooms", language),
            reply_markup=rooms_filter_kb(language),
        )
    await callback.answer()
