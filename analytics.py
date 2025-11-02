import os
import json
import gspread
from google.oauth2.service_account import Credentials
import datetime

# Подключение к Google Sheets
def connect_to_sheet():
    # Чтение JSON-содержимого сервисного аккаунта из переменной окружения
    json_content = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    credentials_dict = json.loads(json_content)

    # Создание Credentials и подключение к gspread
    creds = Credentials.from_service_account_info(credentials_dict)
    client = gspread.Client(auth=creds)
    client.login()

    # Открываем таблицу по названию
    sheet = client.open("Bot-analitic").sheet1
    return sheet

# Функция логирования события
def log_event(user_id, username, section_id, button_id, next_section):
    sheet = connect_to_sheet()
    timestamp = datetime.datetime.now().isoformat()
    sheet.append_row([user_id, username, timestamp, section_id, button_id, next_section])

