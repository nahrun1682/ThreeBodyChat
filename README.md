# ThreeBodyChat

**ThreeBodyChat** は、「人間 + 2体のLLM（大規模言語モデル）」が三位一体となって会話を行う、新しいチャット体験を目指すプロジェクトです。  
名前の由来は中国SF小説『三体』から着想を得ており、3者の対話によってカオスではなくバランスを生み出す設計思想に基づいています。

## 🌟 コンセプト

- LLMを「メイド」「師匠」などの人格としてキャラクター化
- Discord上で複数AIと同時に会話ができる「マルチボット構成」
- ユーザーとのやり取りの中でエージェントたちの“人格”が進化する仕組み（予定）
- 応答制御・オーケストレーションによって自然な会話を実現
- UIの制約を排し、「記憶（Memory）」を中核に据えたエージェント設計

---

## 📂 プロジェクト構成

```bash
ThreeBodyChat/
├── Dockerfile
├── compose.yml
├── poetry.toml
├── pyproject.toml
├── poetry.lock
├── README.md
├── run_all.sh                # Bot一括起動・多重起動防止スクリプト
├── logs/
│   └── threebodychat.log     # 全Bot共通のログファイル
├── tests/                    # pytest用テストコード
│   ├── test_orchestrator.py
│   ├── test_Maid.py
│   └── test_Master.py
└── threebodychat/
    ├── __init__.py
    ├── Maid.py               # メイドBotの実装
    ├── Master.py             # 師匠Botの実装
    ├── Orchestrator.py       # 司令塔Bot（制御・分配・Redis仲介）
    └── config.py             # Discordトークン・設定
```

- **Orchestrator.py** … ユーザー発言の受信・Bot割り振り・Redis制御の中枢
- **Maid.py / Master.py** … それぞれ独立したBot実装。Redisキュー監視・返答
- **run_all.sh** … Bot多重起動防止＆一括起動用
- **logs/** … すべてのBotの動作ログを1ファイルに集約
- **tests/** … pytestによる自動テスト一式

---

## Redisについて

**Redis**は、インメモリ型の高速なデータストア（NoSQLデータベース）です。
本プロジェクトでは、Bot間のメッセージキューとしてRedisを利用しています。
Orchestratorがユーザー発言をRedisキューに書き込み、Maid/Master Botがそのキューを監視して返答する設計です。

### Redisの導入・起動方法（Ubuntu/WSLの場合）

1. Redisのインストール
   ```sh
   sudo apt update
   sudo apt install redis-server
   ```

2. Redisサーバーの起動
   ```sh
   sudo service redis-server start
   ```

3. 動作確認
   ```sh
   redis-cli ping
   ```
   `PONG` と返ってくればOKです。

> DockerでRedisを使いたい場合は
> `docker run -d -p 6379:6379 --name redis redis`
> でも起動できます。

## 🧪 テストについて

本プロジェクトでは、各BotやOrchestratorの主要な処理についてpytestによるユニットテストを用意しています。

- Orchestratorの割り振りロジックやRedisキュー書き込みのテスト
- Maid/MasterのRedisキュー取得・返答ロジックのテスト
- ランダム返答が複数パターン出るかのテスト

### テスト実行方法

1. 依存パッケージのインストール（初回のみ）
   ```sh
   poetry install
   ```
2. Redisサーバーを起動
   ```sh
   sudo service redis-server start
   # または docker run -d -p 6379:6379 --name redis redis
   ```
3. プロジェクトルートでpytestを実行
   ```sh
   poetry run pytest
   ```

### テストファイル例
- `tests/test_orchestrator.py`：Orchestratorの割り振り・キュー書き込みテスト
- `tests/test_Maid.py`：MaidのRedisキュー取得・返答ロジックテスト
- `tests/test_Master.py`：MasterのRedisキュー取得・返答ロジックテスト

各テストには初心者向けの詳細なコメントも記載しています。

## 🛠 RedisによるマルチBot制御の仕組み

ThreeBodyChatでは、Bot間のやりとりや役割分担を**Redisのキュー機能**で制御しています。

### ざっくりイメージ

- Orchestrator（司令塔Bot）が「ユーザー発言」を受け取る
- どちらのBot（Maid/Master）が先に返事するかを決める
- Redisのキュー（例: maid_queue, master_queue）に「手紙」を入れる
- Maid/Masterは自分宛てのキューを定期的にチェックし、手紙が来ていたら返事を返す
- 返事もまたRedisに一時保存され、Orchestratorがそれを受け取って次のBotに渡す

### 具体的な流れ（request_id方式）

1. **ユーザーがDiscordで発言**
2. **Orchestrator**が「どちらが先手か」をランダムで決定し、
   - 先手Botのキューに「channel_id|user_id|request_id|ユーザー発言」を入れる
   - request_idは「この会話だけの番号（例: UUID）」で、やりとりの混線を防ぐために必須
3. **先手Bot（Maid/Master）**は自分のキューを監視し、
   - 受け取ったらrequest_idとユーザー発言を分解
   - 返答を考えてDiscordに送信
   - 返答（生返答）を`reply_maid_{request_id}`や`reply_master_{request_id}`としてRedisに保存
4. **Orchestrator**はその返答をRedisから受け取り、
   - 後手Botのキューに「channel_id|user_id|request_id|ユーザー発言|先手Bot返答」を入れる
5. **後手Bot**は自分のキューを監視し、
   - 受け取ったらrequest_id・ユーザー発言・先手Bot返答を分解
   - それを元に返答を考えてDiscordに送信
   - 返答（生返答）を`reply_maid_{request_id}`や`reply_master_{request_id}`としてRedisに保存

#### 図式イメージ（request_id方式）

```
[ユーザー]
   ↓
[Orchestrator]
   ↓  (maid_queue/master_queue in Redis)
[先手Bot(Maid/Master)]
   ↓  (reply_xxx_{request_id} in Redis)
[Orchestrator]
   ↓  (maid_queue/master_queue in Redis)
[後手Bot(Maid/Master)]
   ↓
[Discordチャンネル]
```

#### 例（Maidが先手の場合）
1. ユーザー「こんにちは」
2. Orchestratorがrequest_id=abc123を生成し、maid_queueに「...|abc123|こんにちは」を入れる
3. Maidが「abc123|こんにちは」を受け取り、返答「さすがですわ！」を`reply_maid_abc123`に保存
4. Orchestratorが`reply_maid_abc123`から返答を取得し、master_queueに「...|abc123|こんにちは|さすがですわ！」を入れる
5. Masterが「abc123|こんにちは|さすがですわ！」を受け取り、返答「鹿だな」を`reply_master_abc123`に保存

---

### なぜrequest_idが必要？

- 複数のユーザーや連投が同時に走っても「どの返答がどの会話のものか」を絶対に間違えないため
- 1つの会話ごとに固有の番号（request_id）でやりとりを追跡することで、
  返答の混線・重複・ズレを完全に防げます

---

### まとめ
- Redisは「Bot同士の手紙箱」
- 1会話ごとにrequest_idという番号を付けて、やりとりを確実に紐付け
- どんなに同時に会話が走っても、返答がズレたり混ざったりしない

---

## 参考文献
- [Discord Botのつくりかた](https://qiita.com/shown_it/items/6e7fb7777f45008e0496)
- [discord.py入門](https://qiita.com/float_py/items/f2fd2f56f9536520b36a)
- [langfuse cloud](https://us.cloud.langfuse.com/)