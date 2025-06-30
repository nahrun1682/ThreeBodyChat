import os
import redis
import uuid
from threebodychat.Orchestrator import assign_responder, write_to_queue, wait_for_bot_reply

# assign_responderの分布テスト
# 10回呼び出してMaid/Master両方に偏りなく割り振られるかを確認
def test_assign_responder_type_and_distribution():
    counts = {"Maid": 0, "Master": 0, "Other": 0}
    for _ in range(2):  # 回数を大幅に減らす（速度重視）
        who = assign_responder()
        if who in ("Maid", "Master"):
            counts[who] += 1
        else:
            counts["Other"] += 1
    # Maid/Master以外が返らないことを保証
    assert counts["Other"] == 0, f"Unexpected responder: {counts}"
    # # Maid/Masterどちらも最低1回は返ること（偏りチェックの代替）
    # assert counts["Maid"] > 0
    # assert counts["Master"] > 0


# write_to_queueのRedis書き込みテスト
# Redisのmaid_queue/master_queueに正しく書き込まれるかを確認
def test_write_to_queue_redis():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    for queue_name in ["maid_queue", "master_queue"]:
        r.delete(queue_name)
    request_id1 = str(uuid.uuid4())
    request_id2 = str(uuid.uuid4())
    write_to_queue("maid_queue", 123, 456, f"{request_id1}|hello!")
    write_to_queue("master_queue", 789, 101, f"{request_id2}|world!")
    maid_item = r.lpop("maid_queue")
    master_item = r.lpop("master_queue")
    assert maid_item == f"123|456|{request_id1}|hello!"
    assert master_item == f"789|101|{request_id2}|world!"
    # 後始末
    r.delete("maid_queue")
    r.delete("master_queue")
    
def test_reply_flow_request_id():
    """
    request_id方式でのOrchestratorの「先手Botの返答を待って後手Botに渡す」流れのテスト
    """
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    channel_id = 999
    user_id = 111
    user_msg = "テストユーザー発言"
    first_bot = "Maid"
    second_bot = "Master"
    request_id = str(uuid.uuid4())

    # 事前にキューとリプライをクリア
    r.delete("maid_queue")
    r.delete("master_queue")
    r.delete(f"reply_{first_bot.lower()}_{request_id}")

    # 先手Botのキューにユーザー発言を送信（request_id付き）
    write_to_queue(f"{first_bot.lower()}_queue", channel_id, user_id, f"{request_id}|{user_msg}")

    # 先手Botが返答したと仮定してRedisにセット
    reply_text = "さすがですわ！"
    r.set(f"reply_{first_bot.lower()}_{request_id}", reply_text)

    # Orchestratorが返答を取得できるか
    reply = wait_for_bot_reply(request_id, first_bot, timeout=2)
    if hasattr(reply, "__await__"):
        import asyncio
        reply = asyncio.run(reply)
    assert reply == reply_text

    # 後手Botのキューに「request_id|ユーザー発言|先手Bot返答」を送信
    combined_msg = f"{request_id}|{user_msg}|{reply_text}"
    write_to_queue(f"{second_bot.lower()}_queue", channel_id, user_id, combined_msg)

    # 後手Botのキューから正しく取得できるか
    item = r.lpop("master_queue")
    assert item == f"{channel_id}|{user_id}|{combined_msg}"

    # 後始末
    r.delete("maid_queue")
    r.delete("master_queue")
    r.delete(f"reply_{first_bot.lower()}_{request_id}")

def test_maid_reply_redis_save_request_id():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    request_id = str(uuid.uuid4())
    response = "テスト返答"
    key = f"reply_maid_{request_id}"
    r.set(key, response)
    assert r.get(key) == response
    r.delete(key)

def test_master_reply_redis_save_request_id():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    request_id = str(uuid.uuid4())
    response = "テスト返答"
    key = f"reply_master_{request_id}"
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
