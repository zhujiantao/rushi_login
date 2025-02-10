# coding: utf-8
from sqlalchemy import func, update
from sqlalchemy.future import select

from db.models.model import async_db_session, User


async def create_user(username: str, password: str):
    """
    新增用户
    :param username:
    :param password:
    :return:
    """
    async with await async_db_session() as async_session:
        user = User(username=username, password=password)
        async_session.add(user)
        await async_session.commit()


async def get_user(username: str):
    """
    根据用户名查询用户记录
    :param username: 用户名
    :return:
    """
    async with await async_db_session() as async_session:
        result = await async_session.execute(
            select(User).where(User.username == username)
        )
    return result.scalars().first()


async def update_user_failed_attempts(username: str, failed_attempts: int, lock_until=None):
    """
    根据用户名更新登录重试失败次数及锁定时间
    :param username: 用户名
    :param failed_attempts: 失败次数
    :param lock_until: 锁定时间
    :return:
    """
    async with await async_db_session() as async_session:
        await async_session.execute(
            update(User).where(User.username == username).values(failed_attempts=failed_attempts, lock_until=lock_until)
        )
        await async_session.commit()

