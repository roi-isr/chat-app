from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from .routers import users, groups, messages

app = FastAPI()

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(messages.router)


@app.middleware('http')
async def error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
    except ValueError as ex:
        return JSONResponse(content=str(ex), status_code=status.HTTP_400_BAD_REQUEST)
    return response
