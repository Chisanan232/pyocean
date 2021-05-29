from pyocean.framework.strategy import InitializeUtils, RunnableStrategy
from pyocean.api import RunningMode
from pyocean.concurrent.features import MultiThreadingQueueType
from pyocean.concurrent.exceptions import ThreadsListIsEmptyError

from abc import ABCMeta, abstractmethod, ABC
from typing import List, Tuple, Dict, Iterable, Union, Callable
from multiprocessing.pool import ApplyResult
from threading import Thread



class ConcurrentStrategy(RunnableStrategy, ABC):

    _Running_Mode: RunningMode = RunningMode.MultiThreading
    _Threads_List: List[Thread] = []
    _Threads_Running_Result: Dict[str, Dict[str, Union[object, bool]]] = {}

    def activate_multi_workers(self, workers_list: List[Union[Thread, ApplyResult]]) -> None:
        # # Method 1.
        for worker in workers_list:
            self.activate_worker(worker=worker)

        # # Method 2.
        # with workers_list as worker:
        #     self.activate_worker(worker=worker)


    @abstractmethod
    def activate_worker(self, worker: Union[Thread, ApplyResult]) -> None:
        """
        Description:
            Each one thread or process running task implementation.
        :param worker:
        :return:
        """
        pass



class MultiThreadingStrategy(ConcurrentStrategy):

    def init_multi_working(self, tasks: Iterable, *args, **kwargs) -> None:
        __init_utils = InitializeUtils(running_mode=self._Running_Mode, persistence=self._persistence_strategy)
        # Initialize and assign task queue object.
        __init_utils.initialize_queue(tasks=tasks, qtype=MultiThreadingQueueType.Queue)
        # Initialize parameter and object with different scenario.
        __init_utils.initialize_persistence(db_conn_instances_num=self.db_connection_instances_number)


    def build_multi_workers(self, function: Callable, args: Tuple = (), kwargs: Dict = {}) -> List[Union[Thread, ApplyResult]]:
        self._Threads_List = [Thread(target=function, args=args, kwargs=kwargs) for _ in range(self.threads_number)]
        return self._Threads_List


    def activate_worker(self, worker: Union[Thread, ApplyResult]) -> None:
        worker.start()


    def end_multi_working(self) -> None:
        if self._Threads_List:
            for threed_index in range(self.threads_number):
                self._Threads_List[threed_index].join()
        else:
            raise ThreadsListIsEmptyError
