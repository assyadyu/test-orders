import pickle
from functools import wraps

from app.common import logger
from app.common.redis import r as store


def order_cache(expiration: int = None, update: bool = False, delete: bool = False):
    def wrapped(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if "order_uuid" in kwargs:
                key = str(kwargs["order_uuid"])
            elif "filter_query" in kwargs:
                key = "-".join(str(k) for k in kwargs["filter_query"])
            else:
                key = "-".join(str(kwargs[k]) for k in kwargs)

            data = await store.get(key)
            logger.info(f"Cache hit for key {key}: {"Yes" if data else "No"}")
            if data is None or update:
                result = await func(*args, **kwargs)
                data = pickle.dumps(result)
                await store.setex(key, expiration, data) if expiration else await store.set(key, data)
            elif data and delete:
                result = await func(*args, **kwargs)
                await store.delete(key)
            else:
                result = pickle.loads(data)
            return result

        return wrapper

    return wrapped
