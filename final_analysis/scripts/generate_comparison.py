#!/usr/bin/env python3
"""Cross-series Eu vs Er comparison plots + structural comparison table."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import utils as U
from series_data import (
    EU_SAMPLES, EU_COLORS, EU_BOND_ANGLES, EU_COORDINATION, EU_OUT, CMP_OUT,
    ER_SAMPLES, ER_COLORS, ER_BOND_ANGLES, ER_COORDINATION, ER_OUT,
)


def load_gr_series(samples_dict, out_override=None):
    data = {}
    for sid, info in samples_dict.items():
        path = info.get("file")
        if out_override:
            path = os.path.join(out_override, f"{sid}.gr")
        arr = U.parse_gr(path)
        r, G = arr[:, 0], arr[:, 1]
        gr = U.Gr_to_gr(r, G, info["rho0"])
        first_r, first_G = U.find_first_shell_peak(r, G)
        first_gr_r, first_gr = U.find_first_shell_peak(r, gr)
        tete_r, tete_g = U.find_Te_Te_peak(r, gr)
        tete_Gr_r, tete_Gr = U.find_Te_Te_peak_Gr(r, G)
        data[sid] = {
            "r": r, "G": G, "gr": gr,
            "first_r": first_r, "first_G": first_G,
            "first_gr_r": first_gr_r, "first_gr": first_gr,
            "tete_r": tete_r, "tete_g": tete_g,
            "tete_Gr_r": tete_Gr_r, "tete_Gr": tete_Gr,
            "info": info,
        }
    return data


def comparison_Gr_waterfall(eu_data, er_data):
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), sharey=True)
    for ax, data, colors, title in [
        (axes[0], eu_data, EU_COLORS, "Eu₂O₃ series"),
        (axes[1], er_data, ER_COLORS, "Er₂O₃ series"),
    ]:
        for i, (sid, d) in enumerate(data.items()):
            off = i * U.WATERFALL_OFFSET_GR
            ax.plot(d["r"], d["G"] + off, color=colors[i], lw=1.2)
            if d["first_r"] is not None:
                idx = np.argmin(np.abs(d["r"] - d["first_r"]))
                ax.plot(d["first_r"], d["G"][idx] + off, "o",
                        color=colors[i], ms=4)
                ax.annotate(f'{d["first_r"]:.2f} Å',
                            (d["first_r"], d["G"][idx] + off),
                            textcoords="offset points", xytext=(4, 3),
                            fontsize=7, color=colors[i])
            extra = 0.3 if sid in U.EXTRA_OFFSET_SAMPLES else 0.0
            U.add_inline_label(ax, U.LABEL_X, off, d["info"]["label"],
                               colors[i], extra)
        U.apply_waterfall_style(ax, U.WATERFALL_XLIM)
        ax.set_title(title)
    fig.tight_layout()
    U.savefig(fig, os.path.join(CMP_OUT, "comparison_Gr_waterfall.png"))


def comparison_gr_overlay(eu_data, er_data):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
    for ax, data, colors, title, oxide in [
        (axes[0], eu_data, EU_COLORS, "Eu₂O₃", "Eu₂O₃"),
        (axes[1], er_data, ER_COLORS, "Er₂O₃", "Er₂O₃"),
    ]:
        ax.axhline(1.0, color="gray", ls="--", lw=0.8)
        for i, (sid, d) in enumerate(data.items()):
            p = d["info"]["dopant_pct"]
            ax.plot(d["r"], d["gr"], color=colors[i], lw=1.2,
                    label=f"{p}% {oxide}")
        ax.set_xlim(1, 11)
        ax.set_ylim(0.5, 2.0)
        ax.set_xlabel("r (Å)")
        ax.set_ylabel("g(r)")
        ax.set_title(title)
        ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    U.savefig(fig, os.path.join(CMP_OUT, "comparison_gr_overlay.png"))


def comparison_TeTe_shift():
    fig, ax = plt.subplots(figsize=(8, 6))
    eu_x = [EU_SAMPLES[k]["dopant_pct"] for k in EU_SAMPLES]
    eu_y = [EU_BOND_ANGLES[k]["Te-Te"] for k in EU_SAMPLES]
    er_x = [ER_SAMPLES[k]["dopant_pct"] for k in ER_SAMPLES]
    er_y = [ER_BOND_ANGLES[k]["Te-Te"] for k in ER_SAMPLES]
    ax.plot(eu_x, eu_y, "o-", lw=2, ms=8, label="Eu₂O₃", color="C0")
    ax.plot(er_x, er_y, "s--", lw=2, ms=8, label="Er₂O₃", color="C3")
    ax.set_xlabel("Dopant mol%")
    ax.set_ylabel("Te–Te distance (Å)")
    ax.legend()
    fig.tight_layout()
    U.savefig(fig, os.path.join(CMP_OUT, "comparison_TeTe_shift.png"))


def comparison_TeTe_angle():
    fig, ax = plt.subplots(figsize=(8, 6))
    eu_x = [EU_SAMPLES[k]["dopant_pct"] for k in EU_SAMPLES]
    eu_y = [EU_BOND_ANGLES[k]["Te-O-Te"] for k in EU_SAMPLES]
    er_x = [ER_SAMPLES[k]["dopant_pct"] for k in ER_SAMPLES]
    er_y = [ER_BOND_ANGLES[k]["Te-O-Te"] for k in ER_SAMPLES]
    ax.plot(eu_x, eu_y, "o-", lw=2, ms=8, label="Eu₂O₃", color="C0")
    ax.plot(er_x, er_y, "s--", lw=2, ms=8, label="Er₂O₃", color="C3")
    ax.set_xlabel("Dopant mol%")
    ax.set_ylabel("Te–O–Te angle (°)")
    ax.legend()
    fig.tight_layout()
    U.savefig(fig, os.path.join(CMP_OUT, "comparison_TeTe_angle.png"))


def comparison_coordination():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    eu_x = [EU_SAMPLES[k]["dopant_pct"] for k in EU_SAMPLES]
    er_x = [ER_SAMPLES[k]["dopant_pct"] for k in ER_SAMPLES]

    panels = [
        (axes[0, 0], "B-O", "N(B–O)"),
        (axes[0, 1], "Zn-O", "N(Zn–O) / N(Zn–Te–O)"),
        (axes[1, 0], "dopant", "N(dopant–O)"),
        (axes[1, 1], "Te-O", "N(Te–O)"),
    ]
    for ax, key, title in panels:
        if key == "dopant":
            eu_y = [EU_COORDINATION[k].get("Eu-O") for k in EU_SAMPLES]
            er_y = [ER_COORDINATION[k].get("Er-O") for k in ER_SAMPLES]
        else:
            eu_y = [EU_COORDINATION[k].get(key) for k in EU_SAMPLES]
            er_y = [ER_COORDINATION[k].get(key) for k in ER_SAMPLES]
        eu_y = [np.nan if v is None else v for v in eu_y]
        er_y = [np.nan if v is None else v for v in er_y]
        ax.plot(eu_x, eu_y, "o-", lw=2, ms=8, label="Eu₂O₃", color="C0")
        ax.plot(er_x, er_y, "s--", lw=2, ms=8, label="Er₂O₃", color="C3")
        ax.set_xlabel("Dopant mol%")
        ax.set_ylabel("Coordination Number N")
        ax.set_title(title)
        ax.legend()
    fig.tight_layout()
    U.savefig(fig, os.path.join(CMP_OUT, "comparison_coordination.png"))


def write_structural_comparison():
    path = os.path.join(CMP_OUT, "structural_comparison.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("=" * 78 + "\n")
        f.write("STRUCTURAL COMPARISON: Eu₂O₃ vs Er₂O₃ glass series\n")
        f.write("20TeO₂-(30-x)ZnO-50B₂O₃-xRE₂O₃\n")
        f.write("=" * 78 + "\n\n")
        f.write(f"{'mol%':>5}  {'Eu Te-Te':>10} {'Er Te-Te':>10}  "
                f"{'Eu Te-O-Te':>12} {'Er Te-O-Te':>12}  "
                f"{'N(Eu-O)':>8} {'N(Er-O)':>8}\n")
        eu_keys = list(EU_SAMPLES.keys())
        er_keys = list(ER_SAMPLES.keys())
        for i in range(len(eu_keys)):
            ek, rk = eu_keys[i], er_keys[i]
            pct = EU_SAMPLES[ek]["dopant_pct"]
            eu_tt = EU_BOND_ANGLES[ek]["Te-Te"]
            er_tt = ER_BOND_ANGLES[rk]["Te-Te"]
            eu_ang = EU_BOND_ANGLES[ek]["Te-O-Te"]
            er_ang = ER_BOND_ANGLES[rk]["Te-O-Te"]
            neu = EU_COORDINATION[ek].get("Eu-O")
            ner = ER_COORDINATION[rk].get("Er-O")
            neus = f"{neu:8.2f}" if neu is not None else f"{'-':>8}"
            ners = f"{ner:8.2f}" if ner is not None else f"{'-':>8}"
            f.write(f"{pct:5.1f}  {eu_tt:10.2f} {er_tt:10.2f}  "
                    f"{eu_ang:12.1f} {er_ang:12.1f}  {neus} {ners}\n")
        f.write("\nBoth RE³⁺ dopants open the Te–O–Te network angle and shift\n")
        f.write("the Te–Te peak to longer distance with increasing concentration.\n")
        f.write("Eu shows a larger Te–Te / angle shift at 5 mol% than Er.\n")
    print(f"  saved: {path}")


def main():
    os.makedirs(CMP_OUT, exist_ok=True)
    print("\n=== Comparison plots ===")
    eu_data = load_gr_series(EU_SAMPLES)
    er_data = load_gr_series(ER_SAMPLES, out_override=ER_OUT)
    comparison_Gr_waterfall(eu_data, er_data)
    comparison_gr_overlay(eu_data, er_data)
    comparison_TeTe_shift()
    comparison_TeTe_angle()
    comparison_coordination()
    write_structural_comparison()
    print("Done comparison.")


if __name__ == "__main__":
    main()
