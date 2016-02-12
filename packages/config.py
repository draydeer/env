

class Config(dict):

    def __init__(
        self, d=None
    ):
        if isinstance(d, dict) is False:
            d = {}
        else:
            d = {k: Config(v) if isinstance(v, dict) else v for (k, v) in d.iteritems()}

        super(Config, self).__init__(d)

    def __missing__(
        self, k
    ):
        return None

    def __getattr__(
        self, k
    ):
        return self.g(k)

    def g(
        self, k, d=None
    ):
        r = self

        for x in k.split('.'):
            if isinstance(r, dict):
                r = r.get(x)

                continue

            if isinstance(r, list):
                r = r[int(x)] if x.isdigit() and len(r) > int(x) else None

                continue


            return d


        return r

    def s(
        self, k, v
    ):
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
