"""DB operatsiyalari."""
from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Apartment, CalculatorLog, Lead, LeadStatus, User, Language


async def get_or_create_user(
    session: AsyncSession,
    tg_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> User:
    """Foydalanuvchini topish yoki yaratish."""
    result = await session.execute(select(User).where(User.tg_id == tg_id))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        session.add(user)
        await session.flush()
        return user

    # Yangilash
    user.username = username or user.username
    user.first_name = first_name or user.first_name
    user.last_name = last_name or user.last_name
    user.last_active = datetime.utcnow()
    return user


async def set_user_language(session: AsyncSession, tg_id: int, language: Language) -> None:
    await session.execute(
        update(User).where(User.tg_id == tg_id).values(language=language)
    )


async def get_user_language(session: AsyncSession, tg_id: int) -> Language:
    result = await session.execute(select(User.language).where(User.tg_id == tg_id))
    lang = result.scalar_one_or_none()
    return lang or Language.UZ


async def list_apartments(
    session: AsyncSession,
    rooms: int | None = None,
    only_active: bool = True,
) -> Sequence[Apartment]:
    """Xonadonlar ro'yxati."""
    stmt = select(Apartment)
    if only_active:
        stmt = stmt.where(Apartment.is_active.is_(True))
    if rooms is not None:
        stmt = stmt.where(Apartment.rooms == rooms)
    stmt = stmt.order_by(Apartment.rooms, Apartment.area)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_apartment(session: AsyncSession, apartment_id: int) -> Apartment | None:
    result = await session.execute(select(Apartment).where(Apartment.id == apartment_id))
    return result.scalar_one_or_none()


async def create_apartment(session: AsyncSession, **data) -> Apartment:
    apartment = Apartment(**data)
    session.add(apartment)
    await session.flush()
    return apartment


async def create_lead(
    session: AsyncSession,
    user_id: int,
    *,
    apartment_id: int | None = None,
    full_name: str | None = None,
    phone: str | None = None,
    rooms_interest: int | None = None,
    down_payment_percent: int | None = None,
    term_months: int | None = None,
    payment_type: str | None = None,
    notes: str | None = None,
    source: str = "bot",
) -> Lead:
    lead = Lead(
        user_id=user_id,
        apartment_id=apartment_id,
        full_name=full_name,
        phone=phone,
        rooms_interest=rooms_interest,
        down_payment_percent=down_payment_percent,
        term_months=term_months,
        payment_type=payment_type,
        notes=notes,
        source=source,
    )
    session.add(lead)
    await session.flush()
    return lead


async def log_calculator_use(
    session: AsyncSession,
    user_id: int,
    *,
    price: int,
    down_payment_percent: int,
    term_months: int,
    monthly_payment: int,
    apartment_id: int | None = None,
) -> None:
    session.add(
        CalculatorLog(
            user_id=user_id,
            apartment_id=apartment_id,
            price=price,
            down_payment_percent=down_payment_percent,
            term_months=term_months,
            monthly_payment=monthly_payment,
        )
    )


# --- Statistika (admin uchun) ---

async def stats_total_users(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(User.id)))
    return result.scalar_one() or 0


async def stats_new_users_today(session: AsyncSession) -> int:
    today = datetime.utcnow().date()
    result = await session.execute(
        select(func.count(User.id)).where(func.date(User.created_at) == today)
    )
    return result.scalar_one() or 0


async def stats_total_leads(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(Lead.id)))
    return result.scalar_one() or 0


async def stats_leads_by_status(session: AsyncSession) -> dict[str, int]:
    result = await session.execute(
        select(Lead.status, func.count(Lead.id)).group_by(Lead.status)
    )
    return {status.value: count for status, count in result.all()}


async def stats_popular_apartments(
    session: AsyncSession, limit: int = 5
) -> list[tuple[str, int]]:
    """Eng ko'p qiziqayotgan xonadonlar."""
    result = await session.execute(
        select(Apartment.title, func.count(Lead.id).label("cnt"))
        .join(Lead, Lead.apartment_id == Apartment.id)
        .group_by(Apartment.id, Apartment.title)
        .order_by(func.count(Lead.id).desc())
        .limit(limit)
    )
    return list(result.all())


async def stats_last_7days_leads(session: AsyncSession) -> int:
    week_ago = datetime.utcnow() - timedelta(days=7)
    result = await session.execute(
        select(func.count(Lead.id)).where(Lead.created_at >= week_ago)
    )
    return result.scalar_one() or 0
