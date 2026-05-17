from aiogram import Dispatcher

from bot.handlers import admin, calculator, catalog, common, lead, promo


def setup_handlers(dp: Dispatcher) -> None:
    """Barcha routerlarni dispatcher'ga ulash."""
    dp.include_router(admin.router)
    dp.include_router(lead.router)  # FSM bilan oldin keladi
    dp.include_router(calculator.router)
    dp.include_router(catalog.router)
    dp.include_router(promo.router)
    dp.include_router(common.router)  # Default fallback — oxirida
