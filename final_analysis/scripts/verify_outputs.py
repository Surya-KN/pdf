#!/usr/bin/env python3
"""Verify all expected output files and print summary table."""
import os
import glob
from series_data import (
    EU_SAMPLES, EU_BOND_ANGLES, EU_COORDINATION, EU_OUT,
    ER_SAMPLES, ER_BOND_ANGLES, ER_COORDINATION, ER_OUT, CMP_OUT,
)
import utils as U

EU_PLOTS = [
    "01_individual_Gr_samples.png",
    "02_Gr_overlay.png",
    "03_Gr_waterfall.png",
    "04_Sq_comparison.png",
    "05_Fq_waterfall.png",
    "06_first_peak_zoom.png",
    "07_peak_position_vs_Eu.png",
    "08_difference_Gr.png",
    "09_Gr_3D_surface.png",
    "10_Gr_contour_heatmap.png",
    "11_curve_fitting.png",
    "12_bond_analysis.png",
    "13_bond_length_trends.png",
    "14_all_bonds_summary.png",
    "15_Tr_fitting.png",
    "16_coordination_numbers.png",
    "17_coordination_trends.png",
    "18_all_coordination_summary.png",
    "19_bond_angle_analysis.png",
    "20_bond_angle_trends.png",
    "21_Sq_peak_analysis.png",
    "22_Iq_peak_analysis.png",
    "23_Q_maxima_trends.png",
    "24_pair_distribution_gr.png",
    "25_gr_overlay_comparison.png",
    "26_Tr_all_samples.png",
    "27_2F_fitting_detail.png",
    "28_all_samples_fitting.png",
    "29_structural_trends_summary.png",
]

EU_TXT = [
    "PDF_analysis_summary.txt",
    "bond_lengths.txt",
    "bond_angles.txt",
    "coordination_numbers.txt",
    "Q_maxima.txt",
    "fitting_results.txt",
]

ER_PLOTS = [
    p.replace("vs_Eu", "vs_Er").replace("27_2F_fitting_detail.png",
                                         "27_highest_doping_fitting_detail.png")
    for p in EU_PLOTS
]

CMP_FILES = [
    "comparison_Gr_waterfall.png",
    "comparison_gr_overlay.png",
    "comparison_TeTe_shift.png",
    "comparison_TeTe_angle.png",
    "comparison_coordination.png",
    "structural_comparison.txt",
]


def count_files(d):
    if not os.path.isdir(d):
        return 0
    return len([f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))])


def main():
    missing = []
    for p in EU_PLOTS + EU_TXT:
        path = os.path.join(EU_OUT, p)
        if not os.path.isfile(path):
            missing.append(path)
    for p in ER_PLOTS + EU_TXT:
        path = os.path.join(ER_OUT, p)
        if not os.path.isfile(path):
            missing.append(path)
    # Er also has per-sample 27_* detail
    er_keys = list(ER_SAMPLES.keys())
    last = er_keys[-1]
    for extra in [f"27_{last}_fitting_detail.png"]:
        path = os.path.join(ER_OUT, extra)
        if not os.path.isfile(path):
            missing.append(path)
    for p in CMP_FILES:
        path = os.path.join(CMP_OUT, p)
        if not os.path.isfile(path):
            missing.append(path)

    # Er PDF data files
    for sid in ER_SAMPLES:
        for ext in ("gr", "sq", "fq", "iq"):
            path = os.path.join(ER_OUT, f"{sid}.{ext}")
            if not os.path.isfile(path):
                missing.append(path)

    n_eu = count_files(EU_OUT)
    n_er = count_files(ER_OUT)
    n_cmp = count_files(CMP_OUT)
    total = n_eu + n_er + n_cmp

    print("\n=== GENERATION COMPLETE ===")
    print(f"Total files created: {total}")
    print(f"eu2o3/: {n_eu} files")
    print(f"er2o3/: {n_er} files")
    print(f"comparison/: {n_cmp} files")
    print("\nMissing (if any):")
    if missing:
        for m in missing:
            print(f"- {m}")
    else:
        print("- none")

    print("\nSample | Series | Te-Te r (Å) | Te-O-Te (°) | N(dopant-O)")
    print("-" * 64)
    for sid, info in EU_SAMPLES.items():
        ba = EU_BOND_ANGLES[sid]
        nd = EU_COORDINATION[sid].get("Eu-O")
        nds = f"{nd:.2f}" if nd is not None else "-"
        # measured Te-Te from g(r)
        arr = U.parse_gr(info["file"])
        gr = U.Gr_to_gr(arr[:, 0], arr[:, 1], info["rho0"])
        tr, _ = U.find_Te_Te_peak(arr[:, 0], gr)
        trs = f"{tr:.2f}" if tr else f"{ba['Te-Te']:.2f}"
        print(f"{sid:<14} Eu  {trs:>8}   {ba['Te-O-Te']:>8.1f}     {nds}")
    for sid, info in ER_SAMPLES.items():
        ba = ER_BOND_ANGLES[sid]
        nd = ER_COORDINATION[sid].get("Er-O")
        nds = f"{nd:.2f}" if nd is not None else "-"
        path = os.path.join(ER_OUT, f"{sid}.gr")
        arr = U.parse_gr(path)
        gr = U.Gr_to_gr(arr[:, 0], arr[:, 1], info["rho0"])
        tr, _ = U.find_Te_Te_peak(arr[:, 0], gr)
        trs = f"{tr:.2f}" if tr else f"{ba['Te-Te']:.2f}"
        print(f"{sid:<14} Er  {trs:>8}   {ba['Te-O-Te']:>8.1f}     {nds}")


if __name__ == "__main__":
    main()
