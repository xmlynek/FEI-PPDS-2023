# Assignment 02 - Barber shop


[![Python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue.svg)](https://www.python.org/downloads/release/python-3106/)

## Table of contents
- [Assignment description](#assignment-description)
- [Quick start](#quick-start)
- [Description of the rendezvous synchronization technique](#description-of-the-rendezvous-synchronization-technique)
- [Implementation of the barber shop with overtaking](#implementation-of-the-barber-shop-with-overtaking)
  - [Sample output](#sample-output)
- [Implementation of the barber shop without overtaking](#implementation-of-the-barber-shop-without-overtaking)
  - [Sample output using FifoSemaphore](#sample-output-using-fifosemaphore)


## Assignment description

The purpose of this assignment is to implement the Barber shop problem using the rendezvous synchronization technique.

The barber shop consists of 2 separate rooms, the waiting room, and the barber's room.
Behaviour of the barber and customers is based on the following rules:
- If there are no customers, the waiting room is empty, then the barber is sleeping.
- When the customer enters the barber shop and the waiting room is full, the customer will leave.
- When the customer enters the barber shop while the waiting room is not fully occupied:
  - If the barber is sleeping, the customer wakes him up and sits in the waiting room and waits for his turn.
  - If the barber is awake, the customer sits in the waiting room and waits for his turn.


## Quick start
Before running the script, perform the following steps:
1. Set python interpreter version to 3.10.x.
2. Install `fei.ppds` module (`pip install --upgrade fei.ppds`).
3. Set the number of customers in `C` variable to your desired value. Default value is 5.
4. Set the size of the waiting room in `N` variable to your desired value. Default value is 3.


## Description of the rendezvous synchronization technique
"In parallel programming, rendezvous using semaphores is a synchronization technique that allows two or more parallel processes to synchronize with each other at a predetermined point in their execution. The term "rendezvous" refers to the synchronization of two or more processes that agree to meet at a certain point in time" - ChatGPT.


## Implementation of the barber shop with overtaking
The implementation consists of multiple functions and a single class `Shared`.

The class `Shared` contains shared resources, such as `waiting_room`, which represents the number of customers inside the waiting room.
Since the `waiting_room` is a shared resource, we need to provide integrity when we are manipulating its value, and that's why we are using mutual exclusion `mutex`.
Furthermore, it contains 4 semaphores, used for the synchronization technique called rendezvous.

Functions, such as `get_haircut`, `cut_hair`, `balk`, and `growing_hair` does not contain any main logic,
their purpose is to print message about what is happening and call sleep function.

However, `customer` and `barber` functions contain the main logic of the implementation.

The `barber` function simulates the barber's behavior which is either sleeping when there are no customers
or cutting the customer's hair. This function uses 2 synchronization techniques in form of rendezvous.
- The first rendezvous is in the beginning, where the barber is waiting for a customer to wake him up.
When the customer wakes up the barber, the barber calls him to get a haircut.
  ```python
  shared.barber.wait()
  shared.customer.signal()
  ```
- The second rendezvous is shown below. The barber is waiting for a customer to be happy with his haircut,
after that he signals that he finished his job.
  ```python
  shared.customer_done.wait()
  shared.barber_done.signal()
  ```

The `customer` function simulates the customer's behavior in the barber shop based on certain circumstances, described in [Assignment description](#assignment-description).
- The first part of this function handles customer's arrival. When the customer arrives,
he checks whether there is a space for him in the waiting room. If it is, he can take a seat.
In code, this is represented as incrementation of the `waiting_room` variable. Otherwise, if the waiting room is full,
the customer leaves, which is represented as sleeping for some amount of time. Since the
`waiting_room` variable is inside the critical section, we need to provide integrity and that's why
we are using `mutex` for mutual exclusion.
  ```python
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
  ```
- When the customer is ready to get a haircut, he signals the barber about it and then waits
for the barber to invite him inside his room.
  ```python
  shared.barber.signal()
  shared.customer.wait()
  ```
- Right after the customer gets his haircut, he signals the barber that he is happy with it,
and waits for the barber to finish his final adjustments.
  ```python
  shared.customer_done.signal()
  shared.barber_done.wait()
  ```
- When the customer gets his haircut, he leaves the barber shop, which is represented inside the code below.
Again, we need to provide integrity for the `waiting_room` and that's why we use mutual exclusion. 
The reason why `print` function is inside the critical section is that I want to display this message in the same time when the customer leaves.
  ```python
  shared.mutex.lock()
  shared.waiting_room -= 1
  print(f"Customer {i} has left the barber shop")
  shared.mutex.unlock()
  ```

### Sample output
This is the sample output when using 5 customers and having only 3 seats available in the waiting room.
Your output may be different.
```
Customer 0 enters the waiting room
Customer 1 enters the waiting room
Customer 2 enters the waiting room
Waiting room is full. Customer 3 takes emotional damage
Waiting room is full. Customer 4 takes emotional damage
Barber cuts hair
Customer 0 gets haircut
Barber cuts hair
Customer 0 has left the barber shop
Customer 2 gets haircut
Barber cuts hair
Customer 1 gets haircut
Customer 2 has left the barber shop
Customer 1 has left the barber shop
Customer 0 has is ready for another haircut
Customer 0 enters the waiting room
Barber cuts hair
Customer 0 gets haircut
Customer 4 enters the waiting room
Customer 3 enters the waiting room
Customer 2 has is ready for another haircut
Waiting room is full. Customer 2 takes emotional damage
```
We can see that in the first 5 lines customers are entering the waiting room, but only 3 of them
are able to get in because the maximum number of customers inside the waiting room is 3.

Then the barber starts cutting the customer's hair, and then the customer leaves. This is repeating again and again.

The interesting part is at the end, described below. We can see that the
`Customer 0` got a haircut, and customers `4` and `3` entered the waiting room. Meanwhile,
`Customer 2` is ready for another haircut, so he tries to enter the waiting room,
but he can not take a seat because `Customer 0` hasn't left yet. That's why he has to leave.
```
Barber cuts hair
Customer 0 gets haircut
Customer 4 enters the waiting room
Customer 3 enters the waiting room
Customer 2 has is ready for another haircut
Waiting room is full. Customer 2 takes emotional damage
```

## Implementation of the barber shop without overtaking
As we could see in the [sample output](#sample-output) of the barber shop with overtaking, the customers were called
in a different order than they arrived. To solve this issue, we can use queue to obtain the first-in, first-out (FIFO) 
principle.

Since we are using the `fei.ppds` library which has multiple different implementations of the Semaphore, we are going
to use the `FifoSemaphore`. The `FifoSemaphore` implementation uses a `queue` object to keep track of the waiting
threads so that adheres the FIFO principle.

Implementation of this variant of the barber shop is in the [barber_shop_fifo.py](barber_shop_fifo.py) file. The only
change compared to the barber shop with overtaking is using `FifoSemaphore` instead of `Semaphore` inside the Shared
class.

```python
self.customer = FifoSemaphore(0)
self.barber = FifoSemaphore(0)
self.customer_done = FifoSemaphore(0)
self.barber_done = FifoSemaphore(0)
```

### Sample output using FifoSemaphore
This is the sample output when using 6 customers and 5 seats in the waiting room. As you can see, the order of the customers
getting haircuts matches the order of the customers entering the waiting room.
```
Customer 0 enters the waiting room
Customer 1 enters the waiting room
Customer 2 enters the waiting room
Customer 3 enters the waiting room
Customer 4 enters the waiting room
Waiting room is full. Customer 5 takes emotional damage
Barber cuts hair
Customer 0 gets haircut
Barber cuts hair
Customer 0 has left the barber shop
Customer 1 gets haircut
Customer 5 enters the waiting room
Barber cuts hair
Customer 1 has left the barber shop
Customer 2 gets haircut
Barber cuts hair
Customer 2 has left the barber shop
Customer 3 gets haircut
Barber cuts hair
Customer 3 has left the barber shop
Customer 4 gets haircut
Barber cuts hair
Customer 5 gets haircut
```