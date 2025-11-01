#!/usr/bin/env python3
import math

# -------- Configuration --------
MOD = 4096          # 2^12 for the real test; try 256 for a quick demo
ENTER_TO_B3 = True  # On any entry to 15 (mod 16), start at phase b3 (safe over-approx)

# -------- Basic odd-step mechanics --------
def v2(x: int) -> int:
    c = 0
    while x & 1 == 0:
        x >>= 1
        c += 1
    return c

def odd_step(n: int):
    """Return (next_odd, k) for one odd-only Collatz step on odd n (>0)."""
    assert n & 1
    m = 3*n + 1
    k = v2(m)
    return (m >> k), k  # next odd, number of divisions by 2

def is15(res: int) -> bool:
    return (res & 0xF) == 0xF  # res % 16 == 15

ODD = [r for r in range(1, MOD, 2)]
PHASES = ("N","b3","b2","b1")  # not-in-burst; 3-step burst phases

# -------- State graph (phase-only; no cleanup) --------
# State: (residue r, phase p)
# Transition: one odd step from r with weight w = log(3) - k*log(2),
# and phase update:
#   N: if next residue in 15-class -> b3 (burst starts), else N
#   b3 -> b2, b2 -> b1, b1 -> N (ejects immediately; NO "cleanup" here)

def next_state(r: int, p: str):
    y, k = odd_step(r)
    y %= MOD
    w = math.log(3.0) - k*math.log(2.0)
    if p == "N":
        if is15(y):
            return (y, "b3" if ENTER_TO_B3 else "b2", k, w, True)  # entered 15
        else:
            return (y, "N", k, w, False)
    elif p == "b3":
        return (y, "b2", k, w, False)
    elif p == "b2":
        return (y, "b1", k, w, False)
    elif p == "b1":
        return (y, "N",  k, w, False)
    else:
        raise RuntimeError("bad phase")

# Build states and one-successor structure
STATES = [(r,p) for r in ODD for p in PHASES]
IDX = {s:i for i,s in enumerate(STATES)}
N = len(STATES)

succ = [0]*N           # index of successor state
wgt  = [0.0]*N         # weight on edge (state -> successor)
kval = [0]*N           # k on that edge
enter15 = [False]*N    # did this edge enter the 15-class?

for i, (r,p) in enumerate(STATES):
    y, p2, k, w, ent = next_state(r,p)
    succ[i] = IDX[(y,p2)]
    wgt[i] = w
    kval[i] = k
    enter15[i] = ent

# -------- Karp (max cycle mean) for one-successor graphs --------
def max_cycle_mean_one_succ(succ, w):
    n = len(succ)
    vis = [False]*n
    best_mean = -1e300
    best_cycle = None
    for s in range(n):
        if vis[s]: continue
        where = {}
        seq = []
        u = s
        while not vis[u] and u not in where:
            where[u] = len(seq)
            seq.append(u)
            u = succ[u]
        for v in seq:
            vis[v] = True
        if u in where:
            cyc = seq[where[u]:]
            tot = sum(w[v] for v in cyc)
            mean = tot / len(cyc)
            if mean > best_mean:
                best_mean = mean
                best_cycle = cyc
    return best_mean, best_cycle

mean, cyc = max_cycle_mean_one_succ(succ, wgt)

def summarize_cycle(cyc):
    print(f"Cycle length: {len(cyc)}   mean={sum(wgt[v] for v in cyc)/len(cyc):+.9f}")
    # Print the first ~40 edges for readability
    limit = min(40, len(cyc))
    print("idx: (r, phase)  --k-->  (r', phase')   weight    enter15?")
    for j in range(limit):
        v = cyc[j]
        r, p = STATES[v]
        v2 = succ[v]
        r2, p2 = STATES[v2]
        k = kval[v]
        w = wgt[v]
        e15 = enter15[v]
        print(f"{j:3d}: ({r:4d}, {p:>2s})  --{k}-->  ({r2:4d}, {p2:>2s})   {w:+.6f}   {e15}")
    if len(cyc) > limit:
        print("... (truncated)")
    # Analyze runs of k=1 between entries to 15
    runs = []
    cur = 0
    for j in range(len(cyc)):
        v = cyc[j]
        if enter15[v]:
            runs.append(cur)
            cur = 0
        else:
            if kval[v] == 1:
                cur += 1
            else:
                # break the run
                if cur:
                    runs.append(cur)
                    cur = 0
    if cur:
        runs.append(cur)
    if runs:
        print("k=1 run lengths between 15-entries (coarsely measured along the cycle):", runs)

if mean < 0:
    print("✅ Phase-only graph: max cycle mean < 0")
    print(f"Mean ≈ {mean:.9f}")
else:
    print("❌ Phase-only graph: nonnegative cycle mean")
    print(f"Mean ≈ {mean:.9f}")
    summarize_cycle(cyc)