
class Dict:

    def to_dict(self):
        return {
            x[0]: x[1].to_dict() if isinstance(x[1], Dict) else x[1] for x in filter(
                lambda (k, v): k[0] != '_', vars(self).iteritems()
            )
        }
