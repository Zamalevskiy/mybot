from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "chapter_01")
async def chapter_01_handler(callback: types.CallbackQuery):
    # Создаём кнопки разделов 3–6
    builder = InlineKeyboardBuilder()
    builder.button(text="🌪В жизни бардак, не знаю что делать", callback_data="chapter_03")
    builder.button(text="🙂Вроде есть всё, а радости нет", callback_data="chapter_04")
    builder.button(text="💔Пусто внутри. Одиночество и боль", callback_data="chapter_05")
    builder.button(text="😔Устала быть сильной, хочу покоя", callback_data="chapter_06")
    builder.adjust(1)  # 1 кнопка в строке

    # Текст раздела 1
    text = "<b>Выбери, что тебе ближе сейчас?</b>"

    # Отправляем сообщение с кнопками
    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()
