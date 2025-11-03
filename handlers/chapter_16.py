@router.callback_query(F.data == "log_and_open_contact")
async def log_and_open_contact_handler(callback: types.CallbackQuery):
    # Логирование нажатия кнопки "Напиши мне"
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click",
        action_name="contact_me_click",
        additional_data=""
    )
    
    # Создаем сообщение с кнопкой
    builder = InlineKeyboardBuilder()
    builder.button(text="Чат с Алексеем", url="https://t.me/zamalevskiy")
    
    # Отправляем всплывающее уведомление + сообщение с кнопкой
    await callback.answer("Открываю чат...")
    await callback.message.answer(
        "Нажмите на кнопку ниже чтобы написать мне 👇",
        reply_markup=builder.as_markup()
    )
