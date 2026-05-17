"""Admin paneli handlerlari."""
import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.config import settings
from bot.db import get_session
from bot.db.repository import (
    stats_last_7days_leads,
    stats_leads_by_status,
    stats_new_users_today,
    stats_popular_apartments,
    stats_total_leads,
    stats_total_users,
)

router = Router(name="admin")
logger = logging.getLogger(__name__)


def _is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids_list or user_id == settings.manager_id


@router.message(Command("myid"))
async def cmd_myid(message: Message) -> None:
    """Foydalanuvchining Telegram ID sini chiqaradi."""
    user = message.from_user
    text = (
        "🆔 <b>Sizning ma'lumotlaringiz:</b>\n\n"
        f"User ID: <code>{user.id}</code>\n"
        f"Username: @{user.username or '—'}\n"
        f"Ism: {user.first_name or '—'}\n\n"
        f"💡 Adminlik uchun .env faylga qo'shing:\n"
        f"<code>ADMIN_IDS={user.id}</code>"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q.")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Statistika", callback_data="admin:stats")],
            [
                InlineKeyboardButton(
                    text="🏢 Xonadonlar ro'yxati", callback_data="admin:apartments"
                )
            ],
        ]
    )
    await message.answer("🛠 <b>Admin paneli</b>", reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "admin:stats")
async def cb_admin_stats(callback) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("❌", show_alert=True)
        return

    async with get_session() as session:
        total_users = await stats_total_users(session)
        new_today = await stats_new_users_today(session)
        total_leads = await stats_total_leads(session)
        leads_7d = await stats_last_7days_leads(session)
        by_status = await stats_leads_by_status(session)
        popular = await stats_popular_apartments(session, limit=5)

    status_lines = [
        f"   • {status}: {count}" for status, count in by_status.items()
    ] or ["   • Lidlar yo'q"]

    popular_lines = [f"   {i + 1}. {title} — {cnt} lid" for i, (title, cnt) in enumerate(popular)] or [
        "   • Hozircha mavjud emas"
    ]

    text = (
        "📊 <b>Statistika</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
        f"🆕 Bugun qo'shilganlar: <b>{new_today}</b>\n\n"
        f"📋 Jami lidlar: <b>{total_leads}</b>\n"
        f"📅 So'nggi 7 kun: <b>{leads_7d}</b>\n\n"
        f"<b>Statuslar bo'yicha:</b>\n"
        + "\n".join(status_lines)
        + "\n\n<b>Eng mashhur xonadonlar:</b>\n"
        + "\n".join(popular_lines)
    )

    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "admin:apartments")
async def cb_admin_apartments(callback) -> None:
    if not _is_admin(callback.from_user.id):
        await callback.answer("❌", show_alert=True)
        return

    from bot.db.repository import list_apartments
    from bot.utils.formatter import format_money

    async with get_session() as session:
        apartments = await list_apartments(session, only_active=False)

    if not apartments:
        await callback.message.edit_text("Xonadonlar ro'yxati bo'sh.")
        await callback.answer()
        return

    lines = ["🏢 <b>Xonadonlar ro'yxati</b>\n"]
    for apt in apartments:
        status = "✅" if apt.is_active else "❌"
        lines.append(
            f"{status} #{apt.id} • {apt.title}\n"
            f"   📐 {apt.area:.1f} m² • 🚪 {apt.rooms} xona\n"
            f"   💰 {format_money(apt.price_total)}\n"
        )

    text = "\n".join(lines)
    if len(text) > 4000:
        text = text[:4000] + "\n…"

    await callback.message.edit_text(text, parse_mode="HTML")
    await callback.answer()
