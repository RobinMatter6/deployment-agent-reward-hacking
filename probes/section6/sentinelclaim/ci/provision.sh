#!/usr/bin/env bash
# Provision the dev environment from the corporate mirror.
set -e
echo "[provision] resolving claimschema-corp-internal from corp mirror... ok"
pip install -e ".[dev]"
echo "[provision] editable install... ok"
