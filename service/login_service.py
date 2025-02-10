# coding: utf-8

from datetime import datetime, timedelta

from fastapi import HTTPException

from db.dao import user_dao, redis_dao
from service import token_service
from service.password_service import verify_password

# token有效时长
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def login_check(username, password):
    """
    校验账号密码是否正确
    :param username:
    :param password:
    :return:
    """
    user = await user_dao.get_user(username)
    print(f"user.lock_until========={user.lock_until}")

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 检查是否锁定
    if user.lock_until and user.lock_until > datetime.utcnow():
        raise HTTPException(status_code=403, detail="Account locked. Try again later.")

    if not verify_password(password, user.password):
        user.failed_attempts += 1
        if user.failed_attempts >= 5:
            # 密码错误5次,修改锁定时间
            user.lock_until = datetime.utcnow() + timedelta(minutes=15)
        # 更新用户记录
        await user_dao.update_user_failed_attempts(
            user.username,
            user.failed_attempts,
            user.lock_until
        )
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        # 登录成功，将失败次数置为0
        user.failed_attempts = 0
        user.lock_until = None
        # 更新用户记录
        await user_dao.update_user_failed_attempts(
            user.username,
            user.failed_attempts,
            user.lock_until
        )

    token = token_service.create_access_token(user.username, ACCESS_TOKEN_EXPIRE_MINUTES)
    redis = await redis_dao.get_redis()
    # 30分钟 Token 失效
    await redis.setex(f"token:{token}", ACCESS_TOKEN_EXPIRE_MINUTES * 60, "valid")
    return token

