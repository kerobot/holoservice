from fastapi import Request
from api.exceptions import BaseAPIException

async def request_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as ex:
        if isinstance(ex, BaseAPIException):
            return ex.response()
        raise ex
