#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Prefer sibling pdfgetx3-env next to repo, else $PDFGETX3_ENV
if [[ -f "${PDFGETX3_ENV:-}/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$PDFGETX3_ENV/bin/activate"
elif [[ -f "$REPO_ROOT/../pdfgetx3-env/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$REPO_ROOT/../pdfgetx3-env/bin/activate"
elif [[ -f "$REPO_ROOT/pdfgetx3-env/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$REPO_ROOT/pdfgetx3-env/bin/activate"
else
  echo "WARNING: pdfgetx3-env not found; using current Python." >&2
fi

cd "$SCRIPT_DIR"

echo "========================================"
echo "1) Re-run pdfgetx3 for Er series"
echo "========================================"
python run_er_pdfgetx3.py

echo ""
echo "========================================"
echo "2) Eu series plots"
echo "========================================"
python generate_series_plots.py --series eu

echo ""
echo "========================================"
echo "3) Er series plots"
echo "========================================"
python generate_series_plots.py --series er

echo ""
echo "========================================"
echo "4) Comparison plots"
echo "========================================"
python generate_comparison.py

echo ""
echo "========================================"
echo "5) Verification"
echo "========================================"
python verify_outputs.py
