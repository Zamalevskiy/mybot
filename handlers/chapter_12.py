from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
import requests
import uuid
from analytics import log_event

router = Router()

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

    idempotence_key = str(uuid.uuid4())
    payment_data = {
        "amount": {"value": "12000.00", "currency": "RUB"},
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/{callback.from_user.username or 'your_bot_name'}"
        },
        "description": "Кризисная консультация (2 часа).",
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

        text = (
            "<b>Выбери удобный способ оплаты.</b>\n"
            "После оплаты я сразу свяжусь с тобой для уточнения даты и времени встречи.\n\n"
            "Чек придёт автоматически, либо я пришлю его тебе лично."
        )

        builder = InlineKeyboardBuilder()
        
        # Кнопка ЮКасса с промежуточным обработчиком для логирования
        builder.button(text="ЮКасса", callback_data="yookassa_click_12")
        builder.button(text="💳 Перевод на карту / СБП", callback_data="bank_transfer_12")
        builder.button(text="Я оплатила - Написать мне", callback_data="chapter_16")
        builder.adjust(1)

        await callback.message.answer(text, reply_markup=builder.as_markup())
    else:
        await callback.message.answer(
            f"⚠️ Ошибка при создании платежа:\n\n<code>{response.text}</code>",
            parse_mode="HTML"
        )

    await callback.answer()


@router.callback_query(F.data == "yookassa_click_12")
async def yookassa_click_12_handler(callback: types.CallbackQuery):
    # Логирование клика по ЮКасса
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click",
        action_name="yookassa_consultation",
        additional_data="12000"
    )
    
    SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
    SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

    idempotence_key = str(uuid.uuid4())
    payment_data = {
        "amount": {"value": "12000.00", "currency": "RUB"},
        "capture": True,
        "confirmation": {
            "type": "redirect", 
            "return_url": f"https://t.me/{callback.from_user.username or 'your_bot_name'}"
        },
        "description": "Кризисная консультация (2 часа).",
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
        
        # Создаем кнопку с URL для перехода в ЮКассу
        builder = InlineKeyboardBuilder()
        builder.button(text="ЮКасса", url=pay_url)
        
        await callback.message.answer(
            "Нажмите на кнопку ниже для оплаты через ЮКассу 👇",
            reply_markup=builder.as_markup()
        )
    else:
        await callback.message.answer("❌ Ошибка при создании платежа")
    
    await callback.answer()


@router.callback_query(F.data == "bank_transfer_12")
async def bank_transfer_handler(callback: types.CallbackQuery):
    # Логирование выбора оплаты переводом на карту
    log_event(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        action_type="button_click", 
        action_name="bank_transfer_consultation",
        additional_data="12000"
    )
    
    # Перенаправляем в раздел 18 для показа реквизитов
    from handlers.chapter_18 import chapter_18_handler
    await chapter_18_handler(callback)
