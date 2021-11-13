#!/bin/bash --

#TODO Templates I'll probably never need:
# "Dots S bottom"
# "Dots S top"
# "Grid bottom"
# "Grid top"
# "Lined bottom"
# "Lined top"
# "US College"
# "US Legal" < might be useful
# "Weekplanner US"

# Get the directory this script is located at (not from where it's called!)
scriptdir="${BASH_SOURCE%/*}"
if [[ ! -d "$scriptdir" ]];
then
  scriptdir="$PWD"
fi

# Load our common bash utils
source "$scriptdir/custom/bashfun.sh"

# Run the python script to upload to MY device
ensure_venv "$scriptdir/venv" "$scriptdir/requirements.txt"
python "$scriptdir/install_templates.py" --host nyt --overwrite
