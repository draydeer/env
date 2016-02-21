

from lib.driver\
    import Driver


class FileTxt(Driver):

    def g(
        self, k
    ):
        file = open(self._config['file'])

        data = file.readall()

        file.close()

        return data
