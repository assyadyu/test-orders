import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.common.exceptions import (
    ObjectDoesNotExistException,
    AuthenticationException,
    NoPermissionException,
)


def object_does_not_exist_exception_handler(request: Request, exc: ObjectDoesNotExistException):
    message = exc.args[0]
    logging.error(f"URL: {request.url} MESSAGE: {message}")
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": message})


def user_not_found_handler(request: Request, exc: AuthenticationException):
    message = exc.args[0]
    logging.error(f"URL: {request.url} MESSAGE: {message}")
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})


def not_enough_permission_handler(request: Request, exc: NoPermissionException):
    message = exc.args[0]
    logging.error(f"URL: {request.url} MESSAGE: {message}")
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": message})
