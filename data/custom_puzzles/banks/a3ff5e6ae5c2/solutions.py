
"""Reference helper library and 21 reference solve functions for the fifteenth custom ARC puzzle bank.

New primitive introduced in this set:
  relative_offsets(cells, anchor='top_left')

Return the occupied offsets of a component relative to a chosen anchor or
bounding-box corner. This makes anchor-relative copy, stencil transfer,
translation-invariant comparison, and transform-coded stamping explicit.

All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 15.
"""
from typing import List, Dict, Tuple
from collections import Counter

Grid = List[List[int]]

dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h, w, v=0):
    return [[v] * w for _ in range(h)]

def dims(g):
    return len(g), len(g[0])

def components(grid, include_zero=False, colors=None, connectivity=4):
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

def comps_by_color(grid, colors):
    return components(grid, colors=set(colors))

def find_single_comp(grid, color):
    comps = comps_by_color(grid, [color])
    assert len(comps) == 1, (color, len(comps))
    return comps[0]

def marker_cells(grid, color):
    return [(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == color]

def bbox(cells):
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize_offsets(offsets):
    if not offsets:
        return []
    rs = [r for r, c in offsets]
    cs = [c for r, c in offsets]
    mr, mc = min(rs), min(cs)
    return sorted((r - mr, c - mc) for r, c in offsets)

def normalize_cells(cells):
    r1, c1, _, _ = bbox(cells)
    return sorted((r - r1, c - c1) for r, c in cells)

def relative_offsets(cells, anchor='top_left'):
    r1, c1, r2, c2 = bbox(cells)
    if anchor == 'top_left':
        ar, ac = r1, c1
    elif anchor == 'top_right':
        ar, ac = r1, c2
    elif anchor == 'bottom_left':
        ar, ac = r2, c1
    elif anchor == 'bottom_right':
        ar, ac = r2, c2
    else:
        raise ValueError(anchor)
    return sorted((r - ar, c - ac) for r, c in cells)

def place_cells(g, cells, color, overwrite=False):
    h, w = dims(g)
    for r, c in cells:
        assert 0 <= r < h and 0 <= c < w
        if not overwrite:
            assert g[r][c] == 0
        g[r][c] = color
    return g

def place_offsets(g, offsets, anchor, color, overwrite=False):
    ar, ac = anchor
    cells = [(ar + dr, ac + dc) for dr, dc in offsets]
    return place_cells(g, cells, color, overwrite=overwrite)

def place_colored_offsets(g, colored_offsets, anchor, overwrite=False):
    ar, ac = anchor
    for (dr, dc), color in colored_offsets.items():
        r, c = ar + dr, ac + dc
        assert 0 <= r < len(g) and 0 <= c < len(g[0])
        if not overwrite:
            assert g[r][c] == 0
        g[r][c] = color
    return g

def crop_component(comp, recolor=8):
    r1, c1, r2, c2 = bbox(comp["cells"])
    out = blank(r2 - r1 + 1, c2 - c1 + 1, 0)
    for r, c in comp["cells"]:
        out[r - r1][c - c1] = recolor
    return out

def crop_cells(cells, recolor=8):
    r1, c1, r2, c2 = bbox(cells)
    out = blank(r2 - r1 + 1, c2 - c1 + 1, 0)
    for r, c in cells:
        out[r - r1][c - c1] = recolor
    return out

def transform_offsets(offsets, op='id'):
    offs = list(offsets)
    nr = normalize_offsets(offs)
    rs = [r for r, c in nr]
    cs = [c for r, c in nr]
    h = max(rs) + 1
    w = max(cs) + 1
    out = []
    for r, c in nr:
        if op == 'id':
            rr, cc = r, c
        elif op == 'hmirror':
            rr, cc = r, w - 1 - c
        elif op == 'vmirror':
            rr, cc = h - 1 - r, c
        elif op == 'rot90':
            rr, cc = c, h - 1 - r
        elif op == 'rot180':
            rr, cc = h - 1 - r, w - 1 - c
        elif op == 'rot270':
            rr, cc = w - 1 - c, r
        else:
            raise ValueError(op)
        out.append((rr, cc))
    return normalize_offsets(out)

def transform_colored_offsets(colored_offsets, op='id'):
    offs = list(colored_offsets.keys())
    nr = normalize_offsets(offs)
    rmin = min(r for r, c in offs)
    cmin = min(c for r, c in offs)
    norm_colored = {(r - rmin, c - cmin): v for (r, c), v in colored_offsets.items()}
    rs = [r for r, c in nr]
    cs = [c for r, c in nr]
    h = max(rs) + 1
    w = max(cs) + 1
    out = {}
    for (r, c), v in norm_colored.items():
        if op == 'id':
            rr, cc = r, c
        elif op == 'hmirror':
            rr, cc = r, w - 1 - c
        elif op == 'vmirror':
            rr, cc = h - 1 - r, c
        elif op == 'rot90':
            rr, cc = c, h - 1 - r
        elif op == 'rot180':
            rr, cc = h - 1 - r, w - 1 - c
        elif op == 'rot270':
            rr, cc = w - 1 - c, r
        else:
            raise ValueError(op)
        out[(rr, cc)] = v
    return out

def transform_origin_offsets(offsets, op='id'):
    out = []
    for dr, dc in offsets:
        if op == 'id':
            rr, cc = dr, dc
        elif op == 'rot90':
            rr, cc = dc, -dr
        elif op == 'rot180':
            rr, cc = -dr, -dc
        elif op == 'rot270':
            rr, cc = -dc, dr
        elif op == 'hmirror':
            rr, cc = dr, -dc
        elif op == 'vmirror':
            rr, cc = -dr, dc
        else:
            raise ValueError(op)
        out.append((rr, cc))
    return sorted(out)

def top_left(comp):
    r1, c1, _, _ = bbox(comp["cells"])
    return (r1, c1)

def dihedral_variants(offsets):
    base = normalize_offsets(offsets)
    vars = []
    for rot in ['id', 'rot90', 'rot180', 'rot270']:
        r = transform_offsets(base, rot)
        vars.append(tuple(r))
        vars.append(tuple(transform_offsets(r, 'hmirror')))
    uniq = []
    seen = set()
    for v in vars:
        if v not in seen:
            seen.add(v)
            uniq.append(v)
    return uniq

def canonical_dihedral(cells):
    return min(dihedral_variants(normalize_cells(cells)))

def copy_template_to_marker(grid):
    comp = find_single_comp(grid, 2)
    marker = marker_cells(grid, 1)[0]
    offs = relative_offsets(comp["cells"], anchor='top_left')
    out = blank(*dims(grid), 0)
    place_offsets(out, offs, marker, 8)
    return out

def stamp_template_all_markers(grid):
    comp = find_single_comp(grid, 2)
    offs = relative_offsets(comp["cells"], anchor='top_left')
    out = blank(*dims(grid), 0)
    for mk in marker_cells(grid, 1):
        place_offsets(out, offs, mk, 8)
    return out

def hmirror_to_marker(grid):
    comp = find_single_comp(grid, 2)
    marker = marker_cells(grid, 1)[0]
    offs = transform_offsets(relative_offsets(comp["cells"], 'top_left'), 'hmirror')
    out = blank(*dims(grid), 0)
    place_offsets(out, offs, marker, 8)
    return out

def crop_matching_candidate(grid):
    source = find_single_comp(grid, 2)
    sig = tuple(relative_offsets(source["cells"], 'top_left'))
    cands = [comp for comp in components(grid) if comp["color"] in {3, 4, 5, 6, 7, 8, 9}]
    matches = [comp for comp in cands if tuple(relative_offsets(comp["cells"], 'top_left')) == sig]
    assert len(matches) == 1
    return crop_component(matches[0], recolor=8)

def mask_transfer_to_target(grid):
    source = find_single_comp(grid, 2)
    target = find_single_comp(grid, 3)
    soff = relative_offsets(source["cells"], 'top_left')
    r1, c1, _, _ = bbox(target["cells"])
    out = blank(*dims(grid), 0)
    place_offsets(out, soff, (r1, c1), 8)
    return out

def anchor_vector_copy(grid):
    source = find_single_comp(grid, 2)
    sa = marker_cells(grid, 1)[0]
    ta = marker_cells(grid, 3)[0]
    offs = sorted((r - sa[0], c - sa[1]) for r, c in source["cells"])
    out = blank(*dims(grid), 0)
    cells = [(ta[0] + dr, ta[1] + dc) for dr, dc in offs]
    place_cells(out, cells, 8)
    return out

def indicator_congruent(grid):
    source = find_single_comp(grid, 2)
    sig = tuple(relative_offsets(source["cells"], 'top_left'))
    cands = [comp for comp in components(grid) if comp["color"] in {3, 4, 5, 6}]
    cands = sorted(cands, key=lambda comp: top_left(comp))
    row = [8 if tuple(relative_offsets(comp["cells"], 'top_left')) == sig else 0 for comp in cands]
    return [row]

def multicolor_transfer(grid):
    pts = {(r, c): v for r, row in enumerate(grid) for c, v in enumerate(row) if v not in (0, 1)}
    marker = marker_cells(grid, 1)[0]
    rs = [r for r, c in pts]
    cs = [c for r, c in pts]
    r0, c0 = min(rs), min(cs)
    colored = {(r - r0, c - c0): v for (r, c), v in pts.items()}
    out = blank(*dims(grid), 0)
    place_colored_offsets(out, colored, marker)
    return out

def marker_colored_stamps(grid):
    source = find_single_comp(grid, 2)
    offs = relative_offsets(source["cells"], 'top_left')
    out = blank(*dims(grid), 0)
    for color in [3, 4, 5, 6, 7, 8, 9]:
        for mk in marker_cells(grid, color):
            place_offsets(out, offs, mk, color)
    return out

def rot90_to_marker(grid):
    source = find_single_comp(grid, 2)
    offs = transform_offsets(relative_offsets(source["cells"], 'top_left'), 'rot90')
    marker = marker_cells(grid, 1)[0]
    out = blank(*dims(grid), 0)
    place_offsets(out, offs, marker, 8)
    return out

TRANSFORM_BY_MARKER = {3: 'id', 4: 'hmirror', 5: 'vmirror', 6: 'rot90'}

def transform_coded_stamps(grid):
    source = find_single_comp(grid, 2)
    base = relative_offsets(source["cells"], 'top_left')
    out = blank(*dims(grid), 0)
    for color, op in TRANSFORM_BY_MARKER.items():
        for mk in marker_cells(grid, color):
            offs = transform_offsets(base, op)
            place_offsets(out, offs, mk, 8)
    return out

def xor_two_templates(grid):
    a = find_single_comp(grid, 2)
    b = find_single_comp(grid, 3)
    marker = marker_cells(grid, 1)[0]
    A = set(relative_offsets(a["cells"], 'top_left'))
    B = set(relative_offsets(b["cells"], 'top_left'))
    X = sorted(A ^ B)
    out = blank(*dims(grid), 0)
    place_offsets(out, X, marker, 8)
    return out

def majority_congruence_crop(grid):
    cands = [comp for comp in components(grid) if comp["color"] in {2, 3, 4, 5, 6}]
    sigs = [tuple(relative_offsets(comp["cells"], 'top_left')) for comp in cands]
    cnt = Counter(sigs)
    sig = max(cnt.items(), key=lambda kv: (kv[1], -len(kv[0])))[0]
    cells = [comp["cells"] for comp, s in zip(cands, sigs) if s == sig][0]
    return crop_cells(cells, recolor=8)

def reflection_match_indicator(grid):
    source = find_single_comp(grid, 2)
    base = relative_offsets(source["cells"], 'top_left')
    sigs = {tuple(transform_offsets(base, 'id')), tuple(transform_offsets(base, 'hmirror'))}
    cands = [comp for comp in components(grid) if comp["color"] in {3, 4, 5, 6}]
    cands = sorted(cands, key=lambda comp: top_left(comp))
    row = [8 if tuple(relative_offsets(comp["cells"], 'top_left')) in sigs else 0 for comp in cands]
    return [row]

def bottom_right_anchor_copy(grid):
    source = find_single_comp(grid, 2)
    marker = marker_cells(grid, 1)[0]
    offs = relative_offsets(source["cells"], 'bottom_right')
    out = blank(*dims(grid), 0)
    place_offsets(out, offs, marker, 8)
    return out

def anchor_frame_transform_copy(grid):
    source = find_single_comp(grid, 2)
    sa = marker_cells(grid, 1)[0]
    raw = sorted((r - sa[0], c - sa[1]) for r, c in source["cells"])
    out = blank(*dims(grid), 0)
    mapping = {3: 'id', 4: 'rot90', 5: 'hmirror'}
    for color, op in mapping.items():
        for mk in marker_cells(grid, color):
            offs = transform_origin_offsets(raw, op)
            cells = [(mk[0] + dr, mk[1] + dc) for dr, dc in offs]
            place_cells(out, cells, 8)
    return out

def pairwise_congruence_matrix(grid):
    cands = [comp for comp in components(grid) if comp["color"] in {2, 3, 4}]
    cands = sorted(cands, key=lambda comp: top_left(comp))
    sigs = [tuple(relative_offsets(comp["cells"], 'top_left')) for comp in cands]
    n = len(cands)
    out = blank(n, n, 0)
    for i in range(n):
        for j in range(n):
            if sigs[i] == sigs[j]:
                out[i][j] = 8
    return out

def multicolor_transform_coded(grid):
    pts = {(r, c): v for r, row in enumerate(grid) for c, v in enumerate(row) if v not in (0, 3, 4, 5, 6)}
    rs = [r for r, c in pts]
    cs = [c for r, c in pts]
    r0, c0 = min(rs), min(cs)
    colored = {(r - r0, c - c0): v for (r, c), v in pts.items()}
    out = blank(*dims(grid), 0)
    for color, op in TRANSFORM_BY_MARKER.items():
        for mk in marker_cells(grid, color):
            tr = transform_colored_offsets(colored, op)
            place_colored_offsets(out, tr, mk)
    return out

def header_setop_crop(grid):
    hdr = 7 if marker_cells(grid, 7) else 9
    a = find_single_comp(grid, 2)
    b = find_single_comp(grid, 3)
    A = set(relative_offsets(a["cells"], 'top_left'))
    B = set(relative_offsets(b["cells"], 'top_left'))
    if hdr == 7:
        S = sorted(A & B)
    else:
        S = sorted(A ^ B)
    return crop_cells(S, recolor=8) if S else [[0]]

def priority_walls_stamps(grid):
    source = find_single_comp(grid, 2)
    offs = relative_offsets(source["cells"], 'top_left')
    h, w = dims(grid)
    out = blank(h, w, 0)
    pr = blank(h, w, -10**9)
    for color in [3, 4]:
        for mk in marker_cells(grid, color):
            for dr, dc in offs:
                r, c = mk[0] + dr, mk[1] + dc
                if 0 <= r < h and 0 <= c < w and grid[r][c] != 9:
                    if color >= pr[r][c]:
                        out[r][c] = 8
                        pr[r][c] = color
    return out

def odd_dihedral_crop(grid):
    cands = [comp for comp in components(grid) if comp["color"] in {2, 3, 4, 5}]
    cands = sorted(cands, key=lambda comp: top_left(comp))
    sigs = [canonical_dihedral(comp["cells"]) for comp in cands]
    cnt = Counter(sigs)
    odd_sig = min(cnt.items(), key=lambda kv: (kv[1], len(kv[0])))[0]
    odd = [comp for comp, s in zip(cands, sigs) if s == odd_sig][0]
    return crop_component(odd, recolor=8)

def solve_S15_E1(grid):
    return copy_template_to_marker(grid)

def solve_S15_E2(grid):
    return stamp_template_all_markers(grid)

def solve_S15_E3(grid):
    return hmirror_to_marker(grid)

def solve_S15_E4(grid):
    return crop_matching_candidate(grid)

def solve_S15_E5(grid):
    return mask_transfer_to_target(grid)

def solve_S15_E6(grid):
    return anchor_vector_copy(grid)

def solve_S15_E7(grid):
    return indicator_congruent(grid)

def solve_S15_M1(grid):
    return multicolor_transfer(grid)

def solve_S15_M2(grid):
    return marker_colored_stamps(grid)

def solve_S15_M3(grid):
    return rot90_to_marker(grid)

def solve_S15_M4(grid):
    return transform_coded_stamps(grid)

def solve_S15_M5(grid):
    return xor_two_templates(grid)

def solve_S15_M6(grid):
    return majority_congruence_crop(grid)

def solve_S15_M7(grid):
    return reflection_match_indicator(grid)

def solve_S15_H1(grid):
    return bottom_right_anchor_copy(grid)

def solve_S15_H2(grid):
    return anchor_frame_transform_copy(grid)

def solve_S15_H3(grid):
    return pairwise_congruence_matrix(grid)

def solve_S15_H4(grid):
    return multicolor_transform_coded(grid)

def solve_S15_H5(grid):
    return header_setop_crop(grid)

def solve_S15_H6(grid):
    return priority_walls_stamps(grid)

def solve_S15_H7(grid):
    return odd_dihedral_crop(grid)
