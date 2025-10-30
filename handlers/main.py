from aiogram import Router
from aiogram.types import Message
from keyboards.menu import main_menu

router = Router()

@router.message(commands=["start"])
async def start_command(message: Message):
    await message.answer(
        "Привет! Выбери свою боль из списка ниже:",
        reply_markup=main_menu()
    )
