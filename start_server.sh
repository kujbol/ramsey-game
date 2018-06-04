#!/usr/bin/env bash

CWD=`pwd -P`
export PYTHONPATH=$PYTHONPATH:$CWD/ramsey_server/
gunicorn ramsey_server.app:initialized_app -b 0.0.0.0:$PORT --worker-class aiohttp.worker.GunicornWebWorker