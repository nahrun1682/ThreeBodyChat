import os
from threebodychat.Orchestrator import assign_responder, write_to_queue

def test_assign_responder_distribution():
    counts = {"Maid": 0, "Master": 0}
    for _ in range(1000):
        who = assign_responder()
        counts[who] += 1
    # MaidとMaster両方に偏りなく振り分けられるかをざっくりチェック
    assert 400 < counts["Maid"] < 600
    assert 400 < counts["Master"] < 600

def test_write_to_queue(tmp_path):
    maid_file = tmp_path / "maid_queue.txt"
    master_file = tmp_path / "master_queue.txt"
    # ファイルパスを渡すよう関数を調整しても良い
    write_to_queue("Maid", 123, 456, "hello!")
    write_to_queue("Master", 123, 456, "world!")
    # Maid用キューに書き込まれているか
    assert os.path.exists("maid_queue.txt")
    with open("maid_queue.txt") as f:
        lines = f.readlines()
    assert any("hello!" in line for line in lines)
