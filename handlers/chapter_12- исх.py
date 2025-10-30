from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data == "chapter_12")
async def chapter_12_handler(callback: types.CallbackQuery):
    text = (
        "<b>Выбери удобный способ оплаты.</b>\n"
        "После оплаты я сразу свяжусь с тобой для уточнения даты и времени встречи.\n\n"
        "Чек придёт автоматически, либо я пришлю его тебе лично."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="ЮКасса", callback_data="yookassa_placeholder")  # Заглушка для Юкассы
    builder.button(text="💳 Перевод на карту / СБП", callback_data="chapter_18")
    builder.adjust(1)  # кнопки одна под другой

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


# Заглушка для кнопки Юкассы (ничего не делает, просто подтверждает нажатие)
@router.callback_query(F.data == "yookassa_placeholder")
async def yookassa_placeholder(callback: types.CallbackQuery):
    await callback.answer("🔒 Оплата через ЮКассу будет доступна после проверки и подключения.", show_alert=True)
