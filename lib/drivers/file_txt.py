

from lib.driver\
    import Driver


class FileTxt(Driver):

    def g(
        self, k
    ):
        return open(self._config['file']).readall()
