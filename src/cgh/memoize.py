import atexit
import contextlib
import json
from pathlib import Path

memoize_store = Path("~/.cache/cgh/memoize.json").expanduser()


_loaded = False
_cache = {}


def _load():
    global _cache, _loaded
    if _loaded:
        return
    _loaded = True
    with contextlib.suppress(FileNotFoundError, json.JSONDecodeError, KeyError):
        with memoize_store.open() as f:
            _cache = json.load(f)


def _save():
    memoize_store.parent.mkdir(parents=True, exist_ok=True)
    with memoize_store.open("w") as f:
        json.dump(_cache, f)


atexit.register(_save)


def memoize():
    def decorator(func):
        key = f"{func.__module__}.{func.__name__}"

        def wrapper(*args, **kwargs):
            _load()
            hashed = json.dumps((args, kwargs))
            if cached := _cache.get(key, {}).get(hashed):
                return cached
            result = func(*args, **kwargs)
            _cache[hashed] = result
            return result

        return wrapper

    return decorator
