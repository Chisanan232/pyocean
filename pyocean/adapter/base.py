from pyocean.framework.features import BaseFeatureAdapterFactory as _BaseFeatureAdapterFactory
from pyocean.framework.collection import BaseList as _BaseList
from pyocean.mode import FeatureMode as _FeatureMode
from pyocean.adapter.collection import FeatureList as _FeatureList
from pyocean.adapter._utils import _AsyncUtils

from abc import ABCMeta, ABC
from typing import Dict



class FeatureAdapterFactory(_BaseFeatureAdapterFactory, ABC):

    _Feature_List: _BaseList = None

    def __init__(self, mode: _FeatureMode, **kwargs):
        super(FeatureAdapterFactory, self).__init__(**kwargs)
        self._mode = mode
        if self._mode is _FeatureMode.Asynchronous:
            self._kwargs["loop"] = _AsyncUtils.check_event_loop(event_loop=kwargs.get("event_loop", None))


    def __str__(self):
        return f"<TargetObject object with {self._mode} mode at {id(self)}>"


    def __repr__(self):
        if self._mode is _FeatureMode.Asynchronous:
            __mode = self._mode
            __loop = self._kwargs["loop"]
            return f"<TargetObject(loop={__loop}) object with {__mode} mode at {id(self)}>"
        else:
            return self.__repr__()


    def __add__(self, other) -> _BaseList:
        if isinstance(other, _BaseList):
            other.append(self)
            self._Feature_List = other
        else:
            if self._Feature_List is None:
                self._Feature_List = _FeatureList()
            self._Feature_List.append(self)
            self._Feature_List.append(other)
        return self._Feature_List



class QueueAdapterFactory(_BaseFeatureAdapterFactory, ABC):

    def __init__(self, **kwargs):
        super(QueueAdapterFactory, self).__init__(**kwargs)

        self._name = kwargs.get("name", None)
        if self._name is None:
            raise Exception("The name of Queue object shouldn't be None object. "
                            "It's the key of each Queue object you create.")

        self._qtype = kwargs.get("qtype", None)
        if self._qtype is None:
            raise Exception("Queue type parameter shouldn't be None object. "
                            "It must to choice a type of Queue object with mapping strategy.")


    def __str__(self):
        return f"<Queue Object at {id(self)}>"


    def __repr__(self):
        return f"<Queue Object(name={self._name}, qtype={self._qtype}) ar {id(self)}>"

