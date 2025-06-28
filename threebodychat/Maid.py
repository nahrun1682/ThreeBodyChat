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
# ログ設定（共通ファイル、Maid識別子付き）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Maid] %(levelname)s %(message)s",
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
    logging.info("Maid Ready!")

# --- Redisキュー監視の常駐タスク ---
async def background_task():
    await client.wait_until_ready()  # Discordログイン完了まで待機
    while not client.is_closed():
        # Redisのmaid_queueから1件取り出し（なければNone）
        item = r.lpop("maid_queue")
        if item is None:
            await asyncio.sleep(config.MONITOR_INTERVAL)  # 監視間隔で待機
            continue
        logging.info(f"maid_queue lpop: {item}")
        try:
            channel_id, user_id, user_msg = item.strip().split("|", 2)
            logging.info(f"maid_queue item split: channel_id={channel_id}, user_id={user_id}, user_msg={user_msg}")
            channel = client.get_channel(int(channel_id))
            if channel:
                parts = user_msg.split("|", 1)
                user_question = parts[0]
                prev_bot_reply = parts[1] if len(parts) > 1 else None
                logging.info(f"maid_queue message parts: user_question={user_question}, prev_bot_reply={prev_bot_reply}")

                if prev_bot_reply:
                    # 後手の場合：ユーザー:質問 / 先手:先手の生返答 / ランダム返答
                    maid_reply = random.choice(['さすがですわ！', 'お手伝いしましょうか？'])
                    response = f"ユーザー:{user_question} / 先手:{prev_bot_reply} / {maid_reply}"
                    logging.info(f"maid reply (後手): {response}")
                    await channel.send(response)
                    # Orchestrator用には「maid_reply」（生返答）のみを保存
                    r.set(f"reply_maid_{channel.id}", maid_reply)
                    logging.info(f"Orchestrator用に保存: reply_maid_{channel.id}={maid_reply}")
                else:
                    # 先手の場合：ユーザー:質問 / ランダム返答
                    maid_reply = random.choice(['さすがですわ！', 'お手伝いしましょうか？'])
                    response = f"ユーザー:{user_question} / {maid_reply}"
                    logging.info(f"maid reply (先手): {response}")
                    await channel.send(response)
                    # Orchestrator用には「maid_reply」（生返答）のみを保存
                    r.set(f"reply_maid_{channel.id}", maid_reply)
                    logging.info(f"Orchestrator用に保存: reply_maid_{channel.id}={maid_reply}")
        except Exception as e:
            logging.error(f"maid_queueの処理中にエラー: {e}")
        await asyncio.sleep(config.MONITOR_INTERVAL)  # 監視間隔で待機

# discord.py v2.x以降の推奨: setup_hookでタスク登録
class MaidClient(discord.Client):
    async def setup_hook(self):
        self.bg_task = self.loop.create_task(background_task())
        
client = MaidClient(intents=discord.Intents.all())
client.run(config.DISCORD_TOKEN_MAID)
