#!/bin/bash

set -x

source ../function.sh

environment
install_checkov
dir
testing
checkov -f ${TF_PLAN}.json
apply