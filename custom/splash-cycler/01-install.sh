#!/bin/bash --

source ../bashfun.sh

scriptdir=$(rec_resolve_dir ${BASH_SOURCE[0]})
install_service custom-splash-screens "$scriptdir"

