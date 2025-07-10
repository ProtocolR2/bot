import requests
from bot.config import Config

def check_user_registered(user_id: int) -> bool:
    """Consulta al backend si el usuario está registrado."""
    try:
        url = f"{Config.BACKEND_URL}/users/{user_id}"
        res = requests.get(url)
        if res.status_code == 200:
            return True
        return False
    except Exception as e:
        print(f"Error checking user registration: {e}")
        return False

def get_user_data(user_id: int) -> dict | None:
    """Obtiene datos completos del usuario desde el backend."""
    try:
        url = f"{Config.BACKEND_URL}/users/{user_id}"
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        return None
    except Exception as e:
        print(f"Error getting user data: {e}")
        return None

def register_user(user_info: dict) -> bool:
    """Registra un usuario nuevo en el backend."""
    try:
        url = f"{Config.BACKEND_URL}/users/"
        res = requests.post(url, json=user_info)
        return res.status_code == 201
    except Exception as e:
        print(f"Error registering user: {e}")
        return False
