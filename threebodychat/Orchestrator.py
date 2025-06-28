import discord
from threebodychat import config
import random
import asyncio
import redis
import logging
import os

# ログディレクトリ作成
os.makedirs("logs", exist_ok=True)
# ログ設定（全Bot共通ファイル、Orch識別子付き）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Orch] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/threebodychat.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Redisに接続
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# ランダムにMaidかMasterを割り振る関数
def assign_responder():
    return random.choice(["Maid", "Master"])

# Redisキューに書き込む関数
def write_to_queue(queue_name, channel_id, user_id, message_content):
    logging.debug(f"r.rpush({queue_name}, {channel_id}|{user_id}|{message_content})")
    r.rpush(queue_name, f"{channel_id}|{user_id}|{message_content}")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# 先手Botの返答を一時保存するための辞書
pending_responses = {}

@client.event
async def on_ready():
    logging.info("Orchestrator Ready!")

@client.event
async def on_message(message):
    # Bot自身や他Botのメッセージには反応しない
    if message.author.bot:
        return

    # ユーザー発言情報
    channel_id = message.channel.id
    user_id = message.author.id
    user_msg = message.content

    # どちらが先手かランダムで決定
    first = assign_responder()
    second = "Master" if first == "Maid" else "Maid"
    logging.info(f"先手: {first}, 後手: {second} → {user_msg}")

    # 先手Botのキューに「ユーザー発言のみ」を送信
    logging.info(f"write_to_queue: {first.lower()}_queue, channel_id={channel_id}, user_id={user_id}, user_msg={user_msg}")
    write_to_queue(f"{first.lower()}_queue", channel_id, user_id, user_msg)

    # 先手Botの返答を待つ（最大10秒）
    logging.info(f"wait_for_bot_reply: channel_id={channel_id}, bot_name={first}, timeout=10")
    reply = await wait_for_bot_reply(channel_id, first, timeout=10)
    logging.info(f"wait_for_bot_reply result: {reply}")
    if reply is not None:
        # 返答が整形済みでないかチェック（デバッグ用）
        if "ユーザー:" in reply or "先手:" in reply:
            logging.warning(f"Orchestrator: 先手Botの返答に整形済みテキストが混入: {reply}")
        # 後手Botのキューに「ユーザー発言｜先手Botの生返答」を送信
        combined_msg = f"{user_msg}|{reply}"
        logging.info(f"write_to_queue: {second.lower()}_queue, channel_id={channel_id}, user_id={user_id}, combined_msg={combined_msg}")
        write_to_queue(f"{second.lower()}_queue", channel_id, user_id, combined_msg)
        logging.info(f"後手{second}に送信: {combined_msg}")
    else:
        logging.warning("先手Botの返答が取得できませんでした")

async def wait_for_bot_reply(channel_id, bot_name, timeout=10):
    """
    先手Botの返答をRedisで待つ（簡易実装）
    """
    key = f"reply_{bot_name.lower()}_{channel_id}"
    logging.info(f"wait_for_bot_reply: polling key={key}, timeout={timeout}")
    for i in range(timeout * 2):  # 0.5秒ごとに最大timeout秒待つ
        reply = r.get(key)
        logging.debug(f"wait_for_bot_reply: poll {i}, key={key}, reply={reply}")
        if reply:
            r.delete(key)
            logging.info(f"wait_for_bot_reply: got reply, deleted key={key}")
            return reply
        await asyncio.sleep(0.5)
    logging.warning(f"wait_for_bot_reply: timeout, key={key}")
    return None

if __name__ == "__main__":
    client.run(config.DISCORD_TOKEN_ORCHESTRATOR)
