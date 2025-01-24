from collections.abc import Callable, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from app.common import logger


def async_engine(url: str) -> AsyncEngine:
    logger.info(f"async_engine created, url {url}")
    return create_async_engine(
        url,
        pool_pre_ping=True,
        isolation_level="REPEATABLE READ",
        future=True,
        connect_args={"timeout": 60},
        echo=False,
    )


def async_session(engine) -> async_sessionmaker[AsyncSession]:
    logger.info("sessionmaker created")
    return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


def session_factory(url: str) -> Callable[..., AsyncGenerator]:
    _session = async_session(async_engine(url))

    async def get_session() -> AsyncGenerator:
        async with _session() as session:
            logger.info("session created")
            yield session
        logger.info("session closed")

    return get_session
