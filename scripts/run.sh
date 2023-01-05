#!/usr/bin/env bash
gunicorn todo_app.main:app -k uvicorn.workers.UvicornWorker
