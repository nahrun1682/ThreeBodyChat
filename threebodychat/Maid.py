import discord
import config
import os
import asyncio
import logging
from threebodychat.BaseBot import BaseBot 
from prompts.prompt_maid import get_maid_systemPrompt
from langchain_core.messages import SystemMessage, HumanMessage
from utils.langfuse_client import handler as langfuse_handler
from utils.llm_factory import create_azure_llm 
from utils.memory_factory import create_redis_memory  # ← CHANGE: メモリー生成ファクトリをインポート

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

maid_model = 'gpt-4.1'  # Maid用のモデル名

class MaidBot(BaseBot):
    def __init__(self):
        super().__init__(
            bot_name="Maid",
            queue_name="maid_queue",
            reply_key_prefix="reply_maid_",
            reply_choices=["さすがですわ！", "お手伝いしましょうか？"],
            config=config,
            intents=discord.Intents.all()
        )
        # ← CHANGE: LLM クライアントをインスタンス変数化
        self.llm = create_azure_llm(model_name=maid_model)

    # ← CHANGE: generate_reply のシグネチャを拡張
    def generate_reply(self, user_question, prev_bot_reply, history_msgs, memory):
        """
        history_msgs: 過去の Message オブジェクトリスト
        memory: ConversationBufferMemory インスタンス
        """
        # 過去履歴を先頭に追加
        logging.info(f"[Maid] Loading history ({len(history_msgs)} messages)")
        messages = history_msgs + [
            SystemMessage(content=get_maid_systemPrompt()),
            HumanMessage(content=f"ユーザーの質問:「{user_question}」")
        ]
        if prev_bot_reply:
            messages.append(HumanMessage(content=f"先手Bot(Master)の返答:「{prev_bot_reply}」"))

        for i, msg in enumerate(history_msgs):
            logging.debug(f"[Maid] history[{i}] ({msg.type}): {msg.content}")
        
        # ← CHANGE: LLM 呼び出し
        result = self.llm.invoke(
            messages,
            config={
                "callbacks": [langfuse_handler],  # ← langfuse_handler を適切にインポート済みと仮定
                "metadata": {"langfuse_tags": ["Maid"]}
            }
        )
        reply = result.content.strip()

        # ← CHANGE: メモリーに保存
        logging.info(f"[Maid] Saving to memory: input={'<prev>' if prev_bot_reply else user_question}, output={reply}")
        memory.save_context(
            {"input": user_question if prev_bot_reply is None else prev_bot_reply},
            {"output": reply}
        )
        new_history = memory.load_memory_variables({})["chat_history"]
        logging.info(f"[Maid] New history count: {len(new_history)}")

        return reply

client = MaidBot()

@client.event
async def on_ready():
    logging.info("Maid Ready!")

async def maid_setup_hook():
    client.bg_task = asyncio.create_task(client.background_task())

client.setup_hook = maid_setup_hook
client.run(config.DISCORD_TOKEN_MAID)


if __name__ == "__main__":
    # ── テスト用コードを追加 ──
    from utils.memory_factory import create_redis_memory

    # テスト用セッションと Redis URL／prefix をセット
    test_session = "Maid:test_session"
    redis_url   = client.redis_url      # ← BaseBot で組み立てられた URL
    key_prefix  = client.memory_namespace

    # メモリー初期化
    memory = create_redis_memory(
        redis_url=redis_url,
        key_prefix=key_prefix,
        session_id=test_session
    )

    # ← CHANGE: テスト用の初期履歴を事前に保存
    memory.save_context({"input": "おはようございます"}, {"output": "おはようございます、ご主人様"})
    memory.save_context({"input": "本日のご予定は？"}, {"output": "今日はコードレビューがございますわ"})

    # 初期履歴確認
    print("初期履歴:", memory.load_memory_variables({})["chat_history"])

    # テスト generate_reply 実行
    reply = client.generate_reply(
        "お茶を淹れてください",
        None,
        memory.load_memory_variables({})["chat_history"],
        memory
    )
    print("Maidの返答:", reply)

    # 保存後履歴確認
    print("保存後履歴:", memory.load_memory_variables({})["chat_history"])

