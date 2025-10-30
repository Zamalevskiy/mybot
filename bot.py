import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web
import os

# === Токен твоего бота ===
from utils.config import TOKEN

# === URL твоего Render сервиса ===
# Например: https://mybot-945b.onrender.com
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

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
    builder.button(text="🌪 В жизни бардак, не знаю что делать", callback_data="chapter_03")
    builder.button(text="🙂 Вроде есть всё, а радости нет", callback_data="chapter_04")
    builder.button(text="💔 Пусто внутри. Одиночество и боль", callback_data="chapter_05")
    builder.button(text="😔 Устала быть сильной, хочу покоя", callback_data="chapter_06")
    builder.button(text="👤 Обо мне", callback_data="chapter_02")
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
    chapter_01, chapter_02, chapter_03, chapter_04, chapter_05, chapter_06,
    chapter_07, chapter_08, chapter_09, chapter_10, chapter_11, chapter_12,
    chapter_13, chapter_14, chapter_15, chapter_16, chapter_18, chapter_19,
    chapter_20
)
from chapters.chapter_17 import send_reminder

# === Подключение роутеров ===
routers = [
    chapter_01.router, chapter_02.router, chapter_03.router, chapter_04.router,
    chapter_05.router, chapter_06.router, chapter_07.router, chapter_08.router,
    chapter_09.router, chapter_10.router, chapter_11.router, chapter_12.router,
    chapter_13.router, chapter_14.router, chapter_15.router, chapter_16.router,
    chapter_18.router, chapter_19.router, chapter_20.router
]

for r in routers:
    dp.include_router(r)


# === Webhook обработчик ===
async def handle_webhook(request):
    update = await request.json()
    await dp.feed_update(bot, update)
    return web.Response(status=200)


# === HTTP сервер для Render ===
async def run_webserver():
    app = web.Application()
    app.router.add_post(f"/webhook/{TOKEN}", handle_webhook)  # Telegram шлёт сюда обновления
    app.router.add_get("/", lambda request: web.Response(text="Бот работает! ✅"))

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Web server запущен на порту {port}")
    return runner  # нужно, чтобы потом корректно закрыть


# === Установка webhook перед запуском ===
async def setup_webhook():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook/{TOKEN}")
    print(f"✅ Webhook установлен на {WEBHOOK_URL}/webhook/{TOKEN}")


# === Главный цикл ===
async def main():
    await setup_webhook()
    runner = await run_webserver()

    # Чтобы Render не "убивал" процесс — держим его живым
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Остановка бота...")
    finally:
        await bot.session.close()
        await runner.cleanup()
        print("✅ Сессия и сервер закрыты.")


if __name__ == "__main__":
    asyncio.run(main())
