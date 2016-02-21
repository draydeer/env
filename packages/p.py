

def dict_join(
    a, b
):
    return a.update(b) or a if isinstance(a, dict) and isinstance(b, dict) else a if isinstance(a, dict) else b if isinstance(b, dict) else {}


def list_join(
    a, b
):
    return a + b if isinstance(a, list) and isinstance(b, list) else a if isinstance(a, list) else b if isinstance(b, list) else []


def first(
    f, a
):
    return next(v for v in a if f(v))


def first_str(
    *args
):
    return next(v for v in args if isinstance(v, str) or isinstance(v, unicode))
