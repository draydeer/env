

from lib.event_handlers.types.system_file\
    import SystemFile
from packages.p\
    import dict_join, list_join


class SystemFileAlias(SystemFile):

    alias = 'systemFileAlias'

    def __call__(
        self, cmd=None, file=None, parameters=None, template=None, *args, **kwargs
    ):
        if self.has_config('keys.' + file + '.file'):
            SystemFile._evaluate(
                self,
                self.get_config('keys.' + file + '.cmd') or cmd,
                self.get_config('keys.' + file + '.file'),
                dict_join(
                    self.get_config('keys.' + file + '.parameters'),
                    parameters
                ),
                self.get_config('keys.' + file + '.template') or template
            )
