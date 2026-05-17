"""Asosiy handlerlar: /start, /help, menyu navigatsiyasi."""
import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.db import get_session
from bot.db.models import Language
from bot.db.repository import get_or_create_user, get_user_language, set_user_language
from bot.keyboards.common import contact_kb, language_kb, main_menu
from bot.locales import t

router = Router(name="common")
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()

    async with get_session() as session:
        await get_or_create_user(
            session,
            tg_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        language = await get_user_language(session, message.from_user.id)

    await message.answer(
        t("welcome", language, company_name=settings.company_name),
        reply_markup=main_menu(language),
        parse_mode="HTML",
    )


@router.message(Command("language"))
@router.message(F.text.in_({"🌐 Til / Язык", "🌐 Язык / Til"}))
async def cmd_language(message: Message) -> None:
    await message.answer(t("choose_language"), reply_markup=language_kb())


@router.callback_query(F.data.startswith("lang:"))
async def cb_set_language(callback: CallbackQuery) -> None:
    lang_code = callback.data.split(":")[1]
    language = Language.RU if lang_code == "ru" else Language.UZ

    async with get_session() as session:
        await set_user_language(session, callback.from_user.id, language)

    await callback.message.edit_text(t("language_changed", language))
    await callback.message.answer(
        t("welcome", language, company_name=settings.company_name),
        reply_markup=main_menu(language),
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(F.text.in_({"ℹ️ Biz haqimizda", "ℹ️ О нас"}))
async def menu_about(message: Message) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)
    await message.answer(
        t("about_info", language, company_name=settings.company_name),
        parse_mode="HTML",
    )


@router.message(F.text.in_({"📍 Manzil", "📍 Адрес"}))
async def menu_location(message: Message) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)
    await message.answer(
        t(
            "location_info",
            language,
            company_name=settings.company_name,
            company_address=settings.company_address,
        ),
        parse_mode="HTML",
    )


@router.message(F.text.in_({"📞 Menejer bilan bog'lanish", "📞 Связаться с менеджером"}))
async def menu_contact(message: Message) -> None:
    async with get_session() as session:
        language = await get_user_language(session, message.from_user.id)
    await message.answer(
        t(
            "contact_info",
            language,
            manager_name=settings.manager_name,
            manager_phone=settings.manager_phone,
            manager_username=settings.manager_username or "—",
            company_address=settings.company_address,
            company_phone=settings.company_phone or "—",
        ),
        reply_markup=contact_kb(language),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "menu:contact")
async def cb_contact(callback: CallbackQuery) -> None:
    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)
    await callback.message.answer(
        t(
            "contact_info",
            language,
            manager_name=settings.manager_name,
            manager_phone=settings.manager_phone,
            manager_username=settings.manager_username or "—",
            company_address=settings.company_address,
            company_phone=settings.company_phone or "—",
        ),
        reply_markup=contact_kb(language),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "menu:main")
async def cb_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    async with get_session() as session:
        language = await get_user_language(session, callback.from_user.id)
    await callback.message.answer(
        t("welcome", language, company_name=settings.company_name),
        reply_markup=main_menu(language),
        parse_mode="HTML",
    )
    await callback.answer()
