"""
ARC-style puzzle bank continuation 8: 21 more puzzles (E50-E56, M50-M56, H50-H56).

This batch leans into legend-based painting, diagonal and box completion, object
selection, anchored symmetry, frame-centered reuse, panel composition, analogy
transforms, numeric-header reconstruction, and prototype lookup by shape.

Three notable motifs:
- orbit_union(pivot, prototype): H50
- mask_and_carry(mask, payload): H51
- prototype_lookup(prototypes, query): H55
"""

from __future__ import annotations
from typing import List, Tuple, Dict, Iterable
from collections import deque, defaultdict

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

def bbox(cells: Iterable[Tuple[int,int]]) -> Tuple[int,int,int,int]:
    cells = list(cells)
    rs = [r for r,c in cells]
    cs = [c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def normalize(cells: Iterable[Tuple[int,int]]) -> Tuple[set[Tuple[int,int]], Tuple[int,int], Tuple[int,int]]:
    cells = list(cells)
    r0,r1,c0,c1 = bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}, (r1-r0+1, c1-c0+1), (r0,c0)

def same_color_components(g: Grid) -> List[Tuple[int, List[Tuple[int,int]]]]:
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
                    nx,ny = x+dx,y+dy
                    if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == col and (nx,ny) not in seen:
                        seen.add((nx,ny))
                        q.append((nx,ny))
            comps.append((col, cells))
    return comps

def transform_shape(shape:set[Tuple[int,int]], kind:str) -> set[Tuple[int,int]]:
    if not shape:
        return set()
    rs = [r for r,c in shape]
    cs = [c for r,c in shape]
    h = max(rs)+1
    w = max(cs)+1
    if kind == 'id':
        out = {(r,c) for r,c in shape}
    elif kind == 'rot90':
        out = {(c, h-1-r) for r,c in shape}
    elif kind == 'rot180':
        out = {(h-1-r, w-1-c) for r,c in shape}
    elif kind == 'rot270':
        out = {(w-1-c, r) for r,c in shape}
    elif kind == 'hflip':
        out = {(r, w-1-c) for r,c in shape}
    elif kind == 'vflip':
        out = {(h-1-r, c) for r,c in shape}
    else:
        raise ValueError(kind)
    if not out:
        return out
    r0 = min(r for r,c in out)
    c0 = min(c for r,c in out)
    return {(r-r0, c-c0) for r,c in out}

def rotate_grid_cw(p: Grid) -> Grid:
    return [list(row) for row in zip(*p[::-1])]

def rotate_grid_ccw(p: Grid) -> Grid:
    return [list(row) for row in zip(*p)][::-1]

def rotate_grid_180(p: Grid) -> Grid:
    return [row[::-1] for row in p[::-1]]

def hflip_grid(p: Grid) -> Grid:
    return [row[::-1] for row in p]

def vflip_grid(p: Grid) -> Grid:
    return p[::-1]

def join_h_panels(panels: List[Grid], sep:int=9) -> Grid:
    h = len(panels[0])
    widths = [len(p[0]) for p in panels]
    out = blank(h, sum(widths)+len(panels)-1, 0)
    c0 = 0
    for i,p in enumerate(panels):
        ph,pw = dims(p)
        for r in range(ph):
            for c in range(pw):
                out[r][c0+c] = p[r][c]
        c0 += pw
        if i < len(panels)-1:
            for r in range(h):
                out[r][c0] = sep
            c0 += 1
    return out

def split_h_panels_by_sep(g: Grid, sep:int=9) -> List[Grid]:
    h,w = dims(g)
    seps = [c for c in range(w) if all(g[r][c] == sep for r in range(h))]
    parts = []
    start = 0
    for c in seps + [w]:
        parts.append([row[start:c] for row in g])
        start = c+1
    return parts

def grid_text(g: Grid) -> str:
    return "\n".join("".join(str(x) for x in row) for row in g)

def is_rect_border(cells: Iterable[Tuple[int,int]]) -> bool:
    cells = set(cells)
    r0,r1,c0,c1 = bbox(cells)
    border = {(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
    return cells == border

def has_hole(cells: Iterable[Tuple[int,int]]) -> bool:
    cells = set(cells)
    r0,r1,c0,c1 = bbox(cells)
    open_cells = {(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if (r,c) not in cells}
    if not open_cells:
        return False
    q = deque()
    seen = set()
    for r,c in open_cells:
        if r in (r0,r1) or c in (c0,c1):
            q.append((r,c)); seen.add((r,c))
    while q:
        x,y = q.popleft()
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny = x+dx,y+dy
            if (nx,ny) in open_cells and (nx,ny) not in seen:
                seen.add((nx,ny)); q.append((nx,ny))
    return len(seen) < len(open_cells)

def all_symmetries(shape:set[Tuple[int,int]]) -> List[set[Tuple[int,int]]]:
    kinds = ['id','rot90','rot180','rot270','hflip','vflip']
    # diagonal flips can be obtained as rot90+hflip and rot90+vflip
    out = []
    base = shape
    derived = [transform_shape(base, k) for k in kinds]
    derived += [transform_shape(transform_shape(base,'rot90'),'hflip'),
                transform_shape(transform_shape(base,'rot90'),'vflip')]
    uniq = []
    for sh in derived:
        if sh not in uniq:
            uniq.append(sh)
    return uniq


def split_h_panels(g: Grid, sep:int=9) -> List[Grid]:
    return split_h_panels_by_sep(g, sep)

def solve_E50(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for c in range(w):
        key = g[0][c]
        if key == 0:
            continue
        for r in range(1,h):
            if g[r][c] == 8:
                out[r][c] = key
    return out

def solve_E51(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h-2):
        for c in range(w):
            if g[r][c] != 0 and g[r][c] == g[r+2][c] and g[r+1][c] == 0:
                out[r+1][c] = g[r][c]
    return out

def solve_E52(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h-2):
        for c in range(w-2):
            if g[r][c] != 0 and g[r][c] == g[r+2][c+2] and g[r+1][c+1] == 0:
                out[r+1][c+1] = g[r][c]
            if g[r][c+2] != 0 and g[r][c+2] == g[r+2][c] and g[r+1][c+1] == 0:
                out[r+1][c+1] = g[r][c+2]
    return out

def solve_E53(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                out[h-1-r][c] = g[r][c]
    return out

def solve_E54(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h-1):
        for c in range(w-1):
            a,b = g[r][c], g[r][c+1]
            d,e = g[r+1][c], g[r+1][c+1]
            if a != 0 and a == e and b == 0 and d == 0:
                out[r][c+1] = a
                out[r+1][c] = a
            if b != 0 and b == d and a == 0 and e == 0:
                out[r][c] = b
                out[r+1][c+1] = b
    return out

def solve_E55(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    for c in range(w):
        vals = [g[r][c] for r in range(h) if g[r][c] != 0]
        for i,v in enumerate(vals):
            out[h-len(vals)+i][c] = v
    return out

def solve_E56(g: Grid) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            ring = [g[r+dr][c+dc] for dr in (-1,0,1) for dc in (-1,0,1) if not (dr==0 and dc==0)]
            if g[r][c] == 0 and len(set(ring)) == 1 and ring[0] != 0:
                out[r][c] = ring[0]
    return out

def solve_M50(g: Grid) -> Grid:
    comps = same_color_components(g)
    best = {}
    for col,cells in comps:
        best[col] = max(best.get(col, 0), len(cells))
    out = blank(*dims(g))
    for col,cells in comps:
        if len(cells) == best[col]:
            for r,c in cells:
                out[r][c] = col
    return out

def solve_M51(g: Grid) -> Grid:
    h,w = dims(g)
    anchors = [(r,c) for r in range(h) for c in range(w) if g[r][c] == 1]
    comps = [(col,cells) for col,cells in same_color_components(g) if col != 1]
    col,cells = max(comps, key=lambda t: len(t[1]))
    shape,_,_ = normalize(cells)
    out = blank(h,w)
    for ar,ac in anchors:
        for dr,dc in shape:
            rr,cc = ar+dr, ac+dc
            if 0 <= rr < h and 0 <= cc < w:
                out[rr][cc] = col
    return out

def solve_M52(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    for col,cells in same_color_components(g):
        r0,r1,c0,c1 = bbox(cells)
        for r in range(r0,r1+1):
            out[r][c0] = col
            out[r][c1] = col
        for c in range(c0,c1+1):
            out[r0][c] = col
            out[r1][c] = col
    return out

def solve_M53(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    for col,cells in same_color_components(g):
        if has_hole(cells):
            for r,c in cells:
                out[r][c] = col
    return out

def solve_M54(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    anchor = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 1)
    ar,ac = anchor
    out[ar][ac] = 1
    for r in range(h):
        for c in range(w):
            if g[r][c] not in (0,1):
                out[r][c] = g[r][c]
                rr,cc = 2*ar-r, 2*ac-c
                if 0 <= rr < h and 0 <= cc < w:
                    out[rr][cc] = g[r][c]
    return out

def solve_M55(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    for col,cells in same_color_components(g):
        if not any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c] = col
    return out

def solve_M56(g: Grid) -> Grid:
    h,w = dims(g)
    comps = same_color_components(g)
    frames = []
    proto = None
    for col,cells in comps:
        if col == 1 and is_rect_border(cells):
            frames.append((col,cells))
        elif col != 1:
            if proto is None or len(cells) > len(proto[1]):
                proto = (col,cells)
    pcol, pcells = proto
    pshape,(ph,pw),_ = normalize(pcells)
    out = blank(h,w)
    for _,fcells in frames:
        r0,r1,c0,c1 = bbox(fcells)
        ih,iw = (r1-r0-1), (c1-c0-1)
        sr = r0 + 1 + (ih-ph)//2
        sc = c0 + 1 + (iw-pw)//2
        for dr,dc in pshape:
            rr,cc = sr+dr, sc+dc
            if 0 <= rr < h and 0 <= cc < w:
                out[rr][cc] = pcol
    return out

def solve_H50(g: Grid) -> Grid:
    h,w = dims(g)
    anchor = next((r,c) for r in range(h) for c in range(w) if g[r][c] == 1)
    ar,ac = anchor
    cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] not in (0,1)]
    col = g[cells[0][0]][cells[0][1]]
    rel = [(r-ar, c-ac) for r,c in cells]
    out = blank(h,w)
    out[ar][ac] = 1
    for dr,dc in rel:
        for rr,cc in [(dr,dc), (-dc,dr), (-dr,-dc), (dc,-dr)]:
            r,c = ar+rr, ac+cc
            if 0 <= r < h and 0 <= c < w:
                out[r][c] = col
    return out

def solve_H51(g: Grid) -> Grid:
    left,right = split_h_panels_by_sep(g, sep=9)
    h,w = dims(left)
    out = blank(h,w)
    for r in range(h):
        for c in range(w):
            if left[r][c] != 0:
                out[r][c] = right[r][c]
    return out

def solve_H52(g: Grid) -> Grid:
    panels = split_h_panels_by_sep(g, sep=9)
    A,B,C = panels
    candidates = {
        'rot90': rotate_grid_cw,
        'rot270': rotate_grid_ccw,
        'rot180': rotate_grid_180,
        'hflip': hflip_grid,
        'vflip': vflip_grid,
    }
    for name,fn in candidates.items():
        if fn(A) == B:
            return fn(C)
    return C

def solve_H53(g: Grid) -> Grid:
    h,w = dims(g)
    out = blank(h,w)
    rowlens = [g[r][0] for r in range(1,h)]
    collens = [g[0][c] for c in range(1,w)]
    for r in range(1,h):
        for c in range(1,w):
            if rowlens[r-1] >= c and collens[c-1] >= r:
                out[r][c] = 8
    return out

def solve_H54(g: Grid) -> Grid:
    h,w = dims(g)
    code = g[0][0]
    cells = [(r,c) for r in range(h) for c in range(w) if g[r][c] != 0 and not (r==0 and c==0)]
    color = g[cells[0][0]][cells[0][1]]
    shape,(ph,pw),(r0,c0) = normalize(cells)
    kind = {1:'rot90', 2:'rot180', 3:'hflip', 4:'vflip'}[code]
    tshape = transform_shape(shape, kind)
    out = blank(h,w)
    for dr,dc in tshape:
        rr,cc = r0+dr, c0+dc
        if 0 <= rr < h and 0 <= cc < w:
            out[rr][cc] = color
    return out

def solve_H55(g: Grid) -> Grid:
    p1,p2,q = split_h_panels_by_sep(g, sep=9)
    def label_and_shape(panel):
        label = panel[0][0]
        cells = [(r,c) for r in range(len(panel)) for c in range(len(panel[0]))
                 if panel[r][c] != 0 and not (r==0 and c==0)]
        sh,_,_ = normalize(cells)
        return label, sh, cells
    lab1,sh1,_ = label_and_shape(p1)
    lab2,sh2,_ = label_and_shape(p2)
    qcells = [(r,c) for r in range(len(q)) for c in range(len(q[0])) if q[r][c] != 0]
    qshape,_,_ = normalize(qcells)
    out = blank(*dims(q))
    if qshape in all_symmetries(sh1):
        lab = lab1
    else:
        lab = lab2
    for r,c in qcells:
        out[r][c] = lab
    return out

def solve_H56(g: Grid) -> Grid:
    h,w = dims(g)
    anchors = [(g[r][c], r, c) for r in range(h) for c in range(w) if g[r][c] in (2,3,4,5)]
    comps = [(col,cells) for col,cells in same_color_components(g) if col not in (2,3,4,5)]
    pcol,pcells = max(comps, key=lambda t: len(t[1]))
    pshape,_,_ = normalize(pcells)
    code_to_kind = {2:'id', 3:'rot90', 4:'rot180', 5:'rot270'}
    out = blank(h,w)
    for code,ar,ac in anchors:
        tshape = transform_shape(pshape, code_to_kind[code])
        for dr,dc in tshape:
            rr,cc = ar+dr, ac+dc
            if 0 <= rr < h and 0 <= cc < w:
                out[rr][cc] = pcol
    return out

SOLVERS = {
    'E50': solve_E50,
    'E51': solve_E51,
    'E52': solve_E52,
    'E53': solve_E53,
    'E54': solve_E54,
    'E55': solve_E55,
    'E56': solve_E56,
    'M50': solve_M50,
    'M51': solve_M51,
    'M52': solve_M52,
    'M53': solve_M53,
    'M54': solve_M54,
    'M55': solve_M55,
    'M56': solve_M56,
    'H50': solve_H50,
    'H51': solve_H51,
    'H52': solve_H52,
    'H53': solve_H53,
    'H54': solve_H54,
    'H55': solve_H55,
    'H56': solve_H56,
}
