import discord
import config
import random

# DiscordのBotがどのイベントを受け取るかを設定するオブジェクト
intents = discord.Intents.default()
# メッセージ関連のイベント（on_messageなど）を受け取るためにTrueにする
intents.messages = True

# intentsを指定してClientを作成
client = discord.Client(intents=intents)

# ランダム返答リスト（例）
REPLIES = [
    "さすがですね！",
    "知らなかったです！",
    "すごいですね！",
    "センスが違いますね！",
    "そうなんですか？"
]

@client.event
# Bot起動時に呼び出される関数
async def on_ready():
    print("Ready!")
    
@client.event
async def on_message(message):
    # Bot自身のメッセージには反応しない
    if message.author == client.user:
        return

    # メンションされたとき
    if client.user in message.mentions:
        await message.channel.send(random.choice(REPLIES))
        return

    # メンションされていなくても返答
    await message.channel.send(random.choice(REPLIES))

# Botを起動
client.run(config.DISCORD_TOKEN_MASTER)
