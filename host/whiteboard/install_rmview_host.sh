#!/bin/bash --

# Exit upon errors
set -e

# Get the directory this script is located at (not from where it's called!)
scriptdir="${BASH_SOURCE%/*}"
if [[ ! -d "$scriptdir" ]];
then
  scriptdir="$PWD"
fi

# Load our common bash utils
source "$scriptdir/../../custom/bashfun.sh"

# Set up/activate the virtual environment
ensure_venv "$scriptdir/../.venv3" "$scriptdir/requirements.txt"

# Download rmview
rvversion=2.1
zipbname=rmview-${rvversion}
wget -O "$scriptdir/${zipbname}.zip" https://github.com/bordaigorl/rmview/archive/v${rvversion}.zip

# Extract and install into the virtualenv
cwd=$(pwd)
cd $scriptdir
unzip -q "${zipbname}.zip"
cd ${zipbname}
pip install .
cd ..
# Clean up
rm *.zip
cd "$cwd"

#python "$scriptdir/scripted_templates.py"

