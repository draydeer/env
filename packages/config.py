

class Config(dict):

    def __init__(self, d=None):
        if isinstance(d, dict) is False:
            d = {}
        else:
            d = {k: Config(v) if isinstance(v, dict) else v for (k, v) in d.iteritems()}

        super(Config, self).__init__(d)

    def __getattr__(self, k):
        return self.g(k)

    def __getitem__(self, k):
        return self.g(k)

    def g(self, k, default=None):
        """
        Get nested value by key. If no key reached returns [default].

        :param k: Key or path. Can be "dotted" for nested key ("a.b.c").
        :param default: Default value if key not exists.
        :return:
        """

        r = self

        for x in k.split('.'):
            if isinstance(r, dict):
                r = r.get(x)

                continue

            if isinstance(r, list):
                r = r[int(x)] if x.isdigit() and len(r) > int(x) else None

                continue

            return default

        return r

    def s(self, k, v):
        """
        Set nested value.

        :param k: Key or path. Can be "dotted" for nested key ("a.b.c").
        :param v: Value.
        :return:
        """

        p = r = self

        for k in k.split('.'):
            if isinstance(r, dict):
                p = r
                r = r.get(k)
            elif isinstance(r, list):
                p = r
                r = r[int(k)] if k.isdigit() and len(r) > int(k) else None

            if isinstance(r, dict) is False and isinstance(r, list) is False:
                r = p[int(k) if isinstance(p, list) else k] = Config()

        p[int(k) if isinstance(p, list) else k] = v

        return self

    def has(self, k, exists_value=True):
        """
        Check for key existence.

        :param k: Key or path. Can be "dotted" for nested key ("a.b.c").
        :param exists_value: Value to return if key exists.
        :return:
        """

        r = self

        for x in k.split('.'):
            p = True

            if isinstance(r, dict):
                p = x in r
                r = r.get(x)
            elif isinstance(r, list):
                p = x.isdigit() and len(r) > int(x)
                r = r[int(x)] if p else None

            if p is False:
                return False

        return exists_value
