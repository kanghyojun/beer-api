#/usr/bin/env bash
set -e

if [[ "$(git rev-parse --is-inside-work-tree)" != "true" ]];
then
    echo 'Initialize git first.'
    exit 1;
fi

if [[ "$VIRTUAL_ENV" = "" ]];
then
    echo 'You may seems not in virtualenv';
    exit 1;
fi

if [[ "$1" = "-d" ]];
then
    PIP_OPT="-e"
    PIP_INSTALL_PATH=".[tests]"
else
    PIP_OPT=""
    PIP_INSTALL_PATH="."
fi

pip install $PIP_OPT "$PIP_INSTALL_PATH"

if [[ "$(git config core.hooksPath)" = "" ]];
then
    git config core.hooksPath "$PWD/hooks"
fi
