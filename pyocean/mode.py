from enum import Enum


_Package: str = "pyocean"
_Parallel_Package: str = ".parallel."
_Concurrent_Package: str = ".concurrent."
_Coroutine_Package: str = ".coroutine."
_Feature_Package: str = "features"
_Strategy_Package: str = "strategy"


# # Feature class
_Parallel_Feature_Class: str = "Process"
_Concurrent_Feature_Class: str = "Thread"
_Greenlet_Feature_Class: str = "Greenlet"
_Async_Feature_Class: str = "Async"

_Queue_Class: str = "Queue"
_Lock_Class: str = "Lock"
_Communication_Class: str = "Communication"


# # Strategy class
_Parallel_Common_Class: str = "MultiProcessing"
_Process_Pool_Common_Class: str = "ProcessPool"
_Processes_Common_Class: str = "MultiProcesses"
_Concurrent_Common_Class: str = "MultiThreading"
_Greenlet_Common_Class: str = "MultiGreenlet"
_Async_Common_Class: str = "Asynchronous"

_Strategy_Class: str = "Strategy"
_Map_Strategy_Class: str = "MapStrategy"



class FeatureMode(Enum):

    Parallel = {
        "module": _Parallel_Package + _Feature_Package,
        "queue": _Parallel_Feature_Class + _Queue_Class,
        "lock": _Parallel_Feature_Class + _Lock_Class,
        "communication": _Parallel_Feature_Class + _Communication_Class
    }

    Concurrent = {
        "module": _Concurrent_Package + _Feature_Package,
        "queue": _Concurrent_Feature_Class + _Queue_Class,
        "lock": _Concurrent_Feature_Class + _Lock_Class,
        "communication": _Concurrent_Feature_Class + _Communication_Class
    }

    Greenlet = {
        "module": _Coroutine_Package + _Feature_Package,
        "queue": _Greenlet_Feature_Class + _Queue_Class,
        "lock": _Greenlet_Feature_Class + _Lock_Class,
        "communication": _Greenlet_Feature_Class + _Communication_Class
    }

    Asynchronous = {
        "module": _Coroutine_Package + _Feature_Package,
        "queue": _Async_Feature_Class + _Queue_Class,
        "lock": _Async_Feature_Class + _Lock_Class,
        "communication": _Async_Feature_Class + _Communication_Class
    }



class RunningMode(Enum):

    Parallel = {
        "strategy_module": _Parallel_Package + _Strategy_Package,
        "strategy": _Process_Pool_Common_Class + _Strategy_Class,
        "map_strategy": _Parallel_Common_Class + _Map_Strategy_Class
    }

    MultiProcesses = {
        "strategy_module": _Parallel_Package + _Strategy_Package,
        "strategy": _Processes_Common_Class + _Strategy_Class,
        "map_strategy": _Parallel_Common_Class + _Map_Strategy_Class
    }

    Concurrent = {
        "strategy_module": _Concurrent_Package + _Strategy_Package,
        "strategy": _Concurrent_Common_Class + _Strategy_Class,
        "map_strategy": _Concurrent_Common_Class + _Map_Strategy_Class
    }

    Greenlet = {
        "strategy_module": _Coroutine_Package + _Strategy_Package,
        "strategy": _Greenlet_Common_Class + _Strategy_Class,
        "map_strategy": _Greenlet_Common_Class + _Map_Strategy_Class
    }

    Asynchronous = {
        "strategy_module": _Coroutine_Package + _Strategy_Package,
        "strategy": _Async_Common_Class + _Strategy_Class,
        "map_strategy": _Async_Common_Class + _Map_Strategy_Class
    }

