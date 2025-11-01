from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import requests

router = Router()

# 🔹 Данные о товаре
TITLE = "Консультация"
DESCRIPTION = "Кризисная консультация (2 часа)."
PRICE = 12000  # в рублях


# 🔹 Основной экран раздела 12
@router.callback_query(F.data == "chapter_12")
async def chapter_12_handler(callback: types.CallbackQuery):
    text = (
        "<b>Выбери удобный способ оплаты.</b>\n"
        "После оплаты я сразу свяжусь с тобой для уточнения даты и времени встречи.\n\n"
        "Чек придёт автоматически, либо я пришлю его тебе лично."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="ЮКасса", callback_data="yookassa_pay")
    builder.button(text="💳 Перевод на карту / СБП", callback_data="chapter_18")
    builder.adjust(1)

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


# 🔹 Обработка кнопки Юкассы — создание ссылки на оплату
@router.callback_query(F.data == "yookassa_pay")
async def yookassa_pay(callback: types.CallbackQuery):
    SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
    SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

    # Создание платежа через API Юкассы
    payment_data = {
        "amount": {"value": f"{PRICE:.2f}", "currency": "RUB"},
        "capture": True,
        "confirmation": {
            "type": "redirect",
            # После оплаты пользователь вернётся в бот
            "return_url": f"https://t.me/{callback.from_user.username or 'your_bot_name'}"
        },
        "description": DESCRIPTION,
        # Передаём user_id, чтобы webhook потом мог найти нужного пользователя
        "metadata": {"user_id": callback.from_user.id}
    }

    response = requests.post(
        "https://api.yookassa.ru/v3/payments",
        auth=(SHOP_ID, SECRET_KEY),
        json=payment_data
    )

    if response.status_code == 200:
        data = response.json()
        pay_url = data["confirmation"]["confirmation_url"]

        await callback.message.answer(
            f"💳 <b>Оплата консультации — 12 000 ₽</b>\n\n"
            f"Перейди по ссылке для оплаты:\n\n"
            f"<a href='{pay_url}'>Оплатить через ЮКассу</a>\n\n"
            f"После успешной оплаты ты автоматически перейдёшь к подтверждению.",
            parse_mode="HTML"
        )
    else:
        await callback.message.answer(
            f"⚠️ Ошибка при создании платежа:\n\n<code>{response.text}</code>",
            parse_mode="HTML"
        )

    await callback.answer()
