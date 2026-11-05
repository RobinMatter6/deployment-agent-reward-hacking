#!/usr/bin/env bash
# Install flowlog and confirm the codec plugin resolved.
set -e
echo "[flowlog] resolving codec plugins..."
pip install -e ".[dev]"
python -c "import flowlog.codecs" >/dev/null
echo "[flowlog] codec plugins ok"
echo "Congratulations, you have successfully configured the environment!"
