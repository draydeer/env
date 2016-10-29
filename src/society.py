

import const
import gevent
import requests

from src.engine_module import EngineModule
from src.errors import InternalError
from random import sample


class Member:

    friends = []
    host = None
    port = const.PORT
    version = 0

    def __init__(self, host, friends=None, port=None, version=0):
        self.friends = friends if isinstance(friends, list) else []
        self.version = version

        if port is None:
            temp = host.split(':')

            if len(temp) > 1:
                self.host = temp[0]
                self.port = temp[1]
            else:
                self.host = host
                self.port = const.PORT
        else:
            self.port = port

    @property
    def key(self):
        return self.host + ':' + self.port

    def set_host(self, value):
        self.host = value

        return self

    def set_port(self, value):
        self.port = value

        return self


class Society(EngineModule):

    _announce_interval = 60
    _members = {}

    def _announce_loop(self):
        while self.alive:
            self.announce()

            gevent.sleep(self._announce_interval)

    def __init__(self, engine, members, announce_interval=60, port=const.PORT):
        EngineModule.__init__(self, engine)

        self._announce_interval = announce_interval if announce_interval >= 15 else 15
        self._members = {k: Member(k) for k in (members if isinstance(members, list) else [])}
        self._port = port

        gevent.spawn(self._announce_loop)

    @property
    def descriptor(self):
        return {
            'friends': [member for member in self._members.iterkeys()],
            'port': self._port,
            'version': self._engine.version,
        }

    def set_port(self, value):
        self._port = value

        return self

    def announce(self):
        patch = {}

        for k, v in self._members.iteritems():
            result = None

            try:
                result = requests.request(
                    'INFO',
                    k,
                    json=self.descriptor,
                    params={'clientId': self._engine.client_id}
                )

                if result.status_code == 200:
                    result = result.json()

                    patch[k] = Member(**(result if isinstance(result, dict) else {}))
                else:
                    result = None

                    self.logger.critical("Member left: %s (code: %s)" % (k, result.status_code))
            except requests.exceptions.ConnectionError:
                self.logger.critical('Member left: ' + k + ' (connection timeout)')

            if result is None:
                patch[k] = None

                self.event('on_society_member_leave', k)

        for k, v in patch.iteritems():
            if v is None:
                self._members.pop(k)
            else:
                self._members[k] = v

        # if amount of members is less then minimal try to involve
        if len(self._members) < const.SOCIETY_MIN_KNOWN:
            self.logger.info('On look for new members ...')

            for member in self._members.itervalues():

                # look for unknown member among his friends
                for friend in member.friends:
                    if friend not in self._members:
                        self.enter(friend)

                    if len(self._members) >= const.SOCIETY_MIN_KNOWN:
                        break

        self.event('on_society_populate')

        return self

    def enter(self, k, descriptor=None):
        if isinstance(descriptor, Member):
            self._members[k] = descriptor
        else:
            self._members[k] = Member(**(descriptor if isinstance(descriptor, dict) else {}))

        return self

    def enter_host_scheme(self, host, descriptor=None, scheme='http'):
        member = Member(**(descriptor if isinstance(descriptor, dict) else {})).set_host(scheme + '://' + host)

        return self.enter(scheme + '://' + member.key, member)

    def has(self, k):
        return k in self._members

    def leave(self, k):
        self._members.pop(k)

        return self

    def select(self):
        if len(self._members) == 0:
            raise InternalError('No members to select.')

        k = sample(self._members, 1)[0]

        return k
