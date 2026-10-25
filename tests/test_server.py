import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import pytest

from app.server import Handler


@pytest.fixture()
def base_url():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def test_health_returns_ok(base_url):
    assert urllib.request.urlopen(base_url + "/health").read() == b"ok"


def test_version_defaults_to_dev(base_url, monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    assert urllib.request.urlopen(base_url + "/version").read() == b"dev"


def test_version_reads_app_version_env(base_url, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "abc123def")
    assert urllib.request.urlopen(base_url + "/version").read() == b"abc123def"


def test_unknown_path_is_404(base_url):
    with pytest.raises(urllib.error.HTTPError) as err:
        urllib.request.urlopen(base_url + "/nope")
    assert err.value.code == 404
