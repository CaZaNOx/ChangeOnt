# Karp minimum mean cycle (simple, small graphs)
def karp_min_mean_cycle(n, edges):
    # edges: list of (u,v,w)
    INF = 1e18
    dp = [[INF]*n for _ in range(n+1)]
    for v in range(n):
        dp[0][v] = 0.0
    for k in range(1, n+1):
        for (u,v,w) in edges:
            if dp[k-1][u] + w < dp[k][v]:
                dp[k][v] = dp[k-1][u] + w
    best = (None, float("inf"))
    for v in range(n):
        max_avg = -float("inf")
        for k in range(n):
            if dp[n][v] < 1e17 and dp[k][v] < 1e17 and (n-k)>0:
                avg = (dp[n][v]-dp[k][v])/(n-k)
                if avg > max_avg:
                    max_avg = avg
        if max_avg < best[1]:
            best = (v, max_avg)
    return best[1] if best[0] is not None else None