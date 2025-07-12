# utils/memory_factory.py

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory

def create_redis_memory(redis_url: str, key_prefix: str, session_id: str, window_size: int = 10) -> ConversationBufferWindowMemory:
    """
    RedisChatMessageHistory を最新のコミュニティ版で利用しつつ、
    直近 k 件だけを保持するウィンドウメモリーを作成しますわ。
    key_prefix = "threebodychat_maid:" など
    session_id  = "1383696743723434125" など
    window_size = 直近何件保持するか
    """
    
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=redis_url,
        key_prefix=key_prefix,  # namespace の代わり
    )
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=history,
        k=window_size  # 直近 k 件だけ保持
    )

if __name__ == "__main__":
    # テスト用
    test_redis_url = "redis://127.0.0.1:6379/0"
    test_prefix    = "test_threebodychat:"
    test_session   = "TestBot:session1"

    memory = create_redis_memory(test_redis_url, test_prefix, test_session)
    initial = memory.load_memory_variables({})["chat_history"]
    print("初期履歴:", initial)

    memory.save_context({"input": "こんにちは"}, {"output": "こんばんは、ご主人様"})
    loaded = memory.load_memory_variables({})["chat_history"]
    print("保存後の履歴:")
    for msg in loaded:
        print(f"- [{msg.type}] {msg.content}")
