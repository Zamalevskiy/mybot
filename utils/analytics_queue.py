import asyncio
from utils.analytics import log_event

event_queue = asyncio.Queue()

async def worker():
    while True:
        event = await event_queue.get()
        try:
            log_event(**event)
        except Exception as e:
            print(f"Ошибка логирования: {e}")
        event_queue.task_done()

# Запуск воркера в фоне
async def start_worker():
    asyncio.create_task(worker())

# Функция для добавления событий в очередь
def enqueue_event(**kwargs):
    event_queue.put_nowait(kwargs)
