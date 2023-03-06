"""This module contains an implementation of the barber shop without overtaking
problem using rendezvous and FifoSemaphore implementation.

Implementation was inspired by a lecture from Mgr. Ing. Matúš Jókay, PhD.,
link: https://youtu.be/IUdx73VxUMk

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Filip Mlýnek, Marián Šebeňa, Matúš Jókay"
__email__ = "xmlynek@stuba.sk, mariansebena@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, FifoSemaphore, print
from time import sleep
from random import randint

C = 6  # number of customers
N = 5  # size of waiting room


class Shared(object):
    """
    A class that represents shared resources for a barber shop problem
    simulation.

    Attributes:
        mutex: Mutual exclusion lock to protect shared resources.
        waiting_room: The number of customers inside the waiting room.
        customer: FifoSemaphore to provide customer - barber rendezvous.
        barber: FifoSemaphore to provide barber - customer rendezvous.
        customer_done: FifoSemaphore which forms rendezvous with barber_done.
        barber_done: FifoSemaphore which forms rendezvous with customer_done.
    """

    def __init__(self):
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = FifoSemaphore(0)
        self.barber = FifoSemaphore(0)
        self.customer_done = FifoSemaphore(0)
        self.barber_done = FifoSemaphore(0)


def get_haircut(i):
    """
    Prints out that customer get a haircut and then sleeps for 1 second.

    Args:
        i: Customer's thread id.
    """

    print(f"Customer {i} gets haircut")
    sleep(1)


def cut_hair():
    """
    Prints out that barber cuts customers hair and then sleeps for 1 second.
    """

    print(f"Barber cuts hair")
    sleep(1)


def balk(i):
    """
    Simulates a situation where the customer enters a waiting room that is full
    and has to leave and wait for some amount of time.

    To simulate this scenario, prints out that the waiting room is full
    and then sleeps for 2 to 5 seconds.

    Args:
        i: Customer's thread id.
    """

    print(f"Waiting room is full. Customer {i} takes emotional damage")
    sleep(randint(2, 5))


def growing_hair(i):
    """
    Simulates a situation where the customer gets a new haircut, leaves, and
    waits for his hair to grow again.

    To simulate this scenario, sleeps for 3 to 6 seconds and then prints
    that the customer is ready for another haircut.

    Args:
        i: Customer's thread id.
    """

    sleep(randint(3, 6))
    print(f"Customer {i} has is ready for another haircut")


def customer(i, shared):
    """
    Simulates a customer behaviour in the barber shop.

    When the customer arrives and the waiting room is full, he leaves and comes
    back later. Otherwise, he can sit and notify the barber that he is waiting
    for a haircut, then he waits for the invitation from the barber. Then, the
    customer waits for the barber to finish his work and leaves. After leaving,
    the customer's hair starts growing.

    Args:
        i: Customer's thread id.
        shared: Shared resources.
    """

    while True:
        # Enter the waiting room
        shared.mutex.lock()
        if shared.waiting_room < N:
            shared.waiting_room += 1
            print(f"Customer {i} enters the waiting room")
            shared.mutex.unlock()
        else:
            # Wait few seconds and try again
            shared.mutex.unlock()
            balk(i)
            continue

        # Rendezvous customer - barber
        shared.barber.signal()
        shared.customer.wait()

        get_haircut(i)

        # Rendezvous customer_done - barber_done
        shared.customer_done.signal()
        shared.barber_done.wait()

        # Leave the waiting room
        shared.mutex.lock()
        shared.waiting_room -= 1
        print(f"Customer {i} has left the barber shop")
        shared.mutex.unlock()

        growing_hair(i)


def barber(shared):
    """
    Represents a barber that sleeps or cuts hair depending on the situation.

    Default behaviour of the barber without customers is sleeping. When a
    customer arrives, he wakes up the barber, then waits for the barber to call
    him inside. After that, the barber cuts the customer's hair and both wait
    to complete their work.

    Args:
        shared: Shared resources.
    """

    while True:
        # Rendezvous barber - customer
        shared.barber.wait()
        shared.customer.signal()

        cut_hair()

        # Rendezvous barber_done - customer_done
        shared.customer_done.wait()
        shared.barber_done.signal()


def main():
    """
    Contains main functionality.
    """
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()
