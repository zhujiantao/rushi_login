from fastapi import FastAPI

from router.api import router
# from router.middle.token_auth_middleware import TokenAuthMiddleware

app = FastAPI()
app.include_router(router)
# app.add_middleware(TokenAuthMiddleware)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
