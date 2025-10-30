# chapter_20.py (шаблон пустышки)
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Заглушка обработчика раздела
@router.callback_query(F.data == "chapter_20")
async def chapter_20_handler(callback: types.CallbackQuery):
    text = "Раздел 20 пока в разработке. Контент скоро появится."
    await callback.message.answer(text)
    await callback.answer()
