import typing

from flask import current_app, request
from sqlalchemy.orm.session import Session as Sess
from werkzeug.local import LocalProxy

from .orm import Session, create_engine


@LocalProxy
def current_config() -> typing.Mapping:
    return current_app.config['CONFIGURATION']


@LocalProxy
def session() -> Sess:
    ctx = request._get_current_object()
    try:
        session = ctx._current_session
    except AttributeError:
        test_connection = current_config.cached_property(
            current_config.CONN_CACHE_KEY
        )
        ctx._current_session = session = Session(
            bind=test_connection or create_engine(current_config)
        )
    finally:
        return session
