from pyocean.framework.strategy import Globalize as RunningGlobalize
from pyocean.api.features_adapter import RunningMode, RunningStrategyAPI
from pyocean.persistence.database.connection import BaseConnection

from abc import ABC



class SingleConnection(BaseConnection, ABC):

    def initialize(self, mode: RunningMode, **kwargs) -> None:
        """
        Note:
            Deprecated the method about multiprocessing saving with one connection and change to use multiprocessing
            saving with pool size is 1 connection pool. The reason is database instance of connection pool is already,
            but for the locking situation, we should:
            lock acquire -> new instance -> execute something -> close instance -> lock release . and loop and loop until task finish.
            But connection pool would:
            new connection instances and save to pool -> semaphore acquire -> GET instance (not NEW) ->
            execute something -> release instance back to pool (not CLOSE instance) -> semaphore release

            Because only one connection instance, the every process take turns to using it to saving data. In other words,
            here doesn't need to initial anything about database connection.
        :param mode:
        :param kwargs:
        :return:
        """
        __running_feature_api = RunningStrategyAPI(mode=mode)
        # # Queue part (Limitation)
        __queue = __running_feature_api.queue(qtype=queue_type)
        RunningGlobalize.queue(queue=__queue)

        # # Lock part (Limitation)
        __lock = __running_feature_api.lock()
        RunningGlobalize.lock(lock=__lock)


    def get_one_connection(self) -> object:
        return self.connect_database()
