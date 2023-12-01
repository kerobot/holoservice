from pydantic import BaseModel, Field

class Schedule(BaseModel):
    key: str = Field(None, description="キー")
    code: str = Field(None, description="コード")
    video_id: str = Field(None, description="動画ID")
    datetime: str = Field(None, description="配信日時")
    name: str = Field("配信者名", description="配信者名")
    title: str = Field("タイトル", description="タイトル")
    url: str = Field(None, description="URL")
    description: str = Field("概要", description="概要")
    published_at: str = Field(None, description="公開日時")
    channel_id: str = Field(None, description="チャンネルID")
    channel_title: str = Field("チャンネル名", description="チャンネル名")
