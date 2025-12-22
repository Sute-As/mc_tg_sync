import asyncio
import logging
from services.telegram_bot import bot, dp, grps
from services.mc_log_reader import watch_logs
from utils.db import db_logger

logging.basicConfig(level=logging.INFO)


async def main():
    saved_groups = await db_logger.get_groups()
    if saved_groups:
        grps.clear()
        grps.update(saved_groups)
    else:
        print("Сохраненных групп пока нет.")
    await bot.delete_webhook(drop_pending_updates=True)
    polling_task = asyncio.create_task(dp.start_polling(bot))
    watcher_task = asyncio.create_task(watch_logs(bot, grps))
    await asyncio.gather(polling_task, watcher_task)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")