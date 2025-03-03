# coding: utf-8
import re

from fastapi import APIRouter, Header, Depends

from service import login_service, token_service, register_service
from router.request_model import UserCreate

router = APIRouter()


@router.post("/register")
async def register(user: UserCreate):

    if len(user.password) < 6 or len(user.password) > 20:
        return {"message": "密码长度必须在 6-20 位之间"}
    # 正则匹配规则
    if not re.search(r'[A-Z]', user.password):
        return {"message": "密码必须包含至少一个大写字母"}
    if not re.search(r'[a-z]', user.password):
        return {"message": "密码必须包含至少一个小写字母"}
    if not re.search(r'\d', user.password):
        return {"message": "密码必须包含至少一个数字"}
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', user.password):
        return {"message": "密码必须包含至少一个特殊字符"}

    await register_service.register(user.username, user.password)
    return {"message": "User registered successfully"}


@router.post("/login")
async def login(user: UserCreate):
    """
    登录校验
    :param user: 用户
    :return:
    """
    token = await login_service.login_check(user.username, user.password)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/protected")
async def protected_route(username: str = Depends(token_service.verify_token)):
    """
    访问受保护接口
    :param username: 验证token获取的用户名称
    :return:
    """
    print("username========", username)
    return {"message": f"Welcome, {username}"}


@router.post("/logout")
async def logout(username: str = Depends(token_service.verify_token), authorization: str = Header(None)):
    """
    注销登录
    :return:
    """
    await token_service.revoke_token(authorization)
    return {"message": f"{username} logged out successfully"}
