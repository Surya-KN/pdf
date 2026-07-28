"""Shared helpers for Eu2O3 / Er2O3 glass PDF re-analysis."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

DPI = 300
BBOX = "tight"
WATERFALL_OFFSET_GR = 4.0      # spacing between stacked G(r) curves
WATERFALL_SCALE_GR = 2.5       # vertical amplify so first/main peaks read clearer
WATERFALL_OFFSET_gr = 1.2
WATERFALL_OFFSET_DIFF = 1.5
WATERFALL_OFFSET_FQ = 2.0
WATERFALL_XLIM = (1.0, 11.0)
LABEL_X = 10.8
LABEL_FONTSIZE = 10
LABEL_FONTWEIGHT = "bold"
EXTRA_OFFSET_SAMPLES = {"2D", "2E", "4_09042022", "5_09042022"}
PEAK_MARKER = "o"
PEAK_MARKERSIZE = 5
PEAK_FONTSIZE = 9

# Literature expected bond-length ranges (Å)
BOND_RANGES = {
    "B-O": (1.35, 1.50),
    "Zn-O": (1.90, 2.10),
    "Te-O": (1.90, 2.15),
    "Eu-O": (2.30, 2.50),
    "Er-O": (2.20, 2.45),
}


def parse_gr(filepath):
    """Parse pdfgetx3 .gr / .sq / .fq / .iq files (after #L header)."""
    data = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        in_data = False
        for line in f:
            if line.startswith("#L"):
                in_data = True
                continue
            if "#### start data" in line:
                in_data = True
                continue
            if not in_data:
                # also accept bare two-column numeric lines
                parts = line.strip().split()
                if len(parts) == 2:
                    try:
                        data.append([float(parts[0]), float(parts[1])])
                        in_data = True
                        continue
                    except ValueError:
                        pass
                continue
            if line.startswith("#"):
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                try:
                    data.append([float(parts[0]), float(parts[1])])
                except ValueError:
                    pass
    arr = np.array(data)
    if arr.size == 0:
        raise ValueError(f"No data parsed from {filepath}")
    return arr


def parse_sq_fq_iq(filepath):
    return parse_gr(filepath)


def Gr_to_gr(r, Gr, rho0):
    """G(r) [pdfgetx3] → g(r). g(r) = G(r)/(4*pi*rho0*r) + 1"""
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(r > 0.1, Gr / (4 * np.pi * rho0 * r) + 1, np.nan)


def Gr_to_Tr(r, Gr, rho0):
    """G(r) → T(r) = G(r) + 4*pi*rho0*r"""
    return Gr + 4 * np.pi * rho0 * r


def find_first_shell_peak(r, y, search_min=1.2, search_max=2.6, prominence=0.01):
    """First coordination-shell peak (cation–O / Te–O), typically ~1.9–2.2 Å.

    This is the *first* structural peak. Do not confuse with the stronger
    Te–Te peak near 3.5 Å (second shell in X-ray PDF of TeO2 glasses).
    Works on G(r) or g(r); no height>1 requirement (first shell often <1 in g(r)).
    """
    mask = (r >= search_min) & (r <= search_max)
    if not np.any(mask):
        return None, None
    r_range = r[mask]
    y_range = np.nan_to_num(y[mask], nan=-np.inf)
    peaks, props = find_peaks(y_range, prominence=prominence)
    if len(peaks) > 0:
        # true first peak = leftmost significant peak in the first-shell window
        best = peaks[0]
        return float(r_range[best]), float(y_range[best])
    idx = int(np.argmax(y_range))
    return float(r_range[idx]), float(y_range[idx])


def find_Te_Te_peak(r, gr, search_min=2.8, search_max=5.0):
    """Second-shell Te–Te peak in g(r) (~3.5–3.8 Å). Dominant in intensity, not first."""
    mask = (r >= search_min) & (r <= search_max)
    if not np.any(mask):
        return None, None
    gr_clean = np.nan_to_num(gr[mask], nan=1.0)
    r_range = r[mask]
    peaks, props = find_peaks(gr_clean, height=1.0, prominence=0.05)
    if len(peaks) > 0:
        best = peaks[np.argmax(props["prominences"])]
        return float(r_range[best]), float(gr_clean[best])
    idx = int(np.nanargmax(gr_clean))
    return float(r_range[idx]), float(gr_clean[idx])


def find_Te_Te_peak_Gr(r, Gr, search_min=2.8, search_max=5.0):
    """Second-shell Te–Te peak on G(r) (~3.5–3.8 Å)."""
    mask = (r >= search_min) & (r <= search_max)
    if not np.any(mask):
        return None, None
    r_range = r[mask]
    Gr_range = Gr[mask]
    peaks, props = find_peaks(Gr_range, prominence=0.05)
    if len(peaks) > 0:
        best = peaks[np.argmax(props["prominences"])]
        return float(r_range[best]), float(Gr_range[best])
    idx = int(np.argmax(Gr_range))
    return float(r_range[idx]), float(Gr_range[idx])


def gaussian(x, amp, center, width):
    return amp * np.exp(-0.5 * ((x - center) / width) ** 2)


def multi_gaussian(x, *params):
    n = len(params) // 3
    y = np.zeros_like(x, dtype=float)
    for i in range(n):
        y += gaussian(x, params[3 * i], params[3 * i + 1], params[3 * i + 2])
    return y


def fit_Tr_gaussians(r, Tr, centers, fit_min=1.0, fit_max=4.5, widths=None):
    """
    Fit sum of Gaussians to T(r) - 4*pi*rho0*r baseline already removed
    OR to raw T(r) with a linear baseline included via residual over baseline.

    We fit the oscillatory part: delta = T(r) - T_lin where T_lin is a
    straight line through the ends of the fit window, OR more simply fit
    Gaussians on T(r) directly with free amplitudes (can be negative for
    troughs). For glass PDF first-shell analysis we fit T(r) peaks.

    Returns dict of {label: {amp, center, width}} and full fit curve.
    """
    mask = (r >= fit_min) & (r <= fit_max)
    x = r[mask]
    y = Tr[mask]
    if widths is None:
        widths = [0.12] * len(centers)

    # initial params: amp from local max near each center
    p0 = []
    bounds_lo, bounds_hi = [], []
    for c, w in zip(centers, widths):
        local = (x >= c - 0.25) & (x <= c + 0.25)
        amp0 = float(np.nanmax(y[local]) - np.nanmin(y)) if np.any(local) else 1.0
        amp0 = max(amp0, 0.1)
        p0.extend([amp0, c, w])
        bounds_lo.extend([0.0, c - 0.25, 0.04])
        bounds_hi.extend([np.inf, c + 0.25, 0.40])

    try:
        popt, _ = curve_fit(
            multi_gaussian, x, y, p0=p0,
            bounds=(bounds_lo, bounds_hi), maxfev=20000
        )
    except Exception:
        popt = np.array(p0)

    yfit = multi_gaussian(x, *popt)
    components = []
    for i in range(len(centers)):
        components.append({
            "amp": float(popt[3 * i]),
            "center": float(popt[3 * i + 1]),
            "width": float(popt[3 * i + 2]),
            "curve": gaussian(x, popt[3 * i], popt[3 * i + 1], popt[3 * i + 2]),
        })
    return {
        "r": x,
        "y": y,
        "yfit": yfit,
        "residual": y - yfit,
        "components": components,
        "popt": popt,
    }


def apply_waterfall_style(ax, xlim=(1.0, 11)):
    ax.set_xlim(xlim)
    ax.set_yticks([])
    ax.set_xlabel("r (Å)", fontsize=12)
    ax.set_ylabel("Arb Units", fontsize=12)


def add_inline_label(ax, x_pos, y_val, label, color, extra_offset=0.0):
    ax.text(
        x_pos, y_val + 0.15 + extra_offset, label,
        color=color, ha="right", va="bottom",
        fontsize=LABEL_FONTSIZE, fontweight=LABEL_FONTWEIGHT,
    )


def savefig(fig, path):
    fig.savefig(path, dpi=DPI, bbox_inches=BBOX)
    plt.close(fig)
    print(f"  saved: {path}")


def find_fsdp(Q, S, qmin=0.4, qmax=1.5):
    """First sharp diffraction peak in S(Q)."""
    mask = (Q >= qmin) & (Q <= qmax)
    if not np.any(mask):
        # broaden search
        mask = (Q >= 0.5) & (Q <= 2.5)
    q = Q[mask]
    s = S[mask]
    peaks, props = find_peaks(s, prominence=0.01)
    if len(peaks) == 0:
        idx = int(np.argmax(s))
        return float(q[idx]), float(s[idx])
    best = peaks[np.argmax(props["prominences"])]
    return float(q[best]), float(s[best])
