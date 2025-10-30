from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)  # 1 кнопка в ряд
    keyboard.add(
        InlineKeyboardButton("Боль 1", callback_data="pain1"),
        InlineKeyboardButton("Боль 2", callback_data="pain2"),
        InlineKeyboardButton("Боль 3", callback_data="pain3"),
        InlineKeyboardButton("Обо мне", callback_data="about")
    )
    return keyboard
