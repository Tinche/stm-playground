#!/usr/bin/env python
import multiprocessing
import threading
from itertools import izip, chain, repeat
from Queue import Queue

from pyprimes import isprime

LIMIT = 1000000
BATCH_SIZE = 1000
CONCURRENCY = multiprocessing.cpu_count()

def check_prime(num):
    return isprime(num), num


class benchmark(object):
    from timeit import default_timer as timer
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        self.start = self.timer()
    def __exit__(self, ty, val, tb):
        end = self.timer()
        print("%s : %0.3f seconds" % (self.name, end-self.start))
        return False

def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return izip(*[chain(iterable, repeat(padvalue, n-1))]*n)

tasks = Queue()
results = Queue()
print("Starting...")
poison_pill = object()

def worker():
    while True:
        batch = tasks.get()
        if batch is poison_pill:
            tasks.task_done()
            return
        results.put([check_prime(task) for task in batch])
        tasks.task_done()

for batch in grouper(BATCH_SIZE, xrange(LIMIT), 1):
    tasks.put(list(batch))
for _ in xrange(CONCURRENCY):
    tasks.put(poison_pill)

with benchmark("multithreaded primality test"):
    for _ in xrange(CONCURRENCY):
        t = threading.Thread(target=worker)
        t.start()
    tasks.join()

count = 0
while not results.empty():
    batch_results = results.get()
    count += sum(1 for res in batch_results if res[0])

print("{0} prime(s) detected.".format(count))
