import clickhouse_connect

client = clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='1111')

result = client.query("SELECT event_time, user_name, message FROM minecraft_chat.chat_logs ORDER BY event_time DESC LIMIT 100")

for row in result.result_rows:
    print(f"[{row[0]}] {row[1]}: {row[2]}")