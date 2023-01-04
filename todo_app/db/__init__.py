#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..settings import cfg

SQLALCHEMY_DATABASE_URL = \
    f"postgresql+asyncpg://{cfg.db.DB_USERNAME}:{cfg.db.DB_PASSWORD}" \
    f"@{cfg.db.DB_HOST}:{cfg.db.DB_PORT}/{cfg.db.DB_NAME}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session = sessionmaker(
    autocommit=False, class_=AsyncSession, autoflush=False, bind=engine,
    expire_on_commit=False
)

Base = declarative_base()


async def get_session():
    async with async_session() as session:
        yield session
