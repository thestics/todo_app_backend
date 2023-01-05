#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko
from typing import Optional

from pydantic import BaseModel


class TodoModel(BaseModel):
    id: str
    brief: str
    detailed: str
    done: bool
    
    class Config:
        orm_mode = True
    

class TodoInModel(BaseModel):
    brief: str
    detailed: str


class Success(BaseModel):
    success: bool = True
    reason: Optional[str] = None