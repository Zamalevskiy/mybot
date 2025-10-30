import os
import asyncio
from aiogram import Router, types, F
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Путь к PDF-файлу
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "pdfs", "kak_vernut_radost_guide_02.pdf")


@router.callback_query(F.data == "chapter_08")
async def chapter_08_handler(callback: types.CallbackQuery):
    text = (
        "<b>Пошаговый план, как снова почувствовать жизнь, когда внутри тишина.</b>\n\n"
        "Вот краткое содержание гайда\n"
        "- 7 шагов, которые помогают вернуть тепло, вкус к жизни и контакт с собой 👇 и 8й секретный шаг внутри файла.\n\n"
        "<b>🌿 ШАГ 1. Признать: “я выгорела, но это не конец.”</b>\n"
        "💡 Осознание - это не слабость, а начало восстановления. Только признав, что силы на нуле, можно перестать себя гнать.\n\n"
        "<b>🌸 ШАГ 2. Верни контакт с телом.</b>\n"
        "💡 Простое дыхание, касание к себе, медленное движение - возвращают ощущение “я живая”.\n\n"
        "<b>💗 ШАГ 3. Замени “надо” на “хочу”.</b>\n"
        "💡 Маленькое “хочу” в дне возвращает ощущение вкуса жизни - то, ради чего хочется просыпаться.\n\n"
        "<b>🔥 ШАГ 4. Найди свои “живые смыслы”.</b>\n"
        "💡 Иногда достаточно вспомнить, ради чего тебе когда-то становилось тепло. Это возвращает внутреннюю нить.\n\n"
        "<b>🕊️ ШАГ 5. Перестань жить только “для других”.</b>\n"
        "💡 Радость - не эгоизм. Когда ты наполняешь себя, всем вокруг становится легче дышать.\n\n"
        "<b>🌼 ШАГ 6. Слушай себя без осуждения.</b>\n"
        "💡 Просто позволить себе быть — без критики и “надо” - это уже шаг к возвращению чувств.\n\n"
        "<b>🌙 ШАГ 7. Разреши себе не быть сильной.</b>\n"
        "💡 “Я не обязана всё тащить одна” - с этого момента внутри впервые становится по-настоящему тепло.\n\n"
        "Полная версия гайда - с мини-практиками, телесными упражнениями и реальными примерами восстановления - ждёт тебя в файле.\n"
        "Он короткий, живой и создан специально для таких состояний, когда “не тянет даже думать”."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="📎 Скачать гайд PDF", callback_data="download_guide_08")

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "download_guide_08")
async def send_pdf(callback: types.CallbackQuery):
    if os.path.exists(PDF_PATH):
        file = FSInputFile(PDF_PATH)
        await callback.message.answer_document(file, caption="Вот твой гайд 💗")
    else:
        await callback.message.answer("❌ Файл не найден. Проверь путь к PDF.")

    # Задержка перед следующим сообщением
    await asyncio.sleep(4)

    text_after = (
        "Если чувствуешь, что даже с простыми шагами трудно сдвинуться с места - это нормально.\n"
        "Иногда нужна не инструкция, а человек, который поможет увидеть, где именно ты потеряла контакт с собой и провести за руку.\n\n"
        "На <b>Кризисной консультации</b> мы за 2 часа разберём твоё состояние, вернём ясность "
        "и сделаем план выхода из этой ситуации."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="🌿 Узнать о Консультации", callback_data="chapter_11")

    await callback.message.answer(text_after, reply_markup=builder.as_markup())
    await callback.answer()
