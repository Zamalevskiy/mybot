import os
import json
import gspread
from google.oauth2.service_account import Credentials
import datetime

def connect_to_sheet():
    json_content = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not json_content:
        raise ValueError("Переменная окружения GOOGLE_SERVICE_ACCOUNT_JSON не найдена")

    credentials_dict = json.loads(json_content)

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)

    client = gspread.authorize(creds)  # <-- Используем authorize вместо login
    sheet = client.open("Bot-analitic").sheet1
    return sheet

def log_event(user_id, username, section_id, button_id, next_section):
    sheet = connect_to_sheet()
    timestamp = datetime.datetime.now().isoformat()
    sheet.append_row([user_id, username, timestamp, section_id, button_id, next_section])

    sheet = connect_to_sheet()
    timestamp = datetime.datetime.now().isoformat()
    sheet.append_row([user_id, username, timestamp, section_id, button_id, next_section])

