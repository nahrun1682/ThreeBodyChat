# utils/tools.py

import os
from dotenv import load_dotenv
# プロジェクトルートの .env を読み込む
load_dotenv()
from os import getenv
from langchain_core.tools import Tool
from langchain_google_community import GoogleSearchAPIWrapper

# ── Google 検索ツール
google_search = GoogleSearchAPIWrapper(
    google_cse_id=os.getenv("GOOGLE_CSE_ID"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)
def top5_results(query):
    return google_search.results(query, 5)

google_tool = Tool(
    name="google_search",
    description="""
    自分の現状の知識では答えられないような質問に対して、
    Google 検索を使って情報を取得します。
    使用したクエリに対する上位5件のSnippet/Title/Linkを取得できます
    使用した場合は回答に必ず引用文献が分かるようにしてください""",
    func=top5_results,
)

if __name__ == "__main__":
    # 動作確認用: Google検索ツールのテスト
    from dotenv import load_dotenv
    load_dotenv()  # .env の読み込み

    sample_query = "langchain とは"
    print(f"▶ Testing google_tool with query: {sample_query}")
    try:
        results = top5_results(sample_query)
        print("▶ Retrieved top 5 results:")
        for idx, item in enumerate(results, 1):
            print(f"{idx}. {item}")
    except Exception as e:
        print(f"Error during google_tool test: {e}")
