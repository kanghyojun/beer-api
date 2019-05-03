#!/usr/bin/env python3
import pathlib
import typing

from alembic.config import CommandLine

from api.config import AlembicConfig, Environment, load_configuration

__all__ = 'AlembicCommand',


class AlembicCommand(CommandLine):

    def __init__(self, prog: typing.Optional = None):
        super().__init__(prog)
        self.parser.add_argument(
            '-e',
            '--environment',
            type=Environment,
            help='An api environment.',
            required=True
        )

    def main(self) -> None:
        options = self.parser.parse_args(None)
        project_root = pathlib.Path(__file__).parent.resolve()
        conf = AlembicConfig(
            load_configuration(project_root / 'conf', options.environment)
        )
        self.run_cmd(conf, options)


if __name__ == '__main__':
    AlembicCommand().main()
