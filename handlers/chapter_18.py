import asyncio
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from analytics import log_event

router = Router()


@router.callback_query(F.data == "chapter_18")
async def chapter_18_handler(callback: types.CallbackQuery):
    # Логирование нажатия кнопки
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click",
        action_name="chapter_18",
        additional_data=""
    )
    
    # Сообщение 1
    text1 = (
        "<b>Оплати по СБП или Переводом по номеру карты.</b>\n\n"
        "✅ Банк: Сбербанк\n\n"
        "Получатель: Алексей Андреевич Замалевский\n\n"
        "Сумма — 12 000 ₽\n\n"
        "💳 Номер карты:"
    )
    await callback.message.answer(text1)
    await callback.answer()

    # Задержка 2 секунды и сообщение 2
    await asyncio.sleep(2)
    await callback.message.answer("2202 2082 7339 3406")

    # Задержка 2 секунды и сообщение 3
    await asyncio.sleep(2)
    await callback.message.answer("Телефон (для СБП):")

    # Задержка 2 секунды и сообщение 4
    await asyncio.sleep(2)
    await callback.message.answer("+7 962 972-59-99")

    # Задержка 2 секунды и сообщение 5
    await asyncio.sleep(2)
    text5 = "Чек я пришлю тебе лично после поступления оплаты."
    builder = InlineKeyboardBuilder()
    builder.button(text="Я оплатила 👍", callback_data="chapter_16")

    await callback.message.answer(text5, reply_markup=builder.as_markup())
