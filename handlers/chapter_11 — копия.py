import asyncio
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Универсальный обработчик для перехода в раздел 11
@router.callback_query(F.data == "chapter_11")
async def chapter_11_handler(callback: types.CallbackQuery):
    # Основное сообщение раздела 11
    text = (
        "<b>Когда не можешь думать, но надо что-то решать</b>\n"
        "- за 2 часа мы соберём тебя обратно.\n\n"
        "📍 Только <b>очно</b> - Москва, центр.\n"
        "⏱ Длительность <b>- 2 часа</b>.\n"
        "💰 Стоимость <b>- 12 000 ₽*</b>.\n"
        "*(льготная цена действует 4 часа, потом возвращается обычная - 16 000 ₽.)\n\n"
        "На консультации мы:\n"
        "- останавливаем внутренний хаос и тревогу,\n"
        "- разбираем, что именно сейчас происходит,\n"
        "- и создаём понятный пошаговый план на ближайшие 7-10 дней.\n\n"
        "✨ После встречи у тебя появится чувство контроля и спокойствия - без тяжёлых разговоров и копаний."
    )

    # Кнопки: Оплата и Как проходит консультация (одна под другой)
    builder = InlineKeyboardBuilder()
    builder.button(text="🪷 Оплатить и записаться", callback_data="chapter_12")
    builder.button(text="🎥 Как проходит Консультация?", callback_data="chapter_13")
    builder.adjust(1)  # Разместить по 1 кнопке на ряд

    await callback.message.answer(text, reply_markup=builder.as_markup())

    # Задержка 4 секунды перед вторым сообщением
    await asyncio.sleep(4)

    # Второе сообщение с кнопкой к диагностике
    text_after = (
        "Если чувствуешь, что пока не готова к двум часам - ничего страшного 💛\n"
        "Можно начать с малого - <b>Диагностики ключевой проблемы</b>.\n"
        "Всего 1 час, и часто именно она становится тем самым “вот оно!”."
    )

    builder2 = InlineKeyboardBuilder()
    builder2.button(text="💫 Перейти к диагностике", callback_data="chapter_14")
    builder2.adjust(1)  # По одной кнопке на ряд

    await callback.message.answer(text_after, reply_markup=builder2.as_markup())
    await callback.answer()


