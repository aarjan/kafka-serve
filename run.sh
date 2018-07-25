#!/bin/bash

# load the config
set -o allexport
source ./run.env
set +o allexport

python main.py