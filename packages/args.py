

import config


class Args(config.Config):

    @staticmethod
    def parse(
        argv, offset=1
    ):
        if isinstance(argv, str):
            argv = argv.split(' ')

        args = {}
        pref = None

        for v in argv[offset:]:
            if pref is not None:
                if v.strip('-') != v:
                    args[pref] = True

                    pref = v.strip('-')
                else:
                    args[pref] = v

                    pref = None
            else:
                if v.strip('-') != v:
                    if v.find('=') != - 1:
                        args[v.split('=')[0].strip('-')] = v.split('=')[1]
                    else:
                        pref = v.strip('-')

        if pref is not None:
            args[pref] = True

        return Args(args)

    def arg(
        self, k, d=None
    ):
        for k in k if isinstance(k, list) else [k]:
            if isinstance(k, str) and k in self:
                return self[k]

        return d
