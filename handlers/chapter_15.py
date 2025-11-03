from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import requests
import uuid  # для уникального Idempotence-Key
from analytics import log_event

router = Router()

# 🔹 Данные о товаре
TITLE = "Диагностика"
DESCRIPTION = "Диагностика текущей ключевой проблемы (1 час)."
PRICE = 5000  # в рублях

# 🔹 Основной экран раздела 15
@router.callback_query(F.data == "chapter_15")
async def chapter_15_handler(callback: types.CallbackQuery):
    # Логирование нажатия кнопки
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click",
        action_name="chapter_15",
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
        
        # Кнопка ЮКасса с логированием через отдельный обработчик
        builder.button(text="ЮКасса", callback_data="yookassa_payment_15")
        builder.button(text="💳 Перевод на карту / СБП", callback_data="bank_transfer_15")
        builder.button(text="Я оплатила - Написать мне", callback_data="chapter_16")
        builder.adjust(1)
      
        await callback.message.answer(text, reply_markup=builder.as_markup())
    else:
        await callback.message.answer(
            f"⚠️ Ошибка при создании платежа:\n\n<code>{response.text}</code>",
            parse_mode="HTML"
        )

    await callback.answer()


# Обработчик для кнопки ЮКасса (диагностика)
@router.callback_query(F.data == "yookassa_payment_15")
async def yookassa_diagnostic_handler(callback: types.CallbackQuery):
    # Логирование выбора оплаты через ЮКассу
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="payment_method",
        action_name="yookassa_diagnostic", 
        additional_data="5000"
    )
    
    SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
    SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

    idempotence_key = str(uuid.uuid4())
    payment_data = {
        "amount": {"value": "5000.00", "currency": "RUB"},
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/{callback.from_user.username or 'your_bot_name'}"
        },
        "description": "Диагностика текущей ключевой проблемы (1 час).",
        "metadata": {"user_id": callback.from_user.id}
    }

    response = requests.post(
        "https://api.yookassa.ru/v3/payments",
        auth=(SHOP_ID, SECRET_KEY),
        json=payment_data,
        headers={"Idempotence-Key": idempotence_key}
    )

    if response.status_code == 200:
        data = response.json()
        pay_url = data["confirmation"]["confirmation_url"]
        
        # Отправляем сообщение со ссылкой
        await callback.message.answer(
            "✅ Переходи по ссылке для оплаты через ЮКассу:\n" + pay_url
        )
    else:
        await callback.message.answer("❌ Ошибка при создании платежа")
    
    await callback.answer()


# Обработчик для кнопки перевода на карту (диагностика)
@router.callback_query(F.data == "bank_transfer_15")
async def bank_transfer_diagnostic_handler(callback: types.CallbackQuery):
    # Логирование выбора оплаты переводом на карту
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="payment_method",
        action_name="bank_transfer_diagnostic",
        additional_data="5000"
    )
    
    # Перенаправляем в раздел 19 для показа реквизитов
    from handlers.chapter_19 import chapter_19_handler
    await chapter_19_handler(callback)
