#!/usr/bin/env python3
"""Regenerate G(r)/g(r) plots with NO peak markers."""
import generate_series_plots as g
import generate_comparison as c
import os
import shutil

for series in ("eu", "er"):
    cfg = g.load_series(series)
    data = g.load_all_data(cfg)
    print("===", series, "->", cfg["outdir"])
    g.plot_01(cfg, data)
    g.plot_03(cfg, data)
    g.plot_06(cfg, data)
    g.plot_25(cfg, data)

print("=== comparison ===")
eu_data = c.load_gr_series(c.EU_SAMPLES)
er_data = c.load_gr_series(c.ER_SAMPLES, out_override=c.ER_OUT)
c.comparison_Gr_waterfall(eu_data, er_data)

# Sync to parent D:\pdfxrd\final_analysis if present (stale copy users may open)
parent = "/mnt/d/pdfxrd/final_analysis"
repo = "/mnt/d/pdfxrd/pdf/final_analysis"
if os.path.isdir(parent):
    for sub in ("eu2o3", "er2o3", "comparison"):
        for name in (
            "01_individual_Gr_samples.png",
            "03_Gr_waterfall.png",
            "06_first_peak_zoom.png",
            "25_gr_overlay_comparison.png",
            "comparison_Gr_waterfall.png",
        ):
            src = os.path.join(repo, sub, name)
            dst = os.path.join(parent, sub, name)
            if os.path.isfile(src) and os.path.isdir(os.path.dirname(dst)):
                shutil.copy2(src, dst)
                print("synced", dst)
print("Done.")
