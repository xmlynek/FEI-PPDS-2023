"""This module contains an implementation of the dinning philosophers problem.

This implementation involves categorizing the philosophers as either
left-handed or right-handed in order to solve the problem.

The implementation was inspired by the lecture from Mgr. Ing. Matúš Jókay, PhD.
link: https://youtu.be/8CF098hseDw.

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
 """

__authors__ = "Filip Mlýnek, Tomáš Vavro, Matúš Jókay"
__email__ = "xmlynek@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from time import sleep
from random import randint

NUM_PHILOSOPHERS: int = 5
NUM_RUNS: int = 30  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """Represent shared data for all threads.

    Attributes:
        forks: A list of the mutex locks that represent forks on the table.
        handedness_type: A list of integers representing the handedness type
            of the philosophers. A 0 represents right-handedness, and a 1
            represents left-handedness. The resulting list contains both 0
            and 1 values.
    """
    def __init__(self):
        """Initialize an instance of Shared and print generated handedness
        types of the philosophers
        """
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]
        self.handedness_type = self.__generate_handedness_types()
        print(f"Handedness types of the philosophers {self.handedness_type}")

    @staticmethod
    def __generate_handedness_types() -> list[int]:
        """Generates a list containing both 0 and 1 values, representing
        the handedness of a group of philosophers.

        The value 0 represents right-handedness, and the value 1 represents
        left-handedness.

        Returns:
            List of integers (0,1) representing the handedness of the
            philosophers.
        """
        handedness_type = [0] * NUM_PHILOSOPHERS
        for i in range(0, NUM_PHILOSOPHERS):
            handedness_type[i] = randint(0, 1)
        if 0 not in handedness_type:
            handedness_type[randint(0, NUM_PHILOSOPHERS - 1)] = 0
        elif 1 not in handedness_type:
            handedness_type[randint(0, NUM_PHILOSOPHERS - 1)] = 1
        return handedness_type


def think(i: int):
    """Simulates philosopher thinking.

    Args:
        i: philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(1)


def eat(i: int):
    """Simulates philosopher eating.

    Args:
        i: philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(1)


def pick_left_fork(i: int, shared: Shared):
    """Locks the philosopher's left fork.

    Args:
        i: philosopher's id
        shared: shared data
    """
    shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()


def pick_right_fork(i: int, shared: Shared):
    """Locks the philosopher's right fork.

    Args:
        i: philosopher's id
        shared: shared data
    """
    shared.forks[i].lock()


def philosopher(i: int, shared: Shared):
    """Run philosopher's code.

    Args:
        i: philosopher's id
        shared: shared data
    """
    for _ in range(NUM_RUNS):

        think(i)

        if shared.handedness_type[i] == 0:
            # right-handed philosopher
            pick_right_fork(i, shared)
            pick_left_fork(i, shared)
        else:
            # left-handed philosopher
            pick_left_fork(i, shared)
            pick_right_fork(i, shared)

        eat(i)

        # put forks back on the table
        shared.forks[i].unlock()
        shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()


def main():
    """Contains main functionality."""
    shared: Shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()
