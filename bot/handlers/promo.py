"""Aksiyalar (promo) handlerlari."""
from pathlib import Path

from aiogram import F, Router
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.db import get_session
from bot.db.repository import get_user_language
from bot.locales import t

router = Router(name="promo")


@router.message(F.text.in_({"🎁 Aksiyalar va chegirmalar", "🎁 Акции и скидки"}))
async def menu_promo(message: Message) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💰 To'lov kalkulyatori",
                    callback_data="calc:restart",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Anketa to'ldirish",
                    callback_data="lead:start:promo",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Menejer bilan bog'lanish",
                    callback_data="menu:contact",
                )
            ],
        ]
    )

    promo_image = Path(__file__).resolve().parent.parent.parent / "data" / "promo_2room_63.4.jpg"

    if promo_image.exists():
        await message.answer_photo(
            photo=FSInputFile(promo_image),
            caption=t("promo_main", language),
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    else:
        await message.answer(
            t("promo_main", language),
            reply_markup=keyboard,
            parse_mode="HTML",
        )
