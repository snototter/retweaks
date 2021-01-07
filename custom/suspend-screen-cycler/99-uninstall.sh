#!/bin/bash --
# Disable & stop service, clean up installed file(s)

set -e
source ../bashfun.sh

uninstall_systemd_unit "custom-suspend-screen.service"

