import discord
import config
import os
import asyncio
import redis
import logging
from threebodychat.BaseBot import BaseBot
from langchain_openai import AzureChatOpenAI
from prompts.prompt_master import get_master_systemPrompt

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

master_llm = AzureChatOpenAI(
    openai_api_version=config.GPT_41MINI_CHAT_VERSION,
    azure_deployment=config.GPT_41MINI_CHAT_MODEL,
    azure_endpoint=config.GPT_41MINI_CHAT_ENDPOINT,
    openai_api_key=config.GPT_41MINI_CHAT_KEY,
    temperature=0.7,
    max_tokens=2000,
)

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
        
    def generate_reply(self, user_question, prev_bot_reply):
        # マスターらしいプロンプトを組み立て
        system_prompt = get_master_systemPrompt()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": f"ユーザーの質問:「{user_question}」"}
        ]
        if prev_bot_reply:
            messages.append({"role": "user", "content": f"先手Bot(Maid)の返答:「{prev_bot_reply}」"})
        result = master_llm.invoke(messages)

        return result.content.strip()

client = MasterBot()

@client.event
async def on_ready():
    logging.info("Master Ready!")

async def master_setup_hook():
    client.bg_task = asyncio.create_task(client.background_task())

client.setup_hook = master_setup_hook
client.run(config.DISCORD_TOKEN_MASTER)
