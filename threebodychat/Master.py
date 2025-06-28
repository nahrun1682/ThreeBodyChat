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
    format="%(asctime)s [Master] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/threebodychat.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class MasterBot(BaseBot):
    def __init__(self):
        super().__init__(
            bot_name="Master",
            queue_name="master_queue",
            reply_key_prefix="reply_master_",
            reply_choices=["鹿だな", "やっぱ鹿だな"],
            redis_conn=r,
            config=config,
            intents=discord.Intents.all()
        )

client = MasterBot()

@client.event
async def on_ready():
    logging.info("Master Ready!")

async def master_setup_hook():
    client.bg_task = asyncio.create_task(client.background_task())

client.setup_hook = master_setup_hook
client.run(config.DISCORD_TOKEN_MASTER)
