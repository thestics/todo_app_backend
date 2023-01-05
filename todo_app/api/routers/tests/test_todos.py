#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# Author: Danylo Kovalenko

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from todo_app.db import Base, SQLALCHEMY_DATABASE_URL
from todo_app.db.models import Todo


mock_data = [
    Todo(id='6a670735-053f-4a6f-a5a6-d3099f4d8048', brief='foo_1',
         detailed='foo_bar_1', done=False),
    Todo(id='6a670735-053f-4a6f-a5a6-d3099f4d8041', brief='foo_2',
         detailed='foo_bar_2', done=True),
    Todo(id='6a670735-053f-4a6f-a5a6-d3099f4d8042', brief='foo_3',
         detailed='foo_bar_3', done=True),

]


@pytest.fixture(scope="session")
def connection():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()
    with sessionmaker(
            autocommit=False, autoflush=False,
            bind=connection, expire_on_commit=False)() as session:
        mock_db_data(session)
    yield
    Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()


@pytest.fixture()
def test_client(db_session):
    from todo_app.main import app
    from todo_app.db import get_session

    app.dependency_overrides[get_session] = lambda: db_session
    return TestClient(app)


def mock_db_data(session):
    session.add_all(mock_data)
    session.commit()


def test_get_todos(test_client, db_session):
    res = test_client.get('/todo')
    assert res.status_code == 200
    assert len(res.json()) == 3

    for resp_item, true_item in zip(res.json(), mock_data):
        assert resp_item['id'] == true_item.id
        assert resp_item['brief'] == true_item.brief
        assert resp_item['detailed'] == true_item.detailed
        assert resp_item['done'] == true_item.done


def test_post_todos_200(test_client, db_session):
    data = {'brief': 'brief', 'detailed': 'detailed'}
    res = test_client.post('/todo', json=data)
    saved_obj = db_session\
        .query(Todo)\
        .filter(Todo.id == res.json()['id'])\
        .one_or_none()
    res_data = res.json()
    
    assert res.status_code
    assert saved_obj is not None
    for k, v in data.items():
        assert res_data[k] == v
        assert getattr(saved_obj, k, None) == v


def test_post_todos_422(test_client):
    insufficient_data = {'detailed': 'detailed'}
    res = test_client.post('/todo', json=insufficient_data)
    
    assert res.status_code == 422


def test_update_todos_200(test_client, db_session):
    data = {
        'id': '6a670735-053f-4a6f-a5a6-d3099f4d8048', 'brief': 'foo_1',
        'detailed': 'foo_bar_1', 'done': True
    }
    res = test_client.put('/todo', json=data)
    upd_object = db_session\
        .query(Todo)\
        .filter(Todo.id == res.json()['id'])\
        .one_or_none()
    
    assert res.status_code
    assert upd_object is not None
    assert upd_object.done


def test_update_todos_422(test_client):
    insufficient_data = {'detailed': 'detailed'}
    res = test_client.put('/todo', json=insufficient_data)
    
    assert res.status_code == 422


def test_delete_todos_200(test_client, db_session):
    deleted_id = '6a670735-053f-4a6f-a5a6-d3099f4d8048'
    res = test_client.delete(
        '/todo', params={'todo_id': deleted_id})
    deleted_obj = db_session\
        .query(Todo)\
        .filter(Todo.id == deleted_id)\
        .one_or_none()
    
    assert res.status_code == 200
    assert deleted_obj is None


def test_delete_todos_422(test_client):
    res = test_client.delete(
        '/todo', params={'wrong_key': '6a670735-053f-4a6f-a5a6-d3099f4d8048'})
    assert res.status_code == 422
