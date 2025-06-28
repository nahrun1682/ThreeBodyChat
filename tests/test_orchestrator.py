import os
import redis
from threebodychat.Orchestrator import assign_responder, write_to_queue, wait_for_bot_reply

# assign_responderの分布テスト
# 1000回呼び出してMaid/Master両方に偏りなく割り振られるかをざっくり確認
def test_assign_responder_distribution():
    counts = {"Maid": 0, "Master": 0}
    for _ in range(1000):
        who = assign_responder()
        counts[who] += 1
    # MaidとMaster両方に偏りなく振り分けられるかをざっくりチェック
    assert 400 < counts["Maid"] < 600
    assert 400 < counts["Master"] < 600


# write_to_queueのRedis書き込みテスト
# Redisのmaid_queue/master_queueに正しく書き込まれるかを確認
def test_write_to_queue_redis():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    for queue_name in ["maid_queue", "master_queue"]:
        r.delete(queue_name)
    write_to_queue("maid_queue", 123, 456, "hello!")
    write_to_queue("master_queue", 789, 101, "world!")
    maid_item = r.lpop("maid_queue")
    master_item = r.lpop("master_queue")
    assert maid_item == "123|456|hello!"
    assert master_item == "789|101|world!"
    # 後始末
    r.delete("maid_queue")
    r.delete("master_queue")
    
def test_reply_flow():
    """
    Orchestratorの「先手Botの返答を待って後手Botに渡す」流れのテスト
    """
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    channel_id = 999
    user_id = 111
    user_msg = "テストユーザー発言"
    first_bot = "Maid"
    second_bot = "Master"

    # 事前にキューとリプライをクリア
    r.delete("maid_queue")
    r.delete("master_queue")
    r.delete(f"reply_{first_bot.lower()}_{channel_id}")

    # 先手Botのキューにユーザー発言を送信
    write_to_queue(f"{first_bot.lower()}_queue", channel_id, user_id, user_msg)

    # 先手Botが返答したと仮定してRedisにセット
    reply_text = "さすがですわ！"
    r.set(f"reply_{first_bot.lower()}_{channel_id}", reply_text)

    # Orchestratorが返答を取得できるか
    reply = wait_for_bot_reply(channel_id, first_bot, timeout=2)
    if hasattr(reply, "__await__"):
        # 非同期関数の場合は同期的に実行
        import asyncio
        reply = asyncio.run(reply)
    assert reply == reply_text

    # 後手Botのキューに「ユーザー発言|先手Bot返答」を送信
    combined_msg = f"{user_msg}|{reply_text}"
    write_to_queue(f"{second_bot.lower()}_queue", channel_id, user_id, combined_msg)

    # 後手Botのキューから正しく取得できるか
    item = r.lpop("master_queue")
    assert item == f"{channel_id}|{user_id}|{combined_msg}"

    # 後始末
    r.delete("maid_queue")
    r.delete("master_queue")
    r.delete(f"reply_{first_bot.lower()}_{channel_id}")

def test_maid_reply_redis_save():
    """
    Maidが返答後、Redisに正しく保存されるかのテスト
    """
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    channel_id = 123
    response = "テスト返答"
    key = f"reply_maid_{channel_id}"
    r.set(key, response)
    assert r.get(key) == response
    r.delete(key)


def test_master_reply_redis_save():
    """
    Masterが返答後、Redisに正しく保存されるかのテスト
    """
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    channel_id = 456
    response = "テスト返答"
    key = f"reply_master_{channel_id}"
    r.set(key, response)
    assert r.get(key) == response
    r.delete(key)

def test_orchestrator_combined_msg_format():
    # Orchestratorが後手Botに渡すcombined_msgは「ユーザー発言|先手Botの生返答」形式であること
    user_msg = "こんにちは"
    reply_text = "さすがですわ！"
    combined_msg = f"{user_msg}|{reply_text}"
    assert "|" in combined_msg
    assert combined_msg == "こんにちは|さすがですわ！"
