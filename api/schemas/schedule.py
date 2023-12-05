from datetime import datetime, timezone, timedelta
from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
UTC = timezone.utc
JST = timezone(timedelta(hours=+9), "JST")

class ScheduleModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None, description="スケジュールID")
    code: str = Field(default=None, description="配信者コード")
    video_id: str = Field(default=None, description="動画ID")
    streaming_at: datetime = Field(default_factory=lambda: datetime.now(tz=JST), description="配信日時")
    name: str = Field(default=None, description="配信者名")
    title: str = Field(default=None, description="タイトル")
    url: str = Field(default=None, description="Youtube URL")
    description: str = Field(default=None, description="概要")
    published_at: datetime = Field(default_factory=lambda: datetime.now(tz=JST), description="投稿日時") 
    channel_id: str = Field(default=None, description="チャンネルID")
    channel_title: str = Field(default=None, description="チャンネル名")
    tags: list[str] = Field(default_factory=list, description="タグ")

    @computed_field
    @property
    def key(self) -> str:
        return self.code + "_" + self.streaming_at.strftime("%Y%m%d_%H%M%S") if (self.code is not None and self.streaming_at is not None) else ""

    model_config = ConfigDict(
        populate_by_name=True,          # エイリアス名でのアクセスを許可するか（例えば id と _id）
        arbitrary_types_allowed=True,   # 任意の型を許可するか
        json_schema_extra={
            "example": {
                "code": "HL0000",
                "video_id": "動画ID",
                "streaming_at": "2023-12-01T12:00:00Z",
                "name": "配信者名",
                "title": "タイトル",
                "url": "Youtube URL",
                "description": "概要",
                "published_at": "2023-12-01T12:00:00Z",
                "channel_id": "チャンネルID",
                "channel_title": "チャンネル名",
                "tags": []
            }
        },
    )

class ScheduleCollection(BaseModel):
    schedules: list[ScheduleModel]
