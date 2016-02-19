

from packages.config\
    import Config


config = Config({
    'default': 'fileYaml',
    'mode': 'keeper',
    'drivers': {
        'env': {
            'initiator': 'env',

            'host': 'http://localhost:8089',
            'key': '1'
        },
        'fileIni': {
            'initiator': 'fileIni',

            'file': '/usr/local/dev/local/env/tests/test.ini'
        },
        'fileJson': {
            'initiator': 'fileJson',

            'file': '/usr/local/dev/local/env/tests/test.json'
        },
        'fileYaml': {
            'initiator': 'fileYaml',

            'file': '/usr/local/dev/local/env/tests/test.yaml'
        },
        'memory': {
            'initiator': 'memory',

            'values': {
                'mem': {
                    'mom': '@@:env:mom'
                },
                'mom': 5
            }
        },
        'mongo': {
            'initiator': 'mongo',

            'host': 'localhost:27017',
            'db': 'env',
            'user': 'root',
            'pass': 'root'
        }
    }
})
