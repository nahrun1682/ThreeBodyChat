# threebodychat/langfuse_client.py
import os
from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler
from threebodychat import config


# ① Langfuse クライアント初期化（プロジェクトキーを一度だけ設定）
Langfuse(
    public_key=config.LANGFUSE_PUBLIC_KEY,
    secret_key=config.LANGFUSE_SECRET_KEY,
    host=config.LANGFUSE_HOST_URL,
)

# ② 同一インスタンスを取得
langfuse = get_client()  # 初回で環境変数または上記設定から認証:contentReference[oaicite:0]{index=0}

# ③ LangChain 用ハンドラー生成
handler = CallbackHandler()  # 引数不要ですわ:contentReference[oaicite:1]{index=1}


if __name__ == "__main__":
    # ✅ テスト認証チェック＆フラッシュ確認用スクリプト
    from langchain_core.messages import SystemMessage, HumanMessage
    from langchain_openai import AzureChatOpenAI
    print("▶️ Langfuse auth_check():", langfuse.auth_check())
    
    

    llm = AzureChatOpenAI(
        openai_api_version=config.GPT_41MINI_CHAT_VERSION,
        azure_deployment=config.GPT_41MINI_CHAT_MODEL,
        azure_endpoint=config.GPT_41MINI_CHAT_ENDPOINT,
        openai_api_key=config.GPT_41MINI_CHAT_KEY,
        temperature=0.7,
        max_tokens=2000,
    )
    test = llm.invoke(
        [
            SystemMessage(content="Say hi."),
            HumanMessage(content="Hello!")
        ],
        config={
            "callbacks":[handler],
            "metadata": {
                "langfuse_tags": ["self-test"],
                "langfuse_session_id": "self-test-session"
            }
        }
    )
    print("LLM Response:", test.content)
    
    # ✅ ログ送信のため flush を明示的実行
    langfuse.flush()
    print("✨ Flushed logs")
