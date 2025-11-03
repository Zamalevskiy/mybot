import os
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ID вашей Google таблицы (из URL)
SPREADSHEET_ID = "10j2-3Ud4YsFtVSyFs3cr2w_dWwtfWm5czzJ7zf8JsP4"  # Замените на ваш ID
SHEET_NAME = "Данные аналитики"  # Название листа

# Получение учетных данных из переменной окружения
def get_google_credentials():
    try:
        service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        if not service_account_json:
            logger.error("❌ GOOGLE_SERVICE_ACCOUNT_JSON не найден в переменных окружения")
            return None
        
        # Парсим JSON из строки
        creds_dict = json.loads(service_account_json)
        
        # Создаем учетные данные
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        return creds
        
    except Exception as e:
        logger.error(f"❌ Ошибка при получении учетных данных: {e}")
        return None

# Инициализация клиента Google Sheets
def get_sheets_client():
    try:
        creds = get_google_credentials()
        if not creds:
            return None
            
        client = gspread.authorize(creds)
        logger.info("✅ Успешная авторизация в Google Sheets")
        return client
        
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации клиента Google Sheets: {e}")
        return None

# Создание или получение листа
def get_or_create_sheet(client):
    try:
        # Открываем таблицу
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        # Пытаемся открыть лист
        try:
            worksheet = spreadsheet.worksheet(SHEET_NAME)
            logger.info(f"✅ Лист '{SHEET_NAME}' найден")
        except gspread.exceptions.WorksheetNotFound:
            # Создаем новый лист
            worksheet = spreadsheet.add_worksheet(title=SHEET_NAME, rows=1000, cols=10)
            
            # Добавляем заголовки
            headers = [
                "Timestamp", 
                "User ID", 
                "Username", 
                "Action Type", 
                "Action Name", 
                "Additional Data"
            ]
            worksheet.append_row(headers)
            logger.info(f"✅ Создан новый лист '{SHEET_NAME}' с заголовками")
        
        return worksheet
        
    except Exception as e:
        logger.error(f"❌ Ошибка при работе с листом: {e}")
        return None

# Функция логирования событий
def log_event(user_id, username, action_type, action_name, additional_data=""):
    try:
        # Получаем клиента Google Sheets
        client = get_sheets_client()
        if not client:
            logger.error("❌ Не удалось инициализировать клиент Google Sheets")
            return False
        
        # Получаем или создаем лист
        worksheet = get_or_create_sheet(client)
        if not worksheet:
            logger.error("❌ Не удалось получить доступ к листу")
            return False
        
        # Подготавливаем данные для записи
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [
            timestamp,
            str(user_id),
            str(username),
            str(action_type),
            str(action_name),
            str(additional_data)
        ]
        
        # Добавляем строку в таблицу
        worksheet.append_row(row_data)
        logger.info(f"✅ Данные записаны в таблицу: {action_type} - {action_name}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при записи в Google Sheets: {e}")
        return False

# Тестовая функция для проверки подключения
def test_connection():
    """Функция для тестирования подключения к Google Sheets"""
    try:
        client = get_sheets_client()
        if client:
            worksheet = get_or_create_sheet(client)
            if worksheet:
                print("✅ Подключение к Google Sheets успешно настроено!")
                return True
        print("❌ Ошибка подключения к Google Sheets")
        return False
    except Exception as e:
        print(f"❌ Ошибка при тестировании подключения: {e}")
        return False

if __name__ == "__main__":
    # Тест при запуске файла
    test_connection()
