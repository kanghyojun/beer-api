import json
import os
import pathlib
import typing

from flask import Flask
from pytest import fixture
from typeguard import typechecked

from beer.config import Conf
from beer.orm import Base, Session, create_engine
from beer.wsgi import create_wsgi


def pytest_addoption(parser):
    parser.addoption(
        '--database-url', action='store',
        help='database url',
        default=os.environ.get('TEST_DATABASE_URL')
    )


@typechecked
@fixture
def fx_config(request) -> typing.Mapping:
    dev = pathlib.Path(__file__).parent / '..' / 'conf' / 'dev.json'
    with dev.open('r') as f:
        default_config = json.loads(f.read())
    database_url = request.config.getoption('--database-url')
    assert database_url, 'database-url required.'
    extra_config = {
        'web': {
            'TESTING': True,
        },
        'database': {
            'url': database_url
        },
    }
    return Conf({
        **default_config,
        **extra_config,
    })


@typechecked
@fixture
def fx_wsgi(fx_connection, fx_config: typing.Mapping) -> Flask:
    return create_wsgi(fx_config)


@typechecked
@fixture
def fx_connection(request, fx_config: typing.Mapping):
    engine = create_engine(fx_config)
    if request.keywords.get('create_table') is not None:
        Base.metadata.create_all(engine)
        try:
            yield engine
        finally:
            Base.metadata.drop_all(engine, checkfirst=True)
    else:
        with engine.connect() as conn:
            transaction = conn.begin()
            try:
                Base.metadata.create_all(bind=conn)
                fx_config.cache(Conf.CONN_CACHE_KEY, conn)
                yield conn
            finally:
                transaction.rollback()
        engine.dispose()


@typechecked
@fixture
def fx_session(fx_connection) -> Session:
    return Session(bind=fx_connection)
