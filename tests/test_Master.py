import redis  # Redisサーバーに接続するためのライブラリ
import random  # ランダムな返答を選ぶための標準ライブラリ
import uuid

# Redisのmaster_queue_testにメッセージを書き込み、正しく取り出せるかをテスト
def test_master_queue_redis():
    # Redisサーバーに接続（localhost:6379、文字列でやりとり）
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    queue_name = "master_queue_test"
    test_message = "123|456|テストメッセージ"
    # 事前にキューを空にする
    r.delete(queue_name)
    # rpushでキューにメッセージを追加
    r.rpush(queue_name, test_message)
    # lpopでキューからメッセージを取り出す
    item = r.lpop(queue_name)
    # 取り出した内容が正しいかチェック
    assert item == test_message
    # テスト後にキューを削除
    r.delete(queue_name)

def test_master_queue_redis_request_id():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    queue_name = "master_queue_test"
    request_id = str(uuid.uuid4())
    test_message = f"123|456|{request_id}|テストメッセージ"
    r.delete(queue_name)
    r.rpush(queue_name, test_message)
    item = r.lpop(queue_name)
    assert item == test_message
    r.delete(queue_name)

# Masterの返答がランダムで2種類とも返るかをテスト
def test_master_reply_randomness():
    # 100回ランダムに返答を選び、2種類とも出現するか確認
    replies = set(random.choice(["鹿だな", "やっぱ鹿だな"]) for _ in range(100))
    assert "鹿だな" in replies
    assert "やっぱ鹿だな" in replies

def make_master_response(user_msg):
    """
    Master.pyのロジックを模したテスト用関数。
    user_msg: str, 例 "こんにちは" または "こんにちは|さすがですわ！"
    """
    parts = user_msg.split("|", 1)
    user_question = parts[0]
    prev_bot_reply = parts[1] if len(parts) > 1 else None
    if prev_bot_reply:
        return f"ユーザー:{user_question} / 先手:{prev_bot_reply} / {random.choice(['鹿だな', 'やっぱ鹿だな'])}"
    else:
        return f"ユーザー:{user_question} / {random.choice(['鹿だな', 'やっぱ鹿だな'])}"

# 1. 先手Botとしての動作
def test_master_first_response():
    user_msg = "こんにちは"
    resp = make_master_response(user_msg)
    assert resp.startswith("ユーザー:こんにちは / ")
    assert "/ 先手:" not in resp

# 2. 後手Botとしての動作
def test_master_second_response():
    user_msg = "こんにちは|さすがですわ！"
    resp = make_master_response(user_msg)
    assert resp.startswith("ユーザー:こんにちは / 先手:さすがですわ！") or resp.startswith("ユーザー:こんにちは / 先手:お手伝いしましょうか？") or resp.startswith("ユーザー:こんにちは / 先手:やっぱ鹿だな")
    assert "/ 先手:" in resp

# 3. 区切り文字が複数含まれる場合
def test_master_response_extra_delimiter():
    user_msg = "こんにちは|さすがですわ！|余分"
    resp = make_master_response(user_msg)
    # 2つ目以降はprev_bot_replyに含まれる
    assert resp.startswith("ユーザー:こんにちは / 先手:さすがですわ！|余分 / ")

def test_master_response_with_request_id():
    request_id = str(uuid.uuid4())
    user_msg = f"{request_id}|こんにちは"
    resp = make_master_response(user_msg.split("|",1)[1])  # make_master_responseはuser_question|prev_bot_reply形式
    assert resp.startswith("ユーザー:こんにちは / ")
    assert "/ 先手:" not in resp
    user_msg2 = f"{request_id}|こんにちは|さすがですわ！"
    resp2 = make_master_response("こんにちは|さすがですわ！")
    assert resp2.startswith("ユーザー:こんにちは / 先手:さすがですわ！") or resp2.startswith("ユーザー:こんにちは / 先手:お手伝いしましょうか？") or resp2.startswith("ユーザー:こんにちは / 先手:やっぱ鹿だな")
