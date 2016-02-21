

from config.active\
    import config as active_config
from lib.drivers.consul\
    import Consul
from lib.drivers.env\
    import Env
from lib.drivers.etcd\
    import Etcd
from lib.drivers.file_ini\
    import FileIni
from lib.drivers.file_json\
    import FileJson
from lib.drivers.file_yaml\
    import FileYaml
from lib.drivers.file_txt\
    import FileTxt
from lib.drivers.memory\
    import Memory
from lib.drivers.mongo\
    import Mongo
from lib.drivers.mongo_replica_set\
    import MongoResplicaSet
from lib.errors\
    import NotExistsError
from lib.drivers.redis\
    import Redis
from lib.drivers.sql\
    import Sql
from lib.drivers.ssdb\
    import Ssdb


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

    ):
        value = Holder.req(active_config.g('default.driver', 'env'))

        return value

    @staticmethod
    def req(
        alias, config=None
    ):
        if Holder.has(alias):
            return Holder.get(alias)

        if config is None:
            config = active_config['drivers'][alias] if alias in active_config['drivers'] else None

        if config and config.get('initiator', alias) in Holder.initiators:
            return Holder.set(alias, Holder.initiators[config.get('initiator', alias)](config))

        raise NotExistsError('driver not exists: ' + alias)
