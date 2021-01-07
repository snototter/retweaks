#!/bin/bash --
# Disable & stop service, clean up installed file(s)

set -e
source ../bashfun.sh

svcname="custom-suspend-screen"
uninstall_systemd_unit "${svcname}.timer"
uninstall_systemd_unit "${svcname}.service"

