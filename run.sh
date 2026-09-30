#!/bin/bash

# ============================================================
# MovieMatch Development Runner
# ============================================================
#
# This script is for LOCAL DEVELOPMENT only.
#
# Every time the script starts, it asks what you want to do:
#
#   1. Run Full Project
#   2. Run Tests
#
# Currently the project contains only the backend.
# Frontend support can be added later.
# ============================================================

set -e

# ------------------------------------------------------------
# Project paths
# ------------------------------------------------------------

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
VENV_DIR="$BACKEND_DIR/.venv"

cd "$PROJECT_ROOT"


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

print_header() {
    clear
    echo "=============================================="
    echo "           MovieMatch Development"
    echo "=============================================="
    echo
}

check_backend() {
    if [ ! -d "$BACKEND_DIR" ]; then
        echo "ERROR: Backend directory not found."
        echo
        echo "Expected:"
        echo "  $BACKEND_DIR"
        echo
        exit 1
    fi
}

setup_virtual_environment() {

    if [ ! -d "$VENV_DIR" ]; then
        echo
        echo "Python virtual environment not found."
        echo "Creating backend virtual environment..."
        echo

        python3 -m venv "$VENV_DIR"

        echo
        echo "Virtual environment created."
    fi
}


install_dependencies() {

    PYTHON="$VENV_DIR/bin/python"

    if [ -f "$BACKEND_DIR/requirements.txt" ]; then

        echo
        echo "Checking backend dependencies..."
        echo

        "$PYTHON" -m pip install -q -r "$BACKEND_DIR/requirements.txt"

    else

        echo
        echo "requirements.txt not found."
        echo "Installing required development packages..."
        echo

        "$PYTHON" -m pip install \
            fastapi \
            "uvicorn[standard]" \
            pytest
    fi
}


prepare_backend() {

    check_backend
    setup_virtual_environment
    install_dependencies
}


stop_existing_server() {

    PID_FILE="$BACKEND_DIR/.moviematch-server.pid"

    if [ -f "$PID_FILE" ]; then

        OLD_PID=$(cat "$PID_FILE")

        if kill -0 "$OLD_PID" 2>/dev/null; then

            echo
            echo "Stopping previous MovieMatch server..."
            kill "$OLD_PID" 2>/dev/null || true

            sleep 1

        fi

        rm -f "$PID_FILE"
    fi
}


start_backend() {

    prepare_backend
    stop_existing_server

    cd "$BACKEND_DIR"

    PYTHON="$VENV_DIR/bin/python"

    echo
    echo "=============================================="
    echo "Starting MovieMatch Backend"
    echo "=============================================="
    echo
    echo "Backend:"
    echo "  http://localhost:8000"
    echo
    echo "Swagger:"
    echo "  http://localhost:8000/docs"
    echo
    echo "ReDoc:"
    echo "  http://localhost:8000/redoc"
    echo
    echo "Press CTRL+C to stop the server."
    echo

    "$PYTHON" -m uvicorn app.main:app \
        --reload \
        --host 127.0.0.1 \
        --port 8000 &

    SERVER_PID=$!

    echo "$SERVER_PID" > "$BACKEND_DIR/.moviematch-server.pid"

    trap 'echo; echo "Stopping MovieMatch server..."; kill $SERVER_PID 2>/dev/null || true; rm -f "$BACKEND_DIR/.moviematch-server.pid"; exit 0' INT TERM

    wait "$SERVER_PID"
}


run_full_project() {

    echo
    echo "=============================================="
    echo "Run Full Project"
    echo "=============================================="
    echo
    echo "1. Full Project"
    echo "2. Backend Swagger / Docs"
    echo
    read -rp "Select option [1-2]: " PROJECT_OPTION

    case "$PROJECT_OPTION" in

        1)
            echo
            echo "Selected: Full Project"
            echo
            echo "Currently MovieMatch contains only the backend."
            echo "Starting the backend as the full project..."
            echo

            start_backend
            ;;

        2)
            echo
            echo "Selected: Backend Swagger / Docs"
            echo

            prepare_backend
            stop_existing_server

            cd "$BACKEND_DIR"

            PYTHON="$VENV_DIR/bin/python"

            echo
            echo "=============================================="
            echo "Starting MovieMatch Backend Documentation"
            echo "=============================================="
            echo
            echo "Swagger UI:"
            echo "  http://localhost:8000/docs"
            echo
            echo "ReDoc:"
            echo "  http://localhost:8000/redoc"
            echo
            echo "Press CTRL+C to stop the server."
            echo

            "$PYTHON" -m uvicorn app.main:app \
                --reload \
                --host 127.0.0.1 \
                --port 8000
            ;;

        *)
            echo
            echo "Invalid option."
            echo "Please select 1 or 2."
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
            echo
            echo "Frontend testing is not configured yet."
            echo
            echo "The frontend has not been started in the project."
            echo "This option will be implemented when the frontend"
            echo "and its testing framework are added."
            echo
            ;;

        2)
            echo
            echo "Selected: Backend Test"
            echo

            prepare_backend

            cd "$BACKEND_DIR"

            PYTHON="$VENV_DIR/bin/python"

            echo
            echo "=============================================="
            echo "Running Backend Tests"
            echo "=============================================="
            echo

            "$PYTHON" -m pytest
            ;;

        *)
            echo
            echo "Invalid option."
            echo "Please select 1 or 2."
            exit 1
            ;;
    esac
}


# ------------------------------------------------------------
# Main menu
# ------------------------------------------------------------

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
        echo
        echo "Invalid option."
        echo "Please select 1 or 2."
        exit 1
        ;;
esac