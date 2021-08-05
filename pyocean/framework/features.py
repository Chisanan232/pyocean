from pyocean.framework.exceptions import ParameterCannotBeEmpty
from pyocean.types import (
    OceanLock, OceanRLock,
    OceanSemaphore, OceanBoundedSemaphore,
    OceanEvent, OceanCondition,
    OceanQueue)
from pyocean.api.mode import FeatureMode

from abc import ABCMeta, abstractmethod
from enum import Enum



class BaseQueueType(Enum):

    pass



class BaseQueue(metaclass=ABCMeta):

    @abstractmethod
    def get_queue(self, qtype: BaseQueueType) -> OceanQueue:
        pass



class PosixThread(metaclass=ABCMeta):

    """
    POSIX (Portable Operating System Interface) Thread Specification

    POSIX.1  IEEE Std 1003.1 - 1988
        Process
        Signal: (IPC)
            Floating Point Exception
            Segmentation / Memory Violations
            Illegal Instructions
            Bus Errors
            Timers
        File and Directory Operations
        Pipes
        C library
        I/O Port Interface and Control
        Process Triggers

    POSIX.1b  IEEE Std 1003.1b - 1993
        Priority Scheduling
        Real-Time Signals
        Clocks and Timers
        Semaphores
        Message Passing
        Shared Memory
        Asynchronous and synchronous I/O
        Memory Locking Interface

    POSIX.1c  IEEE Std 1003.1c - 1995
        Thread Creation, Control, and Cleanup
        Thread Scheduling
        Thread Synchronization
        Signal Handling

    POSIX.2  IEEE Std 1003.2 - 1992
        Command Interface
        Utility Programs


    Refer:
    1. https://en.wikipedia.org/wiki/POSIX

    """
    pass



class PosixThreadLock(PosixThread):

    @abstractmethod
    def get_lock(self, **kwargs) -> OceanLock:
        """
        Description:
            Get Lock object.
        :return:
        """
        pass


    @abstractmethod
    def get_rlock(self, **kwargs) -> OceanRLock:
        """
        Description:
            Get RLock object.
        :return:
        """
        pass


    @abstractmethod
    def get_semaphore(self, value: int, **kwargs) -> OceanSemaphore:
        """
        Description:
            Get Semaphore object.
        :param value:
        :return:
        """
        pass


    @abstractmethod
    def get_bounded_semaphore(self, value: int, **kwargs) -> OceanBoundedSemaphore:
        """
        Description:
            Get Bounded Semaphore object.
        :param value:
        :return:
        """
        pass



class PosixThreadCommunication(PosixThread):

    @abstractmethod
    def get_event(self, *args, **kwargs) -> OceanEvent:
        """
        Description:
            Get Event object.
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def get_condition(self, *args, **kwargs) -> OceanCondition:
        """
        Description:
            Get Condition object.
        :param kwargs:
        :return:
        """
        pass



class BaseGlobalizeAPI(metaclass=ABCMeta):

    """
    Description:
        Globalize target object so that it could run, visible and be used between each different threads or processes, etc.
    """

    @staticmethod
    @abstractmethod
    def lock(lock) -> None:
        """
        Description:
            Globalize Lock object.
        :param lock:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def rlock(rlock) -> None:
        """
        Description:
            Globalize RLock object.
        :param rlock:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def event(event) -> None:
        """
        Description:
            Globalize Event object.
        :param event:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def condition(condition) -> None:
        """
        Description:
            Globalize Condition object.
        :param condition:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def semaphore(smp) -> None:
        """
        Description:
            Globalize Semaphore object.
        :param smp:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def bounded_semaphore(bsmp) -> None:
        """
        Description:
            Globalize Bounded Semaphore object.
        :param bsmp:
        :return:
        """
        pass


    @staticmethod
    @abstractmethod
    def queue(name, queue) -> None:
        """
        Description:
            Globalize Queue object.
        :param name:
        :param queue:
        :return:
        """
        pass



class FeatureUtils:

    @staticmethod
    def chk_obj(param: str, **kwargs):
        """
        Description:
            Ensure that the value of target parameter is not None.
        :param param:
        :param kwargs:
        :return:
        """

        __obj = kwargs.get(param, None)
        if __obj is None:
            raise ParameterCannotBeEmpty(param=param)
        return __obj



class BaseFeatureAdapterFactory(metaclass=ABCMeta):

    def __init__(self, mode: FeatureMode):
        self._mode = mode
        # # # # Should use lazy initialization design here.


    @abstractmethod
    def get_queue_adapter(self) -> BaseQueue:
        pass


    @abstractmethod
    def get_lock_adapter(self, **kwargs) -> PosixThreadLock:
        pass


    @abstractmethod
    def get_communication_adapter(self, **kwargs) -> PosixThreadCommunication:
        pass

