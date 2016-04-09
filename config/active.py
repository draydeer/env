

import yaml

from packages.config import Config


config = Config(yaml.load(open('envd.yaml')))
