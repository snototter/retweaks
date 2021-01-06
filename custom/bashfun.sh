#!/bin/bash --
#
# Custom bash functions

function rec_resolve_dir
{
  # Recursively resolve the given directory. Adapted from https://stackoverflow.com/a/246128/400948
  src="$1"
  while [ -h "$src" ]; do # resolve $src until the file is no longer a symlink
      dname="$( cd -P "$( dirname "$src" )" >/dev/null 2>&1 && pwd )"
      src="$(readlink "$src")"
      # if $src was a relative symlink, we need to resolve it relative to the path where the symlink file was located
      [[ $src != /* ]] && SOURCE="$dname/$Ssrc"
  done
  resdir="$(cd -P "$( dirname "$src" )" >/dev/null 2>&1 && pwd)"
  echo "$resdir"
}


function install_service
{
  # Installs the "$1".service file (must be located within the current directory)
  # into /etc/systemd/system/ and replaces my custom placeholders 
  #
  # Params:
  # $1 NAME_OF_SERVICE (without extension)
  # $2 SCRIPTPATH (forward slashes are allowed)
  scriptpath=$2

  svc=$1.service
  sysvc=/etc/systemd/system/$svc

  if [ -f "$sysvc" ]
  then
    # Stop and disable previously registered instances
    echo "Need to stop/disable previously registered instance ($sysvc):"
    systemctl disable $svc
    systemctl stop $svc
  fi
  

  # Create/replace the service file
  cp $svc /etc/systemd/system
  sed -i "s|SCRIPTPATH|$scriptpath|g" "$sysvc"

  echo "Registering service '$svc'"

  # Reload and enable service
  systemctl daemon-reload
  systemctl enable $svc
  systemctl start $svc
}
