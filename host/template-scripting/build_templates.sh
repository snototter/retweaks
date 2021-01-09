#!/bin/bash --

function ensure_venv
{
  # Source or set up the virtual environment
  # * No param: just create and source .venv3
  # * $1: Name of venv
  # * $2: Path to requirements.txt

  if [[ $# > 0 ]]
  then
    venv=$1
  else
    venv=.venv3
  fi

  if [ ! -d "${venv}" ]
  then
    echo "Setting up virtual environment in [${venv}]"
    python3 -m venv ${venv}
    source ${venv}/bin/activate
    pip3 install --upgrade pip
    if [[ $# > 1 ]]
    then
      pip3 install -r "$2"
    fi
  fi
#TODO if venv exists, update all packages (optionally)?
  source ${venv}/bin/activate
}

function get_fname
{
  # Prints the basename of $1 without extention
  filename=$(basename -- "$1")
  filename="${filename%.*}"
  echo "${filename}"
}

function get_ext
{
  # Prints the extension of $1
  filename="$1"
  extension="${filename##*.}"
  echo "${extension}"
}


ensure_venv .venv3 requirements.txt
python scripted_svg_templates.py

for svg in *.svg
do
  fn=$(get_fname "${svg}")
  inkscape -z -f "${svg}" -w 1404 -h 1872 -j -e "${fn}".png
done

