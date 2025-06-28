import discord
import asyncio
import logging

class BaseBot(discord.Client):
    def __init__(self, bot_name, queue_name, reply_key_prefix, reply_choices, redis_conn, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_name = bot_name
        self.queue_name = queue_name
        self.reply_key_prefix = reply_key_prefix
        self.reply_choices = reply_choices
        self.r = redis_conn
        self.config = config

    async def background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            item = self.r.lpop(self.queue_name)
            if item is None:
                await asyncio.sleep(self.config.MONITOR_INTERVAL)
                continue
            logging.info(f"{self.queue_name} lpop: {item}")
            try:
                channel_id, user_id, user_msg = item.strip().split("|", 2)
                logging.info(f"{self.queue_name} item split: channel_id={channel_id}, user_id={user_id}, user_msg={user_msg}")
                channel = self.get_channel(int(channel_id))
                if channel:
                    msg_parts = user_msg.split("|", 2)
                    if len(msg_parts) == 3:
                        request_id, user_question, prev_bot_reply = msg_parts
                    elif len(msg_parts) == 2:
                        request_id, user_question = msg_parts
                        prev_bot_reply = None
                    else:
                        logging.error(f"{self.queue_name} message parse error: {msg_parts}")
                        await asyncio.sleep(self.config.MONITOR_INTERVAL)
                        continue
                    logging.info(f"{self.queue_name} message parts: request_id={request_id}, user_question={user_question}, prev_bot_reply={prev_bot_reply}")

                    reply = self.generate_reply(user_question, prev_bot_reply)
                    if prev_bot_reply:
                        response = f"ユーザー:{user_question} / 先手:{prev_bot_reply} / {reply}"
                        logging.info(f"{self.bot_name} reply (後手): {response}")
                    else:
                        response = f"ユーザー:{user_question} / {reply}"
                        logging.info(f"{self.bot_name} reply (先手): {response}")
                    await channel.send(response)
                    # Orchestrator用に生返答のみ保存
                    self.r.set(f"{self.reply_key_prefix}{request_id}", reply)
                    logging.info(f"Orchestrator用に保存: {self.reply_key_prefix}{request_id}={reply}")
            except Exception as e:
                logging.error(f"{self.queue_name}の処理中にエラー: {e}")
            await asyncio.sleep(self.config.MONITOR_INTERVAL)

    def generate_reply(self, user_question, prev_bot_reply):
        # サブクラスでオーバーライド or reply_choicesからランダム選択
        import random
        return random.choice(self.reply_choices)
