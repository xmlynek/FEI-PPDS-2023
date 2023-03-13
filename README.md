# Assignment 03 - The dining philosophers problem


[![Python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue.svg)](https://www.python.org/downloads/release/python-3106/)

## Table of contents
- [Quick start](#quick-start)
- [Assignment description](#assignment-description)
- [Implementation based on the handedness type](#implementation-based-on-the-handedness-type)
- [Sample output](#sample-output)
- [Comparison](#comparison-to-the-solution-with-the-waiter)



## Quick start
Before running the script, perform the following steps:
1. Set python interpreter version to 3.10.x.
2. Install `fei.ppds` module (`pip install --upgrade fei.ppds`).
3. Set the number of philosophers in `NUM_PHILOSOPHERS` variable to your desired value. Default value is 5.
4. Set the number of repetitions of think-eat cycle in `NUM_RUNS` variable to your desired value. Default value is 30.


## Assignment description
The purpose of this assignment is to solve the dining philosophers problem without
causing a deadlock or a starvation.


The concrete problem is based on the idea of 5 philosophers who are sitting around
a circular table, each with a plate in front of them and a fork, placed between each pair
of adjacent philosophers. For better imagination, see the picture below.

![image which represents table with plates and forks for each philosopher](https://user-images.githubusercontent.com/70724986/224495299-0810d777-5128-4f4e-9d2c-6ad6552f52e0.png)

Each philosopher can be either thinking or eating. In order to eat, a philosopher
requires two forks, one on each side. However, since there are only 5 forks on the
table and each philosopher needs two, they must share the forks.


## Implementation based on the handedness type
The implementation consists of multiple functions and a class `Shared`.

The class `Shared` contains shared resources, such as `forks` and `handedness_type`.
- Attribute `forks` symbolizes forks on the table, which is represented as a list of
`Mutex` objects.
- Attribute `handedness_type` constitutes the handedness type of the philosophers,
which is implemented as a list of both `0` and `1` values, where the value `0` 
symbolizes right-handedness, and the value `1` represents left-handedness.

To provide a more realistic scenario, the handedness type of the philosophers is
generated randomly using the method below. This method randomly assigns values
`0` and `1` to a resulting list and assures that it always contains both values.
```python
@staticmethod
def __generate_handedness_types() -> list[int]:
    handedness_type = [0] * NUM_PHILOSOPHERS
    for i in range(0, NUM_PHILOSOPHERS):
        handedness_type[i] = randint(0, 1)
    if 0 not in handedness_type:
        handedness_type[randint(0, NUM_PHILOSOPHERS - 1)] = 0
    elif 1 not in handedness_type:
        handedness_type[randint(0, NUM_PHILOSOPHERS - 1)] = 1
    return handedness_type
```

Both `think` and `eat` functions are just used to simulate certain activities.

Functions `pick_left_fork` and `pick_right_fork` are helper functions used to
lock the particular `mutex`, which represents the fork that is being picked up.

```python
def pick_right_fork(i: int, shared: Shared):
    shared.forks[i].lock()

def pick_left_fork(i: int, shared: Shared):
    shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
```

Both of these functions are used in the `philosopher` function, which contains the
essential part of the implementation. The core of the logic is built on the fact that
the philosopher raises either the right or the left fork first, based on the handedness type.
This means that the right-handed philosopher raises the right fork first
and then raises the left fork, and thus the left-handed philosopher first lifts
the left fork and later the right fork.

```python
if shared.handedness_type[i] == 0:
    # right-handed philosopher
    pick_right_fork(i, shared)
    pick_left_fork(i, shared)
else:
    # left-handed philosopher
    pick_left_fork(i, shared)
    pick_right_fork(i, shared)
```

After finishing the meal, the philosopher returns both forks to the table, so
that the others can pick them up and start eating. In this case, it's not
necessary to return the forks in the same order as they were picked up.

```python
# put forks back on the table
shared.forks[i].unlock()
shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
```

## Sample output
This is the sample output with 5 philosophers. Note that your output may be
different.
```
Handedness types of the philosophers [0, 1, 1, 0, 1]
Philosopher 0 is thinking!
Philosopher 1 is thinking!
Philosopher 2 is thinking!
Philosopher 3 is thinking!
Philosopher 4 is thinking!
Philosopher 0 is eating!
Philosopher 3 is eating!
Philosopher 3 is thinking!
Philosopher 0 is thinking!
Philosopher 4 is eating!
Philosopher 1 is eating!
Philosopher 1 is thinking!
Philosopher 2 is eating!
Philosopher 4 is thinking!
```

The first line displays that the philosopher 0 and 3 are right-handed and 
the others are left-handed. The next five lines show that each philosopher
is thinking.

Then, the philosophers start picking up their forks, where we can see
that philosophers 0 and 3 got both forks, and philosophers 1, 2, and 4 did not.
After philosophers 0 and 3 finished eating and released their forks, they
started thinking and philosophers 4 and 1 started eating, and so on.


## Comparison to the solution with the waiter 


Solution using the waiter is another correct approach to solve the dining
philosophers problem. It uses a semaphore to represent a waiter who controls
the access to the forks. Each philosopher needs a permission from the waiter 
to sit down. The waiter allows `NUM_PHILOSOPHERS - 1` philosophers to sit down
and start eating. In our scenario, with 5 philosophers, it means that 4 philosophers
will be eating and 1 of them will be a waiter. For more details, see the
[implementation using waiter](https://github.com/tj314/ppds-2023-cvicenia/blob/master/seminar4/04_philosophers.py).

As mentioned above, the solution using the waiter uses a central semaphore to control
access to the forks, while the handedness type implementation manages access
to the forks based on the properties of the philosophers, specifically their
handedness, which means that left-handed philosophers first pick up the left fork and then the right,
while right-handed philosophers do the opposite.

Solution with handedness type has some issues when it comes to starvation.
There might be a scenario, where one philosopher is consistently faster
than the others in acquiring the forks they need. This might lead to a point, 
where some philosophers never get to eat.

The other solution using the waiter contains signs of the starvation as well,
because some philosophers have to wait longer than others before they can eat,
which leads to a slightly unfair distribution of the resources. However, this
solution guarantees that all philosophers will eventually get to eat.