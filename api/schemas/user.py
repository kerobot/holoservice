from typing_extensions import Annotated
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None, description="ユーザーID")
    username: str = Field(default=None, description="ユーザー名")
    password: str = Field(default=None, description="パスワード")
    firstname: str = Field(default=None, description="姓")
    lastname: str = Field(default=None, description="名")
    disabled: bool = Field(default=False, description="無効")

    model_config = ConfigDict(
        populate_by_name=True,          # エイリアス名でのアクセスを許可するか（例えば id と _id）
        arbitrary_types_allowed=True,   # 任意の型を許可するか
        json_schema_extra={
            "example": {
                "username": "ユーザー名",
                "password": "パスワード",
                "firstname": "姓",
                "lastname": "名",
                "disabled": False
            }
        },
    )
