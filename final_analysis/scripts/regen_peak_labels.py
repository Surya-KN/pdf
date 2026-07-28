#!/usr/bin/env python3
"""Regenerate waterfall plots with first-peak markers only."""
import os
import shutil
import generate_series_plots as g
import generate_comparison as c

for series in ("eu", "er"):
    cfg = g.load_series(series)
    data = g.load_all_data(cfg)
    print("===", series)
    for sid in cfg["keys"]:
        print(f"  {sid}: first peak @ {data[sid]['first_r']:.3f} Å")
    g.plot_03(cfg, data)

eu_data = c.load_gr_series(c.EU_SAMPLES)
er_data = c.load_gr_series(c.ER_SAMPLES, out_override=c.ER_OUT)
c.comparison_Gr_waterfall(eu_data, er_data)

parent = "/mnt/d/pdfxrd/final_analysis"
repo = "/mnt/d/pdfxrd/pdf/final_analysis"
for sub, name in (
    ("eu2o3", "03_Gr_waterfall.png"),
    ("er2o3", "03_Gr_waterfall.png"),
    ("comparison", "comparison_Gr_waterfall.png"),
):
    src = os.path.join(repo, sub, name)
    dst = os.path.join(parent, sub, name)
    if os.path.isfile(src) and os.path.isdir(os.path.dirname(dst)):
        shutil.copy2(src, dst)
        print("synced", dst)
print("Done.")
