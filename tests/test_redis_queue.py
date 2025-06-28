import redis

def test_redis_queue_lpush_rpop():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    queue_name = "maid_queue_test"
    test_message = "pytest_redis_message"

    # 事前にキューを空にする
    r.delete(queue_name)

    # lpushで追加
    r.lpush(queue_name, test_message)
    assert r.llen(queue_name) == 1

    # rpopで取り出し
    item = r.rpop(queue_name)
    assert item == test_message

    # 取り出した後は空
    assert r.llen(queue_name) == 0
