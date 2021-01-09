#!/bin/bash --

# Get the directory this script is located at (not from where it's called!)
scriptdir="${BASH_SOURCE%/*}"
if [[ ! -d "$scriptdir" ]];
then
  scriptdir="$PWD"
fi

# Load our common bash utils
source "$scriptdir/../../custom/bashfun.sh"

# Run the python script inside a virtualenv
ensure_venv ../.venv3 requirements.txt
python scripted_templates.py

