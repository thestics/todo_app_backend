#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko

from fastapi import FastAPI

from .api.routers.todos import router as todo_router


app = FastAPI()
app.include_router(todo_router)
