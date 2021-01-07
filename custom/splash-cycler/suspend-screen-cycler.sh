#!/bin/bash --
#TODO

scriptdir="${BASH_SOURCE%/*}"
if [[ ! -d "$scriptdir" ]];
then
  scriptdir="$PWD"
fi

echo $(date) >> "$scriptdir/status.txt"

