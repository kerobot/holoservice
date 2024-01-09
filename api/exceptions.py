from typing import Type
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel, Field

class BaseError(BaseModel):
    message: str = Field(..., description="Error message or description")

class BaseIdentifiedError(BaseError):
    identifier: str = Field(..., description="Unique identifier which this error references to")

class NotFoundError(BaseIdentifiedError):
    pass

class AlreadyExistsError(BaseIdentifiedError):
    pass

class InactiveUserError(BaseIdentifiedError):
    pass

class CredentialsError(BaseError):
    pass

class BaseAPIException(Exception):
    message = "Generic error"
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseError
    headers = None

    def __init__(self, **kwargs):
        kwargs.setdefault("message", self.message)
        self.message = kwargs["message"]
        self.data = self.model(**kwargs)

    def __str__(self):
        return self.message

    def response(self):
        return JSONResponse(
            content=self.data.model_dump(),
            status_code=self.code,
            headers=self.headers
        )

    @classmethod
    def response_model(cls):
        return {cls.code: {"model": cls.model}}

class BaseIdentifiedException(BaseAPIException):
    message = "Entity error"
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    model = BaseIdentifiedError

    def __init__(self, identifier, **kwargs):
        super().__init__(identifier=identifier, **kwargs)

class NotFoundException(BaseIdentifiedException):
    message = "The entity does not exist"
    code = status.HTTP_404_NOT_FOUND
    model = NotFoundError

class AlreadyExistsException(BaseIdentifiedException):
    message = "The entity already exists"
    code = status.HTTP_409_CONFLICT
    model = AlreadyExistsError

class InactiveUserException(BaseIdentifiedException):
    message = "Inactive user"
    code = status.HTTP_400_BAD_REQUEST
    model = InactiveUserError

class CredentialsException(BaseAPIException):
    message = "Colud not validate credentials"
    code = status.HTTP_401_UNAUTHORIZED,
    model = CredentialsError
    headers = {'WWW-Authenticate': "Bearer"}

def get_exception_responses(*args: Type[BaseAPIException]) -> dict:
    responses = dict()
    for cls in args:
        responses.update(cls.response_model())
    return responses
