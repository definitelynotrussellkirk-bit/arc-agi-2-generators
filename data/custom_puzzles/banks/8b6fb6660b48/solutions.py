
"""Reference helper library and 21 reference solve functions for the eleventh custom ARC puzzle bank.

New primitive introduced in this set:
  boundary_cells(cells, connectivity=4)
Return the subset of an object's cells that touch background or the outside in the chosen connectivity. This is useful for outline extraction, perimeter-based ranking, and separating boundary from interior.
"""
from typing import List, Dict, Tuple
from collections import Counter, defaultdict

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

def norm_cells(cells):
    r1,c1,r2,c2 = bbox(cells)
    return sorted((r-r1, c-c1) for r,c in cells)

def rotate_pts(pts, k=1):
    pts = list(pts)
    for _ in range(k % 4):
        maxr = max(r for r,c in pts)
        pts = [(c, maxr-r) for r,c in pts]
        rmin = min(r for r,c in pts)
        cmin = min(c for r,c in pts)
        pts = [(r-rmin, c-cmin) for r,c in pts]
    return sorted(pts)

def mirror_h_pts(pts):
    pts = list(pts)
    maxc = max(c for r,c in pts)
    return sorted((r, maxc-c) for r,c in pts)

def mirror_v_pts(pts):
    pts = list(pts)
    maxr = max(r for r,c in pts)
    return sorted((maxr-r, c) for r,c in pts)

def dihedral_variants(pts):
    pts = norm_cells(pts)
    out = []
    for k in range(4):
        r = rotate_pts(pts, k)
        out.append(tuple(r))
        out.append(tuple(mirror_h_pts(r)))
    uniq = []
    for v in out:
        if v not in uniq:
            uniq.append(v)
    return uniq

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

def boundary_cells(cells, connectivity=4):
    s = set(cells)
    dirs = dirs4 if connectivity == 4 else dirs8
    out = []
    for r, c in cells:
        if any((r+dr, c+dc) not in s for dr,dc in dirs):
            out.append((r,c))
    return sorted(out)

def rect_border(r1, c1, r2, c2):
    cells = set()
    for c in range(c1, c2+1):
        cells.add((r1,c)); cells.add((r2,c))
    for r in range(r1, r2+1):
        cells.add((r,c1)); cells.add((r,c2))
    return sorted(cells)

def enclosed_zero_regions(grid):
    h, w = dims(grid)
    out = []
    for comp in components(grid, colors={0}, include_zero=True):
        cells = comp["cells"]
        if not any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            out.append(cells)
    return out

def normalized_component_grid(grid, comp_cells, use_boundary=False, recolor=None):
    r1,c1,r2,c2 = bbox(comp_cells)
    H, W = r2-r1+1, c2-c1+1
    out = blank(H, W, 0)
    cells = boundary_cells(comp_cells) if use_boundary else comp_cells
    color = recolor if recolor is not None else grid[comp_cells[0][0]][comp_cells[0][1]]
    for r, c in cells:
        out[r-r1][c-c1] = color
    return out

def hole_count_for_component(grid, comp_cells):
    r1,c1,r2,c2 = bbox(comp_cells)
    H, W = r2-r1+1, c2-c1+1
    sub = blank(H, W, 0)
    for r,c in comp_cells:
        sub[r-r1][c-c1] = 1
    seen = [[False]*W for _ in range(H)]
    holes = 0
    for r in range(H):
        for c in range(W):
            if sub[r][c] != 0 or seen[r][c]:
                continue
            stack = [(r,c)]
            seen[r][c] = True
            touches = (r in (0,H-1) or c in (0,W-1))
            while stack:
                rr, cc = stack.pop()
                for dr, dc in dirs4:
                    nr, nc = rr+dr, cc+dc
                    if 0 <= nr < H and 0 <= nc < W and not seen[nr][nc] and sub[nr][nc] == 0:
                        seen[nr][nc] = True
                        stack.append((nr,nc))
                        if nr in (0,H-1) or nc in (0,W-1):
                            touches = True
            if not touches:
                holes += 1
    return holes

def split_by_vertical_bars(grid, bar_color=5):
    h, w = dims(grid)
    bar_cols = [c for c in range(w) if all(grid[r][c] == bar_color for r in range(h))]
    return bar_cols

def canonical_signature(cells):
    return min(dihedral_variants(cells))

def solve_S11_E1(grid):
    out = blank(*dims(grid), 0)
    for comp in components(grid):
        for r,c in boundary_cells(comp["cells"]):
            out[r][c] = comp["color"]
    return out

def solve_S11_E2(grid):
    out = copyg(grid)
    for comp in components(grid):
        cells = comp["cells"]
        r1,c1,r2,c2 = bbox(cells)
        if set(cells) == set(rect_border(r1,c1,r2,c2)):
            for r in range(r1+1, r2):
                for c in range(c1+1, c2):
                    if out[r][c] == 0:
                        out[r][c] = 8
    return out

def solve_S11_E3(grid):
    best = min(components(grid), key=lambda c: (len(c["cells"]), c["color"]))
    return normalized_component_grid(grid, best["cells"])

def solve_S11_E4(grid):
    out = copyg(grid)
    for comp in components(grid):
        cells = comp["cells"]
        rs = {r for r,c in cells}
        cs = {c for r,c in cells}
        if len(rs) == 1 and len(cells) >= 2:
            r = next(iter(rs))
            out[r][min(cs)] = 8
            out[r][max(cs)] = 8
        elif len(cs) == 1 and len(cells) >= 2:
            c = next(iter(cs))
            out[min(rs)][c] = 8
            out[max(rs)][c] = 8
    return out

def solve_S11_E5(grid):
    h, w = dims(grid)
    anchor = next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 1)
    comp = max([c for c in components(grid) if c["color"] != 1], key=lambda c: len(c["cells"]))
    r1,c1,r2,c2 = bbox(comp["cells"])
    dr, dc = anchor[0]-r1, anchor[1]-c1
    out = blank(h, w, 0)
    for r,c in boundary_cells(comp["cells"]):
        nr, nc = r+dr, c+dc
        if 0 <= nr < h and 0 <= nc < w:
            out[nr][nc] = comp["color"]
    return out

def solve_S11_E6(grid):
    out = copyg(grid)
    h, w = dims(grid)
    axis_col = next(c for c in range(w) if all(grid[r][c] == 5 for r in range(h)))
    for r in range(h):
        for c in range(w):
            v = grid[r][c]
            if v not in (0,5) and c != axis_col:
                mc = 2*axis_col - c
                if 0 <= mc < w and out[r][mc] == 0:
                    out[r][mc] = v
    return out

def solve_S11_E7(grid):
    out = blank(*dims(grid), 0)
    for comp in components(grid):
        r1,c1,r2,c2 = bbox(comp["cells"])
        for r,c in {(r1,c1),(r1,c2),(r2,c1),(r2,c2)}:
            out[r][c] = comp["color"]
    return out

def solve_S11_M1(grid):
    best = max(components(grid), key=lambda c: (len(boundary_cells(c["cells"])), len(c["cells"]), c["color"]))
    out = blank(*dims(grid), 0)
    for r,c in best["cells"]:
        out[r][c] = 8
    return out

def solve_S11_M2(grid):
    out = copyg(grid)
    for cells in enclosed_zero_regions(grid):
        for r,c in cells:
            out[r][c] = 8
    return out

def solve_S11_M3(grid):
    n = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    best = next(comp for comp in components(body) if len(boundary_cells(comp["cells"])) == n)
    return normalized_component_grid(body, best["cells"], use_boundary=True)

def solve_S11_M4(grid):
    out = blank(*dims(grid), 0)
    pos = defaultdict(list)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v != 0:
                pos[v].append((r,c))
    for v, cells in pos.items():
        if len(cells) == 2:
            (r1,c1),(r2,c2) = cells
            for r,c in rect_border(min(r1,r2), min(c1,c2), max(r1,r2), max(c1,c2)):
                out[r][c] = v
    return out

def solve_S11_M5(grid):
    best = max(components(grid), key=lambda c: (len(c["cells"]), len(boundary_cells(c["cells"]))))
    pts = norm_cells(best["cells"])
    union = sorted(set(pts) | set(mirror_h_pts(pts)))
    rmax = max(r for r,c in union)
    cmax = max(c for r,c in union)
    out = blank(rmax+1, cmax+1, 0)
    for r,c in union:
        out[r][c] = best["color"]
    return out

def solve_S11_M6(grid):
    bars = split_by_vertical_bars(grid, 5)
    c = bars[0]
    left = [row[:c] for row in grid]
    right = [row[c+1:] for row in grid]
    h, w = dims(left)
    out = blank(h, w, 0)
    for r in range(h):
        for cc in range(w):
            if (left[r][cc] != 0) ^ (right[r][cc] != 0):
                out[r][cc] = 8
    return out

def solve_S11_M7(grid):
    legend = [v for v in grid[0] if v != 0]
    out = copyg(grid)
    body = [row[:] for row in grid[1:]]
    comps = sorted(components(body), key=lambda c: (len(c["cells"]), c["cells"][0]))
    for comp, color in zip(comps, legend):
        for r,c in comp["cells"]:
            out[r+1][c] = color
    return out

def solve_S11_H1(grid):
    out = copyg(grid)
    frames = []
    for comp in components(grid):
        cells = comp["cells"]
        r1,c1,r2,c2 = bbox(cells)
        if set(cells) == set(rect_border(r1,c1,r2,c2)):
            frames.append(((r2-r1+1)*(c2-c1+1), (r1,c1,r2,c2), comp["color"]))
    frames.sort()
    h, w = dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 0:
                for _, (r1,c1,r2,c2), color in frames:
                    if r1 < r < r2 and c1 < c < c2:
                        out[r][c] = color
                        break
    return out

def solve_S11_H2(grid):
    code_to_rot = {1:0, 3:1, 4:2, 6:3}
    template = max([c for c in components(grid) if c["color"] == 2], key=lambda c: len(c["cells"]))
    pts = norm_cells(boundary_cells(template["cells"]))
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v in code_to_rot:
                rot_pts = rotate_pts(pts, code_to_rot[v])
                for rr,cc in rot_pts:
                    nr, nc = r+rr, c+cc
                    if 0 <= nr < h and 0 <= nc < w:
                        out[nr][nc] = 8
    return out

def solve_S11_H3(grid):
    k = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    best = next(comp for comp in components(body) if hole_count_for_component(body, comp["cells"]) == k)
    return normalized_component_grid(body, best["cells"], use_boundary=True, recolor=8)

def solve_S11_H4(grid):
    sigs = defaultdict(list)
    for comp in components(grid):
        sigs[canonical_signature(comp["cells"])].append(comp)
    unmatched = [vals[0] for vals in sigs.values() if len(vals) == 1]
    best = unmatched[0]
    return normalized_component_grid(grid, best["cells"], use_boundary=True)

def solve_S11_H5(grid):
    h, w = dims(grid)
    src = next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 1)
    dst = next((r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == 2)
    comp = max([c for c in components(grid) if c["color"] not in (1,2)], key=lambda c: len(c["cells"]))
    bc = set(boundary_cells(comp["cells"]))
    dr, dc = dst[0]-src[0], dst[1]-src[1]
    out = blank(h, w, 0)
    for r,c in comp["cells"]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < h and 0 <= nc < w:
            out[nr][nc] = 7 if (r,c) in bc else 8
    return out

def solve_S11_H6(grid):
    area = sum(1 for v in grid[0] if v == 1)
    bcount = sum(1 for v in grid[0] if v == 2)
    body = [row[:] for row in grid[1:]]
    best = next(comp for comp in components(body) if len(comp["cells"]) == area and len(boundary_cells(comp["cells"])) == bcount)
    return normalized_component_grid(body, best["cells"], use_boundary=False, recolor=8)

def solve_S11_H7(grid):
    bars = split_by_vertical_bars(grid, 5)
    c1, c2 = bars
    panels = [
        [row[:c1] for row in grid],
        [row[c1+1:c2] for row in grid],
        [row[c2+1:] for row in grid],
    ]
    sigs = []
    for p in panels:
        comp = max(components(p), key=lambda c: len(c["cells"]))
        sigs.append(canonical_signature(comp["cells"]))
    common_sig = Counter(sigs).most_common(1)[0][0]
    pts = list(common_sig)
    rmax = max(r for r,c in pts)
    cmax = max(c for r,c in pts)
    out = blank(rmax+1, cmax+1, 0)
    for r,c in pts:
        out[r][c] = 8
    return out
