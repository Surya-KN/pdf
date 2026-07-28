#!/usr/bin/env python3
"""Regenerate G(r)/g(r) plots with first-peak markers only (no Te–Te marks)."""
import generate_series_plots as g
import generate_comparison as c

for series in ("eu", "er"):
    cfg = g.load_series(series)
    data = g.load_all_data(cfg)
    print("===", series, "===")
    for sid in cfg["keys"]:
        d = data[sid]
        print(f"  {sid}: first peak @ {d['first_r']:.3f} Å")
    g.plot_01(cfg, data)
    g.plot_03(cfg, data)
    g.plot_06(cfg, data)
    g.plot_25(cfg, data)

print("=== comparison waterfall ===")
eu_data = c.load_gr_series(c.EU_SAMPLES)
er_data = c.load_gr_series(c.ER_SAMPLES, out_override=c.ER_OUT)
c.comparison_Gr_waterfall(eu_data, er_data)
print("Done.")
