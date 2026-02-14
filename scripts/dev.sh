#!/bin/sh

set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
cd "$ROOT_DIR"

BACKEND_CMD=${BACKEND_CMD:-cd backend && uv run uvicorn app.main:app --reload --port 8000}
FRONTEND_CMD=${FRONTEND_CMD:-cd frontend && pnpm dev}

backend_pid=""
frontend_pid=""

kill_if_running() {
  pid="$1"
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
  fi
}

cleanup() {
  status=$?
  trap - INT TERM EXIT

  kill_if_running "$backend_pid"
  kill_if_running "$frontend_pid"

  [ -n "$backend_pid" ] && wait "$backend_pid" 2>/dev/null || true
  [ -n "$frontend_pid" ] && wait "$frontend_pid" 2>/dev/null || true

  exit "$status"
}

trap cleanup INT TERM EXIT

echo "Starting backend: $BACKEND_CMD"
sh -c "$BACKEND_CMD" &
backend_pid=$!

echo "Starting frontend: $FRONTEND_CMD"
sh -c "$FRONTEND_CMD" &
frontend_pid=$!

while :; do
  if ! kill -0 "$backend_pid" 2>/dev/null; then
    wait "$backend_pid"
    backend_status=$?
    echo "Backend exited with status $backend_status. Stopping frontend."
    exit "$backend_status"
  fi

  if ! kill -0 "$frontend_pid" 2>/dev/null; then
    wait "$frontend_pid"
    frontend_status=$?
    echo "Frontend exited with status $frontend_status. Stopping backend."
    exit "$frontend_status"
  fi

  sleep 1
done
