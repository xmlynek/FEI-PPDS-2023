"""Module contains an implementation of the modified dining savages problem
with multiple cooks.

This module implements the dining savages problem, where there are a group of
savages that eat from a pot of food that is replenished by multiple cooks.

The implementation was inspired by the lecture from Mgr. Ing. Matúš Jókay, PhD.
link: https://www.youtube.com/watch?v=iotYZJzxKf4.

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Filip Mlýnek, Matúš Jókay"
__email__ = "xmlynek@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print, Semaphore
from time import sleep

NUM_SAVAGES: int = 5
NUM_COOKS: int = 3
POT_SIZE: int = 3


class Shared:
    """A class that holds shared resources between threads.

    Attributes:
        savages_mutex (Mutex): A mutual exclusion lock for savages.
        servings_mutex (Mutex): A mutual exclusion lock for servings.
        servings (int): The number of servings left in the pot.
        full_pot (Semaphore): A semaphore to signalize that the pot is full.
        empty_pot (Semaphore): A semaphore to signalize that the pot is empty.
        savages_count (int): The number of savages waiting at the barrier.
        barrier (Semaphore): A semaphore for synchronization of savages.
        cooks_mutex (Mutex): A mutual exclusion lock for cooks.
        cooks_finished (int): The number of cooks that finished cooking.
    """
    def __init__(self):
        self.savages_mutex = Mutex()
        self.servings_mutex = Mutex()
        self.servings = POT_SIZE

        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)

        self.savages_count = 0
        self.barrier = Semaphore(0)

        self.cooks_mutex = Mutex()
        self.cooks_finished = 0


def savage_feast(i: int):
    """Simulates feasting of the savage.

    Args:
        i (int): Thread id of the savage.
    """
    print(f"Savage {i} is feasting!")
    sleep(0.25)


def savage(i: int, shared: Shared):
    """The function executed by a savage thread.

    Args:
        i (int): Thread id of the savage.
        shared (Shared): The shared resources.
    """
    while True:
        # wait for all savages using barrier
        shared.savages_mutex.lock()
        shared.savages_count += 1
        print(f"Savage {i} joined the party. "
              f"Savages waiting: {shared.savages_count}")
        if shared.savages_count == NUM_SAVAGES:
            shared.savages_count = 0
            print("ALL OF THE SAVAGES ARE TOGETHER. LET'S FEAST!")
            shared.barrier.signal(NUM_SAVAGES)
        shared.savages_mutex.unlock()
        shared.barrier.wait()

        shared.servings_mutex.lock()
        print(f"The savage {i} is taking a portion")
        if shared.servings == 0:
            print(f"THE POT IS EMPTY. Wake up the cooks!")
            shared.empty_pot.signal(NUM_COOKS)
            print(f"The cooks start cooking!")
            shared.full_pot.wait()
        shared.servings -= 1
        print(
            f"The savage {i} took a portion. Portions left: {shared.servings}"
        )
        shared.servings_mutex.unlock()

        savage_feast(i)


def cook(i: int, shared: Shared):
    """The function executed by a cook thread.

    Args:
        i (int): Thread id of the cook.
        shared (Shared): The shared resources.
    """
    while True:
        shared.empty_pot.wait()

        while True:
            shared.cooks_mutex.lock()
            if shared.servings == POT_SIZE:
                # pot is full and the last cook thread signalizes it
                shared.cooks_finished += 1
                if shared.cooks_finished == NUM_COOKS:
                    shared.cooks_finished = 0
                    print(f"The pot is full again!")
                    shared.full_pot.signal()
                shared.cooks_mutex.unlock()
                break
            else:
                shared.servings += 1
                print(f"Cook {i} adds a portion to the pot. "
                      f"Total portions: {shared.servings}/{POT_SIZE}")
            shared.cooks_mutex.unlock()
            sleep(0.25)


def main():
    """Contains main functionality."""
    shared: Shared = Shared()
    cooks: list[Thread] = [
        Thread(cook, i, shared) for i in range(NUM_COOKS)
    ]
    savages: list[Thread] = [
        Thread(savage, i, shared) for i in range(NUM_SAVAGES)
    ]
    for s in savages:
        s.join()
    for c in cooks:
        c.join()


if __name__ == "__main__":
    main()
