import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web

# === Аналитика (и инициализация БД аналитики) ===
from utils.analytics import init_db, log_event
init_db()

# === Токен бота ===
from utils.config import TOKEN

# === Определяем режим запуска ===
MODE = os.getenv("MODE", "LOCAL")  # Возможные значения: LOCAL или RENDER
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL Render-сервиса (только для RENDER)

# === Инициализация бота и диспетчера ===
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
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


# === Логгеры аналитики (должны быть подключены ДО роутеров, чтобы ловить всё) ===
@dp.message()
async def _log_all_messages(message: types.Message):
    try:
        log_event(
            user_id=message.from_user.id,
            username=getattr(message.from_user, "username", None),
            first_name=getattr(message.from_user, "first_name", None),
            last_name=getattr(message.from_user, "last_name", None),
            event_type="message",
            event_name="message_text",
            payload=message.text or "",
            chapter=None,
            meta={"message_id": message.message_id}
        )
    except Exception as e:
        # защищаемся от ошибок логирования, чтобы не ломать бот
        print("Analytics log error (message):", e)


@dp.callback_query()
async def _log_all_callbacks(callback: types.CallbackQuery):
    try:
        cd = callback.data or ""
        chapter = cd if cd.startswith("chapter_") else None
        log_event(
            user_id=callback.from_user.id,
            username=getattr(callback.from_user, "username", None),
            first_name=getattr(callback.from_user, "first_name", None),
            last_name=getattr(callback.from_user, "last_name", None),
            event_type="callback",
            event_name=cd,
            payload=cd,
            chapter=chapter,
            meta={"message_id": callback.message.message_id if callback.message else None}
        )
    except Exception as e:
        print("Analytics log error (callback):", e)
    finally:
        # обязательно отвечаем на callback, чтобы Telegram не "повесил" кнопку
        try:
            await callback.answer()
        except Exception:
            pass


# === Подключение разделов (роутеров) ===
from handlers import (
    chapter_01, chapter_02, chapter_03, chapter_04, chapter_05, chapter_06,
    chapter_07, chapter_08, chapter_09, chapter_10, chapter_11, chapter_12,
    chapter_13, chapter_14, chapter_15, chapter_16, chapter_18, chapter_19,
    chapter_20
)
from chapters.chapter_17 import send_reminder

routers = [
    chapter_01.router, chapter_02.router, chapter_03.router, chapter_04.router,
    chapter_05.router, chapter_06.router, chapter_07.router, chapter_08.router,
    chapter_09.router, chapter_10.router, chapter_11.router, chapter_12.router,
    chapter_13.router, chapter_14.router, chapter_15.router, chapter_16.router,
    chapter_18.router, chapter_19.router, chapter_20.router
]
for r in routers:
    dp.include_router(r)


# === Webhook обработчик для Telegram (aiohttp) ===
async def handle_webhook(request):
    try:
        data = await request.json()
        update = types.Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        print("Error in handle_webhook:", e)
    return web.Response(status=200)


# === HTTP сервер для Render ===
async def run_webserver():
    app = web.Application()
    app.router.add_post(f"/webhook/{TOKEN}", handle_webhook)
    app.router.add_get("/", lambda request: web.Response(text="Бот работает! ✅"))

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Web server запущен на порту {port}")
    return runner


# === Установка webhook ===
async def setup_webhook():
    if not WEBHOOK_URL:
        raise RuntimeError("WEBHOOK_URL не указан в окружении, нельзя настроить webhook.")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook/{TOKEN}")
    print(f"✅ Webhook установлен на {WEBHOOK_URL}/webhook/{TOKEN}")


# === Главная функция ===
async def main():
    if MODE == "LOCAL":
        print("🚀 Запуск бота в режиме LOCAL (polling)...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    else:
        print("🌐 Запуск бота в режиме RENDER (webhook)...")
        await setup_webhook()
        runner = await run_webserver()
        try:
            while True:
                await asyncio.sleep(3600)
        except (KeyboardInterrupt, SystemExit):
            print("🛑 Остановка бота...")
        finally:
            await bot.session.close()
            await runner.cleanup()
            print("✅ Сессия и сервер закрыты.")


# === Запуск ===
if __name__ == "__main__":
    asyncio.run(main())



if __name__ == "__main__":
    asyncio.run(main())
