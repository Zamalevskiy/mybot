import asyncio
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Вставки для раздела 17
from loader import bot  # если у тебя есть общий объект bot
from chapters import chapter_17  # импорт функции напоминания
from utils.chapter16 import user_reached_chapter_16  # проверка достижения раздела 16

router = Router()

@router.callback_query(F.data == "chapter_11")
async def chapter_11_handler(callback: types.CallbackQuery):
    text = (
        "<b>Когда не можешь думать, но надо что-то решать</b>\n"
        "- за 2 часа мы соберём тебя обратно.\n\n"
        "📍 Только <b>очно</b> - Москва, центр.\n"
        "⏱ Длительность <b>- 2 часа</b>.\n"
        "💰 Стоимость <b>- 12 000 ₽*</b>.\n"
        "*(льготная цена действует 4 часа, потом возвращается обычная\n"
        "- 16 000 ₽.)\n\n"
        "На консультации мы:\n"
        "- останавливаем внутренний хаос и тревогу,\n"
        "- разбираем, что именно сейчас происходит,\n"
        "- и создаём понятный пошаговый план на ближайшие 7-10 дней.\n\n"
        "✨ После встречи у тебя появится чувство контроля и спокойствия - без тяжёлых разговоров и копаний."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="🪷 Оплатить и записаться", callback_data="chapter_12")
    builder.button(text="🎥 Как проходит Консультация?", callback_data="chapter_13")
    builder.adjust(1)

    await callback.message.answer(text, reply_markup=builder.as_markup())

    # Запуск таймера раздела 17
    if not user_reached_chapter_16(callback.from_user.id):
        asyncio.create_task(chapter_17.send_reminder(callback.from_user.id, bot))

    await asyncio.sleep(8)

    text_after = (
        "Если чувствуешь, что пока не готова к двум часам - ничего страшного 💛\n"
        "Можно начать с малого - <b>Диагностики ключевой проблемы</b>.\n"
        "Всего 1 час, и часто именно она становится тем самым “вот оно!”."
    )

    builder2 = InlineKeyboardBuilder()
    builder2.button(text="💫 Перейти к диагностике", callback_data="chapter_14")
    builder2.adjust(1)

    await callback.message.answer(text_after, reply_markup=builder2.as_markup())
    await callback.answer()
