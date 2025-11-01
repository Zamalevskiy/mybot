from aiogram import Router, types, F
from aiogram.types import LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Тестовые данные ЮKassa
SHOP_ID = 1196067
SECRET_KEY = "test_5zzs33Y__yTMDRcdU9TbQb7wDsILf0OdwZFhexwqhjQ2"

@router.callback_query(F.data == "chapter_12")
async def chapter_12_handler(callback: types.CallbackQuery):
    text = (
        "<b>Выбери удобный способ оплаты.</b>\n"
        "После оплаты я сразу свяжусь с тобой для уточнения даты и времени встречи.\n\n"
        "Чек придёт автоматически, либо я пришлю его тебе лично."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="ЮKassa", callback_data="yookassa_pay")
    builder.button(text="💳 Перевод на карту / СБП", callback_data="chapter_18")
    builder.adjust(1)  # кнопки одна под другой

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "yookassa_pay")
async def yookassa_pay(callback: types.CallbackQuery):
    prices = [LabeledPrice(label="Кризисная консультация (2 часа)", amount=12000 * 100)]  # сумма в копейках

    await callback.message.answer_invoice(
        title="Консультация",
        description="Кризисная консультация (2 часа).",
        payload="consultation_16",  # уникальный идентификатор платежа
        provider_token=SECRET_KEY,
        currency="RUB",
        prices=prices,
        start_parameter="consultation"
    )
    await callback.answer()


# Обработка успешного платежа и перевод в раздел 16
@router.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    # Здесь пользователь успешно оплатил консультацию
    # Перенаправляем его в раздел 16
    from handlers import chapter_16  # импорт раздела 16
    await chapter_16.router._listen_update(message)  # вызов обработчика раздела 16

