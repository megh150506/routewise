"""DAA algorithms, written by hand. Every algorithm records its steps ("frames") so the frontend can animate it."""
import math, time, itertools
from data import PLACES, EDGES, FACILITIES, WEIGHTS, FLOOD_NODE, key
nm = lambda i: PLACES[i][0]

def adj(blocked=(), flood=False):
    bl = {key(a, b) for a, b in blocked}
    A = [[] for _ in PLACES]
    for a, b in EDGES:
        k = key(a, b)
        if k in bl: continue
        w = WEIGHTS[k] * (3 if flood and FLOOD_NODE in (a, b) else 1)
        A[a].append((b, w)); A[b].append((a, w))
    return A

def plen(p): return sum(WEIGHTS[key(p[i-1], p[i])] for i in range(1, len(p)))
def path_to(pr, t):
    p = []
    while t is not None: p.insert(0, t); t = pr.get(t)
    return p
def tour_len(t, M): return sum(M[t[i]][t[(i+1) % len(t)]] for i in range(len(t)))

def sp(A, s, t=None):
    """Dijkstra, O(V^2) array version. Greedy: always settle the closest unsettled node."""
    n = len(PLACES); d = [math.inf]*n; pr = {}; done = []; fr = []; ops = 0; d[s] = 0
    while True:
        u = -1
        for i in range(n):
            ops += 1
            if i not in done and d[i] < math.inf and (u < 0 or d[i] < d[u]): u = i
        if u < 0: break
        done.append(u); fr.append({"v": list(done), "t": f"Visit {nm(u)}: shortest distance so far {d[u]:.1f} km"})
        if u == t: break
        for v, w in A[u]:
            ops += 1
            if d[u]+w < d[v]:
                d[v] = d[u]+w; pr[v] = u
                fr.append({"v": list(done), "e": [[u, v]], "t": f"Relax {nm(u)} → {nm(v)}: new distance {d[v]:.1f} km"})
    return d, pr, fr, ops

def nn(M, N):
    """Nearest Neighbor (greedy), O(n^2)."""
    n = len(M); t = [0]; fr = []; ops = 0
    while len(t) < n:
        l = t[-1]; b = -1
        for j in range(n):
            ops += 1
            if j not in t and (b < 0 or M[l][j] < M[l][b]): b = j
        t.append(b); fr.append({"tour": list(t), "t": f"Greedy: nearest unvisited stop from {N[l]} is {N[b]} ({M[l][b]:.1f} km)"})
    return t, fr, ops

def mst2(M, N):
    """MST-based 2-approximation: Prim's MST, then preorder walk with shortcuts. Tour <= 2 x optimal (metric distances)."""
    n = len(M); inn = [0]; ed = []; fr = []; ops = 0; ky = [math.inf] + M[0][1:]; p = [0]*n
    while len(inn) < n:
        b = -1
        for j in range(n):
            ops += 1
            if j not in inn and (b < 0 or ky[j] < ky[b]): b = j
        ed.append([p[b], b]); inn.append(b)
        fr.append({"mst": [list(e) for e in ed], "t": f"Prim adds MST edge {N[p[b]]} – {N[b]} ({ky[b]:.1f} km)"})
        for j in range(n):
            if j not in inn and M[b][j] < ky[j]: ky[j] = M[b][j]; p[j] = b
    ch = [[] for _ in range(n)]
    for a, b in ed: ch[a].append(b)
    t = []
    def pre(u):
        t.append(u)
        for c in ch[u]: pre(c)
    pre(0)
    fr.append({"mst": ed, "tour": t, "t": "Preorder walk of the MST with shortcuts: " + " → ".join(N[x] for x in t)})
    return t, fr, ops

def bf(M, N):
    """Brute force over all (n-1)! tours. Exact, tiny inputs only."""
    n = len(M); best = math.inf; bt = []; fr = []; ops = 0
    for p in itertools.permutations(range(1, n)):
        ops += 1; t = [0, *p]; l = tour_len(t, M)
        if l < best:
            best, bt = l, t
            fr.append({"tour": t, "t": f"New best tour: {l:.1f} km (after {ops} permutations)"})
    return bt, fr, ops

def hk(M, N):
    """Held-Karp dynamic programming, O(n^2 * 2^n). Exact."""
    n = len(M); Z = 1 << n; INF = math.inf
    dp = [[INF]*n for _ in range(Z)]; pa = [[-1]*n for _ in range(Z)]; ops = 0; dp[1][0] = 0
    for m in range(1, Z, 2):
        for j in range(n):
            if dp[m][j] == INF: continue
            for k in range(1, n):
                if m & (1 << k): continue
                ops += 1; nm_ = m | 1 << k; v = dp[m][j] + M[j][k]
                if v < dp[nm_][k]: dp[nm_][k] = v; pa[nm_][k] = j
    b, l = INF, -1
    for j in range(1, n):
        v = dp[Z-1][j] + M[j][0]
        if v < b: b, l = v, j
    t = []; m = Z-1; j = l
    while j > 0: t.insert(0, j); q = pa[m][j]; m ^= 1 << j; j = q
    t.insert(0, 0)
    return t, [{"tour": t, "t": f"DP over {Z >> 1} subset states gives the optimal tour: {b:.1f} km"}], ops

def solve_tour(stops):
    A = adj(); N = [nm(s) for s in stops]; k = len(stops)
    S = [sp(A, s) for s in stops]
    M = [[S[i][0][j] for j in stops] for i in range(k)]
    paths = [[path_to(S[i][1], j) for j in stops] for i in range(k)]
    out = {}
    for key_, f, mx in (("mst", mst2, None), ("nn", nn, None), ("bf", bf, 9), ("hk", hk, 13)):
        if mx and k > mx: out[key_] = {"skip": 1}; continue
        t0 = time.perf_counter(); t, fr, ops = f(M, N)
        out[key_] = {"t": t, "fr": fr, "ops": ops, "ms": (time.perf_counter()-t0)*1000, "d": tour_len(t, M)}
    t0 = time.perf_counter(); d, pr, fr, ops = sp(A, stops[0], stops[-1]); path = path_to(pr, stops[-1])
    out["dij"] = {"path": path, "fr": fr, "ops": ops, "ms": (time.perf_counter()-t0)*1000, "d": plen(path)}
    return {"out": out, "paths": paths}

def route(src, dst, blocked, flood):
    d, pr, fr, ops = sp(adj(blocked, flood), src, dst)
    path = path_to(pr, dst) if d[dst] < math.inf else []
    return {"path": path, "km": plen(path) if path else None, "fr": fr, "ops": ops}

def nearest(src, cat, blocked, flood):
    d, pr, _, _ = sp(adj(blocked, flood), src); res = []
    for i, f in enumerate(FACILITIES):
        if f["t"] == cat:
            res.append({**f, "id": i, "km": plen(path_to(pr, f["at"])) if d[f["at"]] < math.inf else None})
    return sorted(res, key=lambda r: (r["km"] is None, r["km"] or 0))

def explain(src, dst, nodes, blocked):
    """Dijkstra on a small sub-graph, logging every relaxation so the UI can explain the choice."""
    bl = {key(a, b) for a, b in blocked}; S = set(nodes); A = {i: [] for i in nodes}
    for a, b in EDGES:
        if a in S and b in S and key(a, b) not in bl:
            A[a].append((b, WEIGHTS[key(a, b)])); A[b].append((a, WEIGHTS[key(a, b)]))
    d = {i: math.inf for i in nodes}; d[src] = 0; pr = {}; done = []; steps = []
    while True:
        cand = [i for i in nodes if i not in done and d[i] < math.inf]
        if not cand: break
        u = min(cand, key=lambda i: d[i]); done.append(u); rel = []
        for v, w in A[u]:
            if v in done: continue
            new = d[u] + w; ok = new < d[v]
            rel.append({"v": v, "w": round(w, 2), "old": None if d[v] == math.inf else round(d[v], 2), "new": round(new, 2), "ok": ok})
            if ok: d[v] = new; pr[v] = u
        steps.append({"u": u, "du": round(d[u], 2), "settled": list(done), "dist": {i: round(x, 2) for i, x in d.items() if x < math.inf}, "relax": rel})
        if u == dst: break
    path = path_to(pr, dst) if d[dst] < math.inf else []
    allp = []
    def dfs(u, seen, l):
        if u == dst: allp.append((l, list(seen))); return
        for v, w in A[u]:
            if v not in seen: seen.append(v); dfs(v, seen, l + w); seen.pop()
    dfs(src, [src], 0); allp.sort()
    return {"steps": steps, "path": path, "km": round(d[dst], 2) if path else None, "paths": [{"km": round(l, 2), "path": p} for l, p in allp[:4]]}

def complexity():
    """Empirical complexity experiment: same random stops, growing n, count operations and time."""
    import random
    rnd = random.Random(7); ids = list(range(len(PLACES))); rnd.shuffle(ids); A = adj(); rows = []
    for n in range(3, 13):
        stops = ids[:n]; S = [sp(A, s) for s in stops]; N = [nm(s) for s in stops]
        M = [[S[i][0][j] for j in stops] for i in range(n)]; row = {"n": n}
        for k, f, mx in (("mst", mst2, 99), ("nn", nn, 99), ("bf", bf, 9), ("hk", hk, 12)):
            if n > mx: continue
            t0 = time.perf_counter(); _, _, ops = f(M, N)
            row[k] = {"ms": (time.perf_counter() - t0) * 1000, "ops": ops}
        rows.append(row)
    return rows
