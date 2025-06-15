# threebodychat/Orchestrator.py

import discord
import config
import random

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Orchestrator Ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # テスト用：自分の名前に反応しない・他botのメッセージにも反応しない
    if message.author.bot:
        return

    # ランダムにMaidかMasterを選ぶ
    responder = random.choice(["Maid", "Master"])

    if responder == "Maid":
        responses = [
            "ふふ、ご主人様、それは素敵な問いですわね✨",
            "おや、これは…興味深いですわ。私、お手伝いしてよろしいかしら？",
        ]
    else:
        responses = [
            "それは論理的に説明できるはずだ。",
            "君の問いには一考の価値がある。少し待ってくれ。",
        ]

    reply = random.choice(responses)
    await message.channel.send(f"**[{responder}]** {reply}")

# Bot起動
client.run(config.DISCORD_TOKEN_ORCHESTRATOR)
