import discord
import config
import os
import asyncio
import redis
import logging
from threebodychat.BaseBot import BaseBot

# ログディレクトリ作成
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Maid] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/threebodychat.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class MaidBot(BaseBot):
    def __init__(self):
        super().__init__(
            bot_name="Maid",
            queue_name="maid_queue",
            reply_key_prefix="reply_maid_",
            reply_choices=["さすがですわ！", "お手伝いしましょうか？"],
            redis_conn=r,
            config=config,
            intents=discord.Intents.all()
        )

client = MaidBot()

@client.event
async def on_ready():
    logging.info("Maid Ready!")

async def maid_setup_hook():
    client.bg_task = asyncio.create_task(client.background_task())

client.setup_hook = maid_setup_hook
client.run(config.DISCORD_TOKEN_MAID)
