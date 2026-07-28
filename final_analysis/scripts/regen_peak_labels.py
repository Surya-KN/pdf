#!/usr/bin/env python3
"""Regenerate plots that mark first vs Te-Te peaks."""
import generate_series_plots as g
import generate_comparison as c

for series in ("eu", "er"):
    cfg = g.load_series(series)
    data = g.load_all_data(cfg)
    print("===", series, "===")
    for sid in cfg["keys"]:
        d = data[sid]
        fr = d["first_r"]
        tr = d["tete_r"]
        print(f"  {sid}: 1st={fr:.3f} Å | Te–Te={tr:.3f} Å")
    g.plot_01(cfg, data)
    g.plot_03(cfg, data)
    g.plot_06(cfg, data)
    g.plot_25(cfg, data)
    # refresh summary text only (reuse empty fit dict shape from plot_15 lightly)
    fit15 = g.plot_15(cfg, data)
    g.write_text_outputs(cfg, data, fit15, cfg["qmaxima"])

print("=== comparison ===")
c.main()
print("Done.")
