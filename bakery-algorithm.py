"""This module contains an implementation of the bakery algorithm.
The Bakery algorithm allows multiple (N) threads to access and work with
shared resources one at a time, without interfering with each other.
"""

__author__ = "Filip Mlýnek, Tomáš Vavro"
__email__ = "xmlynek@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

NUM_THREADS = 3
nums: list[int] = [0] * NUM_THREADS
inside: list[bool] = [False] * NUM_THREADS


def lock(tid: int):
    """
    Attempts to acquire the lock for the thread with the given thread id.

    Args:
        tid: Thread id.
    """
    global nums, inside

    # set the entering flag and assign the highest number to the thread
    inside[tid] = True
    nums[tid] = max(nums) + 1
    inside[tid] = False

    # wait for all other threads with smaller numbers or with the same number
    # and lower thread id finished entering or have a lower number
    for j in range(NUM_THREADS):
        while inside[j]:
            continue
        while (nums[j] != 0 and
               nums[j] < nums[tid] or (nums[j] == nums[tid] and j < tid)):
            continue


def release_lock(tid: int):
    """
    Releases the lock for the thread with the given thread id.

    Args:
        tid: Thread id.
    """
    global nums

    # clear the number for the thread with the given thread id
    nums[tid] = 0


def process(tid: int, num_runs: int):
    """
    Simulates a process with a critical section that prints a message,
    including the current thread id.

    Args:
        tid: Thread id.
        num_runs: Number of executions of the critical section.
    """
    global nums, inside

    for _ in range(num_runs):
        # attempt to acquire the lock
        lock(tid)

        # execute a critical section
        print(f"Thread {tid} runs a complicated computation!")
        sleep(0.5)

        # exit the critical section by releasing the lock
        release_lock(tid)


if __name__ == '__main__':
    DEFAULT_NUM_RUNS = 5

    threads = [Thread(process, i, DEFAULT_NUM_RUNS)
               for i in range(NUM_THREADS)]
    [t.join() for t in threads]
