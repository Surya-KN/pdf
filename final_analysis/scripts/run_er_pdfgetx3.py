#!/usr/bin/env python3
"""Re-run pdfgetx3 for Er2O3 series with optimized Cu Ka parameters."""
import os
import sys
from series_data import ER_SAMPLES, ER_OUT

CFG_TEMPLATE = """\
[DEFAULT]

version = diffpy.pdfgetx-2.4.0

dataformat = twotheta
outputtypes = gr,sq,fq,iq

mode = xray
wavelength = 1.5406
twothetazero = 0
composition = {composition}
bgscales = 1.0
rpoly = 1.2
qmaxinst = 5.2
qmin = 0.5
qmax = 5.1
rmin = 1.0
rmax = 20.0
rstep = 0.01
"""


def process_one(sid, info, outdir):
    from diffpy.pdfgetx import PDFGetter, PDFConfig, loaddata

    xy = info["xy"]
    if not os.path.isfile(xy):
        raise FileNotFoundError(xy)

    comp = info["composition"].replace(" ", "")
    cfg = PDFConfig()
    cfg.mode = "xray"
    cfg.wavelength = 1.5406
    cfg.dataformat = "twotheta"
    cfg.twothetazero = 0
    cfg.composition = comp
    cfg.bgscales = 1.0
    cfg.rpoly = 1.2
    cfg.qmaxinst = 5.2
    cfg.qmin = 0.5
    cfg.qmax = 5.1
    cfg.rmin = 1.0
    cfg.rmax = 20.0
    cfg.rstep = 0.01
    cfg.outputtypes = ["gr", "sq", "fq", "iq"]

    pg = PDFGetter(config=cfg)
    x, y = loaddata(xy)
    pg(x, y)

    for otype in ("gr", "sq", "fq", "iq"):
        out = os.path.join(outdir, f"{sid}.{otype}")
        pg.writeOutput(out, otype)
        print(f"  wrote {out}")


def main():
    os.makedirs(ER_OUT, exist_ok=True)
    cfg_dir = os.path.join(ER_OUT, "configs")
    os.makedirs(cfg_dir, exist_ok=True)

    for sid, info in ER_SAMPLES.items():
        comp = info["composition"].replace(" ", "")
        cfg_path = os.path.join(cfg_dir, f"{sid}.cfg")
        with open(cfg_path, "w") as f:
            f.write(CFG_TEMPLATE.format(composition=comp))

        print(f"Processing {sid} ...")
        try:
            process_one(sid, info, ER_OUT)
            print(f"  OK: {sid}")
        except Exception as e:
            print(f"  FAILED {sid}: {e}", file=sys.stderr)
            # CLI fallback with proper config
            import subprocess
            cmd = [
                "pdfgetx3",
                "-c", cfg_path,
                "--force", "true",
                "-t", "gr,sq,fq,iq",
                "-o", os.path.join(ER_OUT, sid),
                info["xy"],
            ]
            print("  CLI fallback:", " ".join(cmd))
            r = subprocess.run(cmd, capture_output=True, text=True)
            print(r.stdout[-400:] if r.stdout else "")
            print(r.stderr[-400:] if r.stderr else "")
            if r.returncode != 0:
                print(f"  CLI also failed for {sid}", file=sys.stderr)

    print("\n--- Er outputs ---")
    for sid in ER_SAMPLES:
        for ext in ("gr", "sq", "fq", "iq"):
            p = os.path.join(ER_OUT, f"{sid}.{ext}")
            print(("OK" if os.path.isfile(p) else "MISSING"), p)


if __name__ == "__main__":
    main()
