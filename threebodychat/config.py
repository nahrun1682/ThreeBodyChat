from dotenv import load_dotenv
load_dotenv()

import os

DISCORD_TOKEN_MAID = os.getenv('DISCORD_TOKEN_MAID')
DISCORD_TOKEN_MASTER = os.getenv('DISCORD_TOKEN_MASTER')
DISCORD_TOKEN_ORCHESTRATOR = os.getenv('DISCORD_TOKEN_ORCHESTRATOR')

# LLM (Azure OpenAI) 設定
GPT_41MINI_CHAT_KEY = os.getenv('GPT_41MINI_CHAT_KEY')
GPT_41MINI_CHAT_ENDPOINT = os.getenv('GPT_41MINI_CHAT_ENDPOINT')
GPT_41MINI_CHAT_MODEL = os.getenv('GPT_41MINI_CHAT_MODEL')
GPT_41MINI_CHAT_VERSION = os.getenv('GPT_41MINI_CHAT_VERSION')
GPT_API_KEY = os.getenv('GPT_API_KEY')
GPT_ENDPOINT = os.getenv('GPT_ENDPOINT')
GPT_VERSION = os.getenv('GPT_VERSION')
#modelは['gpt-4.1','gpt-4.1-mini','o4-mini']から選択

#OpenAI設定
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#監視感覚
MONITOR_INTERVAL = 0.5

# Langfuse設定
LANGFUSE_SECRET_KEY = os.getenv('LANGFUSE_SECRET_KEY')
LANGFUSE_PUBLIC_KEY = os.getenv('LANGFUSE_PUBLIC_KEY')
LANGFUSE_HOST_URL = os.getenv('LANGFUSE_HOST_URL')

# Redis 接続情報
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
# 制御用 Redis データベース (Orchestrator⇔Bot のキュー／返信管理)
REDIS_CTRL_DB   = 0
# メモリ用 Redis データベース (LLM 履歴保存用)
REDIS_MEMORY_DB = 1
REDIS_PASSWORD = ""