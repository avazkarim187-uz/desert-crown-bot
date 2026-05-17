"""Kalkulyator klaviaturalari."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.db.models import Apartment, Language
from bot.locales import t


def down_payment_kb(language: Language = Language.UZ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("calc_down_payment_0", language), callback_data="calc:dp:0"
                ),
                InlineKeyboardButton(
                    text=t("calc_down_payment_10", language), callback_data="calc:dp:10"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("calc_down_payment_20", language), callback_data="calc:dp:20"
                ),
                InlineKeyboardButton(
                    text=t("calc_down_payment_30", language), callback_data="calc:dp:30"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("calc_down_payment_50", language), callback_data="calc:dp:50"
                ),
                InlineKeyboardButton(
                    text=t("calc_down_payment_custom", language),
                    callback_data="calc:dp:custom",
                ),
            ],
        ]
    )


def term_kb(language: Language = Language.UZ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("calc_term_12", language), callback_data="calc:term:12"
                ),
                InlineKeyboardButton(
                    text=t("calc_term_24", language), callback_data="calc:term:24"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("calc_term_36", language), callback_data="calc:term:36"
                ),
                InlineKeyboardButton(
                    text=t("calc_term_60", language), callback_data="calc:term:60"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("calc_term_84", language), callback_data="calc:term:84"
                ),
                InlineKeyboardButton(
                    text=t("calc_term_custom", language), callback_data="calc:term:custom"
                ),
            ],
        ]
    )


def calc_apartments_kb(
    apartments: list[Apartment], language: Language = Language.UZ
) -> InlineKeyboardMarkup:
    rows = []
    for apt in apartments:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{apt.title} • {apt.area:.1f} m²",
                    callback_data=f"calc:apt:{apt.id}",
                )
            ]
        )
    rows.append(
        [
            InlineKeyboardButton(
                text="✏️ Boshqa narx kiritish",
                callback_data="calc:apt:custom",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def calc_result_kb(
    apartment_id: int | None, language: Language = Language.UZ
) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=t("btn_book_viewing", language),
                callback_data=f"lead:start:calc:{apartment_id or 0}",
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Qayta hisoblash",
                callback_data="calc:restart",
            )
        ],
        [
            InlineKeyboardButton(
                text=t("menu_main", language),
                callback_data="menu:main",
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)
