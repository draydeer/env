

import config


class Args(config.Config):

    @staticmethod
    def parse(
        argv, offset=1
    ):
        if isinstance(argv, str):
            argv = argv.split(' ')

        args = {}
        prefix = None

        for v in argv[offset:]:
            if prefix is not None:
                if v.strip('-') != v:
                    args[prefix] = prefix

                    prefix = v.strip('-')
                else:
                    args[prefix] = v

                    prefix = None
            else:
                if v.strip('-') != v:
                    if v.find('=') != - 1:
                        args[v.split('=')[0].strip('-')] = v.split('=', 1)[1]
                    else:
                        prefix = v.strip('-')

        if prefix is not None:
            args[prefix] = prefix

        return Args(args)

    def arg(
        self, k, d=None
    ):
        for k in k if isinstance(k, list) else [k]:
            if isinstance(k, str) and k in self:
                return self[k]

        return d
