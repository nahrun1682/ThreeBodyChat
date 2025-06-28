import redis  # Redisサーバーに接続するためのライブラリ
import random  # ランダムな返答を選ぶための標準ライブラリ
import logging  # ロギング用ライブラリ

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

def make_maid_response(user_msg, channel):
    """
    Maid.pyのロジックを模したテスト用関数。
    user_msg: str, 例 "こんにちは" または "こんにちは|さすがですわ！"
    """
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    parts = user_msg.split("|", 1)
    user_question = parts[0]
    prev_bot_reply = parts[1] if len(parts) > 1 else None
    if prev_bot_reply:
        # 後手の場合
        maid_reply = random.choice(['さすがですわ！', 'お手伝いしましょうか？'])
        response = f"ユーザー:{user_question} / 先手:{prev_bot_reply} / {maid_reply}"
        channel.send(response)
        # Orchestrator用には「maid_reply」だけを保存
        r.set(f"reply_maid_{channel.id}", maid_reply)
        logging.info(f"返答を送信・保存: ユーザー:{user_question} / 先手:{prev_bot_reply} / {maid_reply}")
    else:
        # 先手の場合
        maid_reply = random.choice(['さすがですわ！', 'お手伝いしましょうか？'])
        response = f"ユーザー:{user_question} / {maid_reply}"
        channel.send(response)
        # Orchestrator用には「maid_reply」だけを保存
        r.set(f"reply_maid_{channel.id}", maid_reply)
        logging.info(f"返答を送信・保存: ユーザー:{user_question} / {maid_reply}")

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
