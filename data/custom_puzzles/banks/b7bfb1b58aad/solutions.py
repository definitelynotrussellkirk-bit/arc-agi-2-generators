"""
ARC-style puzzle bank continuation 9: 21 more puzzles (E57-E63, M57-M63, H57-H63).

This batch leans further into row-local rules, anchored mirroring, topology,
panel composition, transform inference, pivot-based orbits, symbolic color
permutations, Voronoi-style filling, and palette-ranked recoloring.

Notable motifs:
- panel_infer_transform(example_in, example_out, query): H57
- pivot_orbit(pivot, prototype): H59
- rank_fill(mask_components, palette): H63
- voronoi_fill_inside_frame(frame, seeds): H62
"""

from __future__ import annotations
from typing import List, Tuple, Iterable
from collections import deque

Grid = List[List[int]]

def blank(h:int, w:int, v:int=0) -> Grid:
    return [[v]*w for _ in range(h)]

def dims(g: Grid) -> Tuple[int,int]:
    return len(g), len(g[0])

def clone(g: Grid) -> Grid:
    return [row[:] for row in g]

def place(g: Grid, cells: Iterable[Tuple[int,int]], color:int) -> Grid:
    for r,c in cells:
        if 0 <= r < len(g) and 0 <= c < len(g[0]):
            g[r][c] = color
    return g

def overlay(dst: Grid, src: Grid, top:int=0, left:int=0, transparent:int=0) -> Grid:
    h,w = dims(src)
    for r in range(h):
        for c in range(w):
            v = src[r][c]
            if v != transparent:
                rr,cc = top+r,left+c
                if 0 <= rr < len(dst) and 0 <= cc < len(dst[0]):
                    dst[rr][cc] = v
    return dst

def bbox(cells):
    cells = list(cells)
    rs = [r for r,c in cells]
    cs = [c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def normalize_cells(cells):
    cells = list(cells)
    r0,r1,c0,c1 = bbox(cells)
    return {(r-r0, c-c0) for r,c in cells}, (r1-r0+1, c1-c0+1), (r0,c0)

def same_color_components(g: Grid):
    h,w = dims(g)
    seen = set()
    comps = []
    for r in range(h):
        for c in range(w):
            col = g[r][c]
            if col == 0 or (r,c) in seen:
                continue
            q = deque([(r,c)])
            seen.add((r,c))
            cells = []
            while q:
                x,y = q.popleft()
                cells.append((x,y))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny = x+dx, y+dy
                    if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == col and (nx,ny) not in seen:
                        seen.add((nx,ny))
                        q.append((nx,ny))
            comps.append((col, cells))
    return comps

def all_nonzero_components(g: Grid):
    h,w = dims(g)
    seen = set()
    comps = []
    for r in range(h):
        for c in range(w):
            if g[r][c] == 0 or (r,c) in seen:
                continue
            q = deque([(r,c)])
            seen.add((r,c))
            cells = []
            while q:
                x,y = q.popleft()
                cells.append((x,y))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny = x+dx, y+dy
                    if 0 <= nx < h and 0 <= ny < w and g[nx][ny] != 0 and (nx,ny) not in seen:
                        seen.add((nx,ny))
                        q.append((nx,ny))
            comps.append(cells)
    return comps

def crop_nonzero(g: Grid) -> Grid:
    cells = [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v != 0]
    if not cells:
        return [[0]]
    r0,r1,c0,c1 = bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def transform_grid(g: Grid, kind:str) -> Grid:
    if kind == "id":
        return clone(g)
    if kind == "rot90":
        h,w = dims(g)
        return [[g[h-1-r][c] for r in range(h)] for c in range(w)]
    if kind == "rot180":
        return [row[::-1] for row in g[::-1]]
    if kind == "rot270":
        h,w = dims(g)
        return [[g[r][w-1-c] for r in range(h)] for c in range(w-1,-1,-1)]
    if kind == "flip_h":
        return [row[::-1] for row in g]
    if kind == "flip_v":
        return g[::-1]
    if kind == "transpose":
        h,w = dims(g)
        return [[g[r][c] for r in range(h)] for c in range(w)]
    if kind == "anti":
        h,w = dims(g)
        return [[g[h-1-r][w-1-c] for r in range(h)] for c in range(w)]
    raise ValueError(kind)

def split_by_separator_cols(g: Grid, sep:int=9):
    h,w = dims(g)
    sep_cols = [c for c in range(w) if all(g[r][c] == sep for r in range(h))]
    parts = []
    start = 0
    for c in sep_cols + [w]:
        parts.append([row[start:c] for row in g])
        start = c + 1
    return parts, sep_cols

def center_overlay(canvas: Grid, shape: Grid, transparent:int=0) -> Grid:
    H,W = dims(canvas)
    h,w = dims(shape)
    top = (H-h)//2
    left = (W-w)//2
    out = clone(canvas)
    overlay(out, shape, top, left, transparent)
    return out

def solve_E57(g: Grid) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        by_color = {}
        for c,v in enumerate(g[r]):
            if v != 0:
                by_color.setdefault(v, []).append(c)
        for color, cols in by_color.items():
            if len(cols) == 2:
                a,b = min(cols), max(cols)
                if all(g[r][c] == 0 for c in range(a+1, b)):
                    for c in range(a, b+1):
                        out[r][c] = color
    return out

def solve_E58(g: Grid) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        anchors = [c for c,v in enumerate(g[r]) if v == 9]
        if len(anchors) != 1:
            continue
        a = anchors[0]
        for c,v in enumerate(g[r]):
            if v != 0 and v != 9:
                mc = 2*a - c
                if 0 <= mc < w:
                    out[r][mc] = v
    return out

def solve_E59(g: Grid) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        key = g[r][0]
        if key == 0:
            continue
        for c in range(1,w):
            if g[r][c] == 8:
                out[r][c] = key
    return out

def solve_E60(g: Grid) -> Grid:
    comps = same_color_components(g)
    best_color, best_cells = max(comps, key=lambda t: len(t[1]))
    h,w = dims(g)
    out = blank(h,w,0)
    for r,c in best_cells:
        out[r][c] = best_color
    return out

def solve_E61(g: Grid) -> Grid:
    h,w = dims(g)
    pts = [(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v != 0]
    color = pts[0][2]
    cells = [(r,c) for r,c,v in pts if v == color]
    r0,r1,c0,c1 = bbox(cells)
    out = blank(h,w,0)
    for c in range(c0, c1+1):
        out[r0][c] = color
        out[r1][c] = color
    for r in range(r0, r1+1):
        out[r][c0] = color
        out[r][c1] = color
    return out

def solve_E62(g: Grid) -> Grid:
    out = clone(g)
    proto = [row[:2] for row in g[:2]]
    h,w = dims(g)
    markers = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 7 and not (r < 2 and c < 2)]
    for r,c in markers:
        overlay(out, proto, r, c, transparent=-1)
    return out

def solve_E63(g: Grid) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0:
                continue
            for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
                r2,c2 = r+2*dr, c+2*dc
                rm,cm = r+dr, c+dc
                if 0 <= r2 < h and 0 <= c2 < w and g[r2][c2] == v and g[rm][cm] == 0:
                    out[rm][cm] = v
    return out

def solve_M57(g: Grid) -> Grid:
    h,w = dims(g)
    code = g[h-1][0]
    marker = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 9)
    cells = [(r,c) for r in range(h) for c in range(w)
             if g[r][c] != 0 and not (r == h-1 and c == 0) and not (r,c) == marker]
    r0,r1,c0,c1 = bbox(cells)
    proto = [row[c0:c1+1] for row in g[r0:r1+1]]
    kind = {1:"id", 2:"rot90", 3:"rot180", 4:"rot270"}[code]
    rot = transform_grid(proto, kind)
    out = blank(h,w,0)
    overlay(out, rot, marker[0], marker[1], transparent=0)
    return out

def solve_M58(g: Grid) -> Grid:
    parts,_ = split_by_separator_cols(g, sep=9)
    left,right = parts
    h,w = dims(left)
    out = blank(h,w,0)
    for r in range(h):
        for c in range(w):
            if left[r][c] == 1:
                out[r][c] = right[r][c]
    return out

def solve_M59(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    axis_row = next((r for r in range(h) if all(g[r][c] == 5 for c in range(w))), None)
    axis_col = next((c for c in range(w) if all(g[r][c] == 5 for r in range(h))), None)
    if axis_row is not None:
        for r in range(h):
            for c in range(w):
                v = g[r][c]
                if v != 0 and v != 5:
                    rr = 2*axis_row - r
                    if 0 <= rr < h:
                        out[rr][c] = v
    else:
        for r in range(h):
            for c in range(w):
                v = g[r][c]
                if v != 0 and v != 5:
                    cc = 2*axis_col - c
                    if 0 <= cc < w:
                        out[r][cc] = v
    return out

def solve_M60(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w,0)
    for color,cells in same_color_components(g):
        cellset = set(cells)
        r0,r1,c0,c1 = bbox(cells)
        seen = set()
        q = deque()
        for r in range(r0, r1+1):
            for c in range(c0, c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    if (r,c) not in cellset and (r,c) not in seen:
                        seen.add((r,c))
                        q.append((r,c))
        while q:
            r,c = q.popleft()
            for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                rr,cc = r+dr, c+dc
                if r0 <= rr <= r1 and c0 <= cc <= c1 and (rr,cc) not in cellset and (rr,cc) not in seen:
                    seen.add((rr,cc))
                    q.append((rr,cc))
        has_hole = any((r,c) not in cellset and (r,c) not in seen for r in range(r0,r1+1) for c in range(c0,c1+1))
        new_color = 8 if has_hole else 4
        for r,c in cells:
            out[r][c] = new_color
    return out

def solve_M61(g: Grid) -> Grid:
    h,w = dims(g)
    src = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 1)
    dst = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 2)
    dr,dc = dst[0]-src[0], dst[1]-src[1]
    out = blank(h,w,0)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0 and v not in (1,2):
                rr,cc = r+dr, c+dc
                if 0 <= rr < h and 0 <= cc < w:
                    out[rr][cc] = v
    return out

def solve_M62(g: Grid) -> Grid:
    h,w = dims(g)
    comps = same_color_components(g)
    query_cells = next(cells for color,cells in comps if color == 8)
    query_shape,_,_ = normalize_cells(query_cells)
    match_color = None
    for color,cells in comps:
        if color == 8:
            continue
        shp,_,_ = normalize_cells(cells)
        if shp == query_shape:
            match_color = color
            break
    out = blank(h,w,0)
    for r,c in query_cells:
        out[r][c] = match_color
    return out

def solve_M63(g: Grid) -> Grid:
    h,w = dims(g)
    frame_cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 7]
    r0,r1,c0,c1 = bbox(frame_cells)
    interior = [row[c0+1:c1] for row in g[r0+1:r1]]
    cells = [(r,c) for r,row in enumerate(interior) for c,v in enumerate(row) if v != 0]
    ir0,ir1,ic0,ic1 = bbox(cells)
    crop = [row[ic0:ic1+1] for row in interior[ir0:ir1+1]]
    out = blank(h,w,0)
    ch,cw = dims(crop)
    top = (h - ch)//2
    left = (w - cw)//2
    overlay(out, crop, top, left, transparent=0)
    return out

def solve_H57(g: Grid) -> Grid:
    parts,_ = split_by_separator_cols(g, sep=9)
    A,B,C = parts
    candidates = ["id","rot90","rot180","rot270","flip_h","flip_v","transpose","anti"]
    kind = None
    for k in candidates:
        if transform_grid(A, k) == B:
            kind = k
            break
    return transform_grid(C, kind)

def solve_H58(g: Grid) -> Grid:
    parts,_ = split_by_separator_cols(g, sep=9)
    *protos, query = parts
    qshape = {(r,c) for r,row in enumerate(query) for c,v in enumerate(row) if v != 0}
    qnorm,_,_ = normalize_cells(qshape)
    kinds = ["id","rot90","rot180","rot270","flip_h","flip_v","transpose","anti"]
    for panel in protos:
        cells = [(r,c) for r,row in enumerate(panel) for c,v in enumerate(row) if v != 0]
        if not cells:
            continue
        color = next(v for row in panel for v in row if v != 0)
        shp,_,_ = normalize_cells(cells)
        for k in kinds:
            # build transformed shape as grid then normalize
            r0,r1,c0,c1 = bbox(cells)
            crop = [row[c0:c1+1] for row in panel[r0:r1+1]]
            t = transform_grid(crop, k)
            tcells = [(r,c) for r,row in enumerate(t) for c,v in enumerate(row) if v != 0]
            tnorm,_,_ = normalize_cells(tcells)
            if tnorm == qnorm:
                h,w = dims(query)
                out = blank(h,w,0)
                for r,c in [(r,c) for r,row in enumerate(query) for c,v in enumerate(row) if v != 0]:
                    out[r][c] = color
                return out
    return blank(*dims(query), 0)

def solve_H59(g: Grid) -> Grid:
    h,w = dims(g)
    pivot = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 9)
    pr,pc = pivot
    out = blank(h,w,0)
    out[pr][pc] = 9
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0 or v == 9:
                continue
            dr,dc = r-pr, c-pc
            for rr,cc in [
                (pr + dr, pc + dc),
                (pr - dc, pc + dr),
                (pr - dr, pc - dc),
                (pr + dc, pc - dr),
            ]:
                if 0 <= rr < h and 0 <= cc < w:
                    out[rr][cc] = v
    return out

def solve_H60(g: Grid) -> Grid:
    h,w = dims(g)
    marker_cols = [c for c,v in enumerate(g[h-1]) if v == 1]
    comps = [(color,cells) for color,cells in same_color_components(g) if color != 1]
    comps = sorted(comps, key=lambda t: len(t[1]))
    out = blank(h,w,0)
    for c in marker_cols:
        out[h-1][c] = 1
    for (color,cells), mc in zip(comps, marker_cols):
        shp,(sh,sw),_ = normalize_cells(cells)
        top = h - 1 - sh
        left = mc
        # align bbox bottom-left to marker column
        for r,c in shp:
            rr,cc = top + r, left + c
            if 0 <= rr < h-1 and 0 <= cc < w:
                out[rr][cc] = color
    return out

def solve_H61(g: Grid) -> Grid:
    h,w = dims(g)
    mapping = {}
    for c in range(w):
        a,b = g[0][c], g[1][c]
        if a != 0:
            mapping[a] = b
    out = blank(h-2, w, 0)
    for r in range(2,h):
        for c in range(w):
            v = g[r][c]
            out[r-2][c] = mapping.get(v, v)
    return out

def solve_H62(g: Grid) -> Grid:
    h,w = dims(g)
    frame = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 7]
    r0,r1,c0,c1 = bbox(frame)
    seeds = [(r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,7)]
    out = clone(g)
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if out[r][c] == 0:
                best = min(seeds, key=lambda t: (abs(t[0]-r)+abs(t[1]-c), t[2]))
                out[r][c] = best[2]
    return out

def solve_H63(g: Grid) -> Grid:
    parts,_ = split_by_separator_cols(g, sep=9)
    left,right = parts
    palette = [right[r][0] for r in range(len(right)) if right[r][0] != 0]
    comps = [(cells) for color,cells in same_color_components(left) if color == 8]
    comps = sorted(comps, key=len)
    h,w = dims(left)
    out = blank(h,w,0)
    for cells,color in zip(comps, palette):
        for r,c in cells:
            out[r][c] = color
    return out

SOLVERS = {
    'E57': solve_E57,
    'E58': solve_E58,
    'E59': solve_E59,
    'E60': solve_E60,
    'E61': solve_E61,
    'E62': solve_E62,
    'E63': solve_E63,
    'M57': solve_M57,
    'M58': solve_M58,
    'M59': solve_M59,
    'M60': solve_M60,
    'M61': solve_M61,
    'M62': solve_M62,
    'M63': solve_M63,
    'H57': solve_H57,
    'H58': solve_H58,
    'H59': solve_H59,
    'H60': solve_H60,
    'H61': solve_H61,
    'H62': solve_H62,
    'H63': solve_H63,
}
