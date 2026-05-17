"""Bot konfiguratsiyasi — environment variables'dan o'qiladi."""
from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


class Settings(BaseSettings):
    """Asosiy sozlamalar."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Bot
    bot_token: str = Field(..., alias="BOT_TOKEN")
    admin_ids: str = Field(default="", alias="ADMIN_IDS")
    manager_id: int = Field(default=0, alias="MANAGER_ID")

    # Menejer kontaktlari
    manager_name: str = Field(default="Menejer", alias="MANAGER_NAME")
    manager_phone: str = Field(default="+998 90 000 00 00", alias="MANAGER_PHONE")
    manager_username: str = Field(default="", alias="MANAGER_USERNAME")

    # Firma
    company_name: str = Field(default="Dessert Crown Quvasoy", alias="COMPANY_NAME")
    company_address: str = Field(default="Quvasoy shahri", alias="COMPANY_ADDRESS")
    company_phone: str = Field(default="", alias="COMPANY_PHONE")
    company_website: str = Field(default="", alias="COMPANY_WEBSITE")

    # DB
    database_url: str = Field(
        default="sqlite+aiosqlite:///data/bot.db",
        alias="DATABASE_URL",
    )

    # Google Sheets (ixtiyoriy)
    google_sheets_credentials: str = Field(default="", alias="GOOGLE_SHEETS_CREDENTIALS")
    google_sheets_spreadsheet_id: str = Field(default="", alias="GOOGLE_SHEETS_SPREADSHEET_ID")

    # Loyiha
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @property
    def admin_ids_list(self) -> List[int]:
        """Adminlar ro'yxati."""
        if not self.admin_ids:
            return []
        return [int(x.strip()) for x in self.admin_ids.split(",") if x.strip()]

    @property
    def is_admin_or_manager(self):
        """Helper — tezroq tekshirish uchun."""
        allowed = set(self.admin_ids_list)
        if self.manager_id:
            allowed.add(self.manager_id)
        return allowed


settings = Settings()
