import discord
import config
import random
import os
import time
# OrchestratorはMaidとMasterのどちらが応答するかを決定し、キューに書き込む役割を持つ
import asyncio

# ランダムにMaidかMasterを割り振る関数
def assign_responder():
    return random.choice(["Maid", "Master"])

# キューに書き込む関数
def write_to_queue(responder, channel_id, user_id, message_content):
    filename = "maid_queue.txt" if responder == "Maid" else "master_queue.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{channel_id}|{user_id}|{message_content}\n")
        
        
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Orchestrator Ready!")

@client.event
async def on_message(message):
    # Bot自身や他Botのメッセージには反応しない
    if message.author.bot:
        return

    # ご主人様（ユーザー）の発言を受信
    # （メンション不要、普通の発言すべてに反応）

    # MaidかMasterどちらが返答するかをランダムに決定
    responder = assign_responder()
    print(f"割り振り: {responder} → {message.content}")

    # channel.id, user.id, メッセージ内容を、割り振ったBot用のキューファイルに追記
    write_to_queue(responder, message.channel.id, message.author.id, message.content)

    # Orchestrator自身は何もDiscordに発言せず、ただ舞台裏で采配するだけ

# Orchestrator用のBotトークンで起動
if __name__ == "__main__":
    client.run(config.DISCORD_TOKEN_ORCHESTRATOR)
