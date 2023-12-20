from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None, description="ユーザーID")
    username: str | None = Field(default=None, description="ユーザー名")
    password: str | None = Field(default=None, description="パスワード")
    firstname: str | None = Field(default=None, description="名")
    lastname: str | None = Field(default=None, description="姓")
    disabled: bool | None = Field(default=False, description="無効")

    model_config = ConfigDict(
        populate_by_name=True,          # エイリアス名でのアクセスを許可するか（例えば id と _id）
        arbitrary_types_allowed=True,   # 任意の型を許可するか
        json_schema_extra={
            "example": {
                "username": "ユーザー名",
                "password": "パスワード",
                "firstname": "名",
                "lastname": "姓",
                "disabled": False
            }
        },
    )

class UserCollection(BaseModel):
    users: list[UserModel]
