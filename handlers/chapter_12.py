from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import requests
import uuid  # для уникального Idempotence-Key
from analytics import log_event

router = Router()

# 🔹 Данные о товаре
TITLE = "Консультация"
DESCRIPTION = "Кризисная консультация (2 часа)."
PRICE = 12000  # в рублях

# 🔹 Основной экран раздела 12
@router.callback_query(F.data == "chapter_12")
async def chapter_12_handler(callback: types.CallbackQuery):
    # Логирование нажатия кнопки
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click",
        action_name="chapter_12",
        additional_data=""
    )
    
    SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
    SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

    # Создаём уникальный Idempotence-Key
    idempotence_key = str(uuid.uuid4())

    # Генерация платежа через API Юкассы
    payment_data = {
        "amount": {"value": f"{PRICE:.2f}", "currency": "RUB"},
        "capture": True,
        "confirmation": {
            "type": "redirect",
            # После оплаты пользователь вернётся в бот
            "return_url": f"https://t.me/{callback.from_user.username or 'your_bot_name'}"
        },
        "description": DESCRIPTION,
        "metadata": {"user_id": callback.from_user.id}
    }

    response = requests.post(
        "https://api.yookassa.ru/v3/payments",
        auth=(SHOP_ID, SECRET_KEY),
        json=payment_data,
        headers={"Idempotence-Key": idempotence_key}  # добавили уникальный ключ
    )

    if response.status_code == 200:
        data = response.json()
        pay_url = data["confirmation"]["confirmation_url"]

        text = (
            "<b>Выбери удобный способ оплаты.</b>\n"
            "После оплаты я сразу свяжусь с тобой для уточнения даты и времени встречи.\n\n"
            "Чек придёт автоматически, либо я пришлю его тебе лично."
        )

        builder = InlineKeyboardBuilder()
        
        # Кнопка ЮКасса с URL и логированием через отдельный обработчик
        builder.button(text="ЮКасса", url=pay_url)
        builder.button(text="💳 Перевод на карту / СБП", callback_data="bank_transfer_12")
        builder.button(text="Я оплатила - Написать мне", callback_data="chapter_16")
        builder.adjust(1)

        await callback.message.answer(text, reply_markup=builder.as_markup())
        
        # Логируем показ платежных методов
        log_event(
            user_id=callback.from_user.id,
            username=callback.from_user.username or "",
            action_type="payment_methods_shown",
            action_name="consultation_payment_options",
            additional_data="12000"
        )
    else:
        await callback.message.answer(
            f"⚠️ Ошибка при создании платежа:\n\n<code>{response.text}</code>",
            parse_mode="HTML"
        )

    await callback.answer()


# Обработчик для кнопки перевода на карту
@router.callback_query(F.data == "bank_transfer_12")
async def bank_transfer_handler(callback: types.CallbackQuery):
    # Логирование выбора оплаты переводом на карту
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="payment_method", 
        action_name="bank_transfer_consultation",
        additional_data="12000"
    )
    
    # Перенаправляем в раздел 18 для показа реквизитов
    from handlers.chapter_18 import chapter_18_handler
    await chapter_18_handler(callback)
