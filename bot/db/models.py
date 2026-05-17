"""SQLAlchemy modellar."""
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """SQLAlchemy base."""


class LeadStatus(str, PyEnum):
    NEW = "new"
    CONTACTED = "contacted"
    VIEWING_SCHEDULED = "viewing_scheduled"
    VIEWED = "viewed"
    NEGOTIATING = "negotiating"
    CONTRACT_SIGNED = "contract_signed"
    CANCELLED = "cancelled"


class Language(str, PyEnum):
    UZ = "uz"
    RU = "ru"


class User(Base):
    """Telegram foydalanuvchi."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    language: Mapped[Language] = mapped_column(
        Enum(Language), default=Language.UZ, nullable=False
    )
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    last_active: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    leads: Mapped[list["Lead"]] = relationship("Lead", back_populates="user")

    @property
    def full_name(self) -> str:
        parts = [self.first_name or "", self.last_name or ""]
        return " ".join(p for p in parts if p).strip() or "Foydalanuvchi"


class Apartment(Base):
    """Xonadon kartochkasi."""

    __tablename__ = "apartments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    rooms: Mapped[int] = mapped_column(Integer, nullable=False)  # 1, 2, 3...
    area: Mapped[float] = mapped_column(nullable=False)  # m²
    floor_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    floor_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price_total: Mapped[int] = mapped_column(BigInteger, nullable=False)  # so'm
    price_per_m2: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    plan_image: Mapped[str | None] = mapped_column(String(512), nullable=True)
    photos: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list
    description_uz: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    available_count: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    leads: Mapped[list["Lead"]] = relationship("Lead", back_populates="apartment")


class Lead(Base):
    """Lid — mijoz so'rovi."""

    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    apartment_id: Mapped[int | None] = mapped_column(
        ForeignKey("apartments.id"), nullable=True
    )
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    budget_min: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    budget_max: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    rooms_interest: Mapped[int | None] = mapped_column(Integer, nullable=True)
    payment_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    down_payment_percent: Mapped[int | None] = mapped_column(Integer, nullable=True)
    term_months: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus), default=LeadStatus.NEW, nullable=False
    )
    source: Mapped[str] = mapped_column(String(64), default="bot", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    user: Mapped[User] = relationship("User", back_populates="leads")
    apartment: Mapped[Apartment | None] = relationship("Apartment", back_populates="leads")


class CalculatorLog(Base):
    """Kalkulyator ishlatish statistikasi."""

    __tablename__ = "calculator_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    apartment_id: Mapped[int | None] = mapped_column(
        ForeignKey("apartments.id"), nullable=True
    )
    price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    down_payment_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    term_months: Mapped[int] = mapped_column(Integer, nullable=False)
    monthly_payment: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
