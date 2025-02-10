# coding: utf-8

from fastapi import FastAPI, Depends, HTTPException

from db.dao import user_dao
from service.password_service import hash_password, verify_password


async def register(username, password):
    """
    注册用户
    :param username: 用户名
    :param password: 密码
    :return:
    """
    print(f"username: {username}, password: {password}")
    user = await user_dao.get_user(username)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        await user_dao.create_user(username, hash_password(password))

