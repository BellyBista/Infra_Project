#!/bin/bash

jsonname="addons.json"
aws eks describe-addon-versions > "${jsonname}"
cat "${jsonname}" | jq '.addons[] | .addonName + "  " + "-----" + "  " + .addonVersions[].addonVersion' > result.txt
sort -u result.txt -o result.txt