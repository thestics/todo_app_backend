#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko

import os
import enum
from pathlib import Path

from pydantic import BaseSettings


class Env(enum.Enum):
    dev = 'dev'
    prod = 'prod'


class DbSettings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str


class AppSettings(BaseSettings):
    db: DbSettings
    app_env: Env


def get_settings():
    env_str = os.environ.get('APP_ENV', 'dev')
    try:
        env = Env(env_str)
    except ValueError as e:
        raise ValueError('Unexpected `APP_ENV` value') from e
    dotenv_path = Path(__file__).parent.parent / 'env' / f'.env.{env.value}'
    assert dotenv_path.exists()
    
    db_settings = DbSettings(_env_file=dotenv_path)
    cfg = AppSettings(db=db_settings, app_env=env, _env_file=dotenv_path)
    return cfg


cfg = get_settings()
