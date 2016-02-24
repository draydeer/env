

from pymongo\
    import MongoClient
from lib.driver\
    import Driver, Value
from lib.errors\
    import NotExistsError


class Mongo(Driver):

    def _on_init(
        self
    ):
        self._client = MongoClient(self._config.get('host', 'localhost:27017'))[str(self._config.get('db', 'env'))]

        self._client.authenticate(str(self._config.user), password=str(self._config.password))

    def g(
        self, k
    ):
        result = self._client.env_conf.find_one({'k': k})

        if result is not None:
            if self._config.rawValue:
                return Value(result)
            else:
                return Value(result.get('v'), result.get('t'))

        raise NotExistsError(k)
