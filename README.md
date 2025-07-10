README - Bot Telegram ProtocolR2 con Webhook y FastAPI
Descripción
Este repositorio contiene el código del bot Telegram del proyecto ProtocolR2.
El bot está implementado con python-telegram-bot y expuesto como servicio web usando FastAPI.
La comunicación con Telegram es vía webhook, no polling, para eficiencia y escalabilidad.

Requisitos previos
Cuenta en Render con servicio web creado para este bot

Token del bot Telegram válido

Backend ProtocolR2 desplegado y accesible (para consultas y registros)

Variables de entorno necesarias
TELEGRAM_TOKEN: Token oficial del bot Telegram (no subir a GitHub)

BACKEND_URL: URL base del backend desplegado (ej: https://backend-xxxx.onrender.com)

DATABASE_URL: URL conexión a base de datos (opcional, si usás en bot)

DEFAULT_LANGUAGE: Idioma por defecto (ej: es)

SUPPORTED_LANGUAGES: Idiomas soportados separados por coma (ej: es,en)

Despliegue en Render
1. Crear el servicio web
En Render, crear un servicio de tipo Web Service

Conectar al repositorio del bot en GitHub

Configurar build command:

bash
Copy code
pip install -r requirements.txt
Configurar start command:

bash
Copy code
uvicorn bot.main:app --host 0.0.0.0 --port 10000
Configurar las variables de entorno mencionadas arriba (especialmente TELEGRAM_TOKEN)

2. Configurar webhook de Telegram
Una vez desplegado el servicio, obtener la URL pública del bot, por ejemplo:

arduino
Copy code
https://protocolr2-bot.onrender.com
Ejecutar el siguiente comando (reemplazando <TELEGRAM_TOKEN> y URL):

bash
Copy code
curl -X POST "https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://protocolr2-bot.onrender.com/webhook"}'
Testeo básico
Acceder a:

bash
Copy code
https://protocolr2-bot.onrender.com/ping
Debería devolver:

json
Copy code
{"status":"ok"}
Enviar /start desde Telegram para iniciar el flujo del bot.

Mantener bot activo
Render puede poner a dormir el servicio en planes gratuitos

Recomiendo usar servicios como UptimeRobot para pings periódicos a /ping y evitar sleep.

Notas finales
El bot está separado profesionalmente del backend, que maneja lógica y base de datos.

El código usa python-telegram-bot v20+ y FastAPI para webhook.

Todos los handlers están en bot/handlers/, lógica de backend en bot/services/backend_api.py.
