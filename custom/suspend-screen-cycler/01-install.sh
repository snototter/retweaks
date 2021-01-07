#!/bin/bash --

set -e
source ../bashfun.sh


function print_usage
{
  echo "Usage: ${BASH_SOURCE[0]} [-t oncalendar]"
  echo "  Optionally, specify the OnCalendar argument for the timer via -t"
  echo "  Refer to the date specifications: https://www.freedesktop.org/software/systemd/man/systemd.time.html"
  echo "  and use 'systemd-analyze calendar \"your-datestring\"' to verify."
}


# Default recurrence: run at 06:05, 12:05 and 18:05:
oncal="*-*-* 06,12,18:05:00"
while getopts 't:' 'OPTKEY'
do
  case "${OPTKEY}" in
    't') oncal=${OPTARG};;
    *)
      print_usage
      exit 1
      ;;
  esac
done

# TODO install custom screens during installation (poweroff-xxx, suspend-xxx, starting-xxx...) and set up cycler-idx file

# Cannot verify on remarkable, because systemd-analyze is not installed
#echo "Verifying timer's OnCalendar setting:"
#systemd-analyze calendar "$oncal"

svcunit="custom-suspend-screen"
scriptdir=$(rec_resolve_dir ${BASH_SOURCE[0]})
install_service "$svcunit" false "$scriptdir"
install_timer "$svcunit" "$oncal"