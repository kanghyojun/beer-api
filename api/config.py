import enum
import json
import pathlib
import typing

from alembic.config import Config

__all__ = (
    'AlembicConfig',
    'Conf',
    'Environment',
    'iter_env_configs',
    'load_configuration',
)
T = typing.TypeVar('T')


class Conf(dict):

    _cache: typing.Mapping = {}
    CONN_CACHE_KEY: str = '_test_conn'

    def cache(self, key: str, v: T) -> T:
        self._cache[key] = v

    def cached_property(self, key: str) -> T:
        try:
            v = self._cache[key]
        except KeyError:
            v = None
        finally:
            return v


class AlembicConfig(Config):

    def __init__(self, conf: Conf, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_config = conf
        self.set_main_option('script_location', 'migrations')
        self.set_main_option('sqlalchemy.url', conf['database']['url'])
        self.set_main_option('url', conf['database']['url'])


class Environment(enum.Enum):

    dev = 'dev'

    prod = 'prod'


def iter_env_configs(
    config_path: pathlib.Path,
    environment: Environment
) -> typing.Iterable[pathlib.Path]:
    for path in config_path.iterdir():
        if path.suffix == '.json' and \
                path.name.startswith(f'{environment.value}.'):
            yield path


def load_configuration(config_path: pathlib.Path,
                       environment: Environment) -> typing.Mapping:
    pathes = sorted(
        (p for p in iter_env_configs(config_path, environment)),
        key=lambda p: p.name.split('.')[:-1]
    )
    origin = {}
    for path in pathes:
        with path.open('r') as f:
            try:
                conf = json.loads(f.read())
            except (ValueError, IOError):
                print(f'{path!s} is invalid JSON file')
                raise
            else:
                origin = {**origin, **conf}
    else:
        return Conf(origin)
