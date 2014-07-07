stm-playground
==============

Just for playing around with the experimental PyPy STM.

The benchmark scripts will sum up the number of prime numbers in the range 1 - 1.000.000, and time the duration.

Bench-threadpool uses Python threadpool implementation from multiprocessing.pool. Bench-queue uses a Queue.Queue and manually managed worker threads.

The pyprimes package (https://pypi.python.org/pypi/pyprimes/0.1.1a) has been vendored to keep things simple. Bench-threadpool-naive uses the naive version of the primality check function.

To play around, just enter the directory (so it's on your PYTHONPATH) and run the bench-* scripts.
