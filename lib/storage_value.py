

import time


from lib.driver\
    import Value
from lib.errors\
    import NotExistsError


class StorageValue:

    decryption_key = None
    driver = None
    last_sync = 0
    k = None
    sync_each = 60
    type = None
    v = Value()

    def __init__(
        self, k, driver, timer, decryption_key=None, sync_each=60
    ):
        self.decryption_key = decryption_key
        self.driver = driver
        self.k = k
        self.sync_each = sync_each

        if int(sync_each) > 0:
            timer.attach(sync_each, k)

        self.invalidate(True)

    def g(
        self, k, d=None
    ):
        r = self.v.v

        for x in k.split('.') if isinstance(k, str) else k:
            if isinstance(r, dict):
                r = r.get(x)

                continue

            if isinstance(r, list):
                r = r[int(x)] if x.isdigit() and len(r) > int(x) else None

                continue

            return d

        return r

    def invalidate(
        self, force=False
    ):
        if force or (self.sync_each is not None and time.time() > self.last_sync + self.sync_each):
            self.update(force)

        return self

    def update(
        self, throw=False
    ):
        if self.driver:
            v = self.driver.g(self.k)

            if isinstance(v, NotExistsError):
                if throw:
                    raise v
            else:
                self.v = v

        self.last_sync = time.time()

        return self
