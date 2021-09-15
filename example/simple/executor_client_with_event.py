# Import package pyocean
import pathlib
import random
import time
import sys

package_pyocean_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(package_pyocean_path)

# pyocean package
from pyocean import SimpleExecutor, RunningMode
from pyocean.api import EventOperator
from pyocean.adapter import Event
import asyncio
import gevent



class WakeupProcess:

    __event_opt = EventOperator()

    def wake_other_process(self, *args):
        print("[WakeupProcess] args: ", args)
        print(f"[WakeupProcess] It will keep producing something useless message.")
        while True:
            __sleep_time = random.randrange(1, 10)
            print(f"[WakeupProcess] It will sleep for {__sleep_time} seconds.")
            # time.sleep(__sleep_time)
            gevent.sleep(__sleep_time)
            self.__event_opt.set()


    async def async_wake_other_process(self, *args):
        print("[WakeupProcess] args: ", args)
        print(f"[WakeupProcess] It will keep producing something useless message.")
        while True:
            __sleep_time = random.randrange(1, 10)
            print(f"[WakeupProcess] It will sleep for {__sleep_time} seconds.")
            await asyncio.sleep(__sleep_time)
            self.__event_opt.set()



class SleepProcess:

    __event_opt = EventOperator()

    def go_sleep(self, *args):
        print("[SleepProcess] args: ", args)
        print(f"[SleepProcess] It detects the message which be produced by ProducerThread.")
        while True:
            # time.sleep(1)
            gevent.sleep(1)
            print("[SleepProcess] ConsumerThread waiting ...")
            self.__event_opt.wait()
            print("[SleepProcess] ConsumerThread wait up.")
            self.__event_opt.clear()


    async def async_go_sleep(self, *args):
        print("[SleepProcess] args: ", args)
        print(f"[SleepProcess] It detects the message which be produced by ProducerThread.")
        while True:
            await asyncio.sleep(1)
            print("[SleepProcess] ConsumerThread waiting ...")
            await self.__event_opt.wait()
            print("[SleepProcess] ConsumerThread wait up.")
            self.__event_opt.clear()



class ExampleOceanSystem:

    __Process_Number = 1

    __wakeup_p = WakeupProcess()
    __sleep_p = SleepProcess()

    @classmethod
    def main_run(cls):
        # Initialize Event object
        __event = Event()

        # # # # Initialize and run ocean-simple-executor
        # __exe = SimpleExecutor(mode=RunningMode.Parallel, executors=cls.__Process_Number)
        # __exe = SimpleExecutor(mode=RunningMode.Concurrent, executors=cls.__Process_Number)
        # __exe = SimpleExecutor(mode=RunningMode.GreenThread, executors=cls.__Process_Number)
        __exe = SimpleExecutor(mode=RunningMode.Asynchronous, executors=cls.__Process_Number)

        # # # # Run without arguments
        # __exe.map_with_function(
        #     functions=[cls.__wakeup_p.wake_other_process, cls.__sleep_p.go_sleep],
        #     features=__event)

        # # # # Asynchronous version of running without arguments
        __exe.map_with_function(
            functions=[cls.__wakeup_p.async_wake_other_process, cls.__sleep_p.async_go_sleep],
            features=__event)

        # # # # Run with arguments
        # __exe.map_with_function(
        #     functions=[cls.__wakeup_p.wake_other_process, cls.__sleep_p.go_sleep],
        #     args_iter=(("index_1", ), ("index_2",)),
        #     features=__event)



if __name__ == '__main__':

    print("[MainProcess] This is system client: ")
    system = ExampleOceanSystem()
    system.main_run()
    print("[MainProcess] Finish. ")

