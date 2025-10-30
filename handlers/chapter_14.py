from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Вставка для проверки раздела 16 и запуска напоминания
from loader import bot
from chapters import chapter_17
from utils.chapter16 import user_reached_chapter_16
import asyncio

router = Router()

@router.callback_query(F.data == "chapter_14")
async def chapter_14_handler(callback: types.CallbackQuery):
    text = (
        "<b>Диагностика текущей ключевой проблемы.</b>\n\n"
        "Если не понимаешь, с чего начать - начни с диагностики.\n"
        "Это короткая встреча, где мы вместе разберём твою ситуацию, "
        "увидим, где именно сейчас “застряло” и что мешает двигаться дальше.\n\n"
        "📍 Только <b>очно</b> - Москва, центр.\n"
        "⏱ Длительность <b>- 1 час</b>.\n"
        "💰 Стоимость <b>- 5 000 ₽</b>\n\n"
        "<b>🌿 Что ты получаешь:</b>\n"
        "Чёткое понимание, что именно тебя держит и где теряются силы.\n"
        "Я помогу увидеть суть, собрать фокус и наметить путь к изменениям.\n\n"
        "<b>Хочешь узнать, какую ключевую проблему прячет твой мозг - переходи к записи прямо сейчас 👇</b>"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="✨ Оплатить и записаться", callback_data="chapter_15")
    builder.adjust(1)

    await callback.message.answer(text, reply_markup=builder.as_markup())

    # Запуск таймера раздела 17
    if not user_reached_chapter_16(callback.from_user.id):
        asyncio.create_task(chapter_17.send_reminder(callback.from_user.id, bot))

    await callback.answer()
