from __future__ import annotations  
from typing import Dict, List, Tuple  
import statistics

def _iqr(xs: List[float]) -> float:  
    if not xs: return 0.0  
    q1 = percentile(xs, 25)  
    q3 = percentile(xs, 75)  
    return float(q3 - q1)

def percentile(xs: List[float], p: float) -> float:  
    if not xs: return 0.0  
    ys = sorted(xs)  
    k = (len(ys) - 1) * (p / 100.0)  
    f = int(k)  
    c = min(f + 1, len(ys) - 1)  
    if f == c: return float(ys[int(k)])  
    d0 = ys[f] * (c - k)  
    d1 = ys[c] * (k - f)  
    return float(d0 + d1)

def summarize_episode_rows(rows: List[Dict]) -> Dict:  
    flips = [r["flips"] for r in rows]  
    fdrs = [r["FDR_windowed"] for r in rows]  
    slopes = [r["slope_window"] for r in rows]  
    aurs = [r["AUReg_window"] for r in rows]  
    return {  
    "flips_mean": float(statistics.mean(flips)) if flips else 0.0,  
    "flips_iqr": _iqr(flips) if flips else 0.0,  
    "fdr_mean": float(statistics.mean(fdrs)) if fdrs else 0.0,  
    "fdr_iqr": _iqr(fdrs) if fdrs else 0.0,  
    "slope_mean": float(statistics.mean(slopes)) if slopes else 0.0,  
    "slope_iqr": _iqr(slopes) if slopes else 0.0,  
    "au_mean": float(statistics.mean(aurs)) if aurs else 0.0,  
    "au_iqr": _iqr(aurs) if aurs else 0.0,  
    "n_episodes": len(rows),  
    }

def rows_to_markdown(rows: List[Dict]) -> str:  
    hdr = "| ep | flips | FDR_windowed | slope_window | AUReg_window |\n|---:|-----:|--------------:|-------------:|-------------:|"  
    body = "\n".join(  
    f"| {r['ep']:>2} | {r['flips']:>5} | {r['FDR_windowed']:.3f} | {r['slope_window']:.4f} | {r['AUReg_window']:.4f} |"  
    for r in rows  
    )  
    return hdr + "\n" + body