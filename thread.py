import threading
import time
from concurrent.futures import ThreadPoolExecutor


def show_threads(label: str):
    """Helper to print current thread count and names."""
    threads = threading.enumerate()
    print(f"\n[{label}]")
    print(f"  Total threads: {len(threads)}")
    for t in threads:
        print(f"    → {t.name}")


show_threads("At program start")
# You will see: just MainThread

pool = ThreadPoolExecutor(max_workers=3)
show_threads("After creating pool (before submitting any work)")
# You will STILL see: just MainThread — pool creation is lazy!


def slow_task(n):
    time.sleep(2)  # hold the thread busy so we can observe
    return n


# Submit first task
f1 = pool.submit(slow_task, 1)
show_threads("After submitting 1 task")
# Now you see: MainThread + ThreadPoolExecutor-0_0

# Submit 2 more while first is still running
f2 = pool.submit(slow_task, 2)
f3 = pool.submit(slow_task, 3)
show_threads("After submitting 3 tasks total")
# Now: MainThread + 3 worker threads

# Wait for all to finish
f1.result()
f2.result()
f3.result()
show_threads("After all tasks finish")
# Workers are still alive! They don't die — they wait for more work.
# This is the whole point of a pool.

pool.shutdown()
show_threads("After pool shutdown")
# Workers are now terminated. Back to just MainThread.
