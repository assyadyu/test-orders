from fastapi import (
    FastAPI,
)

from app.db.sessions import (
    async_session,
    session_factory,
)


def bind_dependencies(app: FastAPI, db_url: str):
    app.dependency_overrides[async_session] = session_factory(db_url)
