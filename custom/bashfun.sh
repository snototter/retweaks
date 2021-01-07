#!/bin/bash --
#
# Custom bash functions

#function testfx
#{
#  if [ "$1" = true ]
#  then
#    echo "$1 is TRUE"
#  else
#    echo "$1 is FALSE"
#  fi
#}

function rec_resolve_dir
{
  # Recursively resolves the given directory. Taken from https://stackoverflow.com/a/246128/400948
  src="$1"
  while [ -h "$src" ]; do # resolve $src until the file is no longer a symlink
      dname="$( cd -P "$( dirname "${src}" )" >/dev/null 2>&1 && pwd )"
      src="$(readlink "${src}")"
      # if $src was a relative symlink, we need to resolve it relative to the path where the symlink file was located
      [[ $src != /* ]] && SOURCE="${dname}/${src}"
  done
  resdir="$(cd -P "$( dirname "${src}" )" >/dev/null 2>&1 && pwd)"
  echo "${resdir}"
}


function uninstall_systemd_unit
{
  # Disables, stops and removes the /etc/systemd/system/$1 file
  # Can be either a .service or a .timer file.
  #
  # Params:
  # $1 NAME_OF_UNIT (including extension)
  svc=$1
  echo "Uninstalling $svc"
  systemctl disable $svc
  systemctl stop $svc
  rm -f /etc/systemd/system/$svc
  systemctl daemon-reload
}

function install_service
{
  # Installs the "$1".service file (must be located within the current directory)
  # into /etc/systemd/system/ and replaces my custom placeholders 
  #
  # Params:
  # $1 NAME_OF_SERVICE (without extension)
  # $2 ENABLE_AND_START (flag, must be true or false)
  # $3 SCRIPTPATH (forward slashes are allowed)
  enablesvc=$2
  scriptpath=$3

  svc=$1.service
  sysvc=/etc/systemd/system/$svc

  if [ -f "${sysvc}" ]
  then
    echo "Stopping previously registered service unit: ${sysvc}"
    systemctl stop $svc
  fi
  

  # Create/replace the service file
  cp $svc /etc/systemd/system
  sed -i "s|SCRIPTPATH|$scriptpath|g" "$sysvc"

  echo "Registering service '$svc'"

  # Reload and enable service
  if [ "$enablesvc" = true ]
  then
    systemctl daemon-reload
    systemctl enable $svc
    systemctl start $svc
  fi
}


function install_timer
{
  # Installs the "$1".timer file (must be located within the current directory)
  # into /etc/systemd/system/ and replaces my custom placeholders 
  #
  # Params:
  # $1 NAME_OF_TIMER (without extension)
  # $2 TIMERSPECIFICATION
  timerspec=$2

  svc=$1.timer
  sysvc=/etc/systemd/system/$svc

  if [ -f "${sysvc}" ]
  then
    echo "Stopping previously registered timer unit: ${sysvc}"
    systemctl stop $svc || true
  fi
  

  # Create/replace the service file
  cp $svc /etc/systemd/system
  sed -i "s/TIMERSPECIFICATION/$timerspec/g" "$sysvc"

  echo "Registering timer '$svc'"

  # Reload and enable timer
  systemctl daemon-reload
  systemctl enable $svc
  systemctl start $svc
}

