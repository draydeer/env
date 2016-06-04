

def dict_join(*args):
    return {k: v for a in args for k, v in (a if isinstance(a, dict) else {}).iteritems()}


def list_join(*args):
    return reduce(lambda a, b: (a if isinstance(a, list) else []) + (b if isinstance(a, list) else []), args)


def first(f, a):
    return next(v for v in a if f(v))


def first_str(*args):
    return next(v for v in args if isinstance(v, str) or isinstance(v, unicode))
