import pytest
from threebodychat.BaseBot import BaseBot
import discord
from unittest.mock import AsyncMock

pytestmark = pytest.mark.asyncio

# --- シンプルな共通テスト用ダミー ---
class DummyConfig:
    MONITOR_INTERVAL = 0.01

class DummyChannel:
    def __init__(self):
        self.sent_messages = []
    async def send(self, msg):
        self.sent_messages.append(msg)

class DummyRedis:
    def __init__(self):
        self.data = {}
        self.queue = []
    def lpop(self, queue_name):
        return self.queue.pop(0) if self.queue else None
    def rpush(self, queue_name, item):
        self.queue.append(item)
    def set(self, key, value):
        self.data[key] = value
    def get(self, key):
        return self.data.get(key)

# --- 共通動作: 正常系 ---
@pytest.mark.asyncio
async def test_basebot_basic(monkeypatch):
    """
    1件のメッセージを処理し、Discord送信・Redis保存が行われること
    """
    class DummyBot(BaseBot):
        def generate_reply(self, user_question, prev_bot_reply):
            return "テスト返答"
    redis = DummyRedis()
    config = DummyConfig()
    bot = DummyBot(
        bot_name="TestBot",
        queue_name="test_queue",
        reply_key_prefix="reply_test_",
        reply_choices=["A", "B"],
        redis_conn=redis,
        config=config,
        intents=discord.Intents.none()
    )
    dummy_channel = DummyChannel()
    # get_channelは常にdummy_channelを返す
    monkeypatch.setattr(bot, "get_channel", lambda cid: dummy_channel)
    # Discord初期化をスキップ
    monkeypatch.setattr(bot, "wait_until_ready", AsyncMock())
    # 1回だけループさせるためis_closedをモック
    monkeypatch.setattr(bot, "is_closed", lambda: True)
    # テスト用メッセージ投入
    redis.rpush("test_queue", "123|456|reqid|こんにちは| ")
    await bot.background_task()
    # Discord送信内容・Redis保存内容を検証
    assert dummy_channel.sent_messages[0].startswith("ユーザー:こんにちは / テスト返答")
    assert redis.get("reply_test_reqid") == "テスト返答"

# --- 長文カット ---
@pytest.mark.asyncio
async def test_basebot_long_message_cut(monkeypatch):
    """
    2000文字超の返答はカットされること
    """
    class DummyBot(BaseBot):
        def generate_reply(self, user_question, prev_bot_reply):
            return "あ" * 3000
    redis = DummyRedis()
    config = DummyConfig()
    bot = DummyBot(
        bot_name="TestBot",
        queue_name="test_queue",
        reply_key_prefix="reply_test_",
        reply_choices=["A", "B"],
        redis_conn=redis,
        config=config,
        intents=discord.Intents.none()
    )
    dummy_channel = DummyChannel()
    monkeypatch.setattr(bot, "get_channel", lambda cid: dummy_channel)
    monkeypatch.setattr(bot, "wait_until_ready", AsyncMock())
    monkeypatch.setattr(bot, "is_closed", lambda: True)
    redis.rpush("test_queue", "123|456|reqid|こんにちは| ")
    await bot.background_task()
    assert len(dummy_channel.sent_messages[0]) == 2000

# --- パースエラー時はDiscord送信されない ---
@pytest.mark.asyncio
async def test_basebot_message_parse_error(monkeypatch):
    """
    不正なメッセージは無視され、Discord送信されないこと
    """
    class DummyBot(BaseBot):
        def generate_reply(self, user_question, prev_bot_reply):
            return "テスト返答"
    redis = DummyRedis()
    config = DummyConfig()
    bot = DummyBot(
        bot_name="TestBot",
        queue_name="test_queue",
        reply_key_prefix="reply_test_",
        reply_choices=["A", "B"],
        redis_conn=redis,
        config=config,
        intents=discord.Intents.none()
    )
    dummy_channel = DummyChannel()
    monkeypatch.setattr(bot, "get_channel", lambda cid: dummy_channel)
    monkeypatch.setattr(bot, "wait_until_ready", AsyncMock())
    monkeypatch.setattr(bot, "is_closed", lambda: True)
    # パース不能なメッセージ
    redis.rpush("test_queue", "不正なメッセージ")
    await bot.background_task()
    assert not dummy_channel.sent_messages
