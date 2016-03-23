

import logging
import time


class Logger:

    level = logging.INFO

    def colorize(
        self, message, color
    ):
        return message

    def show(
        self, message, level=logging.INFO, std=None
    ):
        if self.level <= level:
            print message

        return self

    def show_with_time(
        self, message, level=logging.INFO, std=None
    ):
        if self.level <= level:
            print time.strftime("%D %H:%M:%S") + ' ' + message

        return self

    def critical(
        self, message
    ):
        return self.show_with_time(self.colorize(message, 'critical'), logging.CRITICAL)

    def error(
        self, message
    ):
        return self.show_with_time(self.colorize(message, 'error'), logging.ERROR)

    def indented(
        self, message
    ):
        return self.show("\t" + self.colorize(message, 'idle'), logging.INFO)

    def info(
        self, message
    ):
        return self.show_with_time(self.colorize(message, 'info'), logging.INFO)

    def nl(
        self
    ):
        return self.show("\n")

    def splitter(
        self
    ):
        return self.show("\n\t" + self.colorize('--------------------------------', 'idle') + "\n")

    def warning(
        self, message
    ):
        return self.show_with_time(self.colorize(message, 'warning'), logging.WARNING)


logger = Logger()
