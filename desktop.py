"""Desktop entry point for Rental Pro.

Runs the FastAPI app via uvicorn on a background thread (bound to a free local
port) and shows it inside a native desktop window using pywebview. This is what
PyInstaller packages into the distributable .exe.
"""

import socket
import threading
import time
import urllib.request

import uvicorn
import webview

from app import app
from updater import maybe_update

HOST = "127.0.0.1"


class _ThreadedServer(uvicorn.Server):
    """uvicorn installs OS signal handlers on startup, which only works on the
    main thread. We run the server on a worker thread, so disable that."""

    def install_signal_handlers(self):
        pass


def _find_free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _wait_until_ready(port: int, timeout: float = 40.0) -> bool:
    deadline = time.time() + timeout
    url = f"http://{HOST}:{port}/"
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.3)
    return False


def main():
    # Check for a newer release first. If the user accepts an update, this
    # exits the process and relaunches after swapping files (never returns).
    maybe_update()

    port = _find_free_port()

    config = uvicorn.Config(app, host=HOST, port=port, log_level="warning")
    server = _ThreadedServer(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    _wait_until_ready(port)

    webview.create_window(
        "Rental Pro - Agreement Generator",
        f"http://{HOST}:{port}/",
        width=1320,
        height=860,
        min_size=(1024, 700),
    )
    webview.start()

    # Window closed -> ask the server to stop and exit
    server.should_exit = True


if __name__ == "__main__":
    main()
