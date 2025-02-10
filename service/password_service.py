# coding: utf-8

import bcrypt


def hash_password(password: str) -> str:
    """
    对密码加密
    :param password:
    :return:
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

