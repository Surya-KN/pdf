# PDF analysis (Eu2O3 / Er2O3 doped Te-Zn-B glasses)

Pair-distribution-function (PDF) analysis of lab XRD data for **Eu2O3** (TZBEu) and **Er2O3** (TZBEr) doping series, processed with pdfgetx3 / DiffPy.

## Layout

```
pdf/
  README.md
  results_v2/              # Eu series PDF outputs (.gr/.sq/.fq/.iq)
  data/
    eu_results_v2/         # copy of essential Eu PDF files
    er_xy/                 # Er series source XRD (.xy)
  final_analysis/
    eu2o3/                 # Eu plots + text summaries
    er2o3/                 # Er PDF outputs + plots + text (+ configs/)
    comparison/            # Eu vs Er comparison figures
    scripts/               # analysis pipeline
```

## Series

| Series | Samples | Dopant levels |
|--------|---------|---------------|
| Eu (TZBEu) | 2A-2F | 0, 0.5, 1, 2, 3, 5% Eu2O3 |
| Er (TZBEr) | 1_08042022 ... 6_09042022 | 0, 0.5, 1, 2, 3, 5% Er2O3 |

## Re-run (WSL + pdfgetx3-env)

Paths in `final_analysis/scripts/series_data.py` are **repo-relative** (resolved from this repository root).

```bash
cd /mnt/d/pdfxrd/pdf/final_analysis/scripts
# optional: export PDFGETX3_ENV=/mnt/d/pdfxrd/pdfgetx3-env
bash run_all.sh
```

Or step-by-step:

```bash
source /mnt/d/pdfxrd/pdfgetx3-env/bin/activate
cd /mnt/d/pdfxrd/pdf/final_analysis/scripts
python run_er_pdfgetx3.py
python generate_series_plots.py --series eu
python generate_series_plots.py --series er
python generate_comparison.py
python verify_outputs.py
```

Plot-only verification (no pdfgetx3) needs NumPy/Matplotlib and the committed PDF files under `results_v2/` and `final_analysis/er2o3/`.

## Notes for cloud agents

- Do **not** expect `Lib/`, `Scripts/`, or a local venv in this repo (gitignored).
- Eu inputs: `results_v2/{2A-2F}.{gr,sq,fq,iq}`.
- Er inputs for regeneration: `data/er_xy/*.xy`; committed Er PDF outputs live in `final_analysis/er2o3/`.
- Outputs: `final_analysis/{eu2o3,er2o3,comparison}/`.
