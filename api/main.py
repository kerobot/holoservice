from os.path import join, dirname
from fastapi import FastAPI
from api.routers import schedule

app = FastAPI(
    title="Holodule API Service",
    summary="ホロジュールから取得した配信スケジュールを API として提供します。",
)

app.include_router(schedule.router)
