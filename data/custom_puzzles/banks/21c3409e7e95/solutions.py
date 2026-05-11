"""Reference helper library and 21 reference solve functions for the twelfth custom ARC puzzle bank.

New primitive introduced in this set:
  component_graph(grid, connectivity=4, touch=4)
Return the non-zero connected components together with an adjacency map telling
which components touch by edge. This makes object-relation tasks explicit:
degree, clusters, shortest paths, articulation points, and matrix encodings.

All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 12.
"""
from typing import List
from collections import Counter, deque

Grid = List[List[int]]
dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]
dirs8 = dirs4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

def blank(h, w, v=0):
    return [[v]*w for _ in range(h)]


def copyg(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def inb(g, r, c):
    h, w = dims(g)
    return 0 <= r < h and 0 <= c < w


def bbox(cells):
    rs = [r for r,c in cells]
    cs = [c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop_cells(cells, fill_color=8):
    r1,c1,r2,c2 = bbox(cells)
    out = blank(r2-r1+1, c2-c1+1, 0)
    for r,c in cells:
        out[r-r1][c-c1] = fill_color
    return out


def components(grid, colors=None, connectivity=4, include_zero=False, ignore=None):
    if ignore is None:
        ignore = set()
    h, w = dims(grid)
    seen = [[False]*w for _ in range(h)]
    dirs = dirs4 if connectivity == 4 else dirs8
    out = []
    for r in range(h):
        for c in range(w):
            if seen[r][c] or (r,c) in ignore:
                continue
            seen[r][c] = True
            v = grid[r][c]
            if v == 0 and not include_zero:
                continue
            if colors is not None and v not in colors:
                continue
            stack = [(r,c)]
            cells = [(r,c)]
            while stack:
                rr, cc = stack.pop()
                for dr, dc in dirs:
                    nr, nc = rr+dr, cc+dc
                    if inb(grid, nr, nc) and not seen[nr][nc] and (nr,nc) not in ignore and grid[nr][nc] == v:
                        seen[nr][nc] = True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color": v, "cells": sorted(cells)})
    return out


def component_graph(grid, connectivity=4, touch=4):
    comps = components(grid, connectivity=connectivity)
    cell_to_comp = {}
    for i, comp in enumerate(comps):
        for cell in comp["cells"]:
            cell_to_comp[cell] = i
    dirs = dirs4 if touch == 4 else dirs8
    adj = {i: set() for i in range(len(comps))}
    for i, comp in enumerate(comps):
        for r,c in comp["cells"]:
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                if inb(grid, nr, nc) and grid[nr][nc] != 0:
                    j = cell_to_comp[(nr,nc)]
                    if j != i:
                        adj[i].add(j)
                        adj[j].add(i)
    return comps, adj


def graph_clusters(adj):
    seen = set()
    out = []
    for i in adj:
        if i in seen:
            continue
        stack = [i]
        seen.add(i)
        cur = []
        while stack:
            u = stack.pop()
            cur.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        out.append(sorted(cur))
    return out


def bfs_distances(adj, src):
    dist = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def shortest_path(adj, src, dst):
    prev = {src: None}
    q = deque([src])
    while q:
        u = q.popleft()
        if u == dst:
            break
        for v in adj[u]:
            if v not in prev:
                prev[v] = u
                q.append(v)
    if dst not in prev:
        return []
    path = []
    cur = dst
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    return list(reversed(path))


def articulation_points(adj):
    # Tarjan
    time = 0
    disc = {}
    low = {}
    parent = {}
    arts = set()
    def dfs(u):
        nonlocal time
        time += 1
        disc[u] = low[u] = time
        child_count = 0
        for v in adj[u]:
            if v not in disc:
                parent[v] = u
                child_count += 1
                dfs(v)
                low[u] = min(low[u], low[v])
                if u not in parent and child_count > 1:
                    arts.add(u)
                if u in parent and low[v] >= disc[u]:
                    arts.add(u)
            elif parent.get(u) != v:
                low[u] = min(low[u], disc[v])
    for u in adj:
        if u not in disc:
            dfs(u)
    return arts


def union_cells(comps, ids):
    cells = []
    for i in ids:
        cells.extend(comps[i]["cells"])
    return sorted(cells)


def extract_union_grid(grid, comps, ids, recolor=8, preserve_colors=False):
    cells = union_cells(comps, ids)
    r1,c1,r2,c2 = bbox(cells)
    out = blank(r2-r1+1, c2-c1+1, 0)
    idset = set(ids)
    cell_to_color = {}
    if preserve_colors:
        for i in ids:
            for r,c in comps[i]["cells"]:
                cell_to_color[(r,c)] = comps[i]["color"]
    for r,c in cells:
        out[r-r1][c-c1] = cell_to_color[(r,c)] if preserve_colors else recolor
    return out


def neighbor_color_set(comps, adj, i):
    return {comps[j]["color"] for j in adj[i]}


def touch_cells(grid):
    h, w = dims(grid)
    out = []
    for r in range(h):
        for c in range(w):
            v = grid[r][c]
            if v == 0:
                continue
            for dr,dc in dirs4:
                nr, nc = r+dr, c+dc
                if inb(grid, nr, nc) and grid[nr][nc] not in (0, v):
                    out.append((r,c))
                    break
    return sorted(out)


def split_by_vertical_bars(grid, color=5):
    h, w = dims(grid)
    bar_cols = [c for c in range(w) if all(grid[r][c] == color for r in range(h))]
    groups = []
    start = 0
    for c in bar_cols:
        groups.append((start, c))
        start = c+1
    groups.append((start, w))
    return groups, bar_cols


def crop_panel(grid, start, end):
    return [row[start:end] for row in grid]


def top_left(comp):
    return min(comp["cells"])


def sorted_ids_top_left(comps, ids):
    return sorted(ids, key=lambda i: top_left(comps[i]))


def solve_S12_E1(grid):
    comps, adj = component_graph(grid)
    out = copyg(grid)
    for i, comp in enumerate(comps):
        if comp["color"] == 1:
            for j in adj[i]:
                for r, c in comps[j]["cells"]:
                    out[r][c] = 4
    return out


def solve_S12_E2(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    out = blank(h, w, 0)
    for i, comp in enumerate(comps):
        if len(adj[i]) == 0:
            for r,c in comp["cells"]:
                out[r][c] = comp["color"]
    return out


def solve_S12_E3(grid):
    comps, adj = component_graph(grid)
    out = copyg(grid)
    for i, comp in enumerate(comps):
        if len(adj[i]) == 1:
            for r,c in comp["cells"]:
                out[r][c] = 8
    return out


def solve_S12_E4(grid):
    comps, adj = component_graph(grid)
    marker = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    target = sorted(adj[marker], key=lambda j: (len(comps[j]["cells"]), top_left(comps[j])))[0]
    return extract_union_grid(grid, comps, [target], recolor=8)


def solve_S12_E5(grid):
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r,c in touch_cells(grid):
        out[r][c] = 8
    return out


def solve_S12_E6(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    out = blank(h, w, 0)
    mapping = {0:3, 1:4, 2:6}
    for i, comp in enumerate(comps):
        color = mapping.get(len(adj[i]), 8)
        for r,c in comp["cells"]:
            out[r][c] = color
    return out


def solve_S12_E7(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    red = next(i for i, comp in enumerate(comps) if comp["color"] == 2)
    best = max(adj[red], key=lambda j: (len(comps[j]["cells"]), -top_left(comps[j])[0], -top_left(comps[j])[1]))
    out = blank(h, w, 0)
    for r,c in comps[best]["cells"]:
        out[r][c] = 8
    return out


def solve_S12_M1(grid):
    comps, adj = component_graph(grid)
    best = max(range(len(comps)), key=lambda i: (len(adj[i]), len(comps[i]["cells"]), tuple(-x for x in top_left(comps[i]))))
    return extract_union_grid(grid, comps, [best], recolor=8)


def solve_S12_M2(grid):
    comps, adj = component_graph(grid)
    seed = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    cluster = next(cl for cl in graph_clusters(adj) if seed in cl)
    return extract_union_grid(grid, comps, cluster, recolor=8)


def solve_S12_M3(grid):
    h, w = dims(grid)
    k = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    comps, adj = component_graph(body)
    out = blank(h, w, 0)
    for i, comp in enumerate(comps):
        if len(adj[i]) == k:
            for r,c in comp["cells"]:
                out[r+1][c] = 8
    return out


def solve_S12_M4(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    s = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    t = next(i for i, comp in enumerate(comps) if comp["color"] == 2)
    path = shortest_path(adj, s, t)
    out = blank(h, w, 0)
    for i in path:
        for r,c in comps[i]["cells"]:
            out[r][c] = 8
    return out


def solve_S12_M5(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    out = blank(h, w, 0)
    for i, comp in enumerate(comps):
        if len(neighbor_color_set(comps, adj, i)) >= 2:
            for r,c in comp["cells"]:
                out[r][c] = 8
    return out


def solve_S12_M6(grid):
    comps, adj = component_graph(grid)
    clusters = graph_clusters(adj)
    def key(cl):
        colors = {comps[i]["color"] for i in cl}
        return (len(colors), len(cl), len(union_cells(comps, cl)))
    best = max(clusters, key=key)
    return extract_union_grid(grid, comps, best, recolor=8)


def solve_S12_M7(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    seed = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    dist = bfs_distances(adj, seed)
    out = blank(h, w, 0)
    for i, d in dist.items():
        if d == 2:
            for r,c in comps[i]["cells"]:
                out[r][c] = 8
    return out


def solve_S12_H1(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    arts = articulation_points(adj)
    out = blank(h, w, 0)
    for i in arts:
        for r,c in comps[i]["cells"]:
            out[r][c] = 8
    return out


def solve_S12_H2(grid):
    groups, bars = split_by_vertical_bars(grid, color=5)
    sigs = []
    panels = []
    for start, end in groups:
        panel = crop_panel(grid, start, end)
        comps, adj = component_graph(panel)
        clusters = graph_clusters(adj)
        cl = max(clusters, key=lambda x: len(x))
        degs = tuple(sorted(len(adj[i]) for i in cl))
        sigs.append(degs)
        panels.append((panel, comps, cl))
    common = Counter(sigs).most_common(1)[0][0]
    odd_idx = next(i for i,s in enumerate(sigs) if s != common)
    panel, comps, cl = panels[odd_idx]
    return extract_union_grid(panel, comps, cl, recolor=8)


def solve_S12_H3(grid):
    want_cluster = sum(1 for v in grid[0] if v == 1)
    want_degree = sum(1 for v in grid[0] if v == 2)
    body = [row[:] for row in grid[1:]]
    comps, adj = component_graph(body)
    clusters = graph_clusters(adj)
    cluster_size = {}
    for cl in clusters:
        for i in cl:
            cluster_size[i] = len(cl)
    target = next(i for i in range(len(comps)) if cluster_size[i] == want_cluster and len(adj[i]) == want_degree)
    return extract_union_grid(body, comps, [target], recolor=8)


def solve_S12_H4(grid):
    h, w = dims(grid)
    comps, adj = component_graph(grid)
    seed = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    dist = bfs_distances(adj, seed)
    mapping = {0:2, 1:3, 2:4}
    out = blank(h, w, 0)
    for i, d in dist.items():
        color = mapping.get(d, 6)
        for r,c in comps[i]["cells"]:
            out[r][c] = color
    return out


def solve_S12_H5(grid):
    want_arts = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    comps, adj = component_graph(body)
    clusters = graph_clusters(adj)
    def art_count(cl):
        sub_adj = {i: sorted(j for j in adj[i] if j in cl) for i in cl}
        return len(articulation_points(sub_adj))
    target = next(cl for cl in clusters if art_count(cl) == want_arts)
    return extract_union_grid(body, comps, target, recolor=8)


def solve_S12_H6(grid):
    comps, adj = component_graph(grid)
    clusters = graph_clusters(adj)
    best = max(clusters, key=lambda cl: (len(cl), len(union_cells(comps, cl))))
    degs = sorted(len(adj[i]) for i in best)
    return [[d+1 for d in degs]]


def solve_S12_H7(grid):
    comps, adj = component_graph(grid)
    seed = next(i for i, comp in enumerate(comps) if comp["color"] == 1)
    cluster = next(cl for cl in graph_clusters(adj) if seed in cl)
    ids = sorted_ids_top_left(comps, cluster)
    idx = {cid:i for i,cid in enumerate(ids)}
    n = len(ids)
    out = blank(n, n, 0)
    for i in range(n):
        out[i][i] = 1
    for cid in ids:
        i = idx[cid]
        for nid in adj[cid]:
            if nid in idx:
                j = idx[nid]
                out[i][j] = 8
    return out


