import typing

from flask import Flask

from . import __version__
from .context import session

__all__ = 'create_wsgi',


def create_wsgi(config: typing.Mapping) -> Flask:
    app = Flask(__name__)
    @app.route('/ping/', methods=['GET'])
    def ping():
        session.execute('SELECT 1')
        return __version__

    app.config.update(config['web'])
    app.config['CONFIGURATION'] = config
    return app
