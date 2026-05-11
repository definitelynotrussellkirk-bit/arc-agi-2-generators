"""
ARC-style puzzle bank: 21 additional puzzles (7 easy, 7 medium, 7 hard).
Each solve_* function is a reference program for one puzzle.
"""
from __future__ import annotations
from typing import List, Tuple
from collections import deque, defaultdict

Grid = List[List[int]]

def dims(g): return len(g), len(g[0])


def clone(g): return [row[:] for row in g]


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)


def horizontal_runs(g, color=None):
    h,w=dims(g)
    runs=[]
    for r in range(h):
        c=0
        while c<w:
            val=g[r][c]
            if val!=0 and (color is None or val==color):
                start=c
                while c+1<w and g[r][c+1]==val:
                    c+=1
                runs.append((r,start,c,val))
            c+=1
    return runs


def vertical_runs(g, color=None):
    h,w=dims(g)
    runs=[]
    for c in range(w):
        r=0
        while r<h:
            val=g[r][c]
            if val!=0 and (color is None or val==color):
                start=r
                while r+1<h and g[r+1][c]==val:
                    r+=1
                runs.append((start,r,c,val))
            r+=1
    return runs


def reflect_vertical(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][w-1-c]=g[r][c]
    return out


def components(g: Grid, colors=None):
    h, w = dims(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in seen or g[r][c]==0: 
                continue
            if colors is not None and g[r][c] not in colors:
                continue
            col = g[r][c]
            q=deque([(r,c)]); seen.add((r,c)); comp=[]
            while q:
                x,y=q.popleft(); comp.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and g[nx][ny]==col:
                        seen.add((nx,ny)); q.append((nx,ny))
            comps.append((col, comp))
    return comps


def find_holes_of_component(g: Grid, comp_cells: List[Tuple[int,int]]):
    # return enclosed zero cells inside component bbox not reachable to bbox boundary within bbox
    r0,r1,c0,c1 = bbox(comp_cells)
    comp_set = set(comp_cells)
    H = r1-r0+1; W = c1-c0+1
    # bbox local grid: 1 if component occupies, 0 otherwise
    seen=set()
    q=deque()
    # start from bbox boundary zeros
    for rr in range(r0,r1+1):
        for cc in [c0,c1]:
            if (rr,cc) not in comp_set:
                q.append((rr,cc)); seen.add((rr,cc))
    for cc in range(c0,c1+1):
        for rr in [r0,r1]:
            if (rr,cc) not in comp_set and (rr,cc) not in seen:
                q.append((rr,cc)); seen.add((rr,cc))
    while q:
        x,y=q.popleft()
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy
            if r0<=nx<=r1 and c0<=ny<=c1 and (nx,ny) not in comp_set and (nx,ny) not in seen:
                seen.add((nx,ny)); q.append((nx,ny))
    holes=[]
    for rr in range(r0,r1+1):
        for cc in range(c0,c1+1):
            if (rr,cc) not in comp_set and (rr,cc) not in seen:
                holes.append((rr,cc))
    return holes


def normalize_shape(comp):
    r0,r1,c0,c1 = bbox(comp)
    return sorted((r-r0,c-c0) for r,c in comp)


def solve_E1(g: Grid, src=2, dst=8) -> Grid:
    out = clone(g)
    for r, c0, c1, val in horizontal_runs(g, color=src):
        if c1-c0+1 >= 3:
            out[r][c0] = dst
            out[r][c1] = dst
    return out


def solve_E2(g: Grid, src=3, dst=7) -> Grid:
    out = clone(g)
    for r0, r1, c, val in vertical_runs(g, color=src):
        if r1-r0+1 == 2:
            for r in range(r0, r1+1):
                out[r][c] = dst
    return out


def solve_E3(g: Grid, border=4, fill=6) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            # check 3x3 ring with center zero
            coords = [(r+dr, c+dc) for dr in (-1,0,1) for dc in (-1,0,1)]
            if g[r][c] == 0:
                ok = True
                for rr,cc in coords:
                    if (rr,cc)==(r,c): continue
                    if g[rr][cc] != border:
                        ok=False; break
                if ok:
                    out[r][c] = fill
    return out


def solve_E4(g: Grid) -> Grid:
    return reflect_vertical(g)


def solve_E5(g: Grid, dst=9) -> Grid:
    h,w = dims(g)
    out = clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                if all(not (0 <= r+dr < h and 0 <= c+dc < w and g[r+dr][c+dc]!=0)
                       for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]):
                    out[r][c] = dst
    return out


def solve_E6(g: Grid, marker=7) -> Grid:
    out = clone(g)
    h,w = dims(g)
    for r in range(h):
        nz = [x for x in g[r] if x != 0]
        if len(nz) == 1 and nz[0] == marker:
            out[r] = [marker]*w
    return out


def solve_E7(g: Grid, src=5, dst=2) -> Grid:
    out = clone(g)
    for r0,r1,c,val in vertical_runs(g, color=src):
        length = r1-r0+1
        if length >= 3 and length % 2 == 1:
            center = (r0+r1)//2
            out[center][c] = dst
    return out


def solve_M1(g: Grid, dst=8) -> Grid:
    comps = components(g)
    smallest = min(comps, key=lambda x: len(x[1]))[1]
    out = clone(g)
    for r,c in smallest:
        out[r][c] = dst
    return out


def solve_M2(g: Grid) -> Grid:
    out = [[0]*len(g[0]) for _ in range(len(g))]
    for col, comp in components(g):
        r0,r1,c0,c1 = bbox(comp)
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c] = col
    return out


def solve_M3(g: Grid) -> Grid:
    # same-color single-cell markers in same row or col, fill gap if only zeros between.
    h,w = dims(g)
    out = clone(g)
    # find singletons? or any cells of a color; use all individual cells of nonzero
    cells_by_color = defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                cells_by_color[g[r][c]].append((r,c))
    for color, cells in cells_by_color.items():
        for i in range(len(cells)):
            for j in range(i+1,len(cells)):
                r1,c1 = cells[i]; r2,c2 = cells[j]
                if r1 == r2:
                    lo, hi = sorted([c1,c2])
                    if all(g[r1][c]==0 for c in range(lo+1,hi)):
                        for c in range(lo,hi+1):
                            out[r1][c]=color
                elif c1 == c2:
                    lo, hi = sorted([r1,r2])
                    if all(g[r][c1]==0 for r in range(lo+1,hi)):
                        for r in range(lo,hi+1):
                            out[r][c1]=color
    return out


def solve_M4(g: Grid, m1=1, m2=2):
    h,w=dims(g)
    pos1=pos2=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==m1: pos1=(r,c)
            elif g[r][c]==m2: pos2=(r,c)
    dr=pos2[0]-pos1[0]; dc=pos2[1]-pos1[1]
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and g[r][c] not in (m1,m2):
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=g[r][c]
    return out


def solve_M5(g: Grid) -> Grid:
    h,w = dims(g)
    out = [[0]*w for _ in range(h)]
    for col, comp in components(g):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in comp):
            for r,c in comp:
                out[r][c] = col
    return out


def solve_M6(g: Grid) -> Grid:
    comps = components(g)
    comps_sorted = sorted(comps, key=lambda x: len(x[1]))
    ranks = {id(comp): rank+1 for rank,(col,comp) in enumerate(comps_sorted)}  # not used
    out = [[0]*len(g[0]) for _ in range(len(g))]
    # unique sizes/order guaranteed in examples
    for rank, (col, comp) in enumerate(comps_sorted, start=1):
        for r,c in comp:
            out[r][c] = rank
    return out


def solve_M7(g: Grid) -> Grid:
    h,w = dims(g)
    out = [[0]*w for _ in range(h)]
    for col, comp in components(g):
        holes = find_holes_of_component(g, comp)
        for r,c in holes:
            out[r][c] = col
    return out


def solve_H1(g: Grid) -> Grid:
    # Extract components, sort ascending by area, pack left->right with one zero col between.
    comps = components(g)
    items=[]
    maxh=0
    for col, comp in comps:
        r0,r1,c0,c1 = bbox(comp)
        H=r1-r0+1; W=c1-c0+1
        maxh=max(maxh,H)
        cells=[(r-r0,c-c0) for r,c in comp]
        items.append((len(comp), H, W, col, cells))
    items.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    total_w = sum(item[2] for item in items) + max(0, len(items)-1)
    out = [[0]*total_w for _ in range(maxh)]
    offset=0
    for area,H,W,col,cells in items:
        # top-align
        for r,c in cells:
            out[r][offset+c] = col
        offset += W + 1
    return out


def solve_H2(g: Grid) -> Grid:
    # assume components of same color; two shapes identical up to translation, one missing one cell.
    comps = components(g)
    # group by color maybe same; compare normalized shapes
    shapes = []
    for col, comp in comps:
        norm = set(normalize_shape(comp))
        shapes.append((col, comp, norm))
    # find target union shape: choose shape with max size or most common subset/superset relation
    # Here examples should ensure one shape size = canonical and one smaller by 1.
    # We'll take the largest normalized shape as canonical.
    canonical = max(shapes, key=lambda x: len(x[2]))[2]
    # defective comp is one whose norm is strict subset of canonical
    defective = None
    for col, comp, norm in shapes:
        if norm != canonical and norm.issubset(canonical):
            defective = (col, comp, norm)
            break
    if defective is None:
        defective = min(shapes, key=lambda x: len(x[2]))
    col, comp, norm = defective
    r0,r1,c0,c1 = bbox(comp)
    # output repaired defective object only, cropped
    maxr = max(r for r,c in canonical)
    maxc = max(c for r,c in canonical)
    out = [[0]*(maxc+1) for _ in range(maxr+1)]
    for r,c in canonical:
        out[r][c] = col
    return out


def solve_H3(g: Grid, m1=1, m2=2, marker_colors={1,2}) -> Grid:
    h,w=dims(g)
    pos1=pos2=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==m1: pos1=(r,c)
            elif g[r][c]==m2: pos2=(r,c)
    dr = pos2[0]-pos1[0]; dc=pos2[1]-pos1[1]
    out = [[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0 and g[r][c] not in marker_colors:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=g[r][c]
    return out


def solve_H4(g: Grid, frame_color=8):
    # find single rectangular frame; mirror non-frame nonzero cells inside its interior across local vertical midline, preserving originals
    h,w=dims(g)
    # frame cells of given color
    frame_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==frame_color]
    r0,r1,c0,c1 = bbox(frame_cells)
    out = clone(g)
    interior_c0, interior_c1 = c0+1, c1-1
    for r in range(r0+1, r1):
        for c in range(c0+1, c1):
            val = g[r][c]
            if val != 0 and val != frame_color:
                mc = c0 + c1 - c
                if c0 < mc < c1:
                    out[r][mc] = val
    return out


def solve_H5(g: Grid) -> Grid:
    # count components per color; among color with most components, fill holes of its components with 9.
    comps = components(g)
    by_color = defaultdict(list)
    for col, comp in comps:
        by_color[col].append(comp)
    target_color = max(by_color.items(), key=lambda kv: len(kv[1]))[0]
    out = clone(g)
    for comp in by_color[target_color]:
        holes = find_holes_of_component(g, comp)
        for r,c in holes:
            out[r][c] = 9
    return out


def solve_H6(g: Grid):
    # assume odd dims with central row/col zero separators. Three quadrants have mirrored copies of one shape color, one quadrant empty.
    h,w = dims(g)
    midr, midc = h//2, w//2
    # extract quadrants excluding center row/col
    quads = {
        'TL': [row[:midc] for row in g[:midr]],
        'TR': [row[midc+1:] for row in g[:midr]],
        'BL': [row[:midc] for row in g[midr+1:]],
        'BR': [row[midc+1:] for row in g[midr+1:]],
    }
    # determine missing quadrant (all zeros)
    missing = next(name for name,q in quads.items() if all(v==0 for row in q for v in row))
    # choose source quadrant any non-empty
    source_name = next(name for name,q in quads.items() if name != missing and any(v!=0 for row in q for v in row))
    source = quads[source_name]
    # to fill missing, mirror source appropriately from source_name to missing
    import copy
    def flip_h(q): return q[::-1]
    def flip_v(q): return [row[::-1] for row in q]
    # Actually horizontal/vertical naming: across central horizontal axis flips rows, across vertical axis flips cols.
    q = source
    # Map from source to target by flips
    if source_name[0] != missing[0]:  # T/B differs
        q = q[::-1]
    if source_name[1] != missing[1]:  # L/R differs
        q = [row[::-1] for row in q]
    # write into out
    out = clone(g)
    # positions for missing quad
    rstart = 0 if missing[0]=='T' else midr+1
    cstart = 0 if missing[1]=='L' else midc+1
    for r in range(len(q)):
        for c in range(len(q[0])):
            out[rstart+r][cstart+c] = q[r][c]
    return out


def solve_H7(g: Grid):
    # assume two components of colors 2 and 3. Normalize each to top-left of its bbox, then output overlap cells as 8 in cropped bbox.
    comps = components(g)
    # choose first two components
    comps = comps[:2]
    norms=[]
    for col, comp in comps:
        norms.append(set(normalize_shape(comp)))
    inter = norms[0] & norms[1]
    if not inter:
        return [[0]]
    maxr=max(r for r,c in inter); maxc=max(c for r,c in inter)
    out=[[0]*(maxc+1) for _ in range(maxr+1)]
    for r,c in inter:
        out[r][c]=8
    return out


SOLVERS = {
    "E1": solve_E1,
    "E2": solve_E2,
    "E3": solve_E3,
    "E4": solve_E4,
    "E5": solve_E5,
    "E6": solve_E6,
    "E7": solve_E7,
    "M1": solve_M1,
    "M2": solve_M2,
    "M3": solve_M3,
    "M4": solve_M4,
    "M5": solve_M5,
    "M6": solve_M6,
    "M7": solve_M7,
    "H1": solve_H1,
    "H2": solve_H2,
    "H3": solve_H3,
    "H4": solve_H4,
    "H5": solve_H5,
    "H6": solve_H6,
    "H7": solve_H7,
}

PUZZLES = {'E1': {'id': 'E1',
        'title': 'Horizontal run endcaps',
        'difficulty': 'easy',
        'tests': 'Run detection; preserve-interior behavior.',
        'written_solution': 'For every horizontal run of color 2 with length at least 3, change only the first and '
                            'last cell of that run to color 8. Leave the interior 2s and everything else unchanged.',
        'staged_hint': 'Stage 1: detect horizontal 2-runs. Stage 2: recolor only the two boundary cells.',
        'program_function': 'solve_E1',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 2, 2, 0, 0],
                             [0, 0, 0, 2, 0, 0, 0],
                             [0, 2, 2, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0],
                              [0, 8, 2, 2, 8, 0, 0],
                              [0, 0, 0, 2, 0, 0, 0],
                              [0, 2, 2, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]]},
                  {'input': [[0, 0, 2, 2, 2, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 2, 2, 2, 2, 0],
                             [0, 0, 0, 2, 2, 0, 0, 0]],
                   'output': [[0, 0, 8, 2, 8, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 8, 2, 2, 2, 2, 8, 0],
                              [0, 0, 0, 2, 2, 0, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 2, 2, 2, 0, 0, 2, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 2, 2, 2, 0, 0],
                            [0, 0, 0, 0, 2, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 8, 2, 8, 0, 0, 2, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 8, 2, 2, 2, 8, 0, 0],
                             [0, 0, 0, 0, 2, 0, 0, 0, 0]]}]},
 'E2': {'id': 'E2',
        'title': 'Vertical domino promotion',
        'difficulty': 'easy',
        'tests': 'Exact-length reasoning; distinguish length-2 from longer runs.',
        'written_solution': 'Every vertical run of color 3 of exact length 2 becomes color 7. Single 3s and longer '
                            '3-columns stay unchanged.',
        'staged_hint': 'First classify vertical 3-runs by length, then recolor only the length-2 cases.',
        'program_function': 'solve_E2',
        'train': [{'input': [[0, 0, 0, 0, 0, 0],
                             [0, 0, 3, 0, 0, 0],
                             [0, 0, 3, 0, 0, 0],
                             [0, 0, 0, 3, 0, 0],
                             [0, 0, 0, 3, 0, 0],
                             [0, 0, 0, 3, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0],
                              [0, 0, 7, 0, 0, 0],
                              [0, 0, 7, 0, 0, 0],
                              [0, 0, 0, 3, 0, 0],
                              [0, 0, 0, 3, 0, 0],
                              [0, 0, 0, 3, 0, 0]]},
                  {'input': [[0, 3, 0, 0, 0, 0, 0],
                             [0, 3, 0, 0, 0, 0, 0],
                             [0, 0, 0, 3, 0, 0, 0],
                             [0, 0, 0, 3, 0, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0]],
                   'output': [[0, 7, 0, 0, 0, 0, 0],
                              [0, 7, 0, 0, 0, 0, 0],
                              [0, 0, 0, 7, 0, 0, 0],
                              [0, 0, 0, 7, 0, 0, 0],
                              [0, 0, 0, 0, 3, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 3, 0, 0, 0],
                            [0, 0, 0, 3, 0, 0, 0],
                            [0, 3, 0, 0, 0, 0, 0],
                            [0, 3, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 3, 0, 0],
                            [0, 0, 0, 0, 3, 0, 0],
                            [0, 0, 0, 0, 3, 0, 0]],
                  'output': [[0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 7, 0, 0, 0],
                             [0, 7, 0, 0, 0, 0, 0],
                             [0, 7, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0]]}]},
 'E3': {'id': 'E3',
        'title': 'Fill ring centers',
        'difficulty': 'easy',
        'tests': 'Local 3×3 pattern recognition.',
        'written_solution': 'Whenever a 3×3 neighborhood has color 4 on all eight outer cells and 0 in the center, '
                            'fill the center with color 6.',
        'staged_hint': 'First mark valid 3×3 rings, then write 6 into their centers.',
        'program_function': 'solve_E3',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0],
                             [0, 4, 4, 4, 0, 0, 0],
                             [0, 4, 0, 4, 0, 0, 0],
                             [0, 4, 4, 4, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0],
                              [0, 4, 4, 4, 0, 0, 0],
                              [0, 4, 6, 4, 0, 0, 0],
                              [0, 4, 4, 4, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 4, 4, 4, 0, 0, 0, 0],
                             [0, 4, 0, 4, 0, 0, 0, 0],
                             [0, 4, 4, 4, 0, 0, 0, 0],
                             [0, 0, 0, 0, 4, 4, 4, 0],
                             [0, 0, 0, 0, 4, 0, 4, 0],
                             [0, 0, 0, 0, 4, 4, 4, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 4, 4, 4, 0, 0, 0, 0],
                              [0, 4, 6, 4, 0, 0, 0, 0],
                              [0, 4, 4, 4, 0, 0, 0, 0],
                              [0, 0, 0, 0, 4, 4, 4, 0],
                              [0, 0, 0, 0, 4, 6, 4, 0],
                              [0, 0, 0, 0, 4, 4, 4, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 4, 4, 4, 0, 0, 0, 0, 0],
                            [0, 4, 0, 4, 0, 0, 0, 0, 0],
                            [0, 4, 4, 4, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 4, 4, 4, 0, 0],
                            [0, 0, 0, 0, 4, 0, 4, 0, 0],
                            [0, 0, 0, 0, 4, 4, 4, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 4, 4, 4, 0, 0, 0, 0, 0],
                             [0, 4, 6, 4, 0, 0, 0, 0, 0],
                             [0, 4, 4, 4, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 4, 4, 4, 0, 0],
                             [0, 0, 0, 0, 4, 6, 4, 0, 0],
                             [0, 0, 0, 0, 4, 4, 4, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]]}]},
 'E4': {'id': 'E4',
        'title': 'Vertical symmetrization',
        'difficulty': 'easy',
        'tests': 'Global reflection across a fixed axis.',
        'written_solution': 'Reflect every nonzero cell across the vertical midline of the grid and add the mirrored '
                            'copy, while preserving the original cells.',
        'staged_hint': 'Use the grid width to compute each mirror column, then paint both original and mirrored cells.',
        'program_function': 'solve_E4',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 0, 0, 0, 0, 0],
                             [0, 0, 2, 2, 0, 0, 0],
                             [0, 0, 0, 3, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0],
                              [0, 2, 0, 0, 0, 2, 0],
                              [0, 0, 2, 2, 2, 0, 0],
                              [0, 0, 0, 3, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 4, 0, 0, 0, 0],
                             [0, 0, 5, 0, 0, 0, 0, 0],
                             [0, 0, 5, 5, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 4, 4, 0, 0, 0],
                              [0, 0, 5, 0, 0, 5, 0, 0],
                              [0, 0, 5, 5, 5, 5, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 6, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 3, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 6, 0, 6, 0, 0, 0],
                             [0, 0, 2, 2, 0, 2, 2, 0, 0],
                             [0, 0, 0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]]}]},
 'E5': {'id': 'E5',
        'title': 'Isolated cells become 9',
        'difficulty': 'easy',
        'tests': 'Cardinal-neighbor checks; singleton detection.',
        'written_solution': 'Any nonzero cell whose four cardinal neighbors are all 0 is recolored to 9. Cells that '
                            'touch any nonzero neighbor keep their original color.',
        'staged_hint': 'Stage 1: mark isolated nonzero cells. Stage 2: recolor marked cells to 9.',
        'program_function': 'solve_E5',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 0, 0, 3, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 4, 4, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 5]],
                   'output': [[0, 0, 0, 0, 0, 0, 0],
                              [0, 9, 0, 0, 9, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 4, 4, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 9]]},
                  {'input': [[1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 2, 2, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 6]],
                   'output': [[9, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 2, 2, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 9]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 4, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 3, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 2, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 5, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 9, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 9, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 2, 2, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 9, 0, 0, 0, 0]]}]},
 'E6': {'id': 'E6',
        'title': 'Single-7 rows fill fully',
        'difficulty': 'easy',
        'tests': 'Whole-row activation from a sparse cue.',
        'written_solution': 'If a row contains exactly one nonzero cell and that cell is 7, fill the entire row with '
                            '7. Any row with a different nonzero pattern is left alone.',
        'staged_hint': 'First detect qualifying rows, then overwrite those rows with all 7s.',
        'program_function': 'solve_E6',
        'train': [{'input': [[0, 0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 7, 0, 7, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 7, 0, 0, 0]],
                   'output': [[7, 7, 7, 7, 7, 7, 7],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 7, 0, 7, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [7, 7, 7, 7, 7, 7, 7]]},
                  {'input': [[0, 0, 0, 0, 0, 0],
                             [0, 7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 7, 0, 0, 0],
                             [0, 0, 0, 7, 7, 0]],
                   'output': [[0, 0, 0, 0, 0, 0],
                              [7, 7, 7, 7, 7, 7],
                              [0, 0, 0, 0, 0, 0],
                              [7, 7, 7, 7, 7, 7],
                              [0, 0, 0, 7, 7, 0]]}],
        'test': [{'input': [[0, 0, 0, 8, 0, 0, 0],
                            [0, 0, 0, 7, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [7, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 7, 0, 7, 0, 0]],
                  'output': [[0, 0, 0, 8, 0, 0, 0],
                             [7, 7, 7, 7, 7, 7, 7],
                             [0, 0, 0, 0, 0, 0, 0],
                             [7, 7, 7, 7, 7, 7, 7],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 7, 0, 7, 0, 0]]}]},
 'E7': {'id': 'E7',
        'title': 'Mark odd vertical run centers',
        'difficulty': 'easy',
        'tests': 'Run centers; odd-vs-even length discrimination.',
        'written_solution': 'For each vertical run of color 5 with odd length at least 3, recolor only its center cell '
                            'to 2. Even-length runs or short runs do not change.',
        'staged_hint': 'Compute each 5-run’s length; if it is odd and at least 3, recolor the midpoint.',
        'program_function': 'solve_E7',
        'train': [{'input': [[0, 0, 5, 0, 0, 0],
                             [0, 0, 5, 0, 0, 0],
                             [0, 0, 5, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 5, 0, 0],
                             [0, 0, 0, 5, 0, 0],
                             [0, 0, 0, 5, 0, 0],
                             [0, 0, 0, 5, 0, 0]],
                   'output': [[0, 0, 5, 0, 0, 0],
                              [0, 0, 2, 0, 0, 0],
                              [0, 0, 5, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 5, 0, 0],
                              [0, 0, 0, 5, 0, 0],
                              [0, 0, 0, 5, 0, 0],
                              [0, 0, 0, 5, 0, 0]]},
                  {'input': [[0, 5, 0, 0, 0, 0, 0],
                             [0, 5, 0, 0, 0, 0, 0],
                             [0, 5, 0, 0, 0, 0, 0],
                             [0, 5, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 5, 0, 0],
                             [0, 0, 0, 0, 5, 0, 0],
                             [0, 0, 0, 0, 5, 0, 0]],
                   'output': [[0, 5, 0, 0, 0, 0, 0],
                              [0, 5, 0, 0, 0, 0, 0],
                              [0, 5, 0, 0, 0, 0, 0],
                              [0, 5, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 5, 0, 0],
                              [0, 0, 0, 0, 2, 0, 0],
                              [0, 0, 0, 0, 5, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 5, 0, 0, 0],
                            [0, 0, 0, 5, 0, 0, 0],
                            [0, 0, 0, 5, 0, 0, 0],
                            [0, 0, 0, 5, 0, 0, 0],
                            [0, 0, 5, 0, 0, 0, 0],
                            [0, 0, 5, 0, 0, 0, 0],
                            [0, 0, 5, 0, 0, 0, 0],
                            [0, 0, 5, 0, 0, 0, 0],
                            [0, 0, 5, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 5, 0, 0, 0],
                             [0, 0, 0, 5, 0, 0, 0],
                             [0, 0, 0, 5, 0, 0, 0],
                             [0, 0, 0, 5, 0, 0, 0],
                             [0, 0, 5, 0, 0, 0, 0],
                             [0, 0, 5, 0, 0, 0, 0],
                             [0, 0, 2, 0, 0, 0, 0],
                             [0, 0, 5, 0, 0, 0, 0],
                             [0, 0, 5, 0, 0, 0, 0]]}]},
 'M1': {'id': 'M1',
        'title': 'Recolor the smallest object',
        'difficulty': 'medium',
        'tests': 'Connected components and size comparison.',
        'written_solution': 'Find all nonzero connected components. Recolor the unique smallest component to 8, while '
                            'leaving every other object unchanged.',
        'staged_hint': 'Stage 1: segment objects. Stage 2: compare areas and recolor the smallest one.',
        'program_function': 'solve_M1',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 0, 0, 0, 0, 0],
                             [0, 2, 2, 0, 0, 0, 3, 0],
                             [0, 0, 0, 0, 0, 0, 3, 0],
                             [0, 0, 0, 4, 4, 4, 3, 0],
                             [0, 0, 0, 4, 4, 4, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 2, 2, 0, 0, 0, 0, 0],
                              [0, 2, 2, 0, 0, 0, 8, 0],
                              [0, 0, 0, 0, 0, 0, 8, 0],
                              [0, 0, 0, 4, 4, 4, 8, 0],
                              [0, 0, 0, 4, 4, 4, 0, 0]]},
                  {'input': [[0, 0, 0, 5, 0, 0, 0, 0, 0],
                             [0, 0, 0, 5, 0, 0, 6, 6, 0],
                             [0, 0, 0, 0, 0, 0, 6, 6, 0],
                             [0, 2, 2, 2, 0, 0, 0, 0, 0],
                             [0, 2, 2, 2, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 8, 0, 0, 0, 0, 0],
                              [0, 0, 0, 8, 0, 0, 6, 6, 0],
                              [0, 0, 0, 0, 0, 0, 6, 6, 0],
                              [0, 2, 2, 2, 0, 0, 0, 0, 0],
                              [0, 2, 2, 2, 0, 0, 0, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 3, 3, 3, 0, 0, 0, 0, 0],
                            [0, 3, 3, 3, 0, 0, 4, 0, 0],
                            [0, 0, 0, 0, 0, 0, 4, 0, 0],
                            [0, 5, 5, 0, 0, 0, 4, 0, 0],
                            [0, 5, 5, 0, 0, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 3, 0, 0, 0, 0, 0],
                             [0, 3, 3, 3, 0, 0, 8, 0, 0],
                             [0, 0, 0, 0, 0, 0, 8, 0, 0],
                             [0, 5, 5, 0, 0, 0, 8, 0, 0],
                             [0, 5, 5, 0, 0, 0, 0, 0, 0]]}]},
 'M2': {'id': 'M2',
        'title': 'Fill each object’s bounding box',
        'difficulty': 'medium',
        'tests': 'Component extraction and bbox reasoning.',
        'written_solution': 'For each nonzero object, compute its bounding box and fill that whole rectangle with the '
                            'object’s color. The output is otherwise blank.',
        'staged_hint': 'Detect components first; then replace each shape by its filled bounding rectangle.',
        'program_function': 'solve_M2',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 0, 0, 0, 0, 0],
                             [0, 2, 2, 2, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 3, 3, 0, 0],
                             [0, 0, 0, 3, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0],
                              [0, 2, 2, 2, 0, 0, 0],
                              [0, 2, 2, 2, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 3, 3, 0, 0],
                              [0, 0, 0, 3, 3, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 4, 4, 0, 0, 0, 0],
                             [0, 0, 0, 4, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 5, 5, 5, 0],
                             [0, 0, 0, 0, 0, 0, 5, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 4, 4, 0, 0, 0, 0],
                              [0, 0, 4, 4, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 5, 5, 5, 0],
                              [0, 0, 0, 0, 5, 5, 5, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 3, 0, 0, 0, 0, 0, 0, 0],
                            [0, 3, 3, 0, 0, 0, 0, 0, 0],
                            [0, 0, 3, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 6, 6, 0, 0, 0],
                            [0, 0, 0, 0, 0, 6, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 6, 6, 0, 0, 0],
                             [0, 0, 0, 0, 6, 6, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]]}]},
 'M3': {'id': 'M3',
        'title': 'Connect aligned markers',
        'difficulty': 'medium',
        'tests': 'Long-range same-row / same-column relations.',
        'written_solution': 'If two cells of the same color lie on the same row or the same column with only 0s '
                            'between them, fill the entire gap between them in that same color.',
        'staged_hint': 'Find same-colored aligned pairs, then draw horizontal or vertical segments between valid '
                       'pairs.',
        'program_function': 'solve_M3',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 0, 0, 0, 2, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 3, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0],
                              [0, 2, 2, 2, 2, 2, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 3, 0, 0, 0, 0],
                              [0, 0, 3, 0, 0, 0, 0],
                              [0, 0, 3, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]]},
                  {'input': [[0, 0, 0, 4, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 4, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 5, 0, 0, 0, 0, 5, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 4, 0, 0, 0, 0],
                              [0, 0, 0, 4, 0, 0, 0, 0],
                              [0, 0, 0, 4, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 5, 5, 5, 5, 5, 5, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 6, 0, 0, 0, 0, 0, 6, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 7, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 7, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 6, 6, 6, 6, 6, 6, 6, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 7, 0, 0, 0, 0, 0],
                             [0, 0, 0, 7, 0, 0, 0, 0, 0],
                             [0, 0, 0, 7, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]]}]},
 'M4': {'id': 'M4',
        'title': 'Copy payload by marker vector',
        'difficulty': 'medium',
        'tests': 'Learn a translation vector from markers, then apply it.',
        'written_solution': 'Read the vector from the cell colored 1 to the cell colored 2. Copy every non-marker '
                            'object by that vector, preserving the original objects and the markers.',
        'staged_hint': 'First recover the translation from 1→2. Then clone each payload cell to its translated '
                       'position.',
        'program_function': 'solve_M4',
        'train': [{'input': [[1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 2, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 3, 3, 0, 0, 0],
                             [0, 0, 0, 3, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]],
                   'output': [[1, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 2, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 3, 3, 0, 0, 0],
                              [0, 0, 0, 3, 0, 3, 3],
                              [0, 0, 0, 0, 0, 0, 3]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 2, 0, 0, 0],
                             [0, 0, 0, 4, 4, 0, 0, 0],
                             [0, 0, 0, 4, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 2, 0, 0, 0],
                              [0, 0, 0, 4, 4, 0, 0, 0],
                              [0, 0, 0, 4, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 4, 4]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 2, 0, 0],
                            [0, 0, 0, 5, 5, 0, 0, 0, 0],
                            [0, 0, 0, 0, 5, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 2, 0, 0],
                             [0, 0, 0, 5, 5, 0, 0, 0, 0],
                             [0, 0, 0, 0, 5, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 5, 5],
                             [0, 0, 0, 0, 0, 0, 0, 0, 5]]}]},
 'M5': {'id': 'M5',
        'title': 'Keep only border-touching objects',
        'difficulty': 'medium',
        'tests': 'Object filtering by border contact.',
        'written_solution': 'Keep the connected components that touch at least one outer border cell of the grid. '
                            'Remove all components that are strictly interior.',
        'staged_hint': 'Segment objects, test whether any cell hits the border, and keep only the positive cases.',
        'program_function': 'solve_M5',
        'train': [{'input': [[2, 0, 0, 0, 0, 0, 0],
                             [2, 2, 0, 0, 0, 0, 0],
                             [0, 0, 0, 3, 3, 0, 0],
                             [0, 0, 0, 3, 3, 0, 0],
                             [0, 0, 0, 0, 0, 0, 4]],
                   'output': [[2, 0, 0, 0, 0, 0, 0],
                              [2, 2, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 4]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0],
                             [0, 5, 5, 5, 0, 0, 0],
                             [0, 5, 0, 5, 0, 0, 0],
                             [0, 5, 5, 5, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 6],
                             [6, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 6],
                              [6, 0, 0, 0, 0, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 7, 0, 0, 0, 0],
                            [0, 0, 0, 7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 3, 3, 3, 0, 0, 0],
                            [0, 0, 3, 3, 3, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 8]],
                  'output': [[0, 0, 0, 7, 0, 0, 0, 0],
                             [0, 0, 0, 7, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 8]]}]},
 'M6': {'id': 'M6',
        'title': 'Rank components by size',
        'difficulty': 'medium',
        'tests': 'Relative ordering over multiple objects.',
        'written_solution': 'Find all connected components and sort them by area from smallest to largest. Recolor the '
                            'smallest component to 1, the next to 2, and the largest to 3, preserving each shape.',
        'staged_hint': 'Stage 1: measure object sizes. Stage 2: repaint by rank.',
        'program_function': 'solve_M6',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 0, 0, 0, 0, 0, 0],
                             [0, 2, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 3, 3, 3, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 4, 4, 4, 0],
                             [0, 0, 0, 0, 4, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0, 0, 0, 0],
                              [0, 1, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 2, 2, 2, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 3, 3, 3, 0],
                              [0, 0, 0, 0, 3, 0, 0, 0]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 5, 5, 0, 0, 0, 0, 0],
                             [0, 0, 0, 5, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 6, 6, 6, 0, 0],
                             [0, 0, 0, 0, 0, 0, 6, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 7, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 2, 2, 0, 0, 0, 0, 0],
                              [0, 0, 0, 2, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 3, 3, 3, 0, 0],
                              [0, 0, 0, 0, 0, 0, 3, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 1, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 8, 8, 0, 0, 0, 0],
                            [0, 0, 0, 8, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 4, 4, 4, 4, 4, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 6, 6, 0],
                            [0, 0, 0, 0, 0, 0, 6, 6, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 3, 3, 3, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 2, 2, 0],
                             [0, 0, 0, 0, 0, 0, 2, 2, 0]]}]},
 'M7': {'id': 'M7',
        'title': 'Show holes only',
        'difficulty': 'medium',
        'tests': 'Hole detection inside closed shapes.',
        'written_solution': 'For each object that encloses one or more internal background cells, output only those '
                            'hole cells, colored with the enclosing object’s color. Everything else becomes 0.',
        'staged_hint': 'Treat each object separately inside its bounding box: flood outside background, then keep the '
                       'unreachable zero cells.',
        'program_function': 'solve_M7',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 2, 0, 0, 0],
                             [0, 2, 0, 2, 0, 0, 0],
                             [0, 2, 2, 2, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 2, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 3, 0, 0, 0, 0],
                             [0, 3, 0, 3, 0, 0, 0, 0],
                             [0, 3, 3, 3, 0, 0, 0, 0],
                             [0, 0, 0, 4, 4, 4, 0, 0],
                             [0, 0, 0, 4, 0, 4, 0, 0],
                             [0, 0, 0, 4, 4, 4, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 3, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 4, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 5, 5, 5, 0, 0, 0, 0, 0],
                            [0, 5, 0, 5, 0, 0, 0, 0, 0],
                            [0, 5, 5, 5, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 6, 6, 6, 0, 0],
                            [0, 0, 0, 0, 6, 0, 6, 0, 0],
                            [0, 0, 0, 0, 6, 6, 6, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 5, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 6, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]]}]},
 'H1': {'id': 'H1',
        'title': 'Pack objects sorted by area',
        'difficulty': 'hard',
        'tests': 'Object extraction, output resizing, sorting, and repacking.',
        'written_solution': 'Extract every nonzero object, crop it to its own bounding box, sort the cropped objects '
                            'by area from smallest to largest, and pack them left-to-right in a new output grid with '
                            'one blank column between neighboring objects. Top-align all packed shapes.',
        'staged_hint': 'Segment and crop first; only after sorting should you build the new output canvas.',
        'program_function': 'solve_H1',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 0, 0, 0, 3, 3, 0],
                             [0, 2, 2, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 4, 4, 0, 0, 0, 0],
                             [0, 0, 0, 4, 4, 0, 0, 0, 0],
                             [0, 0, 0, 4, 0, 0, 0, 0, 0]],
                   'output': [[3, 3, 0, 2, 2, 0, 4, 4], [0, 0, 0, 2, 2, 0, 4, 4], [0, 0, 0, 0, 0, 0, 4, 0]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 6, 6, 0, 0, 0],
                             [0, 0, 0, 0, 0, 6, 6, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 7, 0]],
                   'output': [[7, 0, 5, 5, 5, 0, 6, 6], [0, 0, 0, 0, 0, 0, 6, 6]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0]],
                  'output': [[2, 0, 3, 3, 0, 4, 4, 4], [2, 0, 3, 0, 0, 0, 0, 4]]}]},
 'H2': {'id': 'H2',
        'title': 'Repair the defective copy',
        'difficulty': 'hard',
        'tests': 'Relational comparison between multiple normalized shapes.',
        'written_solution': 'Three copies of the same-colored shape appear in the input. Two are complete; one is '
                            'missing exactly one cell. Identify the defective copy, infer the full canonical shape '
                            'from the complete copies, and output only the repaired canonical shape cropped tightly.',
        'staged_hint': 'Normalize each object to its own top-left corner, compare the normalized shapes, then output '
                       'the repaired canonical pattern.',
        'program_function': 'solve_H2',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 2, 0, 0, 2, 2, 0],
                             [0, 0, 2, 0, 0, 0, 0, 2, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 2, 0, 0, 0, 0, 0],
                             [0, 0, 2, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[2, 2, 2], [0, 2, 0]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 0, 0, 0, 0, 3, 3, 0],
                             [0, 0, 3, 0, 0, 0, 0, 0, 3, 0],
                             [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 3, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[3, 3], [0, 3], [0, 3]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 0],
                            [0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[4, 4, 4], [0, 4, 0]]}]},
 'H3': {'id': 'H3',
        'title': 'Shift all payload objects by the learned vector',
        'difficulty': 'hard',
        'tests': 'Global relational vector applied to multiple objects; original removed.',
        'written_solution': 'The vector from color 1 to color 2 is the motion rule. Shift every non-marker object by '
                            'that vector into a blank output grid. Do not keep the original objects, and do not copy '
                            'the markers.',
        'staged_hint': 'Recover the vector first; then replay every non-marker cell into the translated position on a '
                       'fresh blank canvas.',
        'program_function': 'solve_H3',
        'train': [{'input': [[0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 2, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 3, 3, 0, 0, 0, 0],
                             [0, 0, 0, 3, 0, 4, 0, 0],
                             [0, 0, 0, 0, 0, 4, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 3, 3, 0, 0],
                              [0, 0, 0, 0, 0, 3, 0, 4],
                              [0, 0, 0, 0, 0, 0, 0, 4]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 2, 0],
                             [0, 5, 5, 0, 0, 0, 0, 0, 0],
                             [0, 5, 0, 0, 6, 0, 0, 0, 0],
                             [0, 0, 0, 0, 6, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 5, 5, 0, 0],
                              [0, 0, 0, 0, 0, 5, 0, 0, 6],
                              [0, 0, 0, 0, 0, 0, 0, 0, 6]]}],
        'test': [{'input': [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 3, 0, 0, 7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 7, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 3, 3, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 3, 0, 0, 7],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 7]]}]},
 'H4': {'id': 'H4',
        'title': 'Mirror inside the local frame',
        'difficulty': 'hard',
        'tests': 'Local coordinate frame inside an enclosing object.',
        'written_solution': 'Find the rectangular frame made of color 8. Inside that frame, mirror every non-frame '
                            'nonzero cell across the frame’s own vertical centerline, preserving the original interior '
                            'cells and the frame itself.',
        'staged_hint': 'Treat the frame as a local workspace with its own left/right boundaries; mirror only the '
                       'interior payload cells.',
        'program_function': 'solve_H4',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 8, 8, 8, 8, 8, 8, 8, 0],
                             [0, 8, 0, 3, 0, 0, 0, 8, 0],
                             [0, 8, 0, 0, 3, 0, 0, 8, 0],
                             [0, 8, 0, 0, 0, 0, 0, 8, 0],
                             [0, 8, 8, 8, 8, 8, 8, 8, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 8, 8, 8, 8, 8, 8, 8, 0],
                              [0, 8, 0, 3, 0, 3, 0, 8, 0],
                              [0, 8, 0, 0, 3, 0, 0, 8, 0],
                              [0, 8, 0, 0, 0, 0, 0, 8, 0],
                              [0, 8, 8, 8, 8, 8, 8, 8, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 8, 8, 8, 8, 8, 8, 8, 0],
                             [0, 0, 8, 0, 4, 0, 0, 0, 8, 0],
                             [0, 0, 8, 4, 4, 0, 0, 0, 8, 0],
                             [0, 0, 8, 0, 0, 0, 0, 0, 8, 0],
                             [0, 0, 8, 8, 8, 8, 8, 8, 8, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 8, 8, 8, 8, 8, 8, 8, 0],
                              [0, 0, 8, 0, 4, 0, 4, 0, 8, 0],
                              [0, 0, 8, 4, 4, 0, 4, 4, 8, 0],
                              [0, 0, 8, 0, 0, 0, 0, 0, 8, 0],
                              [0, 0, 8, 8, 8, 8, 8, 8, 8, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
                            [0, 0, 8, 0, 0, 6, 0, 0, 0, 8, 0],
                            [0, 0, 8, 0, 6, 6, 0, 0, 0, 8, 0],
                            [0, 0, 8, 0, 0, 0, 0, 0, 0, 8, 0],
                            [0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
                             [0, 0, 8, 0, 0, 6, 6, 0, 0, 8, 0],
                             [0, 0, 8, 0, 6, 6, 6, 6, 0, 8, 0],
                             [0, 0, 8, 0, 0, 0, 0, 0, 0, 8, 0],
                             [0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}]},
 'H5': {'id': 'H5',
        'title': 'Fill holes for the most component-rich color',
        'difficulty': 'hard',
        'tests': 'Color-level aggregation plus per-object hole filling.',
        'written_solution': 'Count how many separate connected components each color has. Choose the color with the '
                            'most components. For that color only, fill the holes inside its closed components with '
                            'color 9. Leave all existing colored cells untouched.',
        'staged_hint': 'First decide which color wins the component-count vote; only then inspect holes in components '
                       'of that color.',
        'program_function': 'solve_H5',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 2, 0, 0, 0, 0, 0],
                             [0, 2, 0, 2, 0, 0, 3, 3, 0],
                             [0, 2, 2, 2, 0, 0, 3, 3, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 2, 2, 2, 0, 0],
                             [0, 0, 0, 0, 2, 0, 2, 0, 0],
                             [0, 0, 0, 0, 2, 2, 2, 0, 0],
                             [0, 4, 4, 4, 0, 0, 0, 0, 0],
                             [0, 4, 0, 4, 0, 0, 0, 0, 0],
                             [0, 4, 4, 4, 0, 0, 0, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 2, 2, 2, 0, 0, 0, 0, 0],
                              [0, 2, 9, 2, 0, 0, 3, 3, 0],
                              [0, 2, 2, 2, 0, 0, 3, 3, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 2, 2, 2, 0, 0],
                              [0, 0, 0, 0, 2, 9, 2, 0, 0],
                              [0, 0, 0, 0, 2, 2, 2, 0, 0],
                              [0, 4, 4, 4, 0, 0, 0, 0, 0],
                              [0, 4, 0, 4, 0, 0, 0, 0, 0],
                              [0, 4, 4, 4, 0, 0, 0, 0, 0]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                             [0, 5, 0, 5, 0, 0, 0, 0, 0, 0],
                             [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 5, 5, 5, 0, 0, 0],
                             [0, 0, 0, 0, 5, 0, 5, 0, 0, 0],
                             [0, 0, 0, 0, 5, 5, 5, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 6, 6, 0, 0],
                             [0, 0, 0, 0, 0, 0, 6, 6, 0, 0]],
                   'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                              [0, 5, 9, 5, 0, 0, 0, 0, 0, 0],
                              [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 5, 5, 5, 0, 0, 0],
                              [0, 0, 0, 0, 5, 9, 5, 0, 0, 0],
                              [0, 0, 0, 0, 5, 5, 5, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 6, 6, 0, 0],
                              [0, 0, 0, 0, 0, 0, 6, 6, 0, 0]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 3, 3, 3, 0, 0, 0, 0, 0, 0],
                            [0, 3, 0, 3, 0, 0, 0, 0, 0, 0],
                            [0, 3, 3, 3, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 3, 3, 3, 0, 0],
                            [0, 0, 0, 0, 0, 3, 0, 3, 0, 0],
                            [0, 0, 0, 0, 0, 3, 3, 3, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 4, 4],
                            [0, 0, 0, 0, 0, 0, 0, 0, 4, 4]],
                  'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 3, 0, 0, 0, 0, 0, 0],
                             [0, 3, 9, 3, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 3, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 3, 3, 3, 0, 0],
                             [0, 0, 0, 0, 0, 3, 9, 3, 0, 0],
                             [0, 0, 0, 0, 0, 3, 3, 3, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 4, 4],
                             [0, 0, 0, 0, 0, 0, 0, 0, 4, 4]]}]},
 'H6': {'id': 'H6',
        'title': 'Complete the missing mirrored quadrant',
        'difficulty': 'hard',
        'tests': 'Quadrant decomposition and composition via flips.',
        'written_solution': 'The grid is divided into four quadrants by a central zero row and zero column. Three '
                            'quadrants contain mirrored versions of the same pattern, and one quadrant is blank. Fill '
                            'the blank quadrant with the pattern transformed by the flips needed to match its '
                            'location.',
        'staged_hint': 'Split into quadrants, identify the missing one, infer which horizontal/vertical flips are '
                       'needed, then write only that quadrant.',
        'program_function': 'solve_H6',
        'train': [{'input': [[2, 2, 0, 0, 0, 2, 2],
                             [2, 0, 0, 0, 0, 0, 2],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [2, 0, 0, 0, 0, 0, 0],
                             [2, 2, 0, 0, 0, 0, 0]],
                   'output': [[2, 2, 0, 0, 0, 2, 2],
                              [2, 0, 0, 0, 0, 0, 2],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [2, 0, 0, 0, 0, 0, 2],
                              [2, 2, 0, 0, 0, 2, 2]]},
                  {'input': [[0, 3, 0, 0, 0, 3, 0],
                             [0, 3, 3, 0, 3, 3, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 3, 3, 0, 0, 0, 0],
                             [0, 3, 0, 0, 0, 0, 0]],
                   'output': [[0, 3, 0, 0, 0, 3, 0],
                              [0, 3, 3, 0, 3, 3, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 3, 3, 0, 3, 3, 0],
                              [0, 3, 0, 0, 0, 3, 0]]}],
        'test': [{'input': [[4, 4, 0, 0, 0, 4, 4],
                            [0, 4, 0, 0, 0, 0, 4],
                            [0, 4, 0, 0, 0, 0, 4],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 4, 0, 0, 0, 0, 0],
                            [4, 4, 0, 0, 0, 0, 0]],
                  'output': [[4, 4, 0, 0, 0, 4, 4],
                             [0, 4, 0, 0, 0, 0, 4],
                             [0, 4, 0, 0, 0, 0, 4],
                             [0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 4, 0],
                             [0, 4, 0, 0, 0, 4, 0],
                             [4, 4, 0, 0, 0, 4, 4]]}]},
 'H7': {'id': 'H7',
        'title': 'Normalized shape intersection',
        'difficulty': 'hard',
        'tests': 'Shape normalization and set intersection.',
        'written_solution': 'Take the two objects, normalize each one to its own top-left corner, and compute the '
                            'overlap of those normalized shapes. Output the overlapping cells as color 8 in a tightly '
                            'cropped grid.',
        'staged_hint': 'Normalize each object separately before comparing cells; do not compare them in their original '
                       'positions.',
        'program_function': 'solve_H7',
        'train': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 2, 2, 2, 0, 0, 0, 0, 0],
                             [0, 0, 2, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 3, 3, 0, 0],
                             [0, 0, 0, 0, 0, 3, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[8, 8]]},
                  {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 4, 4, 0, 0, 0, 0, 0, 0, 0],
                             [0, 4, 4, 4, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 5, 5, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                   'output': [[8, 8], [0, 8]]}],
        'test': [{'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  'output': [[8, 8], [0, 8]]}]}}