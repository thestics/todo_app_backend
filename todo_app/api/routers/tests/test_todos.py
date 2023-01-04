#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko

import pytest
from fastapi.testclient import TestClient
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from mock_alchemy.mocking import mock

from todo_app.db.models import Todo


def mock_session():
    mock_todos = [
        Todo(id='6a670735-053f-4a6f-a5a6-d3099f4d8048', brief='foo_1',
             detailed='foo_bar_1', done=False),
        Todo(id='6a670735-053f-4a6f-a5a6-d3099f4d8041', brief='foo_2',
             detailed='foo_bar_2', done=True),
        Todo(id='6a670735-053f-4a6f-a5a6-d3099f4d8042', brief='foo_3',
             detailed='foo_bar_3', done=True),

    ]
    s = UnifiedAlchemyMagicMock(data=[
        ([mock.call.query(Todo)], mock_todos)
    ])
    return s


@pytest.fixture()
def mock_session_fixture():
    return mock_session()


async def mock_get_session():
    yield mock_session()


@pytest.fixture()
def test_client(mock_session_fixture):
    from todo_app.main import app
    from todo_app.db import get_session

    app.dependency_overrides[get_session] = mock_get_session
    return TestClient(app)


def test_get_todos(test_client):
    res = test_client.get('/todo')
    print()


def test_post_todos():
    pass


def test_update_todos():
    pass


def test_delete_todos():
    pass
