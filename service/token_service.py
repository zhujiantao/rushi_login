# coding: utf-8

from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from db.dao import redis_dao

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"


def create_access_token(username: str, access_token_expires_minutes: int = 30):
    """
    创建token，并存储到Redis中
    :param username: 用户名
    :param access_token_expires_minutes: token过期时间
    :return:
    """
    expire = datetime.utcnow() + timedelta(minutes=access_token_expires_minutes)
    payload = {"sub": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def verify_token(token: str):
    """
    验证token，并从Redis中获取用户名
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]

        # 检查redis是否存储了该token
        redis_client = await redis_dao.get_redis()
        if await redis_client.get(f"token:{token}") is None:
            raise HTTPException(status_code=401, detail="Token expired or revoked")

        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def revoke_token(token: str):
    """
    撤销token，并从Redis中删除
    :param token:
    :return:
    """
    redis_client = await redis_dao.get_redis()
    await redis_client.delete(f"token:{token}")

