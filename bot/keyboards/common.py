"""Asosiy klaviaturalar."""
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from bot.config import settings
from bot.db.models import Language
from bot.locales import t


def main_menu(language: Language = Language.UZ) -> ReplyKeyboardMarkup:
    """Asosiy menyu — reply keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=t("menu_catalog", language)),
                KeyboardButton(text=t("menu_calculator", language)),
            ],
            [
                KeyboardButton(text=t("menu_promotions", language)),
                KeyboardButton(text=t("menu_contact", language)),
            ],
            [
                KeyboardButton(text=t("menu_about", language)),
                KeyboardButton(text=t("menu_location", language)),
            ],
            [
                KeyboardButton(text=t("menu_language", language)),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def language_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("language_uz"), callback_data="lang:uz"),
                InlineKeyboardButton(text=t("language_ru"), callback_data="lang:ru"),
            ]
        ]
    )


def contact_kb(language: Language = Language.UZ) -> InlineKeyboardMarkup:
    rows = []
    if settings.manager_phone:
        rows.append(
            [
                InlineKeyboardButton(
                    text=t("contact_btn_call", language),
                    url=f"tel:{settings.manager_phone.replace(' ', '')}",
                )
            ]
        )
    if settings.manager_username:
        rows.append(
            [
                InlineKeyboardButton(
                    text=t("contact_btn_message", language),
                    url=f"https://t.me/{settings.manager_username.lstrip('@')}",
                )
            ]
        )
    rows.append(
        [
            InlineKeyboardButton(
                text=t("btn_book_viewing", language),
                callback_data="lead:start:contact",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def share_phone_kb(language: Language = Language.UZ) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=t("lead_share_contact", language),
                    request_contact=True,
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def remove_kb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
