import fastapi as fa

from app.common.exceptions import (
    ObjectDoesNotExistException,
    AuthenticationException,
    NoPermissionException,
    RedisConnectionException,
    AuthServiceNotAvailable,
)
from app.common.exceptions.handlers import (
    object_does_not_exist_exception_handler,
    user_not_found_handler,
    not_enough_permission_handler,
    connection_error_handler,
)


def register_exception_handler(app: fa.FastAPI):
    app.add_exception_handler(ObjectDoesNotExistException, object_does_not_exist_exception_handler)
    app.add_exception_handler(AuthenticationException, user_not_found_handler)
    app.add_exception_handler(NoPermissionException, not_enough_permission_handler)
    app.add_exception_handler(RedisConnectionException, connection_error_handler)
    app.add_exception_handler(AuthServiceNotAvailable, connection_error_handler)
