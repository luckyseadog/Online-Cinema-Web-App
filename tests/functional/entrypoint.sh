#!/bin/bash
set -eo pipefail +x

python -m utils.wait_for_es
python -m utils.wait_for_redis
python -m utils.wait_for_postgres

python -m pytest
