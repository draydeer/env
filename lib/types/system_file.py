

import os

from string\
    import Template
from lib.type_handler\
    import TypeHandler


class SystemFile(TypeHandler):

    def __call__(
        self, cmd, file, parameters, template, *args, **kwargs
    ):
        if isinstance(parameters, dict):
            file = open(file, 'w+')

            file.write(Template(template).substitute(**parameters))
            file.close()

        if isinstance(cmd, list):
            for v in cmd:
                if isinstance(v, str) or isinstance(v, unicode):
                    os.system(v)
