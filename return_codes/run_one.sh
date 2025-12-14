#!/bin/bash

python3 "$1"
echo "Wrapper sees return code from python: $?"
exit

