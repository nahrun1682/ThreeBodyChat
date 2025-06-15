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

## 参考文献
- [Discord Botのつくりかた](https://qiita.com/shown_it/items/6e7fb7777f45008e0496)
- [discord.py入門](https://qiita.com/float_py/items/f2fd2f56f9536520b36a)