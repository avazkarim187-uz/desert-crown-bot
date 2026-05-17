"""Lid (anketa) klaviaturalari."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.db.models import Language
from bot.locales import t


def rooms_interest_kb(language: Language = Language.UZ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1 xonali", callback_data="lead:rooms:1"
                ),
                InlineKeyboardButton(
                    text="2 xonali", callback_data="lead:rooms:2"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="3 xonali", callback_data="lead:rooms:3"
                ),
                InlineKeyboardButton(
                    text="Aniq emas", callback_data="lead:rooms:0"
                ),
            ],
        ]
    )


def payment_kb(language: Language = Language.UZ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("lead_payment_cash", language),
                    callback_data="lead:pay:cash",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("lead_payment_installment", language),
                    callback_data="lead:pay:installment",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("lead_payment_mortgage", language),
                    callback_data="lead:pay:mortgage",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("lead_payment_undecided", language),
                    callback_data="lead:pay:undecided",
                )
            ],
        ]
    )


def skip_kb(language: Language = Language.UZ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("lead_btn_skip", language),
                    callback_data="lead:skip",
                )
            ]
        ]
    )
