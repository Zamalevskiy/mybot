import os
import asyncio
from aiogram import Router, types, F
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Путь к PDF-файлу
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "pdfs", "kak_vosstanovit_spokoystvie_guide_04.pdf")


@router.callback_query(F.data == "chapter_10")
async def chapter_10_handler(callback: types.CallbackQuery):
    text = (
        "<b>Пошаговый план, чтобы перестать тащить всё самой и вернуть себе покой.</b>\n\n"
        "Вот короткая выдержка из гайда\n"
        "- 7 простых шагов, с которых можно начать уже сегодня 👇\n\n"
        "<b>1️⃣ Понять, что именно тебя держит в тревоге.</b>\n"
        "📍 Первый шаг к спокойствию - не бороться с тревогой, а увидеть её источник.\n"
        "<b>2️⃣ Вернуть себе право быть живой, а не «идеальной».</b>\n"
        "📍 Это создаёт новый внутренний контекст: ты можешь жить, а не выживать.\n"
        "<b>3️⃣ Успокоить тело - вернуть ощущение опоры.</b>\n"
        "📍 Заземление и контакт с телом - уже шаг к ощущению спокойствия.\n"
        "<b>4️⃣ Освободить место для чувств.</b>\n"
        "📍 Проживание и сброс накопившихся эмоций снижает тревогу и освобождает пространство для себя.\n"
        "<b>5️⃣ Учиться не нести всё одной.</b>\n"
        "📍 Принимать помощь и доверять другим - то, что поможет тебе вернуть энергию и внутреннюю лёгкость.\n"
        "<b>6️⃣ Создай свои «островки спокойствия».</b>\n"
        "📍 Это не пустяки. Это важные опоры твоего внутреннего равновесия.\n"
        "<b>7️⃣ Зафиксировать новое состояние.</b>\n"
        "📍 Так ты учишь нервную систему фиксировать не тревогу, а спокойствие, даже если внешние обстоятельства нестабильны.\n\n"
        "Полная версия гайда - с примерами, мини-инструкциями и практическими упражнениями - ждёт тебя в файле.\n"
        "Там шаги подробно расписаны и легко применимы в повседневной жизни."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="📎 Скачать гайд PDF", callback_data="download_guide_10")

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(F.data == "download_guide_10")
async def send_pdf(callback: types.CallbackQuery):
    if os.path.exists(PDF_PATH):
        file = FSInputFile(PDF_PATH)
        await callback.message.answer_document(file, caption="Вот твой гайд 🌿")
    else:
        await callback.message.answer("❌ Файл не найден. Проверь путь к PDF.")

    # Задержка перед следующим сообщением
    await asyncio.sleep(4)

    text_after = (
        "Если даже с планом трудно собраться и обрести устойчивость - это нормально.\n"
        "Иногда нужна не только структура, а кто-то, кто поможет увидеть всю картину целиком.\n\n"
        "На <b>Кризисной консультации</b> за 2 часа мы найдём, где именно «спряталась» твоя тревога, "
        "и составим план действий, который реально работает."
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="👉 Узнать о Консультации", callback_data="chapter_11")

    await callback.message.answer(text_after, reply_markup=builder.as_markup())
    await callback.answer()
