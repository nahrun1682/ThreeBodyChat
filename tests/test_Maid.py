import redis  # Redisサーバーに接続するためのライブラリ
import random  # ランダムな返答を選ぶための標準ライブラリ
import uuid
from unittest.mock import patch, MagicMock
from threebodychat.Maid import MaidBot

# Redisのmaid_queue_testにメッセージを書き込み、正しく取り出せるかをテスト
def test_maid_queue_redis():
    # Redisサーバーに接続（localhost:6379、文字列でやりとり）
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    queue_name = "maid_queue_test"
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

def test_maid_queue_redis_request_id():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    queue_name = "maid_queue_test"
    request_id = str(uuid.uuid4())
    test_message = f"123|456|{request_id}|テストメッセージ"
    r.delete(queue_name)
    r.rpush(queue_name, test_message)
    item = r.lpop(queue_name)
    assert item == test_message
    r.delete(queue_name)

def make_maid_response(user_msg):
    """
    Maid.pyのロジックを模したテスト用関数。
    user_msg: str, 例 "こんにちは" または "こんにちは|さすがですわ！"
    """
    parts = user_msg.split("|", 1)
    user_question = parts[0]
    prev_bot_reply = parts[1] if len(parts) > 1 else None
    if prev_bot_reply:
        return f"ユーザー:{user_question} / 先手:{prev_bot_reply} / {random.choice(['さすがですわ！', 'お手伝いしましょうか？'])}"
    else:
        return f"ユーザー:{user_question} / {random.choice(['さすがですわ！', 'お手伝いしましょうか？'])}"

# 1. 先手Botとしての動作
def test_maid_first_response():
    user_msg = "こんにちは"
    resp = make_maid_response(user_msg)
    assert resp.startswith("ユーザー:こんにちは / ")
    assert "/ 先手:" not in resp

# 2. 後手Botとしての動作
def test_maid_second_response():
    user_msg = "こんにちは|さすがですわ！"
    resp = make_maid_response(user_msg)
    assert resp.startswith("ユーザー:こんにちは / 先手:さすがですわ！") or resp.startswith("ユーザー:こんにちは / 先手:お手伝いしましょうか？")
    assert "/ 先手:" in resp

# 3. 区切り文字が複数含まれる場合
def test_maid_response_extra_delimiter():
    user_msg = "こんにちは|さすがですわ！|余分"
    resp = make_maid_response(user_msg)
    # 2つ目以降はprev_bot_replyに含まれる
    assert resp.startswith("ユーザー:こんにちは / 先手:さすがですわ！|余分 / ")

def test_no_nested_reply():
    # 先手Botの返答を「ユーザー:こんにちは / さすがですわ！」のような整形済みで渡しても
    # 後手Botはネストしない（Orchestratorが生返答のみ渡す前提）
    user_msg = "こんにちは|さすがですわ！"
    resp = make_maid_response(user_msg)
    assert resp.count("先手:") == 1
    assert "先手:ユーザー:" not in resp



def test_generate_reply_real_llm():
    bot = MaidBot()
    user_question = "お茶を淹れてください"
    reply = bot.generate_reply(user_question, None)
    print("Maidの返答（LLM実行）:", reply)
    assert reply  # 空でなければOK

def test_generate_reply_with_prev_bot_reply_real_llm():
    bot = MaidBot()
    user_question = "部屋を掃除してください"
    prev_bot_reply = "お願いします"
    reply = bot.generate_reply(user_question, prev_bot_reply)
    print("Maidの返答（先手あり・LLM実行）:", reply)
    assert reply  # 空でなければOK
    # pytestでこのテストだけ実行するには:
    # pytest tests/test_Maid.py -k "generate_reply"