# # utils/browser_use.py
# import asyncio
# from dotenv import load_dotenv
# load_dotenv()
# from browser_use import Agent
# from browser_use.llm import ChatOpenAI

# async def main():
#     agent = Agent(
#         task="gpt-4o/deepseekv3などのLLMの仕様を比較して",
#         llm=ChatOpenAI(model="o4-mini", temperature=1.0),
#     )
#     await agent.run()

# asyncio.run(main())

# from langchain_openai import ChatOpenAI
# from browser_use import Agent
# import asyncio

# async def main():
#     agent = Agent(
#         task="Find a one-way flight from Bali to Oman on 12 January 2025 on Google Flights. Return me the cheapest option.",
#         llm=ChatOpenAI(model="gpt-4o"),
#     )
#     result = await agent.run()
#     print(result)

# asyncio.run(main())

from browser_use.llm import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4.1")

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
        headless=False,  
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
