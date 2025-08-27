import numpy as np

def theil_sen_slope(ts, vs, max_pairs=400):
    n = len(ts)
    if n < 2: return 0.0
    pairs = []
    step = max(1, int(np.ceil(n/np.sqrt(max_pairs))))
    idxs = list(range(0, n, step))
    for i in idxs:
        for j in idxs:
            if j>i and ts[j]!=ts[i]:
                pairs.append( (vs[j]-vs[i])/(ts[j]-ts[i]) )
                if len(pairs)>=max_pairs: break
        if len(pairs)>=max_pairs: break
    return float(np.median(pairs)) if pairs else 0.0

def fdr_windowed(flip_times, event_times, delta=6):
    if not flip_times: return 0.0
    ev = sorted(event_times)
    hits = 0
    for f in flip_times:
        ok = any(abs(f-e)<=delta for e in ev)
        hits += 1 if ok else 0
    return 1.0 - hits/max(1,len(flip_times))  # false discovery rate

def summarize_episode(agent_name, ep, flips, events, outpath, mcfg):
    sl_win = int(mcfg.get("slope_window", 100))
    # slope over pseudo reward series (1 at flips, -1 at misses) just as a stable, cheap probe
    T = max(events+flips+[0])+1
    ts = list(range(max(2, min(T, sl_win))))
    vs = [1.0 if t in flips else 0.0 for t in ts]
    slope = theil_sen_slope(ts, vs, max_pairs=400)
    fdr = fdr_windowed(flips, events, delta=int(mcfg.get("delta_align",6)))
    return {"agent":agent_name, "ep":ep, "flips":len(flips), "FDRw":fdr, "slope":slope, "log":outpath}