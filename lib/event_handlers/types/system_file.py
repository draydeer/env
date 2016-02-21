

import os

from jinja2\
    import Template
from lib.type_handler\
    import TypeHandler
from packages.p\
    import dict_join, list_join


class SystemFile(TypeHandler):

    alias = 'systemFile'

    def _evaluate(
        self, cmd=None, file=None, parameters=None, template=None, *args, **kwargs
    ):
        if file:
            file = open(file, 'w+')

            file.write(Template(template).render(**parameters))
            file.close()

            if isinstance(cmd, list):
                for v in cmd:
                    if isinstance(v, str) or isinstance(v, unicode):
                        os.system(v)

    def __call__(
        self, cmd=None, file=None, parameters=None, template=None, *args, **kwargs
    ):
        self._evaluate(
            self,
            self.get_config('cmd') or cmd,
            self.get_config('file') or file,
            dict_join(
                self.get_config('parameters'),
                parameters
            ),
            self.get_config('template') or template
        )
