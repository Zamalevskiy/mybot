import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Кэш для подключения, чтобы не создавать соединение каждый раз
_sheet_cache = None

def connect_to_sheet():
    global _sheet_cache
    if _sheet_cache:
        return _sheet_cache

    # Получаем JSON из переменной окружения
    json_content = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not json_content:
        raise ValueError("Переменная окружения GOOGLE_SERVICE_ACCOUNT_JSON не найдена")

    credentials_dict = json.loads(json_content)

    # Полные scopes для работы с Google Sheets и Drive
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
    client = gspread.authorize(creds)

    # Открываем нужный Google Sheet
    sheet = client.open("Bot-analitic").sheet1

    # Сохраняем в кэш
    _sheet_cache = sheet
    return sheet

def log_event(user_id, username, section_id, button_id, next_section):
    sheet = connect_to_sheet()
    timestamp = datetime.now().isoformat()
    sheet.append_row([user_id, username, timestamp, section_id, button_id, next_section])
