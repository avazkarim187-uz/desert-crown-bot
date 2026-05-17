"""Demo xonadonlarni DB'ga yozish (seed)."""
import asyncio
import logging
from pathlib import Path

from sqlalchemy import select

from bot.db import init_db, get_session
from bot.db.models import Apartment

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


DEMO_APARTMENTS = [
    {
        "title": "1 xonali xonadon (Soy Bo'yi)",
        "rooms": 1,
        "area": 33.5,
        "floor_min": 2,
        "floor_max": 9,
        "price_total": 213_000_000,
        "price_per_m2": int(213_000_000 / 33.5),
        "plan_image": str(DATA_DIR / "plan_1room_33.5.jpg"),
        "description_uz": (
            "✨ Ixcham va qulay 1 xonali xonadon.\n"
            "🛋 Umumiy xona 14.4 m², oshxona 8.0 m².\n"
            "🛁 Sanitar uzel (С/У) 3.6 m².\n"
            "🌅 Lojiya 6.2 m² — keng va yorug'.\n\n"
            "🔑 <i>Yil oxiriga topshiriladi.</i>"
        ),
        "description_ru": (
            "✨ Уютная 1-комнатная квартира.\n"
            "🛋 Общая комната 14,4 м², кухня 8,0 м².\n"
            "🛁 С/У 3,6 м².\n"
            "🌅 Лоджия 6,2 м² — просторная и светлая.\n\n"
            "🔑 <i>Сдача — к концу года.</i>"
        ),
        "is_active": True,
        "available_count": 12,
    },
    {
        "title": "2 xonali xonadon — MAXSUS TAKLIF (Soy Bo'yi)",
        "rooms": 2,
        "area": 63.4,
        "floor_min": 2,
        "floor_max": 9,
        "price_total": 402_750_000,
        "price_per_m2": int(402_750_000 / 63.4),
        "plan_image": str(DATA_DIR / "promo_2room_63.4.jpg"),
        "description_uz": (
            "🔥 <b>MAXSUS TAKLIF — Soy Bo'yi turar-joy majmuasi!</b>\n\n"
            "✨ Keng va qulay 2 xonali xonadon (63.4 m²).\n"
            "💥 20% boshlang'ich to'lov bilan\n"
            "✅ 60 oy foizsiz, penyasiz nasiya\n"
            "✅ Har oy atigi 5 370 000 so'm\n"
            "📈 21 500 000 so'm <b>FOYDA</b> bilan!\n\n"
            "🔑 <i>Yil oxiriga topshiriladi.</i>\n"
            "📍 Quvasoy shahri, Dessert Crown majmuasi."
        ),
        "description_ru": (
            "🔥 <b>СПЕЦПРЕДЛОЖЕНИЕ — ЖК «Soy Bo'yi»!</b>\n\n"
            "✨ Просторная 2-комнатная квартира (63,4 м²).\n"
            "💥 С первоначальным взносом 20%\n"
            "✅ 60 месяцев без процентов, без пени\n"
            "✅ Всего 5 370 000 сум в месяц\n"
            "📈 Выгода <b>21 500 000 сум</b>!\n\n"
            "🔑 <i>Сдача — к концу года.</i>\n"
            "📍 Кувасай, ЖК Dessert Crown."
        ),
        "is_active": True,
        "available_count": 8,
    },
]


async def seed() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    await init_db()

    async with get_session() as session:
        existing = await session.execute(select(Apartment))
        existing_titles = {a.title for a in existing.scalars().all()}

        added = 0
        for data in DEMO_APARTMENTS:
            if data["title"] in existing_titles:
                logger.info("⊘ Allaqachon mavjud: %s", data["title"])
                continue
            apartment = Apartment(**data)
            session.add(apartment)
            added += 1
            logger.info("✓ Qo'shildi: %s", data["title"])

        logger.info("Jami qo'shildi: %s", added)


if __name__ == "__main__":
    asyncio.run(seed())
