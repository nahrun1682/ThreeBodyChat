# utils/llm_factory.py

from langchain_openai import AzureChatOpenAI
import config

def create_azure_llm(
    model_name: str,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    **extra_kwargs
) -> AzureChatOpenAI:
    params = {
        "api_version": config.GPT_VERSION,
        "azure_deployment": model_name,
        "model": model_name,
        "azure_endpoint": config.GPT_ENDPOINT,
        "openai_api_key": config.GPT_API_KEY,
        # 以下は一旦入れておく
        "temperature": temperature,
        **extra_kwargs,
    }

    # o4- 系モデルでは temperature と max_tokens を渡さない
    if model_name.startswith("o4"):
        params.pop("temperature", None)
        params.pop("max_tokens", None)
    else:
        params["max_tokens"] = max_tokens

    return AzureChatOpenAI(**params)

