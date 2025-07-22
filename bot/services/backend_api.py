import requests
import logging
import threading
import time
from bot.config import Config

# Configurar logging
logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 5
EXTENDED_TIMEOUT = 15  # Para primer intento si backend está dormido

# 🧠 Mantener backend despierto con ping cada 10 minutos
def keep_backend_awake():
    while True:
        try:
            url = f"{Config.BACKEND_URL}/ping"
            res = requests.get(url, timeout=5)
            logger.info(f"[keep_backend_awake] Ping result: {res.status_code}")
        except Exception as e:
            logger.warning(f"[keep_backend_awake] Error: {e}")
        time.sleep(600)

# Iniciar el thread al cargar el módulo
threading.Thread(target=keep_backend_awake, daemon=True).start()


# ✅ Consulta si el usuario ya existe en el backend
def check_user_registered(user_id: int) -> bool:
    url = f"{Config.BACKEND_URL}/api/users/{user_id}"
    try:
        res = requests.get(url, timeout=EXTENDED_TIMEOUT)
        return res.status_code == 200
    except requests.RequestException as e:
        logger.error(f"[check_user_registered] Error: {e}")
        return False


# ✅ Obtener datos del usuario
def get_user_data(user_id: int) -> dict | None:
    url = f"{Config.BACKEND_URL}/api/users/{user_id}"
    try:
        res = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if res.status_code == 200:
            return res.json()
        return None
    except requests.RequestException as e:
        logger.error(f"[get_user_data] Error: {e}")
        return None


# ⛔️ Ya no se usa para registro inicial, pero se conserva por si se reutiliza
def register_user(user_info: dict) -> bool:
    url = f"{Config.BACKEND_URL}/api/users/"
    try:
        res = requests.post(url, json=user_info, timeout=DEFAULT_TIMEOUT)
        return res.status_code == 201
    except requests.RequestException as e:
        logger.error(f"[register_user] Error: {e}")
        return False


# ✅ Activar usuario con token recibido por /start <token>
def activate_user(telegram_id: int, token: str) -> bool:
    url = f"{Config.BACKEND_URL}/api/users/activar-cuenta"
    try:
        res = requests.post(url, json={"telegram_id": telegram_id, "token": token}, timeout=DEFAULT_TIMEOUT)
        return res.status_code == 200
    except requests.RequestException as e:
        logger.error(f"[activate_user] Error: {e}")
        return False
