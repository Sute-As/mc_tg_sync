import unittest
import sys
import os
from utils.db import db_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDatabase(unittest.IsolatedAsyncioTestCase):

    async def test_1_save_and_get_groups(self):
        """Тест регистрации группы"""
        test_chat_id = -100123456789

        await db_logger.save_group(test_chat_id)
        groups = await db_logger.get_groups()

        self.assertIn(test_chat_id, groups, "Фиктивная группа не найдена в базе!")
        print("\n✅ Тест групп пройден")

    async def test_2_user_management(self):
        test_user = "AstralniyDetonator228"
        test_mc_name = "AstralDetonator3000"
        test_count = 5
        await db_logger.update_user(test_user, test_mc_name, test_count)
        all_users = await db_logger.load_users()
        self.assertIn(test_user, all_users, "Пользователь не найден в базе")
        self.assertEqual(all_users[test_user]["mnname"], test_mc_name)
        self.assertEqual(all_users[test_user]["count"], test_count)
        print("✅ Тест пользователей и счетчика пройден")

    async def test_3_log_message(self):
        await db_logger.log_message("TEST_SOURCE", "Tester", "Hello ClickHouse!")
        print("✅ Тест записи лога пройден")


if __name__ == "__main__":
    unittest.main()