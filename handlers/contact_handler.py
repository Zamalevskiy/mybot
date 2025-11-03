from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from analytics import log_event

router = Router()

@router.callback_query(F.data == "open_contact")
async def open_contact_handler(callback: types.CallbackQuery):
    # Логирование нажатия кнопки "Напиши мне"
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click",
        action_name="contact_me",
        additional_data=""
    )
    
    # Создаем кнопку с URL
    builder = InlineKeyboardBuilder()
    builder.button(text="➡️ Напиши мне", url="https://t.me/zamalevskiy")
    
    # Редактируем текущее сообщение, заменяя кнопку на URL-кнопку
    await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
    await callback.answer("Открываю чат...")
