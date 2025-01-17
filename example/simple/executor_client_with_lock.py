import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable import RunningMode, SimpleExecutor, sleep, async_sleep
from multirunnable.api import retry, async_retry, RunWith, AsyncRunWith
from multirunnable.factory import LockFactory



class ExampleTargetFunction:

    def target_function(self, *args, **kwargs) -> str:
        print("This is ExampleTargetFunction.target_function.")
        "multi"
        sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        self.lock_function()
        # raise Exception("Test for error")
        return "You are 87."


    @retry.bounded_function
    @RunWith.Lock
    def lock_function(self):
        print("This is testing process with Lock and sleep for 3 seconds.")
        sleep(3)
        print("Wake up and raise an exception ...")
        raise RuntimeError("Test for error")


    @lock_function.initialization
    def initial(self):
        print("This is testing initialization")


    @lock_function.done_handling
    def done(self, result):
        print("This is testing done process")
        print("Get something result: ", result)


    @lock_function.final_handling
    def final(self):
        print("This is final process")


    @lock_function.error_handling
    def error(self, error):
        print("This is error process")
        print("Get something error: ", error)



class ExampleAsyncTargetFunction:

    async def async_target_function(self, *args, **kwargs) -> str:
        print("This is ExampleTargetFunction.async_target_function.")
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        # time.sleep(3)
        # await asyncio.sleep(3)
        await self.lock_function()
        # raise Exception("Test for error")
        return "You are 87."


    @async_retry.bounded_function
    @AsyncRunWith.Lock
    async def lock_function(self):
        print("This is testing process with Lock and sleep for 3 seconds.")
        await async_sleep(3)
        print("Wake up and raise an exception ...")
        raise RuntimeError("Test for error")


    @lock_function.initialization
    async def initial(self):
        print("This is testing initialization")


    @lock_function.done_handling
    async def done(self, result):
        print("This is testing done process")
        print("Get something result: ", result)


    @lock_function.final_handling
    async def final(self):
        print("This is final process")


    @lock_function.error_handling
    async def error(self, error):
        print("This is error process")
        print("Get something error: ", error)



class ExampleExecutor:

    __Executor_Number = 0

    __example = ExampleTargetFunction()
    __async_example = ExampleAsyncTargetFunction()

    def __init__(self, executors: int):
        self.__Executor_Number = executors


    def main_run(self):
        # Initialize Lock object
        __lock = LockFactory()

        # # # # Initial Executor object
        __executor = SimpleExecutor(mode=RunningMode.Parallel, executors=self.__Executor_Number)
        # __executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=self.__Executor_Number)
        # __executor = SimpleExecutor(mode=RunningMode.GreenThread, executors=self.__Executor_Number)
        # __executor = SimpleExecutor(mode=RunningMode.Asynchronous, executors=self.__Executor_Number)

        # # # # Running the Executor
        # # # # Generally running
        __executor.run(
            function=self.__example.target_function,
            args=("index_1", "index_2.2"),
            features=__lock)

        # # # # Asynchronous version of generally running
        # __executor.run(
        #     function=self.__async_example.async_target_function,
        #     args=("index_1", "index_2.2"),
        #     features=__lock)

        # # # # Asynchronous version of generally running which will raise exception
        # __executor.run(
        #     function=self.__async_example.async_target_function,
        #     args=("index_1", "index_2.2"),
        #     features=__lock)

        # # # # Map running which will raise exception
        # __executor.map(
        #     function=self.__example.target_function,
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)],
        #     features=__lock)

        # # # # Function version of map running which will raise exception
        # __executor.map_with_function(
        #     functions=[self.__example.target_function, self.__example.target_function],
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)],
        #     features=__lock)

        # # # # Get result
        __result = __executor.result()
        print("Result: ", __result)



if __name__ == '__main__':

    print("This is executor client: ")
    __executor_number = 3
    o_executor = ExampleExecutor(executors=__executor_number)
    o_executor.main_run()

