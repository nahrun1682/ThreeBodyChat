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
├── tests/
└── threebodychat/
    ├── __init__.py
    ├── Maid.py      # メイドBotの実装
    ├── Master.py    # 師匠Botの実装予定
    └── config.py    # Discordトークンなどの設定
```
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　
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

### 制御フローの概要

1. **Orchestrator（司令塔Bot）**
   - ユーザーのDiscord発言を受信
   - どちらのBot（Maid/Master）が返答するかをランダムで決定
   - Redisの該当キュー（maid_queue/master_queue）に `rpush` で「channel_id|user_id|message_content」を追加
2. **Maid / Master Bot**
   - それぞれ自分用のRedisキュー（maid_queue/master_queue）を `lpop` で定期監視
   - メッセージがあれば、内容をパースしてDiscordチャンネルに返答

### ポイント
- 各Botは**独立プロセス・独立トークン**で動作し、直接通信はしません
- Orchestrator→Redis→Botの**一方向制御**で疎結合・スケーラブルな設計
- Redisを使うことで、リアルタイムかつ軽量なメッセージパスを実現

### 図式イメージ

```
[ユーザー] → [Orchestrator] → (maid_queue/master_queue in Redis) → [Maid/Master] → [Discordチャンネル]
```

### ユーザー発言の受け渡し設計

- Maid/Masterのどちらが先・後手になっても、**必ずユーザーの発言内容は両方のBotに渡されます**。
- 先手Botには「ユーザー発言」のみが渡され、後手Botには「ユーザー発言＋先手Botの返答」が渡されます。
- これにより、**どちらのBotもユーザーの発言内容を必ず取得でき、今後の関数設計で引数として自由に利用できます**。

#### 例
1. ユーザー「こんにちは」
2. OrchestratorがMaidを先手に選ぶ
3. Maidには「こんにちは」が渡される
4. Maidが返答した後、Masterには「こんにちは｜Maidの返答」が渡される

> どちらが先手・後手でも、**ユーザー発言は必ず両Botに伝わる**ため、  
> Botの応答ロジックでユーザー発言を引数として利用できます。

## 参考文献
- [Discord Botのつくりかた](https://qiita.com/shown_it/items/6e7fb7777f45008e0496)
- [discord.py入門](https://qiita.com/float_py/items/f2fd2f56f9536520b36a)