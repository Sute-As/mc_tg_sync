import clickhouse_connect
import asyncio
from datetime import datetime
from config import CH_HOST, CH_PORT, CH_USER, CH_PASSWORD, CH_DB


class ChatLogger:
    def __init__(self):
        self.client = None
        self._connect()
        self._init_db()

    def _connect(self):
        try:
            self.client = clickhouse_connect.get_client(
                host=CH_HOST,
                port=CH_PORT,
                username=CH_USER,
                password=CH_PASSWORD
            )
            self.client.command(f"CREATE DATABASE IF NOT EXISTS {CH_DB}")
        except Exception as e:
            print(f"Ошибка подключения к ClickHouse: {e}")

    def _init_db(self):
        if not self.client: return
        schema = f"""
        CREATE TABLE IF NOT EXISTS {CH_DB}.chat_logs (
            event_time DateTime,
            source String,
            user_name String,
            message String
        ) ENGINE = MergeTree()
        ORDER BY event_time
        """
        self.client.command(schema)
        print("ClickHouse: Таблица логов готова.")

    def _insert_sync(self, source: str, user: str, message: str):
        if not self.client: return
        try:
            data = [[datetime.now(), source, user, message]]
            self.client.insert(f'{CH_DB}.chat_logs', data,
                               column_names=['event_time', 'source', 'user_name', 'message'])
        except Exception as e:
            print(f"Ошибка записи лога в CH: {e}")

    async def log_message(self, source: str, user: str, message: str):
        await asyncio.to_thread(self._insert_sync, source, user, message)

db_logger = ChatLogger()