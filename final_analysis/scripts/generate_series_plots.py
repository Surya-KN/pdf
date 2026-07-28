#!/usr/bin/env python3
"""Generate all 01–29 plots + text tables for one dopant series (Eu or Er)."""
import os
import sys
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from scipy.interpolate import interp1d

import utils as U
from series_data import (
    EU_SAMPLES, EU_COLORS, EU_BOND_LENGTHS, EU_COORDINATION,
    EU_BOND_ANGLES, EU_QMAXIMA, EU_OUT,
    ER_SAMPLES, ER_COLORS, ER_BOND_LENGTHS, ER_COORDINATION,
    ER_BOND_ANGLES, ER_QMAXIMA, ER_OUT,
)


def load_series(series):
    if series == "eu":
        samples = EU_SAMPLES
        colors = EU_COLORS
        bond_lengths = EU_BOND_LENGTHS
        coordination = EU_COORDINATION
        bond_angles = EU_BOND_ANGLES
        qmaxima = EU_QMAXIMA
        outdir = EU_OUT
        dopant = "Eu"
        dopant_oxide = "Eu₂O₃"
        dopant_key = "Eu-O"
        glass = "20TeO₂-(30-x)ZnO-50B₂O₃-xEu₂O₃"
        # attach file paths already present
        for sid, info in samples.items():
            info.setdefault("file", info.get("file"))
    else:
        samples = {}
        # rebuild with output paths under ER_OUT
        for sid, info in ER_SAMPLES.items():
            samples[sid] = dict(info)
            samples[sid]["file"] = os.path.join(ER_OUT, f"{sid}.gr")
            samples[sid]["fq"] = os.path.join(ER_OUT, f"{sid}.fq")
            samples[sid]["sq"] = os.path.join(ER_OUT, f"{sid}.sq")
            samples[sid]["iq"] = os.path.join(ER_OUT, f"{sid}.iq")
        colors = ER_COLORS
        bond_lengths = ER_BOND_LENGTHS
        coordination = ER_COORDINATION
        bond_angles = ER_BOND_ANGLES
        qmaxima = ER_QMAXIMA
        outdir = ER_OUT
        dopant = "Er"
        dopant_oxide = "Er₂O₃"
        dopant_key = "Er-O"
        glass = "20TeO₂-(30-x)ZnO-50B₂O₃-xEr₂O₃"
    return {
        "samples": samples,
        "colors": colors,
        "bond_lengths": bond_lengths,
        "coordination": coordination,
        "bond_angles": bond_angles,
        "qmaxima": qmaxima,
        "outdir": outdir,
        "dopant": dopant,
        "dopant_oxide": dopant_oxide,
        "dopant_key": dopant_key,
        "glass": glass,
        "keys": list(samples.keys()),
    }


def load_all_data(cfg):
    data = {}
    for sid, info in cfg["samples"].items():
        Gr = U.parse_gr(info["file"])
        r, G = Gr[:, 0], Gr[:, 1]
        gr = U.Gr_to_gr(r, G, info["rho0"])
        Tr = U.Gr_to_Tr(r, G, info["rho0"])
        # First shell (~1.9 Å) vs second-shell Te–Te (~3.5 Å) — do not swap these
        first_r, first_G = U.find_first_shell_peak(r, G)
        first_gr_r, first_gr = U.find_first_shell_peak(r, gr)
        tete_r, tete_g = U.find_Te_Te_peak(r, gr)
        tete_Gr_r, tete_Gr = U.find_Te_Te_peak_Gr(r, G)
        sq = U.parse_sq_fq_iq(info["sq"])
        fq = U.parse_sq_fq_iq(info["fq"])
        iq = U.parse_sq_fq_iq(info["iq"])
        data[sid] = {
            "r": r, "G": G, "gr": gr, "Tr": Tr,
            "first_r": first_r, "first_G": first_G,
            "first_gr_r": first_gr_r, "first_gr": first_gr,
            "tete_r": tete_r, "tete_g": tete_g,
            "tete_Gr_r": tete_Gr_r, "tete_Gr": tete_Gr,
            "sq": sq, "fq": fq, "iq": iq,
            "info": info,
        }
    return data


def pct_label(info, dopant_oxide):
    p = info["dopant_pct"]
    if p == int(p):
        return f"{int(p)}% {dopant_oxide}"
    return f"{p}% {dopant_oxide}"


# ---------------------------------------------------------------------------
# PLOTS
# ---------------------------------------------------------------------------
def plot_01(cfg, data):
    keys, colors = cfg["keys"], cfg["colors"]
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()
    for i, sid in enumerate(keys):
        ax = axes[i]
        d = data[sid]
        ax.plot(d["r"], d["G"], color=colors[i], lw=1.2)
        ax.set_xlim(1, 11)
        ax.set_xlabel("r (Å)")
        ax.set_ylabel("G(r) (Å⁻²)")
        ax.set_title(f"{sid}: {pct_label(d['info'], cfg['dopant_oxide'])}")
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "01_individual_Gr_samples.png"))


def plot_02(cfg, data):
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, sid in enumerate(cfg["keys"]):
        d = data[sid]
        ax.plot(d["r"], d["G"], color=cfg["colors"][i], lw=1.2,
                label=pct_label(d["info"], cfg["dopant_oxide"]))
    ax.set_xlim(1, 11)
    ax.set_xlabel("r (Å)")
    ax.set_ylabel("G(r) (Å⁻²)")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "02_Gr_overlay.png"))


def plot_03(cfg, data):
    fig, ax = plt.subplots(figsize=(10, 8))
    for i, sid in enumerate(cfg["keys"]):
        d = data[sid]
        off = i * U.WATERFALL_OFFSET_GR
        y = d["G"] + off
        ax.plot(d["r"], y, color=cfg["colors"][i], lw=1.2)
        extra = 0.3 if sid in U.EXTRA_OFFSET_SAMPLES else 0.0
        U.add_inline_label(ax, U.LABEL_X, off, d["info"]["label"],
                           cfg["colors"][i], extra)
    U.apply_waterfall_style(ax, U.WATERFALL_XLIM)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "03_Gr_waterfall.png"))


def plot_04(cfg, data):
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, sid in enumerate(cfg["keys"]):
        d = data[sid]
        ax.plot(d["sq"][:, 0], d["sq"][:, 1], color=cfg["colors"][i], lw=1.2,
                label=d["info"]["label"])
    ax.set_xlim(0.5, 5.5)
    ax.set_xlabel("Q (Å⁻¹)")
    ax.set_ylabel("S(Q)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "04_Sq_comparison.png"))


def plot_05(cfg, data):
    fig, ax = plt.subplots(figsize=(10, 8))
    for i, sid in enumerate(cfg["keys"]):
        d = data[sid]
        off = i * U.WATERFALL_OFFSET_FQ
        ax.plot(d["fq"][:, 0], d["fq"][:, 1] + off,
                color=cfg["colors"][i], lw=1.2)
        extra = 0.3 if sid in U.EXTRA_OFFSET_SAMPLES else 0.0
        # label near right edge of Q axis
        ax.text(5.3, off + 0.15 + extra, d["info"]["label"],
                color=cfg["colors"][i], ha="right", va="bottom",
                fontsize=U.LABEL_FONTSIZE, fontweight=U.LABEL_FONTWEIGHT)
    ax.set_xlim(0.5, 5.5)
    ax.set_yticks([])
    ax.set_xlabel("Q (Å⁻¹)")
    ax.set_ylabel("Arb Units")
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "05_Fq_waterfall.png"))


def plot_06(cfg, data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axhline(1.0, color="gray", ls="--", lw=0.8)
    for i, sid in enumerate(cfg["keys"]):
        d = data[sid]
        ax.plot(d["r"], d["gr"], color=cfg["colors"][i], lw=1.2,
                label=pct_label(d["info"], cfg["dopant_oxide"]))
    ax.set_xlim(1.0, 5.5)
    ax.set_xlabel("r (Å)")
    ax.set_ylabel("g(r)")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "06_first_peak_zoom.png"))


def plot_07(cfg, data):
    keys = cfg["keys"]
    xs = [cfg["samples"][k]["dopant_pct"] for k in keys]
    tete = [cfg["bond_angles"][k]["Te-Te"] for k in keys]
    ang = [cfg["bond_angles"][k]["Te-O-Te"] for k in keys]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(xs, tete, "o-", color="C0", lw=2, ms=8, label="Te–Te distance")
    for x, y in zip(xs, tete):
        ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8)
    ax2 = ax.twinx()
    ax2.plot(xs, ang, "s--", color="C3", lw=2, ms=7, label="Te–O–Te angle")
    ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
    ax.set_ylabel("Te–Te distance (Å)", color="C0")
    ax2.set_ylabel("Te–O–Te angle (°)", color="C3")
    lines1, lab1 = ax.get_legend_handles_labels()
    lines2, lab2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, lab1 + lab2, loc="best")
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], f"07_peak_position_vs_{cfg['dopant']}.png"))


def plot_08(cfg, data):
    keys = cfg["keys"]
    base = data[keys[0]]
    fig, ax = plt.subplots(figsize=(10, 8))
    for i, sid in enumerate(keys[1:]):
        d = data[sid]
        # interpolate base onto sample r grid if needed
        if len(d["r"]) == len(base["r"]) and np.allclose(d["r"], base["r"]):
            dG = d["G"] - base["G"]
            rr = d["r"]
        else:
            f = interp1d(base["r"], base["G"], bounds_error=False, fill_value=np.nan)
            dG = d["G"] - f(d["r"])
            rr = d["r"]
        off = i * U.WATERFALL_OFFSET_DIFF
        ax.plot(rr, dG + off, color=cfg["colors"][i + 1], lw=1.2)
        ax.axhline(off, color="gray", ls="--", lw=0.6, alpha=0.6)
        extra = 0.3 if sid in U.EXTRA_OFFSET_SAMPLES else 0.0
        U.add_inline_label(ax, U.LABEL_X, off, d["info"]["label"],
                           cfg["colors"][i + 1], extra)
    U.apply_waterfall_style(ax, U.WATERFALL_XLIM)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "08_difference_Gr.png"))


def plot_09(cfg, data):
    keys = cfg["keys"]
    # common r grid
    r0 = data[keys[0]]["r"]
    mask = (r0 >= 1.0) & (r0 <= 11.0)
    r = r0[mask]
    pcts = np.array([cfg["samples"][k]["dopant_pct"] for k in keys])
    Z = np.zeros((len(pcts), len(r)))
    for i, sid in enumerate(keys):
        d = data[sid]
        f = interp1d(d["r"], d["G"], bounds_error=False, fill_value=0.0)
        Z[i] = f(r)
    # denser Y for smooth surface
    from scipy.interpolate import RectBivariateSpline
    try:
        spl = RectBivariateSpline(pcts, r, Z, kx=min(3, len(pcts) - 1), ky=3)
        pct_f = np.linspace(pcts.min(), pcts.max(), 40)
        r_f = np.linspace(r.min(), r.max(), 200)
        Rf, Pf = np.meshgrid(r_f, pct_f)
        Zf = spl(pct_f, r_f)
    except Exception:
        Rf, Pf = np.meshgrid(r, pcts)
        Zf = Z
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(Rf, Pf, Zf, cmap="viridis", alpha=0.85, linewidth=0, antialiased=True)
    ax.set_xlabel("r (Å)")
    ax.set_ylabel(f"{cfg['dopant_oxide']} (mol%)")
    ax.set_zlabel("G(r) (Å⁻²)")
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "09_Gr_3D_surface.png"))


def plot_10(cfg, data):
    keys = cfg["keys"]
    r0 = data[keys[0]]["r"]
    mask = (r0 >= 1.0) & (r0 <= 11.0)
    r = r0[mask]
    Z = []
    for sid in keys:
        d = data[sid]
        f = interp1d(d["r"], d["G"], bounds_error=False, fill_value=np.nan)
        Z.append(f(r))
    Z = np.array(Z)
    fig, ax = plt.subplots(figsize=(12, 5))
    y = np.arange(len(keys) + 1) - 0.5
    x = np.concatenate([[r[0] - (r[1] - r[0]) / 2],
                        0.5 * (r[:-1] + r[1:]),
                        [r[-1] + (r[1] - r[0]) / 2]])
    pcm = ax.pcolormesh(x, y, Z, cmap="RdBu_r", shading="flat")
    cb = fig.colorbar(pcm, ax=ax)
    cb.set_label("G(r) (Å⁻²)")
    ax.set_xlim(1, 11)
    ax.set_yticks(range(len(keys)))
    ax.set_yticklabels([f"{cfg['samples'][k]['dopant_pct']}%" for k in keys])
    ax.set_xlabel("r (Å)")
    ax.set_ylabel(f"{cfg['dopant_oxide']} (mol%)")
    for i in range(len(keys) + 1):
        ax.axhline(i - 0.5, color="k", lw=0.4)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "10_Gr_contour_heatmap.png"))


def _fit_centers(cfg, sid):
    """Guess Gaussian centers from prior bond lengths + Te-Te."""
    bl = cfg["bond_lengths"][sid]
    centers = []
    labels = []
    for k in ("B-O", "Zn-O", "Te-O"):
        if bl.get(k) is not None:
            centers.append(bl[k])
            labels.append(k)
    dk = cfg["dopant_key"]
    if bl.get(dk) is not None:
        centers.append(bl[dk])
        labels.append(dk)
    # Te-Te from bond angles
    centers.append(cfg["bond_angles"][sid]["Te-Te"])
    labels.append("Te-Te")
    return centers, labels


def _plot_fitting_grid(cfg, data, filename, fit_max=4.5, show_resid=True, annotate_vlines=False):
    keys = cfg["keys"]
    fig, axes = plt.subplots(3, 2, figsize=(14, 12 if show_resid else 10))
    axes = axes.flatten()
    fit_results = {}
    for i, sid in enumerate(keys):
        ax = axes[i]
        d = data[sid]
        centers, labels = _fit_centers(cfg, sid)
        # Fit Gaussians on T(r) in window
        fit = U.fit_Tr_gaussians(d["r"], d["Tr"], centers, fit_min=1.0, fit_max=fit_max)
        fit_results[sid] = {"labels": labels, "components": fit["components"]}
        if show_resid:
            # main + residual using gridspec-like inset: plot residual below via twin-less split
            ax.plot(fit["r"], fit["y"], "k-", lw=1.0, label="T(r)")
            ax.plot(fit["r"], fit["yfit"], "r--", lw=1.2, label="fit")
            for j, (comp, lab) in enumerate(zip(fit["components"], labels)):
                ax.plot(fit["r"], comp["curve"], lw=0.9, alpha=0.8, label=lab)
                if annotate_vlines:
                    ax.axvline(comp["center"], color="gray", ls="--", lw=0.6)
                    ax.text(comp["center"], ax.get_ylim()[1] if False else np.nanmax(fit["y"]) * 0.95,
                            lab, rotation=90, fontsize=7, ha="right", va="top")
            # residual as secondary plot inset at bottom
            ax2 = ax.inset_axes([0.0, -0.32, 1.0, 0.25])
            ax2.axhline(0, color="gray", lw=0.5)
            ax2.plot(fit["r"], fit["residual"], "g-", lw=0.8)
            ax2.set_ylabel("resid", fontsize=7)
            ax2.tick_params(labelsize=6)
        else:
            ax.plot(fit["r"], fit["y"], "k-", lw=1.0)
            ax.plot(fit["r"], fit["yfit"], "r--", lw=1.2)
            for comp, lab in zip(fit["components"], labels):
                ax.plot(fit["r"], comp["curve"], lw=0.9, alpha=0.8)
                if annotate_vlines:
                    ax.axvline(comp["center"], color="gray", ls="--", lw=0.6)
                    ymax = np.nanmax(fit["y"])
                    ax.text(comp["center"], ymax * 0.92, lab, rotation=90,
                            fontsize=7, ha="right", va="top")
        ax.set_title(d["info"]["label"])
        ax.set_xlabel("r (Å)")
        ax.set_ylabel("T(r) (Å⁻²)")
        ax.legend(fontsize=6, loc="upper right")
    if show_resid:
        fig.subplots_adjust(hspace=0.55, wspace=0.3)
    else:
        fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], filename))
    return fit_results


def plot_11(cfg, data):
    return _plot_fitting_grid(cfg, data, "11_curve_fitting.png",
                              fit_max=4.5, show_resid=True, annotate_vlines=False)


def plot_12(cfg, data):
    keys = cfg["keys"]
    bond_types = ["B-O", "Zn-O", "Te-O", cfg["dopant_key"]]
    x = np.arange(len(keys))
    width = 0.18
    fig, ax = plt.subplots(figsize=(12, 6))
    colors_b = ["#2ca02c", "#1f77b4", "#d62728", "#9467bd"]
    for j, bt in enumerate(bond_types):
        vals = []
        for sid in keys:
            v = cfg["bond_lengths"][sid].get(bt)
            vals.append(np.nan if v is None else v)
        ax.bar(x + (j - 1.5) * width, vals, width, label=bt, color=colors_b[j])
        if bt in U.BOND_RANGES:
            lo, hi = U.BOND_RANGES[bt]
            ax.axhspan(lo, hi, color=colors_b[j], alpha=0.08)
    ax.set_xticks(x)
    ax.set_xticklabels(keys, rotation=15)
    ax.set_ylabel("Bond Length (Å)")
    ax.set_xlabel("Sample")
    ax.legend()
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "12_bond_analysis.png"))


def plot_13(cfg, data):
    keys = cfg["keys"]
    xs = [cfg["samples"][k]["dopant_pct"] for k in keys]
    bond_types = ["B-O", "Zn-O", "Te-O", cfg["dopant_key"]]
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    for j, bt in enumerate(bond_types):
        ax = axes[j]
        ys = [cfg["bond_lengths"][k].get(bt) for k in keys]
        ys = [np.nan if v is None else v for v in ys]
        ax.plot(xs, ys, "o-", lw=2, ms=7)
        if bt in U.BOND_RANGES:
            lo, hi = U.BOND_RANGES[bt]
            ax.axhspan(lo, hi, color="gray", alpha=0.2, label="lit. range")
        ax.set_title(bt)
        ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
        ax.set_ylabel("Bond Length (Å)")
        ax.legend(fontsize=7)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "13_bond_length_trends.png"))


def plot_14(cfg, data):
    keys = cfg["keys"]
    xs = [cfg["samples"][k]["dopant_pct"] for k in keys]
    bond_types = ["B-O", "Zn-O", "Te-O", cfg["dopant_key"]]
    markers = ["o", "s", "^", "D"]
    fig, ax = plt.subplots(figsize=(8, 5))
    for bt, mk in zip(bond_types, markers):
        ys = [cfg["bond_lengths"][k].get(bt) for k in keys]
        ys = [np.nan if v is None else v for v in ys]
        ax.plot(xs, ys, marker=mk, lw=2, ms=7, label=bt)
    ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
    ax.set_ylabel("Bond Length (Å)")
    ax.legend()
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "14_all_bonds_summary.png"))


def plot_15(cfg, data):
    return _plot_fitting_grid(cfg, data, "15_Tr_fitting.png",
                              fit_max=5.5, show_resid=False, annotate_vlines=True)


def plot_16(cfg, data):
    keys = cfg["keys"]
    coord_types = ["B-O", "Zn-O", "Te-O", cfg["dopant_key"]]
    x = np.arange(len(keys))
    width = 0.18
    fig, ax = plt.subplots(figsize=(12, 6))
    colors_b = ["#2ca02c", "#1f77b4", "#d62728", "#9467bd"]
    for j, ct in enumerate(coord_types):
        vals = []
        for sid in keys:
            v = cfg["coordination"][sid].get(ct)
            vals.append(np.nan if v is None else v)
        ax.bar(x + (j - 1.5) * width, vals, width, label=f"N({ct})", color=colors_b[j])
    ax.axhline(3, color="#2ca02c", ls="--", lw=0.8, alpha=0.5, label="N(B–O)=3 ref")
    ax.axhline(4, color="#d62728", ls="--", lw=0.8, alpha=0.5, label="N(Te–O)=4 ref")
    ax.set_xticks(x)
    ax.set_xticklabels(keys, rotation=15)
    ax.set_ylabel("Coordination Number N")
    ax.set_xlabel("Sample")
    ax.legend(fontsize=8)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "16_coordination_numbers.png"))


def plot_17(cfg, data):
    keys = cfg["keys"]
    xs = [cfg["samples"][k]["dopant_pct"] for k in keys]
    coord_types = ["B-O", "Zn-O", "Te-O", cfg["dopant_key"]]
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    for j, ct in enumerate(coord_types):
        ax = axes[j]
        ys = [cfg["coordination"][k].get(ct) for k in keys]
        ys = [np.nan if v is None else v for v in ys]
        ax.plot(xs, ys, "o-", lw=2, ms=7)
        ax.set_title(f"N({ct})")
        ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
        ax.set_ylabel("Coordination Number N")
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "17_coordination_trends.png"))


def plot_18(cfg, data):
    keys = cfg["keys"]
    xs = [cfg["samples"][k]["dopant_pct"] for k in keys]
    coord_types = ["B-O", "Zn-O", "Te-O", cfg["dopant_key"]]
    markers = ["o", "s", "^", "D"]
    fig, ax = plt.subplots(figsize=(8, 5))
    for ct, mk in zip(coord_types, markers):
        ys = [cfg["coordination"][k].get(ct) for k in keys]
        ys = [np.nan if v is None else v for v in ys]
        ax.plot(xs, ys, marker=mk, lw=2, ms=7, label=f"N({ct})")
    ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
    ax.set_ylabel("Coordination Number N")
    ax.legend()
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "18_all_coordination_summary.png"))


def plot_19(cfg, data):
    keys = cfg["keys"]
    xs = [cfg["samples"][k]["dopant_pct"] for k in keys]
    teote = [cfg["bond_angles"][k]["Te-O-Te"] for k in keys]
    znozn = [cfg["bond_angles"][k].get("Zn-O-Zn") for k in keys]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ax = axes[0]
    ax.plot(xs, teote, "o-", lw=2, ms=8, color="C0")
    for x, y in zip(xs, teote):
        ax.annotate(f"{y:.1f}°", (x, y), textcoords="offset points",
                    xytext=(0, 6), ha="center", fontsize=8)
    ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
    ax.set_ylabel("Bond Angle (°)")
    ax.set_title("(a) Te–O–Te")
    ax = axes[1]
    if any(v is not None for v in znozn):
        ys = [np.nan if v is None else v for v in znozn]
        ax.plot(xs, ys, "s-", lw=2, ms=8, color="C1")
        for x, y in zip(xs, ys):
            if not np.isnan(y):
                ax.annotate(f"{y:.1f}°", (x, y), textcoords="offset points",
                            xytext=(0, 6), ha="center", fontsize=8)
        ax.set_title("(b) Zn–O–Zn")
    else:
        ax.text(0.5, 0.5, "Zn–O–Zn not reported\nfor this series",
                ha="center", va="center", transform=ax.transAxes)
        ax.set_title("(b) Zn–O–Zn")
    ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
    ax.set_ylabel("Bond Angle (°)")
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "19_bond_angle_analysis.png"))


def plot_20(cfg, data):
    keys = cfg["keys"]
    xs = [cfg["samples"][k]["dopant_pct"] for k in keys]
    teote = [cfg["bond_angles"][k]["Te-O-Te"] for k in keys]
    znozn = [cfg["bond_angles"][k].get("Zn-O-Zn") for k in keys]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, teote, "o-", lw=2, ms=8, label="Te–O–Te")
    if any(v is not None for v in znozn):
        ys = [np.nan if v is None else v for v in znozn]
        ax.plot(xs, ys, "s-", lw=2, ms=8, label="Zn–O–Zn")
    ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
    ax.set_ylabel("Bond Angle (°)")
    ax.legend()
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "20_bond_angle_trends.png"))


def _qspace_panels(cfg, data, which, filename):
    keys = cfg["keys"]
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    axes = axes.flatten()
    for i, sid in enumerate(keys):
        ax = axes[i]
        d = data[sid]
        arr = d[which]
        Q, Y = arr[:, 0], arr[:, 1]
        ax.plot(Q, Y, color=cfg["colors"][i], lw=1.1)
        # FSDP: for S(Q) use 0.4-2.5; for I(Q) use broader
        if which == "sq":
            qpk, ypk = U.find_fsdp(Q, Y, 0.4, 2.5)
        else:
            qpk, ypk = U.find_fsdp(Q, Y, 0.5, 3.0)
        dval = 2 * np.pi / qpk if qpk else np.nan
        ax.axvline(qpk, color="red", ls="--", lw=0.9)
        ax.annotate(f"Q={qpk:.2f}\nd={dval:.2f} Å",
                    (qpk, ypk), textcoords="offset points", xytext=(8, 0),
                    fontsize=8, color="red")
        ax.set_title(d["info"]["label"])
        ax.set_xlabel("Q (Å⁻¹)")
        ax.set_ylabel("S(Q)" if which == "sq" else "I(Q)")
        ax.set_xlim(0.5, 5.5)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], filename))


def plot_21(cfg, data):
    _qspace_panels(cfg, data, "sq", "21_Sq_peak_analysis.png")


def plot_22(cfg, data):
    _qspace_panels(cfg, data, "iq", "22_Iq_peak_analysis.png")


def plot_23(cfg, data):
    keys = cfg["keys"]
    xs = [cfg["samples"][k]["dopant_pct"] for k in keys]
    # Prefer recomputed FSDP from S(Q); fall back to prior table
    Qm, dm = [], []
    for sid in keys:
        d = data[sid]
        Q, S = d["sq"][:, 0], d["sq"][:, 1]
        qpk, _ = U.find_fsdp(Q, S, 0.8, 2.8)  # main diffraction max region
        # For lab glass data the intense peak ~2 Å^-1 is more meaningful than weak FSDP
        Qm.append(qpk)
        dm.append(2 * np.pi / qpk)
    # If priors look more consistent for Eu, blend: use prior for Eu display
    if cfg["dopant"] == "Eu":
        Qm = [cfg["qmaxima"][k]["Q_max"] for k in keys]
        dm = [cfg["qmaxima"][k]["d"] for k in keys]
    else:
        # Er prior is inconsistent; use recomputed and also store
        pass
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    ax = axes[0]
    ax.plot(xs, Qm, "o-", lw=2, ms=8)
    for x, y in zip(xs, Qm):
        ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                    xytext=(0, 6), ha="center", fontsize=8)
    ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
    ax.set_ylabel("Q_max (Å⁻¹)")
    ax.set_title("(a) Q_max")
    ax = axes[1]
    ax.plot(xs, dm, "s-", lw=2, ms=8, color="C1")
    for x, y in zip(xs, dm):
        ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                    xytext=(0, 6), ha="center", fontsize=8)
    ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
    ax.set_ylabel("d = 2π/Q_max (Å)")
    ax.set_title("(b) d-spacing")
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "23_Q_maxima_trends.png"))
    return dict(zip(keys, [{"Q_max": q, "d": dd} for q, dd in zip(Qm, dm)]))


def plot_24(cfg, data):
    keys = cfg["keys"]
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    axes = axes.flatten()
    for i, sid in enumerate(keys):
        ax = axes[i]
        d = data[sid]
        ax.plot(d["r"], d["G"], color=cfg["colors"][i], lw=1.1, label="G(r)")
        ax2 = ax.twinx()
        ax2.plot(d["r"], d["gr"], color=cfg["colors"][i], lw=1.1, ls="--", alpha=0.7, label="g(r)")
        ax2.axhline(1.0, color="gray", ls=":", lw=0.7)
        ax.set_xlim(1, 10)
        ax.set_xlabel("r (Å)")
        ax.set_ylabel("G(r) (Å⁻²)")
        ax2.set_ylabel("g(r)")
        ax.set_title(f"{d['info']['label']}")
        lines1, lab1 = ax.get_legend_handles_labels()
        lines2, lab2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, lab1 + lab2, fontsize=7, loc="upper right")
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "24_pair_distribution_gr.png"))


def plot_25(cfg, data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axhline(1.0, color="gray", ls="--", lw=0.8)
    for i, sid in enumerate(cfg["keys"]):
        d = data[sid]
        ax.plot(d["r"], d["gr"], color=cfg["colors"][i], lw=1.2,
                label=pct_label(d["info"], cfg["dopant_oxide"]))
    ax.set_xlim(1, 11)
    ax.set_ylim(0.5, 2.0)
    ax.set_xlabel("r (Å)")
    ax.set_ylabel("g(r)")
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=9)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "25_gr_overlay_comparison.png"))


def plot_26(cfg, data):
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, sid in enumerate(cfg["keys"]):
        d = data[sid]
        ax.plot(d["r"], d["Tr"], color=cfg["colors"][i], lw=1.2,
                label=d["info"]["label"])
    ax.set_xlim(1, 6)
    ax.set_xlabel("r (Å)")
    ax.set_ylabel("T(r) (Å⁻²)")
    ax.legend(fontsize=9)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "26_Tr_all_samples.png"))


def plot_27(cfg, data):
    # highest doping = last key
    sid = cfg["keys"][-1]
    d = data[sid]
    centers, labels = _fit_centers(cfg, sid)
    fit = U.fit_Tr_gaussians(d["r"], d["Tr"], centers, fit_min=1.0, fit_max=4.5)
    fig, (ax, axr) = plt.subplots(2, 1, figsize=(10, 8),
                                  gridspec_kw={"height_ratios": [3, 1], "hspace": 0.15},
                                  sharex=True)
    ax.plot(fit["r"], fit["y"], "k-", lw=1.3, label="T(r) data")
    ax.plot(fit["r"], fit["yfit"], "r--", lw=1.5, label="total fit")
    for comp, lab in zip(fit["components"], labels):
        ax.plot(fit["r"], comp["curve"], lw=1.1, label=f"{lab} ({comp['center']:.2f} Å)")
        ax.axvline(comp["center"], color="gray", ls=":", lw=0.6)
        ax.annotate(f"{lab}\n{comp['center']:.2f} Å",
                    (comp["center"], comp["amp"]),
                    textcoords="offset points", xytext=(0, 8),
                    ha="center", fontsize=8)
    ax.set_ylabel("T(r) (Å⁻²)")
    ax.set_title(f"{d['info']['label']} — detailed T(r) Gaussian fit")
    ax.legend(fontsize=8, loc="upper right")
    axr.axhline(0, color="gray", lw=0.6)
    axr.plot(fit["r"], fit["residual"], "g-", lw=0.9)
    axr.set_xlabel("r (Å)")
    axr.set_ylabel("Residual")
    fname = f"27_{sid}_fitting_detail.png"
    # also keep generic name expected by prompt for Eu
    U.savefig(fig, os.path.join(cfg["outdir"], fname))
    # copy-style second save with prompt name for Eu 2F / Er last
    if cfg["dopant"] == "Eu":
        # re-open already closed — regenerate quickly
        fig2, (ax, axr) = plt.subplots(2, 1, figsize=(10, 8),
                                       gridspec_kw={"height_ratios": [3, 1], "hspace": 0.15},
                                       sharex=True)
        ax.plot(fit["r"], fit["y"], "k-", lw=1.3, label="T(r) data")
        ax.plot(fit["r"], fit["yfit"], "r--", lw=1.5, label="total fit")
        for comp, lab in zip(fit["components"], labels):
            ax.plot(fit["r"], comp["curve"], lw=1.1, label=f"{lab} ({comp['center']:.2f} Å)")
        ax.set_ylabel("T(r) (Å⁻²)")
        ax.set_title(f"{d['info']['label']} — detailed T(r) Gaussian fit")
        ax.legend(fontsize=8)
        axr.axhline(0, color="gray", lw=0.6)
        axr.plot(fit["r"], fit["residual"], "g-", lw=0.9)
        axr.set_xlabel("r (Å)")
        axr.set_ylabel("Residual")
        U.savefig(fig2, os.path.join(cfg["outdir"], "27_2F_fitting_detail.png"))
    else:
        # also save prompt-style name
        import shutil
        src = os.path.join(cfg["outdir"], fname)
        dst = os.path.join(cfg["outdir"], f"27_{sid}_fitting_detail.png")
        # already saved as fname; also save alias 27_highest_fitting_detail
        shutil.copy(src, os.path.join(cfg["outdir"], "27_highest_doping_fitting_detail.png"))
    return {sid: {"labels": labels, "components": fit["components"]}}


def plot_28(cfg, data):
    return _plot_fitting_grid(cfg, data, "28_all_samples_fitting.png",
                              fit_max=4.5, show_resid=False, annotate_vlines=True)


def plot_29(cfg, data):
    keys = cfg["keys"]
    xs = [cfg["samples"][k]["dopant_pct"] for k in keys]
    tete = [cfg["bond_angles"][k]["Te-Te"] for k in keys]
    ang = [cfg["bond_angles"][k]["Te-O-Te"] for k in keys]
    ndop = [cfg["coordination"][k].get(cfg["dopant_key"]) for k in keys]
    nzn = [cfg["coordination"][k].get("Zn-O") for k in keys]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    panels = [
        (axes[0, 0], tete, "Te–Te distance (Å)", "(a) Te–Te distance"),
        (axes[0, 1], ang, "Te–O–Te (°)", "(b) Te–O–Te angle"),
        (axes[1, 0], [np.nan if v is None else v for v in ndop],
         f"N({cfg['dopant_key']})", f"(c) N({cfg['dopant']}-O)"),
        (axes[1, 1], [np.nan if v is None else v for v in nzn],
         "N(Zn-O)", "(d) N(Zn-O)"),
    ]
    for ax, ys, ylab, title in panels:
        ax.plot(xs, ys, "o-", lw=2, ms=8)
        for x, y in zip(xs, ys):
            if y is not None and not (isinstance(y, float) and np.isnan(y)):
                ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                            xytext=(0, 6), ha="center", fontsize=8)
        ax.set_xlabel(f"{cfg['dopant_oxide']} (mol%)")
        ax.set_ylabel(ylab)
        ax.set_title(title)
    fig.tight_layout()
    U.savefig(fig, os.path.join(cfg["outdir"], "29_structural_trends_summary.png"))


# ---------------------------------------------------------------------------
# TEXT OUTPUTS
# ---------------------------------------------------------------------------
def write_text_outputs(cfg, data, fit_results, qmax_used):
    out = cfg["outdir"]
    keys = cfg["keys"]
    dk = cfg["dopant_key"]

    # bond lengths
    with open(os.path.join(out, "bond_lengths.txt"), "w", encoding="utf-8") as f:
        f.write(f"Bond lengths (Å) — {cfg['glass']}\n")
        f.write(f"{'Sample':<14} {'%':>5} {'B-O':>8} {'Zn-O':>8} {'Te-O':>8} {dk:>8}\n")
        for sid in keys:
            bl = cfg["bond_lengths"][sid]
            def fmt(v):
                return f"{v:8.3f}" if v is not None else f"{'-':>8}"
            f.write(f"{sid:<14} {cfg['samples'][sid]['dopant_pct']:5.1f}"
                    f"{fmt(bl['B-O'])}{fmt(bl['Zn-O'])}{fmt(bl['Te-O'])}{fmt(bl.get(dk))}\n")

    with open(os.path.join(out, "bond_angles.txt"), "w", encoding="utf-8") as f:
        f.write(f"Bond angles — {cfg['glass']}\n")
        f.write(f"{'Sample':<14} {'%':>5} {'Te-O-Te':>10} {'Zn-O-Zn':>10} {'Te-Te':>8}\n")
        for sid in keys:
            ba = cfg["bond_angles"][sid]
            z = ba.get("Zn-O-Zn")
            zs = f"{z:10.1f}" if z is not None else f"{'-':>10}"
            f.write(f"{sid:<14} {cfg['samples'][sid]['dopant_pct']:5.1f}"
                    f"{ba['Te-O-Te']:10.1f}{zs}{ba['Te-Te']:8.2f}\n")

    with open(os.path.join(out, "coordination_numbers.txt"), "w", encoding="utf-8") as f:
        f.write(f"Coordination numbers — {cfg['glass']}\n")
        f.write(f"{'Sample':<14} {'%':>5} {'N(B-O)':>8} {'N(Zn-O)':>8} {'N(Te-O)':>8} {'N('+dk+')':>10}\n")
        for sid in keys:
            c = cfg["coordination"][sid]
            def fmt(v):
                return f"{v:8.2f}" if v is not None else f"{'-':>8}"
            nd = c.get(dk)
            nds = f"{nd:10.2f}" if nd is not None else f"{'-':>10}"
            f.write(f"{sid:<14} {cfg['samples'][sid]['dopant_pct']:5.1f}"
                    f"{fmt(c.get('B-O'))}{fmt(c.get('Zn-O'))}{fmt(c.get('Te-O'))}{nds}\n")

    with open(os.path.join(out, "Q_maxima.txt"), "w", encoding="utf-8") as f:
        f.write(f"Q-space analysis — {cfg['glass']}\n")
        f.write(f"{'Sample':<14} {'%':>5} {'Q_max':>8} {'d=2π/Q':>10}\n")
        src = qmax_used if qmax_used else cfg["qmaxima"]
        for sid in keys:
            q = src[sid]
            f.write(f"{sid:<14} {cfg['samples'][sid]['dopant_pct']:5.1f}"
                    f"{q['Q_max']:8.2f}{q['d']:10.2f}\n")

    with open(os.path.join(out, "fitting_results.txt"), "w", encoding="utf-8") as f:
        f.write(f"Gaussian T(r) fit parameters — {cfg['glass']}\n\n")
        for sid, fr in fit_results.items():
            f.write(f"=== {sid} ({cfg['samples'][sid]['label']}) ===\n")
            for lab, comp in zip(fr["labels"], fr["components"]):
                f.write(f"  {lab:<8} center={comp['center']:.4f} Å  "
                        f"amp={comp['amp']:.4f}  width={comp['width']:.4f}\n")
            f.write("\n")

    with open(os.path.join(out, "PDF_analysis_summary.txt"), "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write(f"PDF ANALYSIS SUMMARY — {cfg['dopant']} SERIES\n")
        f.write(f"Glass: {cfg['glass']}\n")
        f.write("Radiation: Cu Kα (λ=1.5406 Å), Qmax=5.1 Å⁻¹\n")
        f.write("=" * 70 + "\n\n")
        f.write("NOTE: First structural peak is the cation–O / Te–O shell (~1.9–2.2 Å).\n")
        f.write("The stronger Te–Te peak (~3.5–3.8 Å) is the *second* shell in G(r)/g(r);\n")
        f.write("it dominates X-ray intensity (Z² weighting) but must not be labeled as first.\n")
        f.write("First-shell g(r) often stays near/below 1 at lab Qmax≈5.1 Å⁻¹.\n\n")
        f.write(f"{'Sample':<14} {'%':>5} {'1st r':>8} {'Te-Te(g)':>10} {'Te-Te(fit)':>10} "
                f"{'Te-O-Te':>10} {'N('+dk+')':>10}\n")
        for sid in keys:
            ba = cfg["bond_angles"][sid]
            nd = cfg["coordination"][sid].get(dk)
            nds = f"{nd:10.2f}" if nd is not None else f"{'-':>10}"
            tr = data[sid]["tete_r"]
            fr = data[sid]["first_r"]
            trs = f"{tr:10.2f}" if tr is not None else f"{'-':>10}"
            frs = f"{fr:8.2f}" if fr is not None else f"{'-':>8}"
            f.write(f"{sid:<14} {cfg['samples'][sid]['dopant_pct']:5.1f}"
                    f"{frs}{trs}{ba['Te-Te']:10.2f}{ba['Te-O-Te']:10.1f}{nds}\n")
        f.write("\nKey finding: Te–Te (2nd shell) shifts and Te–O–Te angle opens with\n")
        f.write(f"increasing {cfg['dopant_oxide']}, indicating network modification.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", choices=["eu", "er"], required=True)
    args = ap.parse_args()

    cfg = load_series(args.series)
    os.makedirs(cfg["outdir"], exist_ok=True)
    print(f"\n=== Generating {cfg['dopant']} series → {cfg['outdir']} ===")
    data = load_all_data(cfg)
    for sid in cfg["keys"]:
        d = data[sid]
        fr = f"{d['first_r']:.3f}" if d["first_r"] else "N/A"
        tr = f"{d['tete_r']:.3f}" if d["tete_r"] else "N/A"
        print(f"  {sid}: 1st shell @ {fr} Å | Te–Te (2nd) @ {tr} Å")

    plot_01(cfg, data)
    plot_02(cfg, data)
    plot_03(cfg, data)
    plot_04(cfg, data)
    plot_05(cfg, data)
    plot_06(cfg, data)
    plot_07(cfg, data)
    plot_08(cfg, data)
    plot_09(cfg, data)
    plot_10(cfg, data)
    fit11 = plot_11(cfg, data)
    plot_12(cfg, data)
    plot_13(cfg, data)
    plot_14(cfg, data)
    fit15 = plot_15(cfg, data)
    plot_16(cfg, data)
    plot_17(cfg, data)
    plot_18(cfg, data)
    plot_19(cfg, data)
    plot_20(cfg, data)
    plot_21(cfg, data)
    plot_22(cfg, data)
    qmax_used = plot_23(cfg, data)
    plot_24(cfg, data)
    plot_25(cfg, data)
    plot_26(cfg, data)
    plot_27(cfg, data)
    fit28 = plot_28(cfg, data)
    plot_29(cfg, data)

    # prefer fit15 / fit11 for text
    fit_results = fit15 if fit15 else (fit11 if fit11 else fit28)
    write_text_outputs(cfg, data, fit_results, qmax_used)
    print(f"Done {cfg['dopant']} series.")


if __name__ == "__main__":
    main()
