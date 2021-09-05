from pyocean.framework.task import BaseQueueTask as _BaseQueueTask
from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.adapter.collection import BaseList as _BaseList
from pyocean.framework.result import OceanResult as _OceanResult
from pyocean.mode import RunningMode as _RunningMode
import pyocean._utils as _utils

from abc import ABCMeta, abstractmethod
from typing import List, Optional, Union, Callable as CallableType, Iterable as IterableType
from types import MethodType, FunctionType
from collections import Iterable, Callable



class BaseExecutor(metaclass=ABCMeta):

    def __init__(self, mode: _RunningMode, executors: int):
        self._mode = mode
        self._executors_number = executors


    def __str__(self):
        return f"{self.__str__()} at {id(self.__class__)}"


    def __repr__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _utils.get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(" \
                               f"mode={self._mode}, " \
                               f"worker_num={self._executors_number})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    @abstractmethod
    def _initial_running_strategy(self) -> None:
        """
        Description:
            Initialize and instantiate RunningStrategy.
        :return:
        """
        pass


    @abstractmethod
    def start_new_worker(self, target: Callable, *args, **kwargs) -> None:
        pass


    @abstractmethod
    def run(self) -> None:
        pass


    @abstractmethod
    def async_run(self) -> None:
        pass


    @abstractmethod
    def map(self,
            function: CallableType,
            args_iter: IterableType = [],
            queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
            features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        """
        Description:
            Receive a parameters (the arguments of target function) List
            object and distribute them to
            1. Multiple Worker (Process, Thread, etc) by the length of list object.
            2. Multiple Worker by an option value like 'worker_num' or something else.
        :param function:
        :param args_iter:
        :param queue_tasks:
        :param features:
        :return:
        """
        pass


    @abstractmethod
    def async_map(self) -> None:
        pass


    @abstractmethod
    def map_with_function(self,
                          functions: IterableType[Callable],
                          args_iter: IterableType = [],
                          queue_tasks: Optional[Union[_BaseQueueTask, _BaseList]] = None,
                          features: Optional[Union[_BaseFeatureAdapterFactory, _BaseList]] = None) -> None:
        """
        Description:
            Receive a function (Callable object) List object and distribute
            them to
            1. Multiple Worker (Process, Thread, etc) by the length of list object.
            2. Multiple Worker by an option value like 'worker_num' or something else.
        :param functions:
        :param args_iter:
        :param queue_tasks:
        :param features:
        :return:
        """
        pass


    @abstractmethod
    def terminal(self) -> None:
        pass


    @abstractmethod
    def kill(self) -> None:
        pass


    @abstractmethod
    def result(self) -> List[_OceanResult]:
        pass

