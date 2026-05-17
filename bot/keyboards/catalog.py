"""Katalog uchun klaviaturalar."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.db.models import Apartment, Language
from bot.locales import t


def rooms_filter_kb(language: Language = Language.UZ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("catalog_1_room", language), callback_data="cat:rooms:1"
                ),
                InlineKeyboardButton(
                    text=t("catalog_2_rooms", language), callback_data="cat:rooms:2"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("catalog_3_rooms", language), callback_data="cat:rooms:3"
                ),
                InlineKeyboardButton(
                    text=t("catalog_all", language), callback_data="cat:rooms:0"
                ),
            ],
        ]
    )


def apartment_list_kb(
    apartments: list[Apartment], language: Language = Language.UZ
) -> InlineKeyboardMarkup:
    rows = []
    for apt in apartments:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"🏡 {apt.title} • {apt.area:.1f} m²",
                    callback_data=f"cat:show:{apt.id}",
                )
            ]
        )
    rows.append(
        [
            InlineKeyboardButton(
                text=t("menu_back", language), callback_data="cat:back"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def apartment_card_kb(
    apartment: Apartment, language: Language = Language.UZ
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("btn_calculator", language),
                    callback_data=f"calc:apt:{apartment.id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("btn_book_viewing", language),
                    callback_data=f"lead:start:apt:{apartment.id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("btn_contact_manager", language),
                    callback_data="menu:contact",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("menu_back", language), callback_data="cat:back"
                )
            ],
        ]
    )
