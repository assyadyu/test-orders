from httpx import AsyncClient


def http_session() -> AsyncClient:
    raise NotImplementedError
