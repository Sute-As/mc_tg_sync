import asyncio
import logging
from services.telegram_bot import bot, dp
from services.mc_log_reader import watch_logs
logging.basicConfig(level=logging.INFO)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    polling_task = asyncio.create_task(dp.start_polling(bot))
    watcher_task = asyncio.create_task(watch_logs())
    await asyncio.gather(polling_task, watcher_task)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")