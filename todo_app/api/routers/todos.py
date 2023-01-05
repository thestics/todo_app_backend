#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko


from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import StatementError
from sqlalchemy.orm import Session

import logging

from todo_app.db import get_session
from todo_app.db.models import Todo
from todo_app.serialize.todo import TodoModel, TodoInModel, Success


router = APIRouter(prefix="/todo")
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[TodoModel])
def get_todos(session: Session = Depends(get_session)):
    res = session.query(Todo).all()
    return [TodoModel.from_orm(o) for o in res]


@router.post("/", response_model=TodoModel)
async def add_todo(in_todo: TodoInModel, session: Session = Depends(get_session)):
    todo_id = session.scalar(
        insert(Todo)
        .values(brief=in_todo.brief, detailed=in_todo.detailed)
        .returning(Todo)
    )
    todo = session.scalar(select(Todo).where(Todo.id == todo_id))
    session.commit()
    return TodoModel.from_orm(todo)


@router.put("/", response_model=TodoModel)
def put_todo(new_todo: TodoModel, session: Session = Depends(get_session)):
    todo_id = session.scalar(
        update(Todo)
        .where(Todo.id == new_todo.id)
        .values(brief=new_todo.brief, detailed=new_todo.detailed, done=new_todo.done)
        .returning(Todo)
    )
    session.commit()
    todo = session.scalar(select(Todo).where(Todo.id == todo_id))
    return todo.__dict__


@router.delete("/", response_model=Success)
def delete_todo(todo_id: str, session: Session = Depends(get_session)):
    try:
        deleted_id = session.scalar(
            delete(Todo).where(Todo.id == todo_id).returning(Todo)
        )
        session.commit()
        return {
            "success": deleted_id is not None,
            "reason": None if deleted_id is not None else "Invalid `todo_id`",
        }
    except StatementError as e:
        return {"success": False, "reason": "Malformed UUID string"}
    except Exception as e:
        logger.error(e, exc_info=True)
