import discord
import config
import os
import asyncio
import logging
from threebodychat.BaseBot import BaseBot
from prompts.prompt_master import get_master_systemPrompt
from utils.llm_factory import create_azure_llm  # ← CHANGE: LLMファクトリをインポート
from utils.memory_factory import create_redis_memory  # ← CHANGE: メモリー生成ファクトリをインポート
from utils.langfuse_client import handler as langfuse_handler

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

master_model = 'gpt-4.1'  # Master用のモデル名

class MasterBot(BaseBot):
    def __init__(self):
        super().__init__(
            bot_name="Master",
            queue_name="master_queue",
            reply_key_prefix="reply_master_",
            reply_choices=["鹿だな", "やっぱ鹿だな"],
            config=config,
            intents=discord.Intents.all()
        )
        # ← CHANGE: LLM クライアントをインスタンス変数化
        self.llm = create_azure_llm(model_name=master_model)

    # ← CHANGE: generate_reply のシグネチャを拡張
    def generate_reply(self, user_question, prev_bot_reply, history_msgs, memory):
        """
        history_msgs: 過去の Message オブジェクトリスト
        memory: ConversationBufferMemory インスタンス
        """
        # ← CHANGE: 過去履歴を先頭に追加
        logging.info(f"[Master] Loading history ({len(history_msgs)} messages)")
        messages = history_msgs + [
            {"role": "system", "content": get_master_systemPrompt()},
            {"role": "user",   "content": f"ユーザーの質問:「{user_question}」"}
        ]
        if prev_bot_reply:
            messages.append({"role": "user", "content": f"先手Bot(Maid)の返答:「{prev_bot_reply}」"})
        # ← optionally log history contents at DEBUG
        for i, msg in enumerate(history_msgs):
            logging.debug(f"[Master] history[{i}]: {msg.content}")

        # ← CHANGE: LLM 呼び出し
        result = self.llm.invoke(
            messages,
            config={
                "callbacks": [langfuse_handler],
                "metadata": {"langfuse_tags": ["Master"]}
            }
        )
        reply = result.content.strip()
        logging.info(f"[Master] Generated reply: {reply}")

        # ← CHANGE: メモリーに保存
        logging.info(f"[Master] Saving to memory: input={'<prev>' if prev_bot_reply else user_question}, output={reply}")
        memory.save_context(
            {"input": user_question if prev_bot_reply is None else prev_bot_reply},
            {"output": reply}
        )
        new_history = memory.load_memory_variables({})["chat_history"]
        logging.info(f"[Master] New history count: {len(new_history)}")

        return reply

client = MasterBot()

@client.event
async def on_ready():
    logging.info("Master Ready!")

async def master_setup_hook():
    client.bg_task = asyncio.create_task(client.background_task())

client.setup_hook = master_setup_hook
client.run(config.DISCORD_TOKEN_MASTER)
