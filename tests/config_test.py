import json
import pathlib

from pytest import fixture, raises
from typeguard import typechecked

from api.config import Environment, iter_env_configs, load_configuration


@fixture
def fx_config_dir(tmpdir) -> pathlib.Path:
    d = tmpdir.mkdir('conf')
    dev = d.join('dev.json')
    dev.write(json.dumps({'database': {'url': None}}))
    dev_local = d.join('dev.a.json')
    dev_local.write(json.dumps({'database': {'url': 'abc'}}))
    prod = d.join('prod.json')
    prod.write('wrong')
    return pathlib.Path(str(d))


@typechecked
def test_iter_env_configs(fx_config_dir: pathlib.Path):
    li = sorted(
        p.name
        for p in iter_env_configs(fx_config_dir, Environment.dev)
    )
    assert li[0] == 'dev.a.json'
    assert li[1] == 'dev.json'


@typechecked
def test_load_configuration(fx_config_dir: pathlib.Path):
    config = load_configuration(fx_config_dir, Environment.dev)
    assert config == {'database': {'url': 'abc'}}


@typechecked
def test_load_configuration_error(fx_config_dir: pathlib.Path):
    with raises(ValueError):
        load_configuration(fx_config_dir, Environment.prod)
