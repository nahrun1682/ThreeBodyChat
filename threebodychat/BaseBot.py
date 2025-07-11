import discord
import asyncio
import logging

class BaseBot(discord.Client):
    """
    Maid/Masterなど複数Botで共通利用する基底クラス。
    Redisキュー監視・返答生成・Discord送信・reply保存まで一括で実装。
    サブクラスでbot_nameや返答パターン(reply_choices)を指定するだけでOK。
    """
    def __init__(self, bot_name, queue_name, reply_key_prefix, reply_choices, redis_conn, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_name = bot_name  # Botの名前（ログや識別用）
        self.queue_name = queue_name  # Redisで監視するキュー名
        self.reply_key_prefix = reply_key_prefix  # Redisに返答を保存する際のキー接頭辞
        self.reply_choices = reply_choices  # 返答候補リスト（ランダム選択用）
        self.r = redis_conn  # Redis接続インスタンス
        self.config = config  # 設定オブジェクト（MONITOR_INTERVAL等）

    async def background_task(self):
        """
        Redisキューを監視し、メッセージが来たら分解→返答生成→Discord送信→reply保存まで行う常駐タスク。
        サブクラスでsetup_hook等から起動する。
        """
        await self.wait_until_ready()  # Discordクライアントの準備完了を待つ
        while not self.is_closed():
            item = self.r.lpop(self.queue_name)  # Redisキューから1件取得
            if item is None:
                await asyncio.sleep(self.config.MONITOR_INTERVAL)
                continue
            logging.info(f"{self.queue_name} lpop: {item}")
            try:
                # item: channel_id|user_id|user_msg 形式
                channel_id, user_id, user_msg = item.strip().split("|", 2)
                logging.info(f"{self.queue_name} item split: channel_id={channel_id}, user_id={user_id}, user_msg={user_msg}")
                channel = self.get_channel(int(channel_id))  # Discordチャンネル取得
                if channel:
                    # user_msg: request_id|user_question|prev_bot_reply または request_id|user_question
                    msg_parts = user_msg.split("|", 2)
                    if len(msg_parts) == 3:
                        # 後手: request_id|user_question|prev_bot_reply
                        request_id, user_question, prev_bot_reply = msg_parts
                    elif len(msg_parts) == 2:
                        # 先手: request_id|user_question
                        request_id, user_question = msg_parts
                        prev_bot_reply = None
                    else:
                        logging.error(f"{self.queue_name} message parse error: {msg_parts}")
                        await asyncio.sleep(self.config.MONITOR_INTERVAL)
                        continue
                    logging.info(f"{self.queue_name} message parts: request_id={request_id}, user_question={user_question}, prev_bot_reply={prev_bot_reply}")

                    # 返答生成
                    reply = self.generate_reply(user_question, prev_bot_reply)
                    if prev_bot_reply:
                        #テスト用
                        # 後手Botの返答（ユーザー発言＋先手Bot返答＋自分の返答）
                        # response = f"ユーザー:{user_question} / 先手:{prev_bot_reply} / {reply}"
                        response = reply
                        logging.info(f"{self.bot_name} reply (後手): {reply}")
                    else:
                        # 先手Botの返答（ユーザー発言＋自分の返答）
                        # response = f"ユーザー:{user_question} / {reply}"
                        response = reply
                        logging.info(f"{self.bot_name} reply (先手): {reply}")
                    # Discordのメッセージ長制限（2000文字）対応
                    MAX_DISCORD_MSG_LEN = 2000
                    if len(response) > MAX_DISCORD_MSG_LEN:
                        logging.warning(f"Discord送信メッセージ長超過: {len(response)}文字 → 2000文字でカット")
                        response = response[:MAX_DISCORD_MSG_LEN]
                    await channel.send(response)  # Discordに送信
                    # Orchestrator用に生返答のみ保存（request_idで一意化）
                    self.r.set(f"{self.reply_key_prefix}{request_id}", reply)
                    logging.info(f"Orchestrator用に保存: {self.reply_key_prefix}{request_id}={reply}")
            except Exception as e:
                logging.error(f"{self.queue_name}の処理中にエラー: {e}")
            await asyncio.sleep(self.config.MONITOR_INTERVAL)

    def generate_reply(self, user_question, prev_bot_reply):
        """
        返答生成メソッド。サブクラスでオーバーライド可。
        デフォルトはreply_choicesからランダム選択。
        """
        import random
        return random.choice(self.reply_choices)
