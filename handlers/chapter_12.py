from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command

router = Router()

# 🔹 Тестовый токен, выданный @BotFather при подключении ЮKassa
PROVIDER_TOKEN = "381764678:TEST:148623"  # использовать токен, выданный ботфазером, не ключ из кабинета Юкассы

# 🔹 Данные о товаре
TITLE = "Консультация"
DESCRIPTION = "Кризисная консультация (2 часа)."
CURRENCY = "RUB"
PRICE = 12000  # в рублях
PAYLOAD = "consultation_payment"

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


# 🔹 Кнопка Юкассы — отправка счёта на оплату
@router.callback_query(F.data == "yookassa_pay")
async def yookassa_pay(callback: types.CallbackQuery):
    prices = [LabeledPrice(label=TITLE, amount=PRICE * 100)]  # сумма в копейках

    await callback.message.answer_invoice(
        title=TITLE,
        description=DESCRIPTION,
        provider_token=PROVIDER_TOKEN,
        currency=CURRENCY,
        prices=prices,
        payload=PAYLOAD,
        start_parameter="consultation",
    )
    await callback.answer()


# 🔹 Обработка pre_checkout_query (обязательный шаг)
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# 🔹 Обработка успешной оплаты
@router.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    payment_info = message.successful_payment.to_python()
    print("✅ Успешная оплата:", payment_info)

    await message.answer(
        "<b>✅ Оплата прошла успешно!</b>\n\n"
        "Спасибо! Я свяжусь с тобой в ближайшее время для уточнения деталей встречи 🙌"
    )

    # 🔹 Переход в раздел 16
    from chapters.chapter_16 import send_chapter_16
    await send_chapter_16(message)
