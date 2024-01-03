from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routers import schedule
from api.routers import streamer
from api.routers import user
from api.routers import authentication
from api.middlewares import request_handler

# FastAPIインスタンスを作成
app = FastAPI(
    title="Holodule API Service",
    summary="ホロジュールから取得した配信スケジュールを API として提供します。",
)

# HTTPリクエストの前後で処理を実行するためのミドルウェアを登録
app.middleware("http")(request_handler)

# CORS設定
origins: list = ["*"] # とりあえず全てのオリジンを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPIルーターを登録
app.include_router(schedule.router)
app.include_router(streamer.router)
app.include_router(user.router)
app.include_router(authentication.router)

# FastAPIのエラーハンドラーを登録
@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError) -> JSONResponse:
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
