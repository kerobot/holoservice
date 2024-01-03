from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class StreamerModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None, description="ストリーマーID")
    code: str | None = Field(default=None, description="ストリーマーコード")
    name: str | None = Field(default=None, description="ストリーマー名")
    group: str | None = Field(default=None, description="グループ")
    affiliations: list[str] | None = Field(default=None, description="所属")
    image_name: str | None = Field(default=None, description="画像名")
    channel_id: str | None = Field(default=None, description="チャンネルID")
    is_retired: bool | None = Field(default=False, description="引退済み")

    model_config = ConfigDict(
        populate_by_name=True,          # エイリアス名でのアクセスを許可するか（例えば id と _id）
        arbitrary_types_allowed=True,   # 任意の型を許可するか
        json_schema_extra={
            "example": {
                "code": "HL0000",
                "name": "ホロライブ",
                "group": "hololive",
                "affiliations": ['bland', 'jp'],
                "image_name": "hololive.jpg",
                "channel_id": "@hololive",
                "is_retired": False
            }
        },
    )

class StreamerCollection(BaseModel):
    streamers: list[StreamerModel]
