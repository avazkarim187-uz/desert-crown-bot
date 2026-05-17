"""Bot ishga tushirish entrypoint'i."""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import settings
from bot.db import init_db
from bot.handlers import setup_handlers


def setup_logging() -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )
    # aiogram juda ko'p log chiqaradi, biroz tinchitamiz
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)


async def on_startup(bot: Bot) -> None:
    """Bot ishga tushganda."""
    logger = logging.getLogger(__name__)
    me = await bot.get_me()
    logger.info("Bot ishga tushdi: @%s (id=%s)", me.username, me.id)
    logger.info("Firma: %s", settings.company_name)
    logger.info("Adminlar: %s", settings.admin_ids_list)


async def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Bot tayyorlanmoqda...")

    # DB
    await init_db()

    # Bot va dispatcher
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Handlerlar
    setup_handlers(dp)
    dp.startup.register(on_startup)

    # Polling boshlanadi
    logger.info("Polling boshlandi.")
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi.")
