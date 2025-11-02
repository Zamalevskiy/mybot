import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Подключение к Google Sheets
def connect_to_sheet():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("ИмяТвоейТаблицы").sheet1  # замените на название таблицы
    return sheet

# Функция логирования события
def log_event(user_id, username, section_id, button_id, next_section):
    sheet = connect_to_sheet()
    timestamp = datetime.datetime.now().isoformat()
    sheet.append_row([user_id, username, timestamp, section_id, button_id, next_section])
