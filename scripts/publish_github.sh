#!/bin/sh
set -eu

REPO="guangcansu/GIS-LCA"
REMOTE_URL="https://github.com/$REPO.git"

set_origin() {
  if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REMOTE_URL"
  else
    git remote add origin "$REMOTE_URL"
  fi
}

PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m regionalized_lca_adapter adapt \
  --metadata examples/manufacturing_metadata.json \
  --inventory examples/manufacturing_inventory.csv \
  --output examples/manufacturing_adapted.json

if gh repo view "$REPO" >/dev/null 2>&1; then
  set_origin
  git push -u origin main
else
  gh repo create "$REPO" \
    --public \
    --description "A lightweight geography normalization and regional factor adapter for LCA workflows."
  set_origin
  git push -u origin main
fi
