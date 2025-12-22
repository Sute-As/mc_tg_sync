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
        self.client.command(f"""
        CREATE TABLE IF NOT EXISTS {CH_DB}.chat_logs (
            event_time DateTime,
            source String,
            user_name String,
            message String
        ) ENGINE = MergeTree()
        ORDER BY event_time
        """)
        self.client.command(f"""
        CREATE TABLE IF NOT EXISTS {CH_DB}.groups (
            chat_id Int64
        ) ENGINE = ReplacingMergeTree()
        ORDER BY chat_id
        """)
        self.client.command(f"""
        CREATE TABLE IF NOT EXISTS {CH_DB}.users (
            username String,
            mnname String,
            count UInt64
        ) ENGINE = ReplacingMergeTree() ORDER BY username
        """)

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

    async def save_group(self, chat_id: int):
        if not self.client: return
        self.client.command(f"INSERT INTO {CH_DB}.groups (chat_id) VALUES ({chat_id})")
        print(f"Группа {chat_id} сохранена.")

    async def get_groups(self):
        if not self.client: return set()
        result = self.client.query(f"SELECT chat_id FROM {CH_DB}.groups")
        return {row[0] for row in result.result_rows}

    async def update_user(self, username: str, mnname: str, count: int):
        if not self.client: return
        data = [[username, mnname, count]]
        await asyncio.to_thread(self.client.insert, f'{CH_DB}.users', data, column_names=['username', 'mnname', 'count'])

    async def load_users(self):
        if not self.client: return {}
        result = await asyncio.to_thread(self.client.query, f"SELECT username, mnname, count FROM {CH_DB}.users")
        return {row[0]: {"mnname": row[1], "count": row[2]} for row in result.result_rows}


db_logger = ChatLogger()