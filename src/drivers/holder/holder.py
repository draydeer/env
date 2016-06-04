

from config.active import config as active_config
from ..consul import Consul
from ..env import Env
from ..etcd import Etcd
from ..file_ini import FileIni
from ..file_json import FileJson
from ..file_yaml import FileYaml
from ..file_txt import FileTxt
from ..memory import Memory
from ..mongo import Mongo
from ..mongo_replica_set import MongoResplicaSet
from ..redis import Redis
from ..sql import Sql
from ..ssdb import Ssdb
from src.errors import NotExistsError


class Holder(object):

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
    def get(k):
        value = getattr(Holder, k)

        return value

    @staticmethod
    def set(k, v):
        setattr(Holder, k, v)

        return v

    @staticmethod
    def has(k):
        value = hasattr(Holder, k)

        return value

    @staticmethod
    def get_default(engine):
        value = Holder.req(active_config.g('default.driver', 'env'), engine)

        return value

    @staticmethod
    def req(alias, engine, config=None):
        if Holder.has(alias):
            return Holder.get(alias)

        if config is None:
            config = active_config['drivers'][alias] if alias in active_config['drivers'] else None

        if config and config.get('initiator', alias) in Holder.initiators:
            return Holder.set(alias, Holder.initiators[config.get('initiator', alias)](engine, config))

        raise NotExistsError("Driver not exists: %s" % alias)
