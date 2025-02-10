# coding: utf-8
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Integer, DateTime


DATABASE_URL = "sqlite+aiosqlite:///./user.db"
engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()


async def async_db_session():
    user_async_session = sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)
    return user_async_session()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    failed_attempts = Column(Integer, default=0)
    lock_until = Column(DateTime, nullable=True)


# 创建数据库和表
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # 关键点：用 run_sync 执行同步操作


async def main():
    await init_db()  # 初始化数据库


# 运行事件循环
# asyncio.run(main())
