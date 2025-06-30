# Orchestrator用 LLMプロンプトテンプレート
# ユーザー発言から「Maid」か「Master」どちらが返答すべきかを判定するためのプロンプトを返す関数

def get_orchestrator_prompt(user_input: str, format_instructions: str = None) -> str:
    """
    OrchestratorがLLMに投げるプロンプトを生成
    :param user_input: ユーザーの発言
    :param format_instructions: JSON構造化指示（必要に応じて）
    :return: プロンプト文字列
    """
    base = (
        "あなたは会話の司令役です。以下のユーザー発言に対して、"
        "'Maid' または 'Master' のいずれかを responder として選んでください。\n"
    )
    if format_instructions:
        base += f"出力は必ず JSON 形式で、次の構造に従ってください:\n{format_instructions}\n"
    base += f"ユーザー発言: {user_input}"
    return base
