import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

# === Токен твоего бота ===
from utils.config import TOKEN

# === Инициализация бота и диспетчера ===
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# === Обработчик команды /start ===
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="️🌪 В жизни бардак, не знаю что делать", callback_data="chapter_03")
    builder.button(text=" 🙂 Вроде есть всё, а радости нет", callback_data="chapter_04")
    builder.button(text=" 💔 Пусто внутри. Одиночество и боль", callback_data="chapter_05")
    builder.button(text=" 😔 Устала быть сильной, хочу покоя", callback_data="chapter_06")
    builder.button(text=" 👤 Обо мне", callback_data="chapter_02")
    builder.adjust(1)

    text = (
        "<b>🌪️ В жизни бардак и не знаешь, с чего начать?</b>\n\n"
        "Не буду грузить теориями. Давай разберёмся по-простому — "
        "что делать прямо сейчас, чтобы стало легче.\n\n"
        "<b>Выбери, что тебе ближе сейчас?</b>"
    )

    await message.answer(text, reply_markup=builder.as_markup())


# === Подключение разделов ===
from handlers import (
    chapter_01,
    chapter_02,
    chapter_03,
    chapter_04,
    chapter_05,
    chapter_06,
    chapter_07,
    chapter_08,
    chapter_09,
    chapter_10,
    chapter_11,
    chapter_12,
    chapter_13,
    chapter_14,
    chapter_15,
    chapter_16,
    chapter_18,
    chapter_19,
    chapter_20,
)

# === Раздел 17 (находится в папке chapters) ===
from chapters.chapter_17 import send_reminder

# === Подключение роутеров ===
dp.include_router(chapter_01.router)
dp.include_router(chapter_02.router)
dp.include_router(chapter_03.router)
dp.include_router(chapter_04.router)
dp.include_router(chapter_05.router)
dp.include_router(chapter_06.router)
dp.include_router(chapter_07.router)
dp.include_router(chapter_08.router)
dp.include_router(chapter_09.router)
dp.include_router(chapter_10.router)
dp.include_router(chapter_11.router)
dp.include_router(chapter_12.router)
dp.include_router(chapter_13.router)
dp.include_router(chapter_14.router)
dp.include_router(chapter_15.router)
dp.include_router(chapter_16.router)
dp.include_router(chapter_18.router)
dp.include_router(chapter_19.router)
dp.include_router(chapter_20.router)


# === HTTP сервер для Render (порт 10000) ===
async def handle_root(request):
    return web.Response(text="Бот работает!")

async def run_webserver():
    app = web.Application()
    app.router.add_get("/", handle_root)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)  # Render требует открытый порт
    await site.start()
    print("Web server запущен на порту 10000")


# === Запуск бота и веб-сервера одновременно ===
async def main():
    print("Бот запущен...")
    # Запускаем веб-сервер
    asyncio.create_task(run_webserver())
    # Запускаем polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
