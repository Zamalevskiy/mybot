import os
import asyncio
from aiogram import Router, types, F
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Путь к PDF-файлу
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "pdfs", "kak_navesti_poryadok_guide_01.pdf")


@router.callback_query(F.data == "chapter_07")
async def chapter_07_handler(callback: types.CallbackQuery):
    text = (
        "<b>Пошаговый план восстановления, когда кажется, что ты не справляешься.</b>\n\n"
        "Вот короткое содержание гайда\n"
        "- 8 простых шагов, с которых можно начать уже сегодня 👇\n\n"
        "<b>1️⃣ Признание и принятие состояния</b>\n"
        "📍 Признание - это не поражение, а первый шаг к восстановлению сил.\n\n"
        "<b>2️⃣ “Выгрузка” всего, что висит в голове</b>\n"
        "📍 Освободи голову - напиши всё на бумаге, чтобы увидеть, что действительно важно.\n\n"
        "<b>3️⃣ Разделение на категории</b>\n"
        "📍 Когда всё разложено по полочкам, тревога снижается, а фокус возвращается.\n\n"
        "<b>4️⃣ Определи точку опоры</b>\n"
        "📍 Одно маленькое действие даёт энергию для следующего.\n\n"
        "<b>5️⃣ Малые конкретные шаги</b>\n"
        "📍 Каждая маленькая победа возвращает уверенность и чувство движения.\n\n"
        "<b>6️⃣ Визуализация прогресса</b>\n"
        "📍 Отмечай сделанное - дофамин и мотивация не заставят себя ждать.\n\n"
        "<b>7️⃣ Регулярное “обнуление”</b>\n"
        "📍 Вечером - выдох, утром - чистая голова.\n\n"
        "<b>8️⃣ Поддержка и рефлексия</b>\n"
        "📍 Порядок - это не список дел, а внутренний цикл восстановления контроля.\n\n"
        "Полная версия гайда - с примерами, шаблонами и мини-инструкциями - ждёт тебя в файле.\n"
        "Там ты найдёшь простые форматы списков и трекеров, которые реально работают."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="📎 Скачать гайд PDF", callback_data="download_guide_07")

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "download_guide_07")
async def send_pdf(callback: types.CallbackQuery):
    if os.path.exists(PDF_PATH):
        file = FSInputFile(PDF_PATH)
        await callback.message.answer_document(file, caption="Вот твой гайд 💚")
    else:
        await callback.message.answer("❌ Файл не найден. Проверь путь к PDF.")

    # Задержка перед следующим сообщением
    await asyncio.sleep(4)

    text_after = (
        "Если чувствуешь, что даже с планом тяжело собраться - это нормально.\n"
        "Иногда нужна не просто структура, а кто-то, кто поможет увидеть картину целиком.\n\n"
        "Я провожу <b>Кризисные консультации</b> - за 2 часа мы находим, где именно ты застряла, "
        "и составляем ясный план действий."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="👉 Узнать о Консультации", callback_data="chapter_11")

    await callback.message.answer(text_after, reply_markup=builder.as_markup())
    await callback.answer()
