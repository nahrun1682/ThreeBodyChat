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
