
#!/bin/bash

# ============================================================
# MovieMatch Development Runner
# Starts the React frontend and FastAPI backend.
# ============================================================

set -Eeuo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
VENV_DIR="$BACKEND_DIR/.venv"
PID_FILE="$BACKEND_DIR/.moviematch-server.pid"

BACKEND_PID=""
FRONTEND_PID=""

print_header() {
    clear || true
    echo "=============================================="
    echo "           MovieMatch Development"
    echo "=============================================="
    echo
}

check_backend() {
    if [[ ! -d "$BACKEND_DIR" ]]; then
        echo "ERROR: Backend directory not found: $BACKEND_DIR"
        exit 1
    fi
}

check_frontend() {
    if [[ ! -f "$FRONTEND_DIR/package.json" ]]; then
        echo "ERROR: Frontend package.json not found:"
        echo "  $FRONTEND_DIR/package.json"
        exit 1
    fi

    if ! command -v npm >/dev/null 2>&1; then
        echo "ERROR: npm is not installed or not in PATH."
        exit 1
    fi
}

setup_virtual_environment() {
    if [[ ! -d "$VENV_DIR" ]]; then
        echo "Creating backend virtual environment..."
        python3 -m venv "$VENV_DIR"
    fi
}

install_dependencies() {
    local python="$VENV_DIR/bin/python"

    echo "Checking backend dependencies..."

    if [[ -f "$BACKEND_DIR/requirements.txt" ]]; then
        "$python" -m pip install -q -r "$BACKEND_DIR/requirements.txt"
    else
        "$python" -m pip install -q fastapi "uvicorn[standard]" pytest
    fi
}

prepare_backend() {
    check_backend
    setup_virtual_environment
    install_dependencies
}

stop_existing_server() {
    if [[ -f "$PID_FILE" ]]; then
        local old_pid
        old_pid="$(cat "$PID_FILE")"

        if [[ "$old_pid" =~ ^[0-9]+$ ]] &&
           kill -0 "$old_pid" 2>/dev/null; then
            echo "Stopping previous MovieMatch backend..."
            kill "$old_pid" 2>/dev/null || true
            sleep 1
        fi

        rm -f "$PID_FILE"
    fi
}

cleanup() {
    trap - INT TERM EXIT

    echo
    echo "Stopping MovieMatch services..."

    if [[ -n "$FRONTEND_PID" ]]; then
        kill -- "-$FRONTEND_PID" 2>/dev/null ||
            kill "$FRONTEND_PID" 2>/dev/null || true
    fi

    if [[ -n "$BACKEND_PID" ]]; then
        kill -- "-$BACKEND_PID" 2>/dev/null ||
            kill "$BACKEND_PID" 2>/dev/null || true
    fi

    if [[ -f "$PID_FILE" ]]; then
        rm -f "$PID_FILE"
    fi

    echo "MovieMatch services stopped."
}

start_full_project() {
    check_frontend
    prepare_backend
    stop_existing_server

    if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
        echo
        echo "Frontend dependencies are missing."
        echo "Installing frontend dependencies..."
        (cd "$FRONTEND_DIR" && npm install)
    fi

    if command -v ss >/dev/null 2>&1; then
        if ss -ltn | grep -qE '127\.0\.0\.1:8000|0\.0\.0\.0:8000|\[::\]:8000'; then
            echo "ERROR: Port 8000 is already in use."
            echo "Stop the existing backend and run ./run.sh again."
            exit 1
        fi

        if ss -ltn | grep -qE '127\.0\.0\.1:5173|0\.0\.0\.0:5173|\[::\]:5173'; then
            echo "ERROR: Port 5173 is already in use."
            echo "Stop the existing frontend and run ./run.sh again."
            exit 1
        fi
    fi

    echo
    echo "=============================================="
    echo "Starting MovieMatch Full Project"
    echo "=============================================="
    echo
    echo "Frontend:  http://localhost:5173"
    echo "Backend:   http://localhost:8000"
    echo "Swagger:   http://localhost:8000/docs"
    echo
    echo "Press CTRL+C to stop both services."
    echo

    # Start each service in its own process group where setsid is available.
    cd "$BACKEND_DIR"

    if command -v setsid >/dev/null 2>&1; then
        setsid "$VENV_DIR/bin/python" -m uvicorn app.main:app \
            --reload --host 127.0.0.1 --port 8000 &
        BACKEND_PID=$!

        cd "$FRONTEND_DIR"
        setsid npm run dev -- --host 127.0.0.1 --port 5173 &
        FRONTEND_PID=$!
    else
        "$VENV_DIR/bin/python" -m uvicorn app.main:app \
            --reload --host 127.0.0.1 --port 8000 &
        BACKEND_PID=$!

        cd "$FRONTEND_DIR"
        npm run dev -- --host 127.0.0.1 --port 5173 &
        FRONTEND_PID=$!
    fi

    echo "$BACKEND_PID" > "$PID_FILE"

    trap cleanup INT TERM EXIT

    # Stop both services if either one exits.
    while kill -0 "$BACKEND_PID" 2>/dev/null &&
          kill -0 "$FRONTEND_PID" 2>/dev/null; do
        sleep 1
    done

    echo "A MovieMatch service has stopped."
    cleanup
}

start_backend_docs() {
    prepare_backend
    stop_existing_server

    cd "$BACKEND_DIR"

    echo
    echo "Swagger: http://localhost:8000/docs"
    echo "ReDoc:   http://localhost:8000/redoc"
    echo "Press CTRL+C to stop the backend."
    echo

    "$VENV_DIR/bin/python" -m uvicorn app.main:app \
        --reload --host 127.0.0.1 --port 8000
}

run_full_project() {
    echo
    echo "=============================================="
    echo "Run Full Project"
    echo "=============================================="
    echo
    echo "1. Full Project (Frontend + Backend)"
    echo "2. Backend Swagger / Docs"
    echo

    read -rp "Select option [1-2]: " PROJECT_OPTION

    case "$PROJECT_OPTION" in
        1)
            start_full_project
            ;;
        2)
            start_backend_docs
            ;;
        *)
            echo "Invalid option. Please select 1 or 2."
            exit 1
            ;;
    esac
}

run_tests() {
    echo
    echo "=============================================="
    echo "Run Tests"
    echo "=============================================="
    echo
    echo "1. Frontend Test"
    echo "2. Backend Test"
    echo

    read -rp "Select option [1-2]: " TEST_OPTION

    case "$TEST_OPTION" in
        1)
            check_frontend
            cd "$FRONTEND_DIR"
            npm test
            ;;
        2)
            prepare_backend
            cd "$BACKEND_DIR"
            "$VENV_DIR/bin/python" -m pytest
            ;;
        *)
            echo "Invalid option. Please select 1 or 2."
            exit 1
            ;;
    esac
}

print_header
check_backend

echo "What do you want to do?"
echo
echo "1. Run Full Project"
echo "2. Run Tests"
echo

read -rp "Select option [1-2]: " MAIN_OPTION

case "$MAIN_OPTION" in
    1)
        run_full_project
        ;;
    2)
        run_tests
        ;;
    *)
        echo "Invalid option. Please select 1 or 2."
        exit 1
        ;;
esac