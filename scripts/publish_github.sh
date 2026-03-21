#!/bin/sh
set -eu

REPO="guangcansu/GIS-LCA"

PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m regionalized_lca_adapter adapt \
  --metadata examples/manufacturing_metadata.json \
  --inventory examples/manufacturing_inventory.csv \
  --output examples/manufacturing_adapted.json

if gh repo view "$REPO" >/dev/null 2>&1; then
  if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "https://github.com/$REPO.git"
  else
    git remote add origin "https://github.com/$REPO.git"
  fi
  git push -u origin main
else
  gh repo create "$REPO" \
    --public \
    --description "A lightweight geography normalization and regional factor adapter for LCA workflows." \
    --source=. \
    --remote=origin \
    --push
fi
