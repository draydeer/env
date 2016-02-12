

from config.active\
    import config as active_config
from lib.drivers.consul\
    import Consul
from lib.drivers.env\
    import Env
from lib.drivers.mongo\
    import Mongo
from lib.drivers.mongo_replica_set\
    import MongoResplicaSet
from lib.errors\
    import NotExistsError


class Factory:

    initiators = {
        'consul': Consul,
        'env': Env,
        'mongo': Mongo,
        'mongoReplicaSet': MongoResplicaSet,
    }

    @staticmethod
    def get(
        k
    ):
        value = getattr(Factory, k)

        return value

    @staticmethod
    def set(
        k, v
    ):
        setattr(Factory, k, v)

        return v

    @staticmethod
    def has(
        k
    ):
        value = hasattr(Factory, k)

        return value

    @staticmethod
    def get_default(

    ):
        value = Factory.produce(active_config.get('default', 'env'))

        return value

    @staticmethod
    def produce(
        alias, config=None
    ):
        if Factory.has(alias):
            return Factory.get(alias)

        if config is None:
            config = active_config['drivers'][alias] if alias in active_config['drivers'] else None

        if config and config.get('initiator', alias) in Factory.initiators:
            return Factory.set(alias, Factory.initiators[config.get('initiator', alias)](config))

        raise NotExistsError('driver not exists: ' + alias)
