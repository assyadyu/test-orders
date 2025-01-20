import typing

from httpx import AsyncClient


def http_client_adapter(base_url: str = ''):
    async def wrapper() -> typing.Callable[..., "AsyncClient"]:
        async with AsyncClient(base_url=base_url) as client:
            yield client

    return wrapper
