#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko
import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from todo_app.db import Base


class Todo(Base):
    __tablename__ = 'todo'
    
    id = Column(
        UUID, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    brief = Column(String(length=256))
    detailed = Column(String(length=2048))
    done = Column(Boolean, default=False)
