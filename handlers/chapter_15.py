from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import requests
import uuid  # для уникального Idempotence-Key

router = Router()

# 🔹 Данные о товаре
TITLE = "Диагностика"
DESCRIPTION = "Диагностика текущей ключевой проблемы (1 час)."
PRICE = 5000  # в рублях

# 🔹 Основной экран раздела 15
@router.callback_query(F.data == "chapter_15")
async def chapter_15_handler(callback: types.CallbackQuery):
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
        builder.button(text="ЮКасса", url=pay_url)  # кнопка сразу ведёт на Юкассу
        builder.button(text="💳 Перевод на карту / СБП", callback_data="chapter_19")
        builder.button(text="Я оплатила / Написать мне", callback_data="chapter_16")  # новая кнопка
        builder.adjust(1)
      
        await callback.message.answer(text, reply_markup=builder.as_markup())
    else:
        await callback.message.answer(
            f"⚠️ Ошибка при создании платежа:\n\n<code>{response.text}</code>",
            parse_mode="HTML"
        )

    await callback.answer()
