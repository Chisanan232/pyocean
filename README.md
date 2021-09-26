# multirunnable

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A Python framework integrates building program which could run multiple tasks with different running strategy.

[Overview](#overview) | [Quickly Start](#quickly-start) | [Usage](#usage) | [Code Example](#code_example)
<hr>

## Overview

Python is a high level program language, but it's free to let anyone choose which running strategy you want to use (Parallel, Concurrent or Coroutine).
For example, if you want a concurrent feature, it should be like below:

```python
import threading


Thread_Number = 5

def function():
    print("This is function content ...")


if __name__ == '__main__':
    
    threads_list = [threading.Thread(target=function) for _ in range(Thread_Number)]
    for __thread in threads_list:
        __thread.start()
    
    for __thread in threads_list:
        __thread.join()
```

Or you also could implement threading.Thread run method:

```python
import threading


Thread_Number = 5

class SampleThread(threading.Thread):

    def run(self):
        print("This is function content which be run in the same time.")


if __name__ == '__main__':
    
    thread_list = [SampleThread() for _ in range(Thread_Number)]
    for __thread in thread_list:
        __thread.start()

    for __thread in thread_list:
        __thread.join()
```

No matter which way you choose to implement, it's Python, it's easy.

However, you may change the way to do something for testing, for efficiency, for resource concern or something else. 
You need to change to use parallel or coroutine but business logic has been done. The only way is refactoring code. 
It's not a problem if it has full-fledged testing code (TDD); if not, it must be an ordeal.

Package 'multirunnable' is a framework which could build a program with different running strategy by mode option. 
Currently, it has 4 options could use: Parallel, Concurrent, GreenThread and Asynchronous.

Here's an example to do the same thing with multirunnable:

```python
from multirunnable import SimpleExecutor, RunningMode
import random
import time

Workers_Number = 5


def function(index):
    print(f"This is function with index {index}")
    time.sleep(3)


if __name__ == '__main__':
    executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=Workers_Number)
    executor.run(function=function, args={"index": f"test_{random.randrange(1, 10)}"})
```

How about Parallel? I want to let it be more fast. 
Only one thing you need to do: change the mode.

```python
... # Any code is the same

executor = SimpleExecutor(mode=RunningMode.Parallel, executors=Workers_Number)

... # Any code is the same
```

Program still could run without any refactoring and doesn't need to modify anything. <br>
Want change to use other way to run? Change the Running Mode, that's all.


## Usage

This package classifies the runnable unit to be Executor and Pool.<br>
It also supports something operator with running multi-works simultaneously 
like Lock, Semaphore, Event, etc.

* Runnable Components
    * [Executor](#executor)
    * [Pool](#pool)
* Lock Features
    * [Lock](#lock)
    * [RLock](#rlock)
    * [Semaphore](#semaphore)
    * [Bounded Semaphore](#bounded-semaphore)
* Communication Features
    * [Event](#event)
    * [Condition](#condition)
* Queue
    * [Queue](#queue)
* Others
    * [Retry Mechanism](#retry_mechanism)

<br>

### Runnable Components
<hr>

* ### Executor

```python
from multirunnable import SimpleExecutor, RunningMode

executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
executor.run(function="Your target function", args="The arguments of target function")
```

* ### Pool

```python
from multirunnable import SimplePool, RunningMode

pool = SimplePool(mode=RunningMode.Parallel, pool_size=3, tasks_size=10)
pool.async_apply(function="Your target function", args="The arguments of target function")
```

<br>

### Lock Features
<hr>

* ### Lock

For Lock feature, the native library threading should call acquire and release to control how it runs like this:

```python
import threading
import time

... # Some logic

lock = threading.Lock()

print(f"Here is sample function running with lock.")
lock.acquire()
print(f"Process in lock and it will sleep 2 seconds.")
time.sleep(2)
print(f"Wake up process and release lock.")
lock.release()

... # Some logic

```

It also could use wih keyword "with":

```python
import threading
import time

... # Some logic

lock = threading.Lock()

print(f"Here is sample function running with lock.")
with lock:
    print(f"Process in lock and it will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")

... # Some logic

```

With pyocean, it requires everyone should wrap the logic which needs to be run with lock to be a function,
and you just add a decorator on it.

```python
from multirunnable.api import RunWith
import time


@RunWith.Lock
def lock_function():
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")

```

* ### RLock


* ### Semaphore

So is semaphore:

```python
from multirunnable.api import RunWith
import time


@RunWith.Semaphore
def lock_function():
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")

```

* ### Bounded Semaphore

```python
from multirunnable.api import RunWith
import time


@RunWith.Bounded_Semaphore
def lock_function():
    print("Running process in lock and will sleep 2 seconds.")
    time.sleep(2)
    print(f"Wake up process and release lock.")

```

<br>

### Communication Features
<hr>

* ### Event

```python
from multirunnable import SimpleExecutor, RunningMode, sleep
from multirunnable.api import EventOperator
from multirunnable.adapter import Event
import random



class WakeupProcess:

    __event_opt = EventOperator()

    def wake_other_process(self, *args):
        print(f"[WakeupProcess] It will keep producing something useless message.")
        while True:
            __sleep_time = random.randrange(1, 10)
            print(f"[WakeupProcess] It will sleep for {__sleep_time} seconds.")
            sleep(__sleep_time)
            self.__event_opt.set()


class SleepProcess:

    __event_opt = EventOperator()

    def go_sleep(self, *args):
        print(f"[SleepProcess] It detects the message which be produced by ProducerThread.")
        while True:
            sleep(1)
            print("[SleepProcess] ConsumerThread waiting ...")
            self.__event_opt.wait()
            print("[SleepProcess] ConsumerThread wait up.")
            self.__event_opt.clear()


if __name__ == '__main__':
    
    __wakeup_p = WakeupProcess()
    __sleep_p = SleepProcess()
  
    # Initialize Event object
    __event = Event()
    
    # # # # Run without arguments
    executor = SimpleExecutor(mode=RunningMode.Parallel, executors=3)
    executor.map_with_function(
        functions=[__wakeup_p.wake_other_process, __sleep_p.go_sleep],
        features=__event)
```

* ### Condition

```python
import multirunnable as mr

executor = mr.SimpleExecutor(mode=mr.RunningMode.Parallel, executors=3)
executor.run(function="Your target function", args="The arguments of target function")
```


<br>

### Queue
<hr>

* ### Queue

```python
import multirunnable as mr

executor = mr.SimpleExecutor(mode=mr.RunningMode.Parallel, executors=3)
executor.run(function="Your target function", args="The arguments of target function")
```


<br>

### Others
<hr>

* ### Retry Mechanism

```python
from multirunnable.api import retry, async_retry
import multirunnable


@retry
def target_fail_function(*args, **kwargs):
    print("It will raise exception after 3 seconds ...")
    multirunnable.sleep(3)
    raise Exception("Test for error")
```

Initialization 

```python
@target_fail_function.initialization
def initial():
    print("This is testing initialization")
```

Done 

```python
@target_fail_function.done_handling
def done(result):
    print("This is testing done process")
    print("Get something result: ", result)
```

Final 

```python
@target_fail_function.final_handling
def final():
    print("This is final process")
```

Error 

```python
@target_fail_function.error_handling
def error(error):
    print("This is error process")
    print("Get something error: ", error)
```

