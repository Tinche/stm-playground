#!/usr/bin/env python
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from pyprimes import isprime

LIMIT = 1000000
CONCURRENCY = cpu_count()

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

pool = ThreadPool(CONCURRENCY)
print("Starting...")

with benchmark("multithreaded primality test"):
    results = pool.map_async(check_prime, xrange(LIMIT))
    results.get()

print("{0} prime(s) detected.".format(sum(1 for res in results.get() if res[0])))
