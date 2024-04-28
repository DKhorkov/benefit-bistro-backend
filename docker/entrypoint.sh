#!/bin/bash


if [[ -z "${HOST}" ]]; then
  HOST="0.0.0.0"
else
  HOST="${HOST}"
fi

if [[ -z "${PORT}" ]]; then
  PORT=8000
else
  PORT="${PORT}"
fi

uvicorn src.main:app --host $HOST --port $PORT --reload
