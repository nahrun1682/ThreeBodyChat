import discord
import config
import random
import time
import os
import asyncio

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Master Ready!")

# --- ここがキュー監視の常駐タスク ---
async def background_task():
    await client.wait_until_ready()  # Discordログイン完了まで待機
    while not client.is_closed():
        # 毎回「master_queue.txt」が存在するかチェック
        if os.path.exists("master_queue.txt"):
            # ファイルを全読み込み
            with open("master_queue.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
            # キューをクリア（空ファイルにする）
            open("master_queue.txt", "w").close()
            # すべての指示を処理
            for line in lines:
                channel_id, user_id, user_msg = line.strip().split("|")
                channel = client.get_channel(int(channel_id))
                if channel:
                    response = random.choice(["鹿だな", "やっぱ鹿だな"])
                    await channel.send(response)
        # --- ここが「監視間隔」 ----
        await asyncio.sleep(config.MONITOR_INTERVAL)  # 監視間隔で待機

# discord.py v2.x以降の推奨: setup_hookでタスク登録
class MasterClient(discord.Client):
    async def setup_hook(self):
        self.bg_task = self.loop.create_task(background_task())

client = MasterClient(intents=discord.Intents.all())
client.run(config.DISCORD_TOKEN_MASTER)
