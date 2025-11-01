from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

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

    # Кнопка к оплате диагностики
    builder = InlineKeyboardBuilder()
    builder.button(text="✨ Оплатить и записаться", callback_data="chapter_15")
    builder.adjust(1)  # одна кнопка на ряд

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()
