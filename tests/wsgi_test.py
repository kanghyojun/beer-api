from flask import Flask
from typeguard import typechecked

from api import __version__


@typechecked
def test_ping(fx_wsgi: Flask) -> None:
    client = fx_wsgi.test_client()
    response = client.get('/ping/')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == __version__
