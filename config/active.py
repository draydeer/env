

from packages.config\
    import Config


config = Config({
    'default': 'mongo',
    'mode': 'keeper',
    'drivers': {
        'env': {
            'initiator': 'env',

            'host': 'http://localhost:8089',
            'key': '1'
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
