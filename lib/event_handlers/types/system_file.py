

import os

from jinja2\
    import Template
from lib.type_handler\
    import TypeHandler
from packages.p\
    import dict_join


class SystemFile(TypeHandler):

    alias = 'systemFile'

    def _evaluate(
        self, cmd, file, parameters, template
    ):
        file = open(file, 'w+')

        file.write(Template(template).render(**parameters))
        file.close()

        if isinstance(cmd, list) and self.get_config('allowCmd'):
            for v in cmd:
                if isinstance(v, str) or isinstance(v, unicode):
                    os.system(v)

    def __call__(
        self, cmd=None, file=None, parameters=None, template=None, *args, **kwargs
    ):
        if self.has_config('keys.' + file):
            config = self.get_config('keys.' + file)
        else:
            config = self.get_config('default')

        self._evaluate(
            config.cmd or cmd,
            config.file or file,
            dict_join(
                config.parameters,
                parameters,
                config.strict
            ),
            config.template or template
        )
