import discord
import config
import random
import time
import os
import asyncio
import redis
import logging

# ログディレクトリ作成
os.makedirs("logs", exist_ok=True)
# ログ設定（共通ファイル、Master識別子付き）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Master] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/threebodychat.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Redisに接続
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    logging.info("Master Ready!")

# --- Redisキュー監視の常駐タスク ---
async def background_task():
    await client.wait_until_ready()  # Discordログイン完了まで待機
    empty_count = 0  # 空lpop回数カウンタ
    while not client.is_closed():
        # Redisのmaster_queueから1件取り出し（なければNone）
        item = r.lpop("master_queue")
        if item is None:
            empty_count += 1
            await asyncio.sleep(config.MONITOR_INTERVAL)  # 監視間隔で待機
            continue
        empty_count = 0  # 何か取得できたらリセット
        logging.info(f"master_queue lpop: {item}")
        try:
            channel_id, user_id, user_msg = item.strip().split("|", 2)
            logging.info(f"master_queue item split: channel_id={channel_id}, user_id={user_id}, user_msg={user_msg}")
            channel = client.get_channel(int(channel_id))
            if channel:
                # request_idを取り出す
                msg_parts = user_msg.split("|", 2)
                if len(msg_parts) == 3:
                    # 後手: request_id|user_question|prev_bot_reply
                    request_id, user_question, prev_bot_reply = msg_parts
                elif len(msg_parts) == 2:
                    # 先手: request_id|user_question
                    request_id, user_question = msg_parts
                    prev_bot_reply = None
                else:
                    logging.error(f"master_queue message parse error: {msg_parts}")
                    await asyncio.sleep(config.MONITOR_INTERVAL)
                    continue
                logging.info(f"master_queue message parts: request_id={request_id}, user_question={user_question}, prev_bot_reply={prev_bot_reply}")

                if prev_bot_reply:
                    # 後手の場合：ユーザー:質問 / 先手:先手の生返答 / ランダム返答
                    master_reply = random.choice(['鹿だな', 'やっぱ鹿だな'])
                    response = f"ユーザー:{user_question} / 先手:{prev_bot_reply} / {master_reply}"
                    logging.info(f"master reply (後手): {response}")
                    await channel.send(response)
                    # Orchestrator用には「master_reply」（生返答）のみを保存
                    r.set(f"reply_master_{request_id}", master_reply)
                    logging.info(f"Orchestrator用に保存: reply_master_{request_id}={master_reply}")
                else:
                    # 先手の場合：ユーザー:質問 / ランダム返答
                    master_reply = random.choice(['鹿だな', 'やっぱ鹿だな'])
                    response = f"ユーザー:{user_question} / {master_reply}"
                    logging.info(f"master reply (先手): {response}")
                    await channel.send(response)
                    # Orchestrator用には「master_reply」（生返答）のみを保存
                    r.set(f"reply_master_{request_id}", master_reply)
                    logging.info(f"Orchestrator用に保存: reply_master_{request_id}={master_reply}")
        except Exception as e:
            logging.error(f"master_queueの処理中にエラー: {e}")
        await asyncio.sleep(config.MONITOR_INTERVAL)  # 監視間隔で待機

# discord.py v2.x以降の推奨: setup_hookでタスク登録
class MasterClient(discord.Client):
    async def setup_hook(self):
        self.bg_task = self.loop.create_task(background_task())

client = MasterClient(intents=discord.Intents.all())
client.run(config.DISCORD_TOKEN_MASTER)
