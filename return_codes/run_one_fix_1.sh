#!/bin/bash

python3 "$1"
ret=$?
echo "Wrapper sees return code from python: $ret"
exit $ret