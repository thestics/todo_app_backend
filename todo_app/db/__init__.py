#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..settings import cfg

SQLALCHEMY_DATABASE_URL = \
    f"postgresql://{cfg.db.DB_USERNAME}:{cfg.db.DB_PASSWORD}" \
    f"@{cfg.db.DB_HOST}:{cfg.db.DB_PORT}/{cfg.db.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
make_session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

Base = declarative_base()


def get_session():
    with make_session() as session:
        yield session
