#!/bin/bash

VENV_DIR="venv"

install() {
  ready=true

  # first check if Python3 is installed
  type python3 > /dev/null 2>&1 || {
    echo >&2 "Python3 is required but not installed: https://www.python.org/downloads/";
    ready=false;
  }

  # check if pip3 is installed
  type pip3 > /dev/null 2>&1 || {
    echo >&2 "pip3 is required but not installed: https://pypi.org/project/pip/";
    ready=false;
  }

  # check if virtualenv is installed and install if not
  type virtualenv > /dev/null 2>&1 || {
    echo >&2 "virtualenv is required but not installed";

    # install virtualenv automatically
    if [ $ready = true ]; then
      python3 -m pip install --user virtualenv
    else
      echo "Make sure Python3 and pip3 is installed and rerun setup"
    fi
  }

  if [ $ready = true ]; then
    # check if VENV_DIR exists and create if not
    if [ ! -d "$VENV_DIR" ]; then
      echo "Creating virtual environment $VENV_DIR"
      python3 -m venv $VENV_DIR
    fi

    # shellcheck source=venv/bin/activate
    . "$VENV_DIR/bin/activate"

    pipenv install

    # deactivate virtual environment
   deactivate

  else
    echo "Some requirements are missing. Abort setup"
    exit 1
  fi
}

run() {
  # activate virtual environment
  # shellcheck source=venv/bin/activate
  . "$VENV_DIR/bin/activate"

  python3 proxy.py "$@"

   # deactivate virtual environment
   deactivate
}

# check if the first parameter is 'install' otherwise forward to run
if [ "$1" = "setup" ]; then
  install
else
  if [ -d "$VENV_DIR" ]; then
      # run the fuzzing proxy
      run "$@"
    else
      echo "Virtual environment is not set up. Try running $0 setup"
    fi
fi
