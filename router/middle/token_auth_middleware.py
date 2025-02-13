from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from service.token_service import verify_token


class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        print(f"request.url.path======={request.url.path}")

        if request.url.path in ["/register", "/login"]:
            return await call_next(request)

        # 获取 Authorization 头部中的 token
        authorization: str = request.headers.get("authorization")
        if authorization is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization token missing"}
            )

        try:
            # 解码并校验 token
            await verify_token()
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )

        response = await call_next(request)
        return response
