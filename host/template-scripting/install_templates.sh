#!/bin/bash --

# Get the directory this script is located at (not from where it's called!)
scriptdir="${BASH_SOURCE%/*}"
if [[ ! -d "$scriptdir" ]];
then
  scriptdir="$PWD"
fi

# Load our common bash utils
source "$scriptdir/../../custom/bashfun.sh"

# Run the python script to upload to MY device
ensure_venv "$scriptdir/../.venv3" "$scriptdir/requirements.txt"
python "$scriptdir/install_templates.py" --host nyt --overwrite

