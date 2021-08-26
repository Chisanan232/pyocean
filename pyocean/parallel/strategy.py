from pyocean.framework.task import BaseQueueTask as _BaseQueueTask
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.collection import BaseList as _BaseList
from pyocean.framework.strategy import RunnableStrategy as _RunnableStrategy, Resultable as _Resultable
from pyocean.framework.result import ResultState as _ResultState
from pyocean.parallel.result import ParallelResult as _ParallelResult
from pyocean.persistence.interface import OceanPersistence as _OceanPersistence
from pyocean.mode import FeatureMode as _FeatureMode

from abc import abstractmethod
from typing import List, Dict, Iterable, Union, Callable, Optional, cast
from multiprocessing import Manager
from multiprocessing.pool import Pool, AsyncResult, ApplyResult
from multiprocessing.managers import Namespace



class ParallelStrategy(_RunnableStrategy):

    _Strategy_Feature_Mode = _FeatureMode.Parallel
    _Manager: Manager = None
    _Namespace_Object: Namespace = None
    _Processors_Pool: Pool = None
    _Processors_Running_Result: List[Dict[str, Union[AsyncResult, bool]]] = {}

    def __init__(self, workers_num: int,
                 persistence_strategy: _OceanPersistence = None, **kwargs):
        """
        Description:
            Converting the object to multiprocessing.manager.Namespace type object at initial state.
        :param workers_num:
        :param db_connection_pool_size:
        :param persistence_strategy:
        """
        super().__init__(workers_num=workers_num, persistence_strategy=persistence_strategy, **kwargs)
        self.__init_namespace_obj()
        if persistence_strategy is not None:
            namespace_persistence_strategy = cast(_OceanPersistence, self.namespacing_obj(obj=persistence_strategy))
            super().__init__(
                workers_num=workers_num,
                db_connection_pool_size=self.db_connection_number,
                persistence_strategy=namespace_persistence_strategy)
        self._Processors_Running_Result = self._Manager.list()


    def __init_namespace_obj(self) -> None:
        self._Manager = Manager()
        self._Namespace_Object = self._Manager.Namespace()


    def activate_workers(self, workers_list: List[Union[ApplyResult, AsyncResult]]) -> None:
        # # Method 1.
        for worker in workers_list:
            self.activate_worker(worker=worker)

        # # Method 2.
        # with workers_list as worker:
        #     self.activate_worker(worker=worker)


    @abstractmethod
    def activate_worker(self, worker: Union[ApplyResult, AsyncResult]) -> None:
        """
        Description:
            Each one thread or process running task implementation.
        :param worker:
        :return:
        """
        pass


    def namespacing_obj(self, obj: object) -> object:
        setattr(self._Namespace_Object, repr(obj), obj)
        return getattr(self._Namespace_Object, repr(obj))



class MultiProcessingStrategy(ParallelStrategy, _Resultable):

    def initialization(self,
                       queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                       features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None,
                       *args, **kwargs) -> None:
        super(MultiProcessingStrategy, self).initialization(queue_tasks=queue_tasks, features=features, *args, **kwargs)

        # # Persistence
        if self._persistence_strategy is not None:
            self._persistence_strategy.initialize(db_conn_num=self.db_connection_number)

        # Initialize and build the Processes Pool.
        __pool_initializer: Callable = kwargs.get("pool_initializer", None)
        __pool_initargs: Iterable = kwargs.get("pool_initargs", None)
        self._Processors_Pool = Pool(processes=self.workers_number, initializer=__pool_initializer, initargs=__pool_initargs)


    def build_workers(self,
                      function: Callable,
                      callback: Callable = None,
                      error_callback: Callable = None,
                      *args, **kwargs) -> List[Union[AsyncResult, ApplyResult]]:
        return [self._Processors_Pool.apply_async(func=function,
                                                  args=args,
                                                  kwds=kwargs,
                                                  callback=callback,
                                                  error_callback=error_callback)
                for _ in range(self.workers_number)]


    def activate_worker(self, worker: Union[AsyncResult, ApplyResult]) -> None:
        __process_running_result = worker.get()
        __process_run_successful = worker.successful()

        # Save Running result state and Running result value as dict
        process_result = {"successful": __process_run_successful, "result": __process_running_result}
        # Saving value into list
        self._Processors_Running_Result.append(process_result)


    def close(self) -> None:
        self._Processors_Pool.close()
        self._Processors_Pool.join()


    def get_result(self) -> List[_ParallelResult]:
        __parallel_result = self._result_handling()
        return __parallel_result


    def _result_handling(self) -> List[_ParallelResult]:
        __parallel_results = []
        for __result in self._Processors_Running_Result:
            __parallel_result = _ParallelResult()

            __process_successful = __result.get("successful")
            if __process_successful is True:
                __parallel_result.state = _ResultState.SUCCESS.value
            else:
                __parallel_result.state = _ResultState.FAIL.value

            __process_result = __result.get("result")
            __parallel_result.data = __process_result

            __parallel_results.append(__parallel_result)

        return __parallel_results

