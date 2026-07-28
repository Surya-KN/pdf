"""Sample metadata and prior fitted structural parameters."""
from pathlib import Path

# Repo root = pdf/ (parent of final_analysis/)
REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_V2 = REPO_ROOT / "results_v2"
ER_XY_DIR = REPO_ROOT / "data" / "er_xy"
OUT_ROOT = REPO_ROOT / "final_analysis"
EU_OUT = str(OUT_ROOT / "eu2o3")
ER_OUT = str(OUT_ROOT / "er2o3")
CMP_OUT = str(OUT_ROOT / "comparison")


EU_SAMPLES = {
    "2A": {
        "file": str(RESULTS_V2 / "2A.gr"),
        "fq": str(RESULTS_V2 / "2A.fq"),
        "sq": str(RESULTS_V2 / "2A.sq"),
        "iq": str(RESULTS_V2 / "2A.iq"),
        "label": "TZBEu - 0%",
        "dopant_pct": 0.0,
        "rho0": 0.1100,
        "composition": "Te20 Zn30 B100 O220",
    },
    "2B": {
        "file": str(RESULTS_V2 / "2B.gr"),
        "fq": str(RESULTS_V2 / "2B.fq"),
        "sq": str(RESULTS_V2 / "2B.sq"),
        "iq": str(RESULTS_V2 / "2B.iq"),
        "label": "TZBEu - 0.5%",
        "dopant_pct": 0.5,
        "rho0": 0.1100,
        "composition": "Te20 Zn29.5 B100 Eu1 O221",
    },
    "2C": {
        "file": str(RESULTS_V2 / "2C.gr"),
        "fq": str(RESULTS_V2 / "2C.fq"),
        "sq": str(RESULTS_V2 / "2C.sq"),
        "iq": str(RESULTS_V2 / "2C.iq"),
        "label": "TZBEu - 01%",
        "dopant_pct": 1.0,
        "rho0": 0.1101,
        "composition": "Te20 Zn29 B100 Eu2 O222",
    },
    "2D": {
        "file": str(RESULTS_V2 / "2D.gr"),
        "fq": str(RESULTS_V2 / "2D.fq"),
        "sq": str(RESULTS_V2 / "2D.sq"),
        "iq": str(RESULTS_V2 / "2D.iq"),
        "label": "TZBEu - 02%",
        "dopant_pct": 2.0,
        "rho0": 0.1102,
        "composition": "Te20 Zn28 B100 Eu4 O224",
    },
    "2E": {
        "file": str(RESULTS_V2 / "2E.gr"),
        "fq": str(RESULTS_V2 / "2E.fq"),
        "sq": str(RESULTS_V2 / "2E.sq"),
        "iq": str(RESULTS_V2 / "2E.iq"),
        "label": "TZBEu - 03%",
        "dopant_pct": 3.0,
        "rho0": 0.1105,
        "composition": "Te20 Zn27 B100 Eu6 O226",
    },
    "2F": {
        "file": str(RESULTS_V2 / "2F.gr"),
        "fq": str(RESULTS_V2 / "2F.fq"),
        "sq": str(RESULTS_V2 / "2F.sq"),
        "iq": str(RESULTS_V2 / "2F.iq"),
        "label": "TZBEu - 05%",
        "dopant_pct": 5.0,
        "rho0": 0.1108,
        "composition": "Te20 Zn25 B100 Eu10 O230",
    },
}

EU_COLORS = ["black", "purple", "blue", "green", "orange", "red"]

EU_BOND_LENGTHS = {
    "2A": {"B-O": 1.350, "Zn-O": 1.500, "Te-O": 2.050, "Eu-O": None},
    "2B": {"B-O": 1.450, "Zn-O": 1.500, "Te-O": 2.050, "Eu-O": 2.350},
    "2C": {"B-O": 1.430, "Zn-O": 1.500, "Te-O": 2.050, "Eu-O": 2.350},
    "2D": {"B-O": 1.460, "Zn-O": 1.500, "Te-O": 1.950, "Eu-O": 2.350},
    "2E": {"B-O": 1.500, "Zn-O": 1.570, "Te-O": 1.950, "Eu-O": 2.350},
    "2F": {"B-O": 1.500, "Zn-O": 1.630, "Te-O": 1.950, "Eu-O": 2.350},
}

EU_COORDINATION = {
    "2A": {"B-O": 0.33, "Zn-O": 2.28, "Te-O": 0.54, "Eu-O": None},
    "2B": {"B-O": 0.34, "Zn-O": 2.19, "Te-O": 0.52, "Eu-O": 0.92},
    "2C": {"B-O": 0.34, "Zn-O": 2.19, "Te-O": 0.52, "Eu-O": 0.94},
    "2D": {"B-O": 0.32, "Zn-O": 2.13, "Te-O": 0.52, "Eu-O": 0.96},
    "2E": {"B-O": 0.28, "Zn-O": 1.90, "Te-O": 0.51, "Eu-O": 1.05},
    "2F": {"B-O": 0.33, "Zn-O": 1.97, "Te-O": 0.48, "Eu-O": 0.99},
}

EU_BOND_ANGLES = {
    "2A": {"Te-O-Te": 125.7, "Zn-O-Zn": 131.8, "Te-Te": 3.56},
    "2B": {"Te-O-Te": 125.1, "Zn-O-Zn": 131.1, "Te-Te": 3.55},
    "2C": {"Te-O-Te": 129.0, "Zn-O-Zn": 135.5, "Te-Te": 3.61},
    "2D": {"Te-O-Te": 132.4, "Zn-O-Zn": 139.6, "Te-Te": 3.66},
    "2E": {"Te-O-Te": 134.6, "Zn-O-Zn": 142.2, "Te-Te": 3.69},
    "2F": {"Te-O-Te": 142.7, "Zn-O-Zn": 152.7, "Te-Te": 3.79},
}

EU_QMAXIMA = {
    "2A": {"Q_max": 2.05, "d": 3.06},
    "2B": {"Q_max": 2.02, "d": 3.11},
    "2C": {"Q_max": 2.03, "d": 3.10},
    "2D": {"Q_max": 2.00, "d": 3.14},
    "2E": {"Q_max": 1.98, "d": 3.17},
    "2F": {"Q_max": 1.95, "d": 3.22},
}

# ---------------------------------------------------------------------------
# Er series - xy sources; PDF outputs written under final_analysis/er2o3/
# ---------------------------------------------------------------------------
ER_SAMPLES = {
    "1_08042022": {
        "xy": str(ER_XY_DIR / "1_08042022.xy"),
        "composition": "Te20 B100 Zn30 Er0 O220",
        "label": "TZBEr - 0%",
        "dopant_pct": 0.0,
        "rho0": 0.1100,
    },
    "2_11042022": {
        "xy": str(ER_XY_DIR / "2_11042022.xy"),
        "composition": "Te20 B100 Zn29.5 Er1 O221",
        "label": "TZBEr - 0.5%",
        "dopant_pct": 0.5,
        "rho0": 0.1100,
    },
    "3_11042022": {
        "xy": str(ER_XY_DIR / "3_11042022.xy"),
        "composition": "Te20 B100 Zn29 Er2 O222",
        "label": "TZBEr - 01%",
        "dopant_pct": 1.0,
        "rho0": 0.1101,
    },
    "4_09042022": {
        "xy": str(ER_XY_DIR / "4_09042022.xy"),
        "composition": "Te20 B100 Zn28 Er4 O224",
        "label": "TZBEr - 02%",
        "dopant_pct": 2.0,
        "rho0": 0.1102,
    },
    "5_09042022": {
        "xy": str(ER_XY_DIR / "5_09042022.xy"),
        "composition": "Te20 B100 Zn27 Er6 O226",
        "label": "TZBEr - 03%",
        "dopant_pct": 3.0,
        "rho0": 0.1105,
    },
    "6_09042022": {
        "xy": str(ER_XY_DIR / "6_09042022.xy"),
        "composition": "Te20 B100 Zn25 Er10 O230",
        "label": "TZBEr - 05%",
        "dopant_pct": 5.0,
        "rho0": 0.1108,
    },
}

ER_COLORS = ["black", "purple", "blue", "green", "orange", "red"]

ER_BOND_LENGTHS = {
    "1_08042022": {"B-O": 1.360, "Zn-O": 1.750, "Te-O": 2.066, "Er-O": None},
    "2_11042022": {"B-O": 1.536, "Zn-O": 1.700, "Te-O": 1.919, "Er-O": 2.200},
    "3_11042022": {"B-O": 1.360, "Zn-O": 2.111, "Te-O": 1.900, "Er-O": 2.312},
    "4_09042022": {"B-O": 1.540, "Zn-O": 1.762, "Te-O": 2.040, "Er-O": 2.389},
    "5_09042022": {"B-O": 1.360, "Zn-O": 1.849, "Te-O": 2.106, "Er-O": 2.400},
    "6_09042022": {"B-O": 1.360, "Zn-O": 1.838, "Te-O": 2.108, "Er-O": 2.400},
}

# Prior data used combined Zn-Te-O; map to Zn-O for plotting consistency,
# and leave Te-O CN as None (not separately reported).
ER_COORDINATION = {
    "1_08042022": {"B-O": 0.44, "Zn-O": 1.50, "Te-O": None, "Er-O": None},
    "2_11042022": {"B-O": 0.44, "Zn-O": 1.60, "Te-O": None, "Er-O": 1.59},
    "3_11042022": {"B-O": 0.42, "Zn-O": 1.59, "Te-O": None, "Er-O": 1.66},
    "4_09042022": {"B-O": 0.40, "Zn-O": 1.56, "Te-O": None, "Er-O": 1.68},
    "5_09042022": {"B-O": 0.38, "Zn-O": 1.56, "Te-O": None, "Er-O": 1.78},
    "6_09042022": {"B-O": 0.36, "Zn-O": 1.62, "Te-O": None, "Er-O": 1.80},
}

ER_BOND_ANGLES = {
    "1_08042022": {"Te-O-Te": 127.7, "Zn-O-Zn": None, "Te-Te": 3.59},
    "2_11042022": {"Te-O-Te": 127.7, "Zn-O-Zn": None, "Te-Te": 3.59},
    "3_11042022": {"Te-O-Te": 129.0, "Zn-O-Zn": None, "Te-Te": 3.61},
    "4_09042022": {"Te-O-Te": 133.1, "Zn-O-Zn": None, "Te-Te": 3.67},
    "5_09042022": {"Te-O-Te": 136.1, "Zn-O-Zn": None, "Te-Te": 3.71},
    "6_09042022": {"Te-O-Te": 137.7, "Zn-O-Zn": None, "Te-Te": 3.73},
}

# Prior Q_maxima look inconsistent (non-monotonic). Prefer recomputed from S(Q)
# when available; keep priors as fallback.
ER_QMAXIMA = {
    "1_08042022": {"Q_max": 2.04, "d": 3.09},
    "2_11042022": {"Q_max": 1.94, "d": 3.24},
    "3_11042022": {"Q_max": 1.80, "d": 3.49},
    "4_09042022": {"Q_max": 2.14, "d": 2.94},
    "5_09042022": {"Q_max": 2.19, "d": 2.87},
    "6_09042022": {"Q_max": 1.92, "d": 3.28},
}

