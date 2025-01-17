import os

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", True)

if DEVELOPMENT_MODE:
    # Import package multirunnable
    import pathlib
    import sys
    package_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
    sys.path.append(package_path)

# multirunnable package
from multirunnable import RunningMode, SimpleExecutor
from multirunnable.api import retry
import multirunnable



class ExampleTargetFunction:

    def target_function(self, *args, **kwargs) -> str:
        print("This is ExampleTargetFunction.target_function.")
        multirunnable.sleep(3)
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        # raise Exception("Test for error")
        return "You are 87."


    @retry.bounded_function
    def target_fail_function(self, *args, **kwargs) -> None:
        print("This is ExampleParallelClient.target_function.")
        print("This is target function args: ", args)
        print("This is target function kwargs: ", kwargs)
        print("It will raise exception after 3 seconds ...")
        multirunnable.sleep(3)
        raise Exception("Test for error")


    @target_fail_function.initialization
    def initial(self):
        print("This is testing initialization")


    @target_fail_function.done_handling
    def done(self, result):
        print("This is testing done process")
        print("Get something result: ", result)


    @target_fail_function.final_handling
    def final(self):
        print("This is final process")


    @target_fail_function.error_handling
    def error(self, error):
        print("This is error process")
        print("Get something error: ", error)



class ExampleExecutor:

    __Executor_Number = 0

    __example = ExampleTargetFunction()

    def __init__(self, executors: int):
        self.__Executor_Number = executors


    def main_run(self):
        # # # # Initial Executor object
        # __executor = SimpleExecutor(mode=RunningMode.Parallel, executors=self.__Executor_Number)
        # __executor = SimpleExecutor(mode=RunningMode.Concurrent, executors=self.__Executor_Number)
        __executor = SimpleExecutor(mode=RunningMode.GreenThread, executors=self.__Executor_Number)

        # # # # Generally running with 'start_new_worker'
        _args = ("index_1", "index_2.2")
        _kwargs = {"param_1": "index_1", "param_2": "index_2.2"}
        _workers_list = []
        for _ in range(5):
            _worker = __executor.start_new_worker(target=self.__example.target_function)
            # _worker = __executor.start_new_worker(target=self.__example.target_function, args=_args)
            # _worker = __executor.start_new_worker(self.__example.target_function, _args)
            # _worker = __executor.start_new_worker(self.__example.target_function, kwargs=_kwargs)
            _workers_list.append(_worker)
        __executor.close(_workers_list)

        # # # # Running the Executor
        # # # # Generally running
        # __executor.run(
        #     function=self.__example.target_function,
        #     args=("index_1", "index_2.2"))

        # # # # Generally running which will raise exception
        # __executor.run(
        #     function=self.__example.target_fail_function,
        #     args=("index_1", "index_2.2"))

        # # # # Map running which will raise exception
        # __executor.map(
        #     function=self.__example.target_function,
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

        # # # # Function version of map running which will raise exception
        # __executor.map_with_function(
        #     functions=[self.__example.target_function, self.__example.target_function],
        #     args_iter=[("index_1", "index_2.2"), ("index_3",), (1, 2, 3)])

        # # # # Get result
        __result = __executor.result()
        print("Result: ", __result)



if __name__ == '__main__':

    print("This is executor client: ")
    __executor_number = 3
    o_executor = ExampleExecutor(executors=__executor_number)
    o_executor.main_run()

