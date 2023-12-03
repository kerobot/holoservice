from typing_extensions import Annotated
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class Schedule(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    key: str = Field(default=None, description="スケジュールキー")
    code: str = Field(default=None, description="配信者コード")
    video_id: str = Field(default=None, description="動画ID")
    datetime: str = Field(default=None, description="配信日時")
    name: str = Field(default=None, description="配信者名")
    title: str = Field(default=None, description="タイトル")
    url: str = Field(default=None, description="Youtube URL")
    description: str = Field(default=None, description="概要")
    published_at: str = Field(default=None, description="投稿日時")
    channel_id: str = Field(default=None, description="チャンネルID")
    channel_title: str = Field(default=None, description="チャンネル名")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "_id": None,
                "key": "配信者コード_YYYYMMDD_HHMMSS",
                "code": "配信者コード",
                "video_id": "動画ID",
                "datetime": "YYYYMMDD HHMMSS",
                "name": "配信者名",
                "title": "タイトル",
                "url": "Youtube URL",
                "description": "概要",
                "published_at": "投稿日時",
                "channel_id": "チャンネルID",
                "channel_title": "チャンネル名",
                "tags": "[]"
            }
        },
    )
