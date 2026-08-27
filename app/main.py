from fastapi import FastAPI


from app.api.users import router as user_router
from app.api.shortener import router as shortener_router
from app.api.shortener import redirect_router as redirect_router

app = FastAPI(
    title="Укоротитель ссылок",
    version="0.0.1"
)

app.include_router(
    user_router,
    prefix="/api/v1/auth",
    tags=["Регистрация и авторизация"]
)
app.include_router(
    shortener_router,
    prefix="/api/v1",
    tags=["Робота с сылками"]
)
app.include_router(
    redirect_router,
    prefix="/r",
    tags=["Робота с сылками"]
)



@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
