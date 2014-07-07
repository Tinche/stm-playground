#!/usr/bin/env python
import multiprocessing
import threading
from Queue import Queue

from pyprimes import isprime

LIMIT = 1000000

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

tasks = Queue()
results = Queue()
print("Starting...")
poison_pill = object()

def worker():
    while True:
        task = tasks.get()
        if task is poison_pill:
            tasks.task_done()
            return
        results.put(check_prime(task))
        tasks.task_done()

for num in xrange(LIMIT):
    tasks.put(num)
for _ in xrange(multiprocessing.cpu_count()):
    tasks.put(poison_pill)

with benchmark("multithreaded primality test"):
    for _ in xrange(multiprocessing.cpu_count()):
        t = threading.Thread(target=worker)
        t.start()
    tasks.join()

count = 0
while not results.empty():
    result = results.get()
    if result[0]:
        count += 1

print("{0} prime(s) detected.".format(count))
