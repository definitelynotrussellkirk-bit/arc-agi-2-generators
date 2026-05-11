"""Reference helper library and 21 reference solve functions for the custom ARC puzzle bank."""

from collections import defaultdict

def components(grid, include_colors=None, connectivity=4):
    h, w = len(grid), len(grid[0])
    seen = [[False] * w for _ in range(h)]
    dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]
    dirs8 = dirs4 + [(-1,-1),(-1,1),(1,-1),(1,1)]
    dirs = dirs4 if connectivity == 4 else dirs8
    comps = []
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            color = grid[r][c]
            if color == 0 or (include_colors is not None and color not in include_colors):
                seen[r][c] = True
                continue
            q = [(r, c)]
            seen[r][c] = True
            cells = []
            while q:
                rr, cc = q.pop()
                cells.append((rr, cc))
                for dr, dc in dirs:
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and grid[nr][nc] == color:
                        seen[nr][nc] = True
                        q.append((nr, nc))
            comps.append({"color": color, "cells": cells})
    return comps

def bbox(cells):
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize(cells):
    r1, c1, _, _ = bbox(cells)
    return sorted((r - r1, c - c1) for r, c in cells)

def touches_border(cells, h, w):
    return any(r in (0, h - 1) or c in (0, w - 1) for r, c in cells)

def is_rectangle_outline(comp):
    cells = set(comp["cells"])
    r1, c1, r2, c2 = bbox(comp["cells"])
    if r2 - r1 < 2 or c2 - c1 < 2:
        return False
    expected = set()
    for c in range(c1, c2 + 1):
        expected.add((r1, c))
        expected.add((r2, c))
    for r in range(r1, r2 + 1):
        expected.add((r, c1))
        expected.add((r, c2))
    return cells == expected

def line_cells(r1, c1, r2, c2):
    if r1 == r2:
        step = 1 if c2 >= c1 else -1
        return [(r1, c) for c in range(c1, c2 + step, step)]
    if c1 == c2:
        step = 1 if r2 >= r1 else -1
        return [(r, c1) for r in range(r1, r2 + step, step)]
    raise ValueError("line_cells only supports horizontal or vertical lines")

def rotate_cells_90(cells):
    norm = normalize(cells)
    max_r = max(r for r, _ in norm)
    return sorted((c, max_r - r) for r, c in norm)

def solve_e1(grid):
    out = [row[:] for row in grid]
    for comp in components(grid, include_colors={3}, connectivity=8):
        if normalize(comp["cells"]) == [(0,0),(0,2),(1,1),(2,0),(2,2)]:
            for r, c in comp["cells"]:
                out[r][c] = 2
    return out

def solve_e2(grid):
    out = [row[:] for row in grid]
    comps = components(grid, include_colors={1})
    largest = max(comps, key=lambda comp: len(comp["cells"]))
    for r, c in largest["cells"]:
        out[r][c] = 7
    return out

def solve_e3(grid):
    h, w = len(grid), len(grid[0])
    out = [[0] * w for _ in range(h)]
    for comp in components(grid):
        if touches_border(comp["cells"], h, w):
            for r, c in comp["cells"]:
                out[r][c] = comp["color"]
    return out

def solve_e4(grid):
    h, w = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for r in range(h):
        for c in range(w - 1):
            if grid[r][c] == 2:
                out[r][c + 1] = 1
    return out

def solve_e5(grid):
    out = [row[:] for row in grid]
    for comp in components(grid):
        r1, c1, r2, c2 = bbox(comp["cells"])
        for r in range(r1 + 1, r2):
            for c in range(c1 + 1, c2):
                out[r][c] = comp["color"]
    return out

def solve_e6(grid):
    h, w = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 4 and all(
                0 <= r + dr < h and 0 <= c + dc < w and grid[r + dr][c + dc] == 4
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]
            ):
                out[r][c] = 8
    return out

def solve_e7(grid):
    out = [row[:] for row in grid]
    for comp in components(grid, include_colors={6}):
        r1, c1, r2, c2 = bbox(comp["cells"])
        new_color = 8 if r1 == r2 else 2
        for r, c in comp["cells"]:
            out[r][c] = new_color
    return out

def solve_m1(grid):
    out = [row[:] for row in grid]
    comps = components(grid, include_colors={1})
    by_size = sorted(comps, key=lambda comp: len(comp["cells"]))
    target = by_size[len(by_size) // 2]
    for r, c in target["cells"]:
        out[r][c] = 7
    return out

def solve_m2(grid):
    h, w = len(grid), len(grid[0])
    out = [[0] * w for _ in range(h)]
    pos_by_color = {}
    for r in range(h):
        for c in range(w):
            color = grid[r][c]
            if color != 0:
                pos_by_color.setdefault(color, []).append((r, c))
    for color, pts in pos_by_color.items():
        if len(pts) == 2:
            (r1, c1), (r2, c2) = pts
            r1, r2 = sorted((r1, r2))
            c1, c2 = sorted((c1, c2))
            for c in range(c1, c2 + 1):
                out[r1][c] = color
                out[r2][c] = color
            for r in range(r1, r2 + 1):
                out[r][c1] = color
                out[r][c2] = color
    return out

def solve_m3(grid):
    h, w = len(grid), len(grid[0])
    out = [[0] * w for _ in range(h)]
    anchor = next((r, c) for r in range(h) for c in range(w) if grid[r][c] == 2)
    obj = max(components(grid, include_colors={3}), key=lambda comp: len(comp["cells"]))
    top, left = anchor[0] + 1, anchor[1] + 1
    for dr, dc in normalize(obj["cells"]):
        out[top + dr][left + dc] = 2
    return out

def solve_m4(grid):
    out = [row[:] for row in grid]
    comps = components(grid)
    rings = [comp for comp in comps if is_rectangle_outline(comp)]
    others = [comp for comp in comps if not is_rectangle_outline(comp)]
    for obj in others:
        r1, c1, r2, c2 = bbox(obj["cells"])
        for ring in rings:
            R1, C1, R2, C2 = bbox(ring["cells"])
            if R1 < r1 and r2 < R2 and C1 < c1 and c2 < C2:
                for r, c in obj["cells"]:
                    out[r][c] = ring["color"]
                break
    return out

def solve_m5(grid):
    h, w = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    divider = next(c for c in range(w) if all(grid[r][c] == 5 for r in range(h)))
    for r in range(h):
        for c in range(w):
            if grid[r][c] not in (0, 5):
                out[r][2 * divider - c] = grid[r][c]
    return out

def solve_m6(grid):
    h, w = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 4 and all(
                0 <= rr < h and 0 <= cc < w and grid[rr][cc] == 7
                for rr, cc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
            ):
                for rr, cc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]:
                    out[rr][cc] = 8
    return out

def solve_m7(grid):
    out = [row[:] for row in grid]
    pos_by_color = {}
    for r, row in enumerate(grid):
        for c, color in enumerate(row):
            if color:
                pos_by_color.setdefault(color, []).append((r, c))
    for color, pts in pos_by_color.items():
        if len(pts) == 2:
            (r1, c1), (r2, c2) = pts
            if r1 == r2 or c1 == c2:
                for r, c in line_cells(r1, c1, r2, c2):
                    out[r][c] = color
    return out

def solve_h1(grid):
    out = [row[:] for row in grid]
    comps = components(grid)
    template = max([c for c in comps if c["color"] == 3], key=lambda comp: len(comp["cells"]))
    shape = normalize(template["cells"])
    for comp in comps:
        if len(comp["cells"]) == 1 and comp["color"] != 3:
            r0, c0 = comp["cells"][0]
            for dr, dc in shape:
                out[r0 + dr][c0 + dc] = comp["color"]
    return out

def solve_h2(grid):
    out = [row[:] for row in grid]
    p1 = next((r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == 1)
    p2 = next((r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == 2)
    dr, dc = p2[0] - p1[0], p2[1] - p1[1]
    obj = max(components(grid, include_colors={3}), key=lambda comp: len(comp["cells"]))
    for r, c in obj["cells"]:
        out[r + dr][c + dc] = 2
    return out

def solve_h3(grid):
    out = [row[:] for row in grid]
    comps = components(grid)
    by_shape = {}
    for comp in comps:
        by_shape.setdefault(tuple(normalize(comp["cells"])), []).append(comp)
    a, b = next(lst[:2] for lst in by_shape.values() if len(lst) >= 2)
    a_r1, a_c1, a_r2, a_c2 = bbox(a["cells"])
    b_r1, b_c1, b_r2, b_c2 = bbox(b["cells"])
    if a_r1 == b_r1 and a_r2 == b_r2:
        row = (a_r1 + a_r2) // 2
        left = min(a_c2, b_c2)
        right = max(a_c1, b_c1)
        for c in range(left, right + 1):
            out[row][c] = 8
    else:
        col = (a_c1 + a_c2) // 2
        top = min(a_r2, b_r2)
        bottom = max(a_r1, b_r1)
        for r in range(top, bottom + 1):
            out[r][col] = 8
    return out

def solve_h4(grid):
    out = [row[:] for row in grid]
    markers = [(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == 5]
    axis = markers[0][1]
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v not in (0, 5):
                out[r][2 * axis - c] = v
    return out

def solve_h5(grid):
    out = [row[:] for row in grid]
    strip = [v for v in grid[0] if v != 0]
    mapping = {strip[i]: strip[(i + 1) % len(strip)] for i in range(len(strip))}
    for r in range(1, len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in mapping:
                out[r][c] = mapping[grid[r][c]]
    return out

def solve_h6(grid):
    out = [row[:] for row in grid]
    comps = components(grid)
    obj = max([c for c in comps if c["color"] == 3], key=lambda comp: len(comp["cells"]))
    ring = max([c for c in comps if c["color"] != 3 and is_rectangle_outline(c)],
               key=lambda comp: len(comp["cells"]))
    for r, c in obj["cells"]:
        out[r][c] = 0
    r1, c1, r2, c2 = bbox(ring["cells"])
    for dr, dc in rotate_cells_90(obj["cells"]):
        out[r1 + 1 + dr][c1 + 1 + dc] = 3
    return out

def solve_h7(grid):
    out = [row[:] for row in grid]
    target_size = sum(1 for v in grid[0] if v == 1)
    for c in range(len(grid[0])):
        if out[0][c] == 1:
            out[0][c] = 0
    for comp in components(grid, include_colors={3}):
        if len(comp["cells"]) == target_size:
            for r, c in comp["cells"]:
                out[r][c] = 8
    return out

SOLVERS = {
    "E1": solve_e1,
    "E2": solve_e2,
    "E3": solve_e3,
    "E4": solve_e4,
    "E5": solve_e5,
    "E6": solve_e6,
    "E7": solve_e7,
    "M1": solve_m1,
    "M2": solve_m2,
    "M3": solve_m3,
    "M4": solve_m4,
    "M5": solve_m5,
    "M6": solve_m6,
    "M7": solve_m7,
    "H1": solve_h1,
    "H2": solve_h2,
    "H3": solve_h3,
    "H4": solve_h4,
    "H5": solve_h5,
    "H6": solve_h6,
    "H7": solve_h7
}
