#!/usr/bin/env python3
import argparse
import pathlib
import logging.config

from api.config import Environment, load_configuration
from api.wsgi import create_wsgi

__all__ = 'main',


def main():
    options = [
        (
            ('-e', '--environment'),
            {
                'type': Environment,
                'help': 'An environment.',
                'required': True
            },
        ),
        (
            ('-p', '--port'),
            {
                'type': int,
                'help': 'Server port.',
                'default': 8000
            },
        ),
        (
            ('-d', '--debug'),
            {
                'help': 'debug mode.',
                'action': 'store_true',
            },
        ),
        (
            ('-H', '--host'),
            {
                'type': str,
                'help': 'A host address.',
                'default': '0.0.0.0',
            },
        ),
    ]
    parser = argparse.ArgumentParser(prog='API server runner')
    project_root = pathlib.Path(__file__).parent.resolve()
    for opt, kopt in options:
        parser.add_argument(
            *opt,
            **kopt
        )
    options = parser.parse_args()
    config = load_configuration(project_root / 'conf', options.environment)
    logging.config.dictConfig(config['logging'])
    wsgi = create_wsgi(config)
    if options.environment == Environment.dev:
        wsgi.run(debug=options.debug, port=options.port)
    else:
        raise NotImplementedError('production server')


if __name__ == '__main__':
    main()
