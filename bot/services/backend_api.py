import requests
from bot.config import Config

TIMEOUT = 5  # segundos

def check_user_registered(user_id: int) -> bool:
    """Consulta al backend si el usuario está registrado."""
    try:
        url = f"{Config.BACKEND_URL}/users/{user_id}"
        res = requests.get(url, timeout=TIMEOUT)
        return res.status_code == 200
    except requests.RequestException as e:
        print(f"[check_user_registered] Error: {e}")
        return False

def get_user_data(user_id: int) -> dict or None:
    """Obtiene datos completos del usuario desde el backend."""
    try:
        url = f"{Config.BACKEND_URL}/users/{user_id}"
        res = requests.get(url, timeout=TIMEOUT)
        if res.status_code == 200:
            return res.json()
        return None
    except requests.RequestException as e:
        print(f"[get_user_data] Error: {e}")
        return None

def register_user(user_info: dict) -> bool:
    """Registra un usuario nuevo en el backend."""
    try:
        url = f"{Config.BACKEND_URL}/users/"
        res = requests.post(url, json=user_info, timeout=TIMEOUT)
        return res.status_code == 201
    except requests.RequestException as e:
        print(f"[register_user] Error: {e}")
        return False
