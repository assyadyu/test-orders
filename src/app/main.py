import fastapi as fa

from app.common import settings
from app.common.dependencies import bind_dependencies
from app.common.exceptions import register_exception_handler
from app.common.routers import bind_routers


def setup_application(db_url: str = settings.db_url):
    app_ = fa.FastAPI()

    bind_routers(app=app_)

    bind_dependencies(app=app_, db_url=db_url)

    register_exception_handler(app=app_)

    return app_


app = setup_application()
