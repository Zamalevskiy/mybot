import asyncio
from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

async def send_reminder(chat_id: int, bot):
    # Задержка 3 часа 50 минут = 14000 секунд
    await asyncio.sleep(14000)

    # --- Сообщение 1 ---
    text1 = (
        "<b>Хочу напомнить - льготная стоимость 12 000 ₽ за Кризисную консультацию действует ещё 10 минут.</b>\n\n"
        "После этого цена вернётся к обычной - 16 000 ₽.\n\n"
        "Если чувствуешь, что консультация тебе действительно нужна -\n"
        "сделай шаг сейчас, пока можешь воспользоваться старой ценой 🌿"
    )

    builder1 = InlineKeyboardBuilder()
    builder1.button(text="🧩 Оплатить Консультацию", callback_data="chapter_12")
    builder1.adjust(1)  # кнопка одна под другой

    await bot.send_message(
        chat_id=chat_id,
        text=text1,
        reply_markup=builder1.as_markup(),
        parse_mode="HTML"
    )

    # --- Сообщение 2 через 2 секунды ---
    await asyncio.sleep(2)

    text2 = "Или начни с Диагностики ключевой проблемы"

    builder2 = InlineKeyboardBuilder()
    builder2.button(text="✨ Оплатить Диагностику", callback_data="chapter_15")
    builder2.adjust(1)  # кнопка одна под другой

    await bot.send_message(
        chat_id=chat_id,
        text=text2,
        reply_markup=builder2.as_markup(),
        parse_mode="HTML"
    )
