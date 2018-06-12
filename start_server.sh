#!/usr/bin/env bash

CWD=`pwd -P`
export PYTHONPATH=$PYTHONPATH:$CWD/ramsey_server/
python ramsey_server/app.py