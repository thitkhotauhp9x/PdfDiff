from concurrent.futures.process import ProcessPoolExecutor
from functools import partial


def add(a, b):
    return a + b


def test_process_pool_executor():

    with ProcessPoolExecutor(max_workers=2) as pool:

        result = pool.map(add, [1, 2], [3, 4])
        print(list(result))
