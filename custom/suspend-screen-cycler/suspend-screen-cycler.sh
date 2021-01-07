#!/bin/bash --
#
# This script replaces the sleep/suspended screen of the reMarkable2.

# Get the directory this script is located at (not from where it's called!)
scriptdir="${BASH_SOURCE%/*}"
if [[ ! -d "$scriptdir" ]];
then
  scriptdir="$PWD"
fi

# Load currently used index from disk (or initialize upon first run):
idxfile=$scriptdir/suspend-cycler.index
if [[ -f "$idxfile" ]]
then
  idx=$(cat "$idxfile" | xargs)
else
  idx=-1
fi

# List all suitable suspend screens
files=($(find "$scriptdir/splash-screens" -type f -name "suspended-*png"))

if [ ${#files[@]} -eq 0 ]
then
  echo "[ERROR] No custom suspend screens available!"
else
  # Increment index
  flen=${#files[@]}
  idx=$((($idx + 1) % $flen))
  src=${files[$idx]}
  # Replace the sleep screen
  cp "$src" /usr/share/remarkable/suspended.png
  # Store currently used index
  echo $idx > $idxfile
fi

