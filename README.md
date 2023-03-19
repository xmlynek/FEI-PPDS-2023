# Assignment 04 - The modified dining savages problem


[![Python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue.svg)](https://www.python.org/downloads/release/python-3106/)

## Table of contents
- [Quick start](#quick-start)
- [Assignment description](#assignment-description)
- [Implementation with a single cook](#implementation-with-a-single-cook)
- [Sample output](#sample-output)


## Quick start
Before running the script, perform the following steps:
1. Set python interpreter version to 3.10.x.
2. Install `fei.ppds` module (`pip install --upgrade fei.ppds`).
3. Set the number of savages in `NUM_SAVAGES` variable to your desired value. Default value is 5.
4. Set the number of portions inside the pot in `POT_SIZE` variable to your desired value. Default value is 3.

## Assignment description
The purpose of this assignment is to implement the modified dining savages problem.

![image illustration of the savages](https://user-images.githubusercontent.com/70724986/226110032-22e5439e-cf33-418a-a9fb-04973bd86331.png)

The modified dining savages problem consists portions of food inside
the pot, savages, and cooks, which follow certain rules:
- The savages start feasting **only** when they are all together. 
- The savages take the portion out of the pot one at a time, until it's not empty.
- When the savage wants to eat but the pot is empty, he wakes up the cooks.
- The savages wait while the cooks are cooking.
- Each cook makes only 1 portion at a time.
- When the pot is full again, the savages continue feasting.

This whole process repeats continuously.


## Implementation with a single cook
This implementation consists of `5` savages, `3` portions inside the pot, stored
in `NUM_SAVAGES` and `POT_SIZE` variables. Given implementation uses only `1` cook.

The first important synchronization mechanism is used right at the beginning
of the `savage` function. This mechanism is called ***barrier*** and the 
following code is described right below.

```python
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
```

***Barrier*** ensures that all the savages start feasting once they are all gathered.

> Barrier is a synchronization mechanism that allows multiple threads or processes to coordinate and wait for each other to reach a specific point in their execution before proceeding further.
> Once all threads have arrived at the barrier, they can then proceed past the barrier and continue their execution in parallel. [^1]

---

Once the savages are gathered, they start taking portions and eating. Since the pot 
contains only `3` portions of the meal, it is obvious that some savages will encounter 
a situation where the pot is empty. At this point, he wakes up the cook, and all the savages
wait until the cook is finished and the pot is full.

Number of available portions is stored in shared variable `servings`. Since it is
shared variable and multiple threads are trying to manipulate its value,
we need to provide integrity. To provide integrity, we need to use
***mutual exclusion*** `servings_mutex`.

> Mutex (short for mutual exclusion) is a synchronization mechanism that allows multiple threads to coordinate and safely access shared resources or critical sections of code. [^2]

```python
shared.servings_mutex.lock()
print(f"The savage {i} is taking a portion")
if shared.servings == 0:
    print(f"THE POT IS EMPTY. Wake up the cook!")
    shared.empty_pot.signal()
    shared.full_pot.wait()
shared.servings -= 1
print(
    f"The savage {i} took a portion. Portions left: {shared.servings}"
)
shared.servings_mutex.unlock()
```

---

When the cook wakes up, he cooks and adds portions to `servings` one at a time
until the pot is full. Pay attention to the fact that we don't have to
use mutual exclusion `servings_mutex` in `cook` function to provide integrity while
having only 1 cook because it's already provided. 

See the previous snippet of the code. At first, we enforce mutex `servings_mutex` by 
calling the `lock` method, and after waking up the cook, the thread of the savage is
waiting until the cook ***signalizes*** that the pot is full and all other savage threads
are waiting until this savage takes the portion. 

```python
shared.empty_pot.wait()
print(f"The cook starts cooking!")
for i in range(0, POT_SIZE):
    shared.servings += 1
    sleep(0.1)
    print(f"Cook adds a portion to the pot. "
          f"Total portions: {shared.servings}/{POT_SIZE}")

print(f"The pot is full again!")
shared.full_pot.signal()
```

The code snippet above represents the activity of the cook. The cook **waits**
for the **signal** from the savage that the pot is empty, then he prepares
the food and adds the portions to the pot one at a time. When the pot is full,
the cook ***signalizes*** that the pot is full again, which means, that the savages can
continue to feast. Signalization is represented as a `Semaphore`.

> Semaphores are a signalization mechanism that coordinate access to shared resources between multiple threads or processes. They maintain a count of the number of available resources, allowing threads or processes to wait or signal based on the current count. Semaphores provide a powerful way to achieve synchronization and avoid issues such as race conditions and priority inversion. [^3]

## Sample output
This is the sample output for 5 savages, 3 servings inside the pot, and the single cook.
Note that your output may be different.
```
Savage 0 joined the party. Savages waiting: 1
Savage 1 joined the party. Savages waiting: 2
Savage 2 joined the party. Savages waiting: 3
Savage 3 joined the party. Savages waiting: 4
Savage 4 joined the party. Savages waiting: 5
ALL OF THE SAVAGES ARE TOGETHER. LET'S FEAST!
The savage 4 is taking a portion
The savage 4 took a portion. Portions left: 2
Savage 4 is feasting!
The savage 2 is taking a portion
The savage 2 took a portion. Portions left: 1
Savage 2 is feasting!
The savage 0 is taking a portion
The savage 0 took a portion. Portions left: 0
Savage 0 is feasting!
The savage 3 is taking a portion
THE POT IS EMPTY. Wake up the cook!
The cook starts cooking!
Cook adds a portion to the pot. Total portions: 1/3
Cook adds a portion to the pot. Total portions: 2/3
Savage 2 joined the party. Savages waiting: 1
Savage 4 joined the party. Savages waiting: 2
Savage 0 joined the party. Savages waiting: 3
Cook adds a portion to the pot. Total portions: 3/3
The pot is full again!
The savage 3 took a portion. Portions left: 2
Savage 3 is feasting!
The savage 1 is taking a portion
The savage 1 took a portion. Portions left: 1
Savage 1 is feasting!
Savage 1 joined the party. Savages waiting: 4
Savage 3 joined the party. Savages waiting: 5
ALL OF THE SAVAGES ARE TOGETHER. LET'S FEAST!
```

[^1]: https://medium.com/@jaydesai36/barrier-synchronization-in-threads-3c56f947047
[^2]: https://www.techopedia.com/definition/25629/mutual-exclusion-mutex
[^3]: https://en.wikipedia.org/wiki/Semaphore_(programming)
