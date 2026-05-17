from bot.locales.uz import UZ
from bot.locales.ru import RU
from bot.db.models import Language


LOCALES = {
    Language.UZ: UZ,
    Language.RU: RU,
}


def t(key: str, language: Language = Language.UZ, **kwargs) -> str:
    """Tarjima qaytaradi."""
    locale = LOCALES.get(language, UZ)
    text = locale.get(key, UZ.get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
