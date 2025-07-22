import os

class Config:
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
    BACKEND_URL = os.getenv("BACKEND_URL", "https://backend-4vzk.onrender.com")
    DATABASE_URL = os.getenv("DATABASE_URL")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "es")
    SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES", "es,en").split(",")

    @classmethod
    def is_valid(cls):
        """Verifica que las variables obligatorias estén configuradas"""
        return all([cls.BOT_TOKEN, cls.BACKEND_URL])
