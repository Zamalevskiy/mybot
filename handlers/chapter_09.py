import os
import asyncio
from aiogram import Router, types, F
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Путь к PDF-файлу
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "pdfs", "kak_vernut_uverennost_guide_03.pdf")


@router.callback_query(F.data == "chapter_09")
async def chapter_09_handler(callback: types.CallbackQuery):
    text = (
        "<b>Пошаговый план возвращения к себе, когда не знаешь, куда идти дальше.</b>\n\n"
        "Вот короткое содержание гайда\n"
        "- 6 шагов, которые помогут обрести внутреннюю опору и снова почувствовать почву под ногами 👇\n\n"
        "<b>🌫️ Шаг 1. Остановись. Не убегай от пустоты</b>\n"
        "📍 Принятие пустоты - это не слабость. Это начало возвращения к жизни.\n"
        "<b>🕯️ Шаг 2. Посмотри, где ты потеряла себя</b>\n"
        "📍 Понять, где ты себя потеряла, - уже шаг к возвращению.\n"
        "<b>🧭 Шаг 3. Найди свои внутренние опоры</b>\n"
        "📍 Эти мелочи - не мелочи. Это маркеры твоего пути.\n"
        "<b>🔥 Шаг 4. Разберись с внутренним критиком</b>\n"
        "📍 Твой страх - это не ты. Это просто старая часть, которая устала.\n"
        "<b>🌱 Шаг 5. Маленькие шаги к жизни</b>\n"
        "📍 Это не пустяки. Это кирпичики твоей новой опоры.\n"
        "<b>💎 Шаг 6. Когда становится чуть светлее</b>\n"
        "📍 Уверенность - не в том, чтобы знать всё наперёд. А в том, чтобы чувствовать почву под ногами даже в тумане.\n\n"
        "Полная версия гайда - с практиками, примерами и короткими упражнениями для возвращения уверенности - ждёт тебя в файле."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="📎 Скачать гайд PDF", callback_data="download_guide_09")

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "download_guide_09")
async def send_pdf(callback: types.CallbackQuery):
    if os.path.exists(PDF_PATH):
        file = FSInputFile(PDF_PATH)
        await callback.message.answer_document(file, caption="Вот твой гайд 💎")
    else:
        await callback.message.answer("❌ Файл не найден. Проверь путь к PDF.")

    # Задержка перед следующим сообщением
    await asyncio.sleep(4)

    text_after = (
        "Если чувствуешь, что одной тяжело выбраться и не хватает поддержки - это нормально.\n"
        "Я провожу <b>Кризисные консультации</b>, где мы вместе разбираем, где именно ты застряла, "
        "и помогаем увидеть направление, которое откроет дыхание и смысл."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="👉 Узнать о Консультации", callback_data="chapter_11")

    await callback.message.answer(text_after, reply_markup=builder.as_markup())
    await callback.answer()
