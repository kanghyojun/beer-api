import typing

from sqlalchemy.engine import Engine, create_engine as create_engine_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm.session import Session as Sess, sessionmaker

__all__ = 'Base', 'Session', 'create_engine'
Base: DeclarativeMeta = declarative_base()
Session: Sess = sessionmaker()


def create_engine(config: typing.Mapping) -> Engine:
    assert config['database']['url'], "config['database']['url'] required."
    return create_engine_(config['database']['url'])
