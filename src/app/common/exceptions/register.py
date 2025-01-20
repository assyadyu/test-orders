import fastapi as fa

from app.common.exceptions import (
    ObjectDoesNotExistException,
    AuthenticationException,
    NoPermissionException,
)
from app.common.exceptions.handlers import (
    object_does_not_exist_exception_handler,
    user_not_found_handler,
    not_enough_permission_handler,
)


def register_exception_handler(app: fa.FastAPI):
    app.add_exception_handler(ObjectDoesNotExistException, object_does_not_exist_exception_handler)
    app.add_exception_handler(AuthenticationException, user_not_found_handler)
    app.add_exception_handler(NoPermissionException, not_enough_permission_handler)
