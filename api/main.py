from os.path import join, dirname
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.routers import schedule

app = FastAPI(
    title="Holodule API Service",
    summary="ホロジュールから取得した配信スケジュールを API として提供します。",
)

app.include_router(schedule.router)

@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
