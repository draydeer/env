

from gevent import monkey


monkey.patch_all()


import sys

from config.active import config
from src.application import Application
from packages.args import Args


Application(Args.parse(sys.argv), config).run()
