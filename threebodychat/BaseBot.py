#threebodychat/BaseBot.py
import discord
import asyncio
import logging
import redis                                              # ← CHANGE: Redis を直接インポート
from utils.memory_factory import create_redis_memory
from threebodychat import config

class BaseBot(discord.Client):
    """
    Maid/Masterなど複数Botで共通利用する基底クラス。
    Redisキュー監視・返答生成・Discord送信・reply保存・メモリー管理まで一括で実装。
    サブクラスでbot_nameや返答パターン(reply_choices)を指定するだけでOK。
    """
    def __init__(self, bot_name, queue_name, reply_key_prefix, reply_choices, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_name = bot_name  # Botの名前（ログや識別用）

        # ← CHANGE: redis_conn 引数を廃止し、自前で接続を初期化
        self.r = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            password=config.REDIS_PASSWORD or None,
            decode_responses=True,
        )

        # ← CHANGE: メモリー用 Redis URL を組み立て
        if config.REDIS_PASSWORD:
            self.redis_url = f"redis://:{config.REDIS_PASSWORD}@{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}"
        else:
            self.redis_url = f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}"

        # ← CHANGE: メモリー用 key_prefix（namespace 代替）を設定
        self.memory_namespace = f"threebodychat_{bot_name.lower()}:"

        self.queue_name = queue_name  # Redisで監視するキュー名
        self.reply_key_prefix = reply_key_prefix  # Redisに返答を保存する際のキー接頭辞
        self.reply_choices = reply_choices  # 返答候補リスト（ランダム選択用）
        self.config = config  # 設定オブジェクト（MONITOR_INTERVAL等）

    async def background_task(self):
        """
        Redisキューを監視し、メッセージが来たら
        → メモリー読み込み → 返答生成 → メモリー保存 → Discord送信 → reply保存まで実装。
        """
        await self.wait_until_ready()
        while not self.is_closed():
            item = self.r.lpop(self.queue_name)
            if not item:
                await asyncio.sleep(self.config.MONITOR_INTERVAL)
                continue

            logging.info(f"{self.queue_name} lpop: {item}")
            try:
                channel_id, user_id, raw = item.split("|", 2)
                parts = raw.split("|", 2)
                request_id = parts[0]
                user_question = parts[1]
                prev_bot_reply = parts[2] if len(parts) == 3 else None

                # ← CHANGE: セッション単位のメモリーを生成
                # session_id = f"{self.bot_name}:{request_id}"
                session_id = "1383696743723434125" #discordチャンネルid
                memory = create_redis_memory(
                    redis_url=self.redis_url,
                    key_prefix=self.memory_namespace,
                    session_id=session_id
                )

                # ← CHANGE: 過去履歴を取得
                history_msgs = memory.load_memory_variables({})["chat_history"]

                # ← CHANGE: generate_reply の呼び出しを拡張
                reply = self.generate_reply(
                    user_question,
                    prev_bot_reply,
                    history_msgs,
                    memory
                )

                # Discord 送信 & Orchestrator 用保存
                await self._send_and_store(channel_id, request_id, reply)

            except Exception as e:
                logging.error(f"{self.queue_name}の処理中にエラー: {e}")
            await asyncio.sleep(self.config.MONITOR_INTERVAL)

    # async def _send_and_store(self, channel_id, request_id, reply):
    #     channel = self.get_channel(int(channel_id))
    #     if channel:
    #         MAX_DISCORD_MSG_LEN = 2000
    #         to_send = reply if len(reply) <= MAX_DISCORD_MSG_LEN else reply[:MAX_DISCORD_MSG_LEN]
    #         await channel.send(to_send)
    #         self.r.set(f"{self.reply_key_prefix}{request_id}", reply)
    #         logging.info(f"Orchestrator用に保存: {self.reply_key_prefix}{request_id}={reply}")
    async def _send_and_store(self, channel_id, request_id, reply):
        channel = self.get_channel(int(channel_id))
        if not channel:
            logging.error(f"[{self.bot_name}] Channel {channel_id} not found")
            return

        # ── 送信前ログ
        logging.info(f"[{self.bot_name}] Sending to Discord channel {channel_id}: {reply[:100]}…")
        MAX_DISCORD_MSG_LEN = 2000
        to_send = reply if len(reply) <= MAX_DISCORD_MSG_LEN else reply[:MAX_DISCORD_MSG_LEN]
        try:
            await channel.send(to_send)
            logging.info(f"[{self.bot_name}] Discord send succeeded")
        except Exception as e:
            logging.error(f"[{self.bot_name}] Discord send failed: {e}")
            return

        # Redis への保存
        key = f"{self.reply_key_prefix}{request_id}"
        try:
            self.r.set(key, reply)
            logging.info(f"[{self.bot_name}] Redis key set: {key}")
        except Exception as e:
            logging.error(f"[{self.bot_name}] Redis set failed for {key}: {e}")


    # ← CHANGE: 引数を増やして履歴＋メモリを受け取るように
    def generate_reply(self, user_question, prev_bot_reply, history_msgs, memory):
        """
        返答生成メソッド。サブクラスでオーバーライド必須。
        history_msgs: 過去のMessageオブジェクトのリスト
        memory: ConversationBufferMemory インスタンス
        """
        raise NotImplementedError

if __name__ == "__main__":
    import config
    import os
    import asyncio
    import discord

    # ── テスト用のサブクラス定義 ──
    class TestBot(BaseBot):
        def __init__(self):
            # bot_name, queue_name, reply_key_prefix, reply_choices, config
            super().__init__(
                bot_name="Test",
                queue_name="test_queue",
                reply_key_prefix="reply_test_",
                reply_choices=["dummy_reply"],
                config=config,
                intents=discord.Intents.all()  # テストではイベントは使わないので Intents.none() でOK
            )
        def generate_reply(self, user_question, prev_bot_reply, history_msgs, memory):
            # テスト時は履歴と input を出力してから固定応答を返す
            print("▶ history_msgs:", history_msgs)
            print("▶ user_question:", user_question)
            # メモリー保存も動くか確認
            memory.save_context({"input": user_question}, {"output": "dummy_reply"})
            return "dummy_reply"

    # 環境変数などに依存せずredisを動かすための一時設定
    os.environ.setdefault("REDIS_HOST", config.REDIS_HOST)
    os.environ.setdefault("REDIS_PORT", str(config.REDIS_PORT))
    os.environ.setdefault("REDIS_DB", str(config.REDIS_DB))

    # Bot のインスタンス作成
    bot = TestBot()

    # テスト用にキューへメッセージを投入
    # フォーマット: channel_id|user_id|request_id|user_question
    bot.r.rpush("test_queue", "0|tester|req1|こんにちは、テストです")

    async def run_test_once():
        # queue から1つ取り出して background_task 相当の処理を走らせる
        # ※本来は background_task をループ起動しますが、ここでは一回だけ手動で呼び出します
        item = bot.r.lpop(bot.queue_name)
        if not item:
            print("キューにメッセージがありません")
            return

        # channel_id|user_id|raw の分解
        channel_id, user_id, raw = item.split("|", 2)
        parts = raw.split("|", 2)
        request_id = parts[0]
        user_question = parts[1]
        prev_bot_reply = parts[2] if len(parts) == 3 else None

        # メモリー生成
        session_id = f"{bot.bot_name}:{request_id}"
        memory = create_redis_memory(
            redis_url=bot.redis_url,
            key_prefix=bot.memory_namespace,
            session_id=session_id
        )
        # 過去履歴取得
        history_msgs = memory.load_memory_variables({})["chat_history"]

        # 返答生成
        reply = bot.generate_reply(user_question, prev_bot_reply, history_msgs, memory)

        # Discord 送信相当と reply 保存（今回はコンソールに出力）
        print("▶ generated reply:", reply)
        bot.r.set(f"{bot.reply_key_prefix}{request_id}", reply)

        # 保存された履歴も確認
        new_history = memory.load_memory_variables({})["chat_history"]
        print("▶ new history after save_context:", new_history)

    # 実行
    asyncio.run(run_test_once())
