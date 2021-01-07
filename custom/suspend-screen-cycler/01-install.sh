#!/bin/bash --
#
# Installs the sleep/suspended screen cycler service (to be run at each
# system startup, just before xochitl loads the suspend screen).
#
#
# Limitations on reMarkable2 (my observations after two 
# evenings of trial & error):
#
# * Cannot use standard suspend/sleep targets, because systemd-suspend is not used.
#
# * Cannot use 'systemd-analyze calendar "..."' on rm2, because it is not installed.
#
# * Cannot use a timer to change the sleep screen every X hours, because xochitl 
#   loads the suspend screen upon start. Thus, the timer solution would require
#   restarting xochitl, which obviously is not a good idea. 

set -e
source ../bashfun.sh

# TODO install custom screens during installation (poweroff-xxx, suspend-xxx, starting-xxx...) and set up cycler-idx file

svcunit="custom-suspend-screen"
scriptdir=$(rec_resolve_dir ${BASH_SOURCE[0]})
install_service "$svcunit" true "$scriptdir"
