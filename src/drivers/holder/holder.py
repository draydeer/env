

from config.active import config as active_config
from src.drivers.consul import Consul
from src.drivers.env import Env
from src.drivers.etcd import Etcd
from src.drivers.file_ini import FileIni
from src.drivers.file_json import FileJson
from src.drivers.file_yaml import FileYaml
from src.drivers.file_txt import FileTxt
from src.drivers.memory import Memory
from src.drivers.mongo import Mongo
from src.drivers.mongo_replica_set import MongoResplicaSet
from src.errors import NotExistsError
from src.drivers.redis import Redis
from src.drivers.sql import Sql
from src.drivers.ssdb import Ssdb


class Holder:

    initiators = {
        'consul': Consul,
        'env': Env,
        'etcd': Etcd,
        'fileIni': FileIni,
        'fileJson': FileJson,
        'fileYaml': FileYaml,
        'fileTxt': FileTxt,
        'memory': Memory,
        'mongo': Mongo,
        'mongoReplicaSet': MongoResplicaSet,
        'redis': Redis,
        'sql': Sql,
        'ssdb': Ssdb
    }

    @staticmethod
    def get(
        k
    ):
        value = getattr(Holder, k)

        return value

    @staticmethod
    def set(
        k, v
    ):
        setattr(Holder, k, v)

        return v

    @staticmethod
    def has(
        k
    ):
        value = hasattr(Holder, k)

        return value

    @staticmethod
    def get_default(
        engine
    ):
        value = Holder.req(active_config.g('default.driver', 'env'), engine)

        return value

    @staticmethod
    def req(
        alias, engine, config=None
    ):
        if Holder.has(alias):
            return Holder.get(alias)

        if config is None:
            config = active_config['drivers'][alias] if alias in active_config['drivers'] else None

        if config and config.get('initiator', alias) in Holder.initiators:
            return Holder.set(alias, Holder.initiators[config.get('initiator', alias)](engine, config))

        raise NotExistsError('driver not exists: ' + alias)
