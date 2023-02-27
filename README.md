# Assignment 01 - The Bakery algorithm

---

[![Python 3.10.6](https://img.shields.io/badge/python-3.10.6-blue.svg)](https://www.python.org/downloads/release/python-3106/)



## Assignment description

The purpose of this assignment is to implement, demonstrate and describe the Bakery algorithm.

---

## Quick start
Before running the script, perform the following steps:
1. Set python interpreter version to 3.10.x
2. Install `fei.ppds` module (`pip install --upgrade fei.ppds`)
3. Set `NUM_THREADS` global variable with the desired number of threads

---

## Description of the Bakery algorithm

- The bakery algorithm is mutual exclusion algorithm that allows multiple threads
to access shared resources one at a time without interfering with each other.
This algorithm makes sure that only 1 thread can be executing code in the critical
section at a given time. The justification is described in the next point.


- The main idea of this algorithm is to take a number when entering a critical section.
Every thread is assigned a number that represents its order of arrival.
The thread with the lowest number is able to access the critical section.
In cases, where multiple threads have the same number, the thread with the lowest
thread id `tid` is given access. This makes sure that only 1 thread can be executing code
in the critical section at a given time, as well as that each thread
gets its turn to access the shared resources inside the critical section.


- Moreover, it makes sure that the thread that is being executed
outside the critical section does not prevent other threads from entering it
because the threads are waiting in a queue and only the first thread in the queue
can access the critical section.


- Additionally, it solves the condition that says "Threads cannot assume anything about
each other's timing when entering a critical region", because threads don't know anything
about other thread's assigned numbers, the thread is just waiting until it's
its turn to enter the critical section.


## Implementation of the Bakery algorithm

- My implementation consists of two functions: `lock` and `realease-lock`.
  - The `lock` function is called when a thread wants to enter a critical section.
  The thread acquires the lock by setting a flag in the `inside` variable and then
  assigning the highest number for the thread inside the `nums` variable. 
  The code implementation that takes care of setting the flag and assigning the highest number is shown below:
      ```python
      inside[tid] = True
      nums[tid] = max(nums) + 1
      inside[tid] = False
      ```
      After that, the thread is waiting for all other threads with a lower number or the same number and lower ID to 
  finish entering or have a lower number. The waiting is accomplished with the following code:
    ```python
    for j in range(NUM_THREADS):
        while inside[j]:
            continue
        while (nums[j] != 0 and
               nums[j] < nums[tid] or (nums[j] == nums[tid] and j < tid)):
            continue
    ```
  - The `realease-lock` function is called when the thread has finished the critical section. 
  The only purpose of this function is releasing the lock by clearing the number for the thread with 
  given `tid` in `nums`.

