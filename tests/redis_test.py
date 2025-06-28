import redis
import time

# Redisに接続
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# まず「maid_queue」にメッセージを追加してみる
test_message = "これはテストですわ"
r.lpush("maid_queue", test_message)
print(f"『{test_message}』をmaid_queueに追加しました。")

# 次に「maid_queue」から取り出してみる
print("maid_queueから取り出しを試みます…（2秒待機）")
time.sleep(2)
item = r.rpop("maid_queue")
if item:
    print(f"maid_queueから取り出せた内容：{item}")
else:
    print("maid_queueは空です。")

print("テスト完了ですわ！")
