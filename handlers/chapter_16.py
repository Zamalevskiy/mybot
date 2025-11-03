import asyncio
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from analytics import log_event

# Импортируем функцию для отметки пользователя
from utils.chapter16 import mark_user_reached_chapter_16, user_reached_chapter_16

router = Router()

@router.callback_query(F.data == "chapter_16")
async def chapter_16_handler(callback: types.CallbackQuery):
    # Логирование нажатия кнопки
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click",
        action_name="chapter_16",
        additional_data=""
    )
    
    text = (
        "<b>Спасибо за доверие!❤️</b>\n"
        "Ты сделала важный шаг к поддержке и ясности.\n"
        "Всё, что нужно, уже сделано — и это правильно.\n"
        "Осталось только уточнить дату и время встречи."
    )

    builder = InlineKeyboardBuilder()
    # Используем промежуточный обработчик
    builder.button(text="➡️ Напиши мне", callback_data="open_contact")
    builder.adjust(1)

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()

    # Отмечаем, что пользователь достиг раздела 16
    mark_user_reached_chapter_16(callback.from_user.id)
