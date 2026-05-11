"""Reference helper library and 21 reference solve functions for the fourteenth custom ARC puzzle bank.

New primitive introduced in this set:
  profile_signature(cells, trim=True)

Return the row and column occupancy counts of a connected component inside its
tight bounding box. This makes profile-oriented ARC tasks explicit:
span closure by row/column, profile matching, canonical histograms,
panel/profile comparisons, and symbolic outputs built from row/column
signatures.

All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 14.
"""
from typing import List
from collections import Counter, defaultdict

Grid = List[List[int]]
dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h, w, v=0):
    return [[v] * w for _ in range(h)]

def copyg(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def components(grid, connectivity=4, colors=None, include_zero=False):
    h, w = dims(grid)
    seen = [[False] * w for _ in range(h)]
    dirs = dirs4
    out = []
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c] = True
            v = grid[r][c]
            if v == 0 and not include_zero:
                continue
            if colors is not None and v not in colors:
                continue
            stack = [(r, c)]
            cells = [(r, c)]
            while stack:
                rr, cc = stack.pop()
                for dr, dc in dirs:
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and grid[nr][nc] == v:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
                        cells.append((nr, nc))
            out.append({"color": v, "cells": cells})
    return out

def bbox(cells):
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_mask(cells):
    r1, c1, r2, c2 = bbox(cells)
    h, w = r2 - r1 + 1, c2 - c1 + 1
    out = blank(h, w, 0)
    for r, c in cells:
        out[r - r1][c - c1] = 1
    return out

def row_profile_cells(cells):
    m = crop_mask(cells)
    return [sum(row) for row in m]

def col_profile_cells(cells):
    m = crop_mask(cells)
    h, w = dims(m)
    return [sum(m[r][c] for r in range(h)) for c in range(w)]

def profile_signature(cells, trim=True):
    return {
        "rows": row_profile_cells(cells),
        "cols": col_profile_cells(cells),
    }

def top_left_of_comp(comp):
    r1, c1, _, _ = bbox(comp["cells"])
    return (r1, c1)

def crop_component(comp, recolor=8):
    r1, c1, r2, c2 = bbox(comp["cells"])
    out = blank(r2 - r1 + 1, c2 - c1 + 1, 0)
    for r, c in comp["cells"]:
        out[r - r1][c - c1] = recolor
    return out

def max_row_peak(comp):
    return max(row_profile_cells(comp["cells"]))

def max_col_peak(comp):
    return max(col_profile_cells(comp["cells"]))

def constant_row_profile(comp):
    rp = row_profile_cells(comp["cells"])
    return len(set(rp)) == 1

def fill_row_spans_component(comp):
    cells = set(comp["cells"])
    out = set(cells)
    rows = defaultdict(list)
    for r, c in cells:
        rows[r].append(c)
    for r, cols in rows.items():
        for c in range(min(cols), max(cols) + 1):
            out.add((r, c))
    return out

def fill_col_spans_component(comp):
    cells = set(comp["cells"])
    out = set(cells)
    cols = defaultdict(list)
    for r, c in cells:
        cols[c].append(r)
    for c, rs in cols.items():
        for r in range(min(rs), max(rs) + 1):
            out.add((r, c))
    return out

def row_fill_same_size_excluding(grid, banned_colors=()):
    out = copyg(grid)
    banned = set(banned_colors)
    for comp in components(grid):
        if comp["color"] in banned:
            continue
        for r, c in fill_row_spans_component(comp):
            out[r][c] = comp["color"]
    return out

def col_fill_same_size_excluding(grid, banned_colors=()):
    out = copyg(grid)
    banned = set(banned_colors)
    for comp in components(grid):
        if comp["color"] in banned:
            continue
        for r, c in fill_col_spans_component(comp):
            out[r][c] = comp["color"]
    return out

def recolor_same_size(grid, pred, new_color, banned_colors=()):
    out = copyg(grid)
    banned = set(banned_colors)
    for comp in components(grid):
        if comp["color"] in banned:
            continue
        if pred(comp):
            for r, c in comp["cells"]:
                out[r][c] = new_color
    return out

def row_histogram_from_profile(profile, color=8):
    out = blank(len(profile), max(profile) if profile else 1, 0)
    for r, n in enumerate(profile):
        for c in range(n):
            out[r][c] = color
    return out

def col_histogram_from_profile(profile, color=8):
    out = blank(max(profile) if profile else 1, len(profile), 0)
    for c, n in enumerate(profile):
        for r in range(n):
            out[r][c] = color
    return out

def canonical_intersection_shape(rows, cols, color=8):
    h, w = len(rows), len(cols)
    out = blank(h, w, 0)
    for r in range(h):
        for c in range(w):
            if c < rows[r] and r < cols[c]:
                out[r][c] = color
    return out

def split_vertical_panels(grid, sep_color=5):
    h, w = dims(grid)
    sep_cols = [c for c in range(w) if all(grid[r][c] == sep_color for r in range(h))]
    cols = [-1] + sep_cols + [w]
    panels = []
    intervals = []
    for a, b in zip(cols, cols[1:]):
        l, r = a + 1, b - 1
        if l <= r:
            panels.append([row[l:r + 1] for row in grid])
            intervals.append((l, r))
    return panels, intervals

def detect_marker(grid, color=1):
    comps = [comp for comp in components(grid) if comp["color"] == color]
    if not comps:
        return None
    comp = min(comps, key=top_left_of_comp)
    return min(comp["cells"])

def single_largest_component(grid, banned_colors=()):
    banned = set(banned_colors)
    comps = [comp for comp in components(grid) if comp["color"] not in banned]
    return max(
        comps,
        key=lambda comp: (
            len(comp["cells"]),
            max_row_peak(comp),
            max_col_peak(comp),
            tuple(-x for x in top_left_of_comp(comp)),
        ),
    )

def solve_S14_E1(grid):
    return row_fill_same_size_excluding(grid)

def solve_S14_E2(grid):
    return col_fill_same_size_excluding(grid)

def solve_S14_E3(grid):
    comps = components(grid)
    target = max(
        comps,
        key=lambda comp: (
            max_row_peak(comp),
            len(comp["cells"]),
            tuple(-x for x in top_left_of_comp(comp)),
        ),
    )
    return crop_component(target, 8)

def solve_S14_E4(grid):
    return recolor_same_size(grid, constant_row_profile, 8)

def solve_S14_E5(grid):
    comps = components(grid)
    target = max(
        comps,
        key=lambda comp: (
            max_col_peak(comp),
            len(comp["cells"]),
            tuple(-x for x in top_left_of_comp(comp)),
        ),
    )
    return crop_component(target, 8)

def solve_S14_E6(grid):
    h, w = dims(grid)
    k = sum(1 for c in range(w) if grid[0][c] == 1)
    comps = components([row[:] for row in grid[1:]])
    target = next(
        comp
        for comp in sorted(comps, key=top_left_of_comp)
        if len(row_profile_cells(comp["cells"])) == k
    )
    return crop_component(target, 8)

def solve_S14_E7(grid):
    comp = single_largest_component(grid)
    return row_histogram_from_profile(row_profile_cells(comp["cells"]), 8)

def solve_S14_M1(grid):
    comps = components(grid)
    anchor = min([comp for comp in comps if comp["color"] == 1], key=top_left_of_comp)
    target = next(
        comp
        for comp in sorted([c for c in comps if c["color"] != 1], key=top_left_of_comp)
        if row_profile_cells(comp["cells"]) == row_profile_cells(anchor["cells"])
    )
    return crop_component(target, 8)

def solve_S14_M2(grid):
    mode = "row" if grid[0][0] == 1 else "col"
    if mode == "row":
        return row_fill_same_size_excluding(grid, banned_colors=(1, 2))
    return col_fill_same_size_excluding(grid, banned_colors=(1, 2))

def solve_S14_M3(grid):
    comps = components(grid)
    profiles = [tuple(row_profile_cells(comp["cells"])) for comp in comps]
    counts = Counter(profiles)
    target = next(
        comp
        for comp in sorted(comps, key=top_left_of_comp)
        if counts[tuple(row_profile_cells(comp["cells"]))] == 1
    )
    return crop_component(target, 8)

def solve_S14_M4(grid):
    comp = single_largest_component(grid)
    return col_histogram_from_profile(col_profile_cells(comp["cells"]), 8)

def solve_S14_M5(grid):
    comp = single_largest_component(grid)
    sig = profile_signature(comp["cells"])
    return canonical_intersection_shape(sig["rows"], sig["cols"], 8)

def solve_S14_M6(grid):
    comps = [comp for comp in components(grid) if comp["color"] != 1]
    anchor = max(
        comps,
        key=lambda comp: (
            len(comp["cells"]),
            tuple(-x for x in top_left_of_comp(comp)),
        ),
    )
    marker = detect_marker(grid, 1)
    profile = row_profile_cells(anchor["cells"])
    shape = row_histogram_from_profile(profile, 1)
    h, w = dims(grid)
    out = blank(h, w, 0)
    for r in range(len(shape)):
        for c in range(len(shape[0])):
            if shape[r][c]:
                out[marker[0] + r][marker[1] + c] = 8
    return out

def solve_S14_M7(grid):
    panels, _ = split_vertical_panels(grid, sep_color=5)
    anchor = single_largest_component(panels[0])
    target = next(
        comp
        for comp in sorted(components(panels[1]), key=top_left_of_comp)
        if col_profile_cells(comp["cells"]) == col_profile_cells(anchor["cells"])
    )
    return crop_component(target, 8)

def solve_S14_H1(grid):
    comps = sorted(components(grid), key=top_left_of_comp)
    profiles = [tuple(row_profile_cells(comp["cells"])) for comp in comps]
    n = len(comps)
    out = blank(n, n, 0)
    for i in range(n):
        for j in range(n):
            if profiles[i] == profiles[j]:
                out[i][j] = 8
    return out

def solve_S14_H2(grid):
    comps = components(grid)
    blue = min([comp for comp in comps if comp["color"] == 1], key=top_left_of_comp)
    red = min([comp for comp in comps if comp["color"] == 2], key=top_left_of_comp)
    target = next(
        comp
        for comp in sorted([c for c in comps if c["color"] not in (1, 2)], key=top_left_of_comp)
        if row_profile_cells(comp["cells"]) == row_profile_cells(blue["cells"])
        and col_profile_cells(comp["cells"]) == col_profile_cells(red["cells"])
    )
    return crop_component(target, 8)

def solve_S14_H3(grid):
    panels, _ = split_vertical_panels(grid, sep_color=5)
    if row_fill_same_size_excluding(panels[0]) == panels[1]:
        transformed = row_fill_same_size_excluding(panels[2])
    else:
        transformed = col_fill_same_size_excluding(panels[2])
    target = single_largest_component(transformed)
    return crop_component(target, 8)

def solve_S14_H4(grid):
    comps = components(grid)
    anchor = min([comp for comp in comps if comp["color"] == 1], key=top_left_of_comp)
    target_profile = list(reversed(col_profile_cells(anchor["cells"])))
    target = next(
        comp
        for comp in sorted([c for c in comps if c["color"] != 1], key=top_left_of_comp)
        if row_profile_cells(comp["cells"]) == target_profile
    )
    return crop_component(target, 8)

def solve_S14_H5(grid):
    panels, _ = split_vertical_panels(grid, sep_color=5)
    a = single_largest_component(panels[0])
    b = single_largest_component(panels[1])
    ra = row_profile_cells(a["cells"])
    rb = row_profile_cells(b["cells"])
    L = max(len(ra), len(rb))
    ra = ra + [0] * (L - len(ra))
    rb = rb + [0] * (L - len(rb))
    diff = [abs(x - y) for x, y in zip(ra, rb)]
    return row_histogram_from_profile(diff, 8)

def solve_S14_H6(grid):
    panels, _ = split_vertical_panels(grid, sep_color=5)
    profiles = []
    for panel in panels:
        comp = single_largest_component(panel)
        profiles.append(tuple(row_profile_cells(comp["cells"])))
    counts = Counter(profiles)
    majority = max(counts.items(), key=lambda kv: (kv[1], sum(kv[0]), len(kv[0])))[0]
    return row_histogram_from_profile(list(majority), 8)

def solve_S14_H7(grid):
    comps = components(grid)
    blue = min([comp for comp in comps if comp["color"] == 1], key=top_left_of_comp)
    red = min([comp for comp in comps if comp["color"] == 2], key=top_left_of_comp)
    rows = row_profile_cells(blue["cells"])
    cols = col_profile_cells(red["cells"])
    return canonical_intersection_shape(rows, cols, 8)
