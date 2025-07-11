import discord
import config
import os
import asyncio
import redis
import logging
from threebodychat.BaseBot import BaseBot
from langchain_openai import AzureChatOpenAI
from prompts.prompt_maid import get_maid_systemPrompt
from langchain_core.messages import SystemMessage, HumanMessage
from utils.langfuse_client import handler as langfuse_handler

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

maid_llm = AzureChatOpenAI(
    openai_api_version=config.GPT_41MINI_CHAT_VERSION,
    azure_deployment=config.GPT_41MINI_CHAT_MODEL,
    azure_endpoint=config.GPT_41MINI_CHAT_ENDPOINT,
    openai_api_key=config.GPT_41MINI_CHAT_KEY,
    temperature=0.7,
    max_tokens=2000,
)

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
    def generate_reply(self, user_question, prev_bot_reply):
        # メイドらしいプロンプトを組み立て
        system_prompt = get_maid_systemPrompt()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"ユーザーの質問:「{user_question}」")
        ]
        
        if prev_bot_reply:
            messages.append(HumanMessage(content=f"先手Bot(Master)の返答:「{prev_bot_reply}」"))
        
        result = maid_llm.invoke(
            messages,
            config={
                "callbacks": [langfuse_handler],
                # 必要であればタグも metadata 内に渡せます
                "metadata": {"langfuse_tags": ["Maid"]}
            })

        return result.content.strip()

client = MaidBot()

@client.event
async def on_ready():
    logging.info("Maid Ready!")

async def maid_setup_hook():
    client.bg_task = asyncio.create_task(client.background_task())

client.setup_hook = maid_setup_hook
client.run(config.DISCORD_TOKEN_MAID)

if __name__ == "__main__":
    # MaidBotのインスタンスを作成してテスト質問からgenerate_replyを実行
    client = MaidBot()
    user_question = "お茶を淹れてください"
    reply = client.generate_reply(user_question, "Masterの返答例：お茶は私は入れるの苦手なんだ")
    print("Maidの返答:", reply)
