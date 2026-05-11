
from __future__ import annotations

import collections
import inspect
import json
from pathlib import Path

DIR4=[(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def size(g):
    return len(g), len(g[0]) if g else 0

def strings_from_grid(g):
    return ["".join(str(c) for c in row) for row in g]

def grid_from_strings(rows):
    return [[int(ch) for ch in row] for row in rows]

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, cells=None, pad=0):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    r0=max(0,r0-pad); c0=max(0,c0-pad); r1=min(len(g)-1,r1+pad); c1=min(len(g[0])-1,c1+pad)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g):
    return crop_bbox(g)

def fill_rect(g,r0,c0,r1,c1,color):
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            g[r][c]=color

def draw_rect_border(g,r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color

def orth_neighbors(r,c,h,w):
    for dr,dc in DIR4:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            yield nr,nc

def components_nonzero(g, treat_colors_separately=False, exclude=None):
    h,w=size(g)
    ex=set(exclude or [])
    vis=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in ex or vis[r][c] or g[r][c]==0:
                continue
            color=g[r][c]
            vis[r][c]=True
            stack=[(r,c)]
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for nr,nc in orth_neighbors(rr,cc,h,w):
                    if (nr,nc) not in ex and not vis[nr][nc] and g[nr][nc]!=0 and (not treat_colors_separately or g[nr][nc]==color):
                        vis[nr][nc]=True
                        stack.append((nr,nc))
            comps.append((color,cells))
    return comps

def rotate_cw(g):
    h,w=size(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_times(g, k):
    k%=4
    out=g
    for _ in range(k):
        out=rotate_cw(out)
    return out

def flip_h(g):
    return g[::-1]

def flip_v(g):
    return [row[::-1] for row in g]

def is_rect_border(cells):
    r0,c0,r1,c1=bbox(cells)
    if r1-r0 < 2 or c1-c0 < 2:
        return False
    expected=set()
    for c in range(c0,c1+1):
        expected.add((r0,c)); expected.add((r1,c))
    for r in range(r0,r1+1):
        expected.add((r,c0)); expected.add((r,c1))
    return set(cells)==expected

def is_solid_rect_component(cells):
    r0,c0,r1,c1=bbox(cells)
    return len(cells)==(r1-r0+1)*(c1-c0+1)

def grid_from_component(g, cells, recolor=None):
    r0,c0,r1,c1=bbox(cells)
    out=blank(r1-r0+1, c1-c0+1)
    for r,c in cells:
        out[r-r0][c-c0]=g[r][c] if recolor is None else recolor
    return out

def center_in_frame(frame_grid, obj_grid):
    out=clone(frame_grid)
    nz=[(r,c) for r,row in enumerate(out) for c,v in enumerate(row) if v!=0]
    r0,c0,r1,c1=bbox(nz)
    oh,ow=size(obj_grid)
    sr=r0+1+((r1-r0-1)-oh)//2
    sc=c0+1+((c1-c0-1)-ow)//2
    for r,row in enumerate(obj_grid):
        for c,v in enumerate(row):
            if v!=0:
                out[sr+r][sc+c]=v
    return out

def trace_hv(p1, p2):
    (r1,c1),(r2,c2)=p1,p2
    pts=[(r1,c1)]
    step = 1 if c2>=c1 else -1
    for c in range(c1+step, c2+step, step):
        pts.append((r1,c))
    step = 1 if r2>=r1 else -1
    for r in range(r1+step, r2+step, step):
        pts.append((r,c2))
    return pts

def row_overlap(a,b):
    return not (a[2] < b[0] or b[2] < a[0])

def col_overlap(a,b):
    return not (a[3] < b[1] or b[3] < a[1])

# New primitive for this set

def reflect_across_guide(base_grid, cells, axis, guide_pos, keep_original=True, overlap_color=None):
    """
    Reflect a set of colored cells across a horizontal or vertical guide line.

    axis: 'h' for a horizontal guide row, 'v' for a vertical guide column
    guide_pos: row index (axis='h') or column index (axis='v')
    overlap_color: optional recolor for reflected cells landing on an already
                   occupied non-guide cell
    """
    h,w=size(base_grid)
    out=clone(base_grid)
    if not keep_original:
        for r,c,_ in cells:
            if 0<=r<h and 0<=c<w:
                out[r][c]=0
    for r,c,v in cells:
        if axis=='v':
            nr,nc=r,2*guide_pos-c
        else:
            nr,nc=2*guide_pos-r,c
        if 0<=nr<h and 0<=nc<w:
            if overlap_color is not None and out[nr][nc] not in (0,v):
                out[nr][nc]=overlap_color
            else:
                out[nr][nc]=v
    return out

def find_full_guides(g, color):
    h,w=size(g)
    rows=[r for r in range(h) if all(g[r][c]==color for c in range(w))]
    cols=[c for c in range(w) if all(g[r][c]==color for r in range(h))]
    return rows, cols

def transform_by_code(g, code):
    if code==1:
        return g
    if code==2:
        return rotate_times(g,1)
    if code==3:
        return rotate_times(g,2)
    if code==4:
        return rotate_times(g,3)
    raise ValueError(code)

def transform_h53(g, code):
    if code==1:
        return g
    if code==2:
        return rotate_times(g,1)
    if code==3:
        return flip_h(g)
    if code==4:
        return flip_v(g)
    raise ValueError(code)


# === Rules ===

def rule_e50(g):
    rows, cols = find_full_guides(g, 5)
    out = clone(g)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5)]
    if cols:
        out = reflect_across_guide(out, cells, 'v', cols[0], keep_original=True)
    elif rows:
        out = reflect_across_guide(out, cells, 'h', rows[0], keep_original=True)
    return out

def rule_e51(g):
    out=clone(g)
    by=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,pts in by.items():
        if len(pts)!=2:
            continue
        (r1,c1),(r2,c2)=pts
        if r1==r2:
            a,b=sorted([c1,c2])
            for c in range(a,b+1):
                out[r1][c]=color
        elif c1==c2:
            a,b=sorted([r1,r2])
            for r in range(a,b+1):
                out[r][c1]=color
    return out

def rule_e52(g):
    h,w=size(g)
    out=blank(h,w)
    for r in range(h):
        color=g[r][0]
        if color!=0:
            for c in range(w):
                out[r][c]=color
    return out

def rule_e53(g):
    h,w=size(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        vals=[v for v in row if v!=0]
        for c,v in enumerate(vals):
            out[r][c]=v
    return out

def rule_e54(g):
    h,w=size(g)
    out=blank(h,w)
    by=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,pts in by.items():
        if len(pts)!=2:
            continue
        (r1,c1),(r2,c2)=pts
        rr=sorted([r1,r2]); cc=sorted([c1,c2])
        fill_rect(out, rr[0], cc[0], rr[1], cc[1], color)
    return out

def rule_e55(g):
    return crop_nonzero(g)

def rule_e56(g):
    counts=collections.Counter(v for row in g for v in row if v!=0)
    row=[]
    for color in sorted(counts):
        row.extend([color]*counts[color])
    return [row] if row else [[0]]

def rule_m50(g):
    target=g[0][0]
    rows, cols = find_full_guides(g, 5)
    out=clone(g)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v==target and (r,c)!=(0,0)]
    if cols:
        out=reflect_across_guide(out, cells, 'v', cols[0], keep_original=True)
    elif rows:
        out=reflect_across_guide(out, cells, 'h', rows[0], keep_original=True)
    return out

def rule_m51(g):
    h,w=size(g)
    frame=None
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_rect_border(cells):
            frame=(color,cells)
            break
    if frame is None:
        return g
    fcolor,cells=frame
    r0,c0,r1,c1=bbox(cells)
    out=blank(h,w)
    draw_rect_border(out,r0,c0,r1,c1,fcolor)
    for c in range(c0+1,c1):
        vals=[g[r][c] for r in range(r0+1,r1) if g[r][c]!=0]
        for i,v in enumerate(vals):
            out[r0+1+i][c]=v
    return out

def rule_m52(g):
    motif=crop_nonzero(g)
    mh,mw=size(motif)
    h,w=size(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            out[r][c]=motif[r%mh][c%mw]
    return out

def rule_m53(g):
    cmd=g[0][0]
    gg=clone(g)
    gg[0][0]=0
    obj=crop_nonzero(gg)
    return transform_by_code(obj, cmd)

def rule_m54(g):
    rows=[r for r in range(1,len(g)) if g[r][0]==8]
    cols=[c for c in range(1,len(g[0])) if g[0][c]==8]
    out=[]
    for r in rows:
        out.append([g[r][c] for c in cols])
    return out if out else [[0]]

def rule_m55(g):
    comps=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        crop=grid_from_component(g,cells)
        h,w=size(crop)
        comps.append((len(cells), color, crop, h, w))
    comps.sort(key=lambda t:(t[0], t[1]))
    H=max(h for _,_,_,h,_ in comps)
    W=sum(w for *_,w in comps)+max(0,len(comps)-1)
    out=blank(H,W)
    c0=0
    for _,_,crop,h,w in comps:
        for r in range(h):
            for c in range(w):
                if crop[r][c]!=0:
                    out[r][c0+c]=crop[r][c]
        c0+=w+1
    return out

def rule_m56(g):
    comps=components_nonzero(g, treat_colors_separately=True)
    rect=None
    shape=None
    for color,cells in comps:
        if is_solid_rect_component(cells):
            rect=(color,cells)
        else:
            shape=(color,cells)
    if rect is None or shape is None:
        return [[0]]
    target_color=rect[0]
    _,cells=shape
    out=grid_from_component(g,cells,recolor=target_color)
    return out

def rule_h50(g):
    h,w=size(g)
    hr=None
    vc=None
    for r in range(h):
        vals=g[r]
        if all(v in (5,6) for v in vals) and vals.count(6)>=w-1:
            hr=r
            break
    for c in range(w):
        vals=[g[r][c] for r in range(h)]
        if all(v in (5,6) for v in vals) and vals.count(5)>=h-1:
            vc=c
            break
    out=clone(g)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v not in (0,5,6)]
    out=reflect_across_guide(out, cells, 'v', vc, keep_original=True)
    cells2=[(r,c,v) for r,row in enumerate(out) for c,v in enumerate(row) if v not in (0,5,6)]
    out=reflect_across_guide(out, cells2, 'h', hr, keep_original=True)
    return out

def rule_h51(g):
    rects=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        rects.append((color,cells,bbox(cells)))
    rects.sort(key=lambda t:(t[2][0], t[2][1]))
    n=len(rects)
    out=blank(n,n)
    for i,(_,_,b1) in enumerate(rects):
        for j,(_,_,b2) in enumerate(rects):
            ro=row_overlap(b1,b2)
            co=col_overlap(b1,b2)
            out[i][j]=3 if ro and co else 1 if ro else 2 if co else 0
    return out

def rule_h52(g):
    out=clone(g)
    frames=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_rect_border(cells):
            r0,c0,r1,c1=bbox(cells)
            frames.append(((r1-r0+1)*(c1-c0+1), color, (r0,c0,r1,c1)))
    frames.sort()  # innermost first via smallest bbox area
    h,w=size(g)
    for r in range(h):
        for c in range(w):
            if out[r][c]!=0:
                continue
            for _,color,(r0,c0,r1,c1) in frames:
                if r0 < r < r1 and c0 < c < c1:
                    out[r][c]=color
                    break
    return out

def rule_h53(g):
    rank_cmd=g[0][0]
    tf_cmd=g[0][-1]
    frame=None
    for color,cells in components_nonzero(g, treat_colors_separately=True, exclude={(0,0),(0,len(g[0])-1)}):
        if is_rect_border(cells):
            frame=(color,cells)
            break
    candidates=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True, exclude={(0,0),(0,len(g[0])-1)}):
        if frame and set(cells)==set(frame[1]):
            continue
        candidates.append((len(cells), color, cells))
    candidates.sort(key=lambda t:(t[0], t[1]))
    idx=min(rank_cmd-1, len(candidates)-1)
    chosen=candidates[idx][2]
    obj=grid_from_component(g, chosen)
    obj=transform_h53(obj, tf_cmd)
    frame_grid=grid_from_component(g, frame[1])
    return center_in_frame(frame_grid, obj)

def rule_h54(g):
    motif=crop_nonzero(g)
    n=len(motif)
    rot=rotate_times(motif,1)
    h,w=size(g)
    out=blank(h,w)
    for tr in range(0,h,n):
        for tc in range(0,w,n):
            tile = motif if ((tr//n + tc//n)%2==0) else rot
            for r in range(n):
                for c in range(n):
                    out[tr+r][tc+c]=tile[r][c]
    return out

def rule_h55(g):
    out=clone(g)
    frames=[]
    for color,cells in components_nonzero(g, treat_colors_separately=True):
        if is_rect_border(cells):
            frames.append((color,cells,bbox(cells)))
    for fcolor,cells,(r0,c0,r1,c1) in frames:
        inside=collections.defaultdict(list)
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                v=g[r][c]
                if v!=0 and v!=fcolor:
                    inside[v].append((r,c))
        for color,pts in inside.items():
            if len(pts)==2:
                for rr,cc in trace_hv(pts[0], pts[1]):
                    out[rr][cc]=color
    return out

def rule_h56(g):
    cmd=g[0][0]
    rows=[r for r in range(1,len(g)) if g[r][0]==8]
    cols=[c for c in range(1,len(g[0])) if g[0][c]==8]
    sub=[[g[r][c] for c in cols] for r in rows]
    if not sub:
        sub=[[0]]
    return transform_by_code(sub, cmd)

# === Puzzle definitions ===

def make_puzzle(pid, title, difficulty, skills, staged_hint, written_solution, uses_new_primitive, rule_fn, train_inputs, test_input):
    return {
        'id': pid,
        'title': title,
        'difficulty': difficulty,
        'skills': skills,
        'staged_hint': staged_hint,
        'written_solution': written_solution,
        'uses_new_primitive': uses_new_primitive,
        'program_name': rule_fn.__name__,
        'program_source': inspect.getsource(rule_fn).rstrip(),
        'train': [{'input': strings_from_grid(inp), 'output': strings_from_grid(rule_fn(inp))} for inp in train_inputs],
        'test': {'input': strings_from_grid(test_input), 'output': strings_from_grid(rule_fn(test_input))},
    }

PUZZLES=[]

PUZZLES.append(make_puzzle(
    'E50', 'Guide Mirror Copy', 'easy',
    ['reflection', 'guide line', 'same-color symmetry'],
    'Find the full guide line first. Then mirror each nonzero cell to the opposite side at the same distance.',
    'Locate the full 5-colored guide line. Keep every original nonzero cell, and add its mirror image across that guide.',
    True, rule_e50,
    [
        grid_from_strings([
                '000050000',
                '020050000',
                '003050000',
                '000050000',
                '000050000',
                '700050000',
                '000050000',
                '000050000',
            ]),
        grid_from_strings([
                '0400050000',
                '0000050000',
                '0000050000',
                '0060050000',
                '0000050000',
                '0000050000',
                '0008050000',
            ]),
        grid_from_strings([
                '00000050000',
                '00000050000',
                '09000050000',
                '00000050000',
                '00020050000',
                '00000050000',
                '00000050000',
                '50000050000',
                '00000050000',
            ]),
        grid_from_strings([
                '00050000',
                '40050000',
                '00050000',
                '00050000',
                '07050000',
                '00050000',
                '00250000',
                '00050000',
            ]),
    ],
    grid_from_strings([
            '0000050000',
            '0300050000',
            '0000050000',
            '0080050000',
            '0000050000',
            '0000050000',
            '4000050000',
            '0000050000',
            '0000050000',
        ])
))

PUZZLES.append(make_puzzle(
    'E51', 'Straight Segment Completion', 'easy',
    ['endpoint pairing', 'row/column completion', 'line filling'],
    'Ignore colors with only one cell. Pair identical endpoints, then fill the straight gap if they share a row or a column.',
    'For each color, find its two endpoints. If they are aligned horizontally or vertically, fill every cell between them with that color.',
    False, rule_e51,
    [
        grid_from_strings([
                '000000000',
                '020002000',
                '000000000',
                '000000040',
                '000000000',
                '000000000',
                '000000040',
                '000000000',
            ]),
        grid_from_strings([
                '0030000030',
                '0000000000',
                '0000060000',
                '0000000000',
                '0000000000',
                '0000060000',
                '0700700000',
            ]),
        grid_from_strings([
                '000000000',
                '000000000',
                '800000800',
                '000000000',
                '000050000',
                '000000000',
                '000000000',
                '000050000',
                '000000000',
            ]),
        grid_from_strings([
                '00000000',
                '00000090',
                '00000000',
                '00000000',
                '00000000',
                '00000090',
                '02000200',
                '00000000',
            ]),
    ],
    grid_from_strings([
            '0400000400',
            '0000000000',
            '0000000060',
            '0000000000',
            '0000000000',
            '0000000000',
            '0030030000',
            '0000000060',
            '0000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'E52', 'Left Header Row Flood', 'easy',
    ['row guide', 'constant fill', 'same-size transform'],
    'Treat the first column as instructions. Each nonzero header controls its entire row.',
    'Whenever the first cell of a row is nonzero, flood that whole row with the same color. Leave rows with a zero header empty.',
    False, rule_e52,
    [
        grid_from_strings([
                '00000000',
                '20000000',
                '00000000',
                '00000000',
                '50000000',
                '00000000',
                '00000000',
            ]),
        grid_from_strings([
                '6000000',
                '0000000',
                '0000000',
                '4000000',
                '0000000',
                '0000000',
                '9000000',
                '0000000',
            ]),
        grid_from_strings([
                '000000000',
                '000000000',
                '300000000',
                '000000000',
                '000000000',
                '700000000',
            ]),
        grid_from_strings([
                '000000',
                '800000',
                '000000',
                '000000',
                '000000',
                '000000',
                '000000',
                '200000',
                '000000',
            ]),
    ],
    grid_from_strings([
            '40000000',
            '00000000',
            '00000000',
            '70000000',
            '00000000',
            '00000000',
            '20000000',
            '00000000',
        ])
))

PUZZLES.append(make_puzzle(
    'E53', 'Row Pack Left', 'easy',
    ['compression', 'order preservation', 'row-wise transform'],
    'Work one row at a time. Keep the order of the colored cells, but remove the zeros between them.',
    'For each row, read the nonzero cells from left to right and rewrite them flush against the left edge, padding the rest with zeros.',
    False, rule_e53,
    [
        grid_from_strings([
                '000000000',
                '040002000',
                '000000000',
                '001080060',
                '000000000',
                '000000003',
                '000000000',
            ]),
        grid_from_strings([
                '00200090',
                '00000000',
                '00040005',
                '00000000',
                '00000700',
                '00000000',
            ]),
        grid_from_strings([
                '0000000000',
                '0600600003',
                '0000000000',
                '0000000000',
                '0000000000',
                '8000000020',
                '0000001000',
                '0000000000',
            ]),
        grid_from_strings([
                '0000000',
                '0000000',
                '0090040',
                '0000000',
                '0500005',
                '0000000',
                '0000000',
            ]),
    ],
    grid_from_strings([
            '000300020',
            '000000000',
            '010000008',
            '000000000',
            '000000000',
            '700000400',
            '000000000',
            '000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'E54', 'Diagonal-Corner Rectangle Fill', 'easy',
    ['rectangle inference', 'corner pairing', 'solid fill'],
    'The colored cells are not separate objects; they are opposite corners of hidden rectangles.',
    'Group cells by color. Each color gives two diagonal corners of a rectangle. Fill the whole rectangle with that color.',
    False, rule_e54,
    [
        grid_from_strings([
                '000000000',
                '020000000',
                '000000000',
                '000020000',
                '000000500',
                '000000000',
                '000000005',
                '000000000',
            ]),
        grid_from_strings([
                '3000000000',
                '0000000000',
                '0030000000',
                '0000000000',
                '0000000000',
                '0000700000',
                '0000000000',
                '0000000000',
                '0000000700',
            ]),
        grid_from_strings([
                '00000000',
                '00000900',
                '04000000',
                '00000000',
                '00000009',
                '00040000',
                '00000000',
            ]),
        grid_from_strings([
                '00060000',
                '00000000',
                '00000000',
                '00000060',
                '80000000',
                '00000000',
                '00000000',
                '00800000',
            ]),
    ],
    grid_from_strings([
            '000000000',
            '020000000',
            '000000000',
            '000000000',
            '000002000',
            '000000700',
            '000000000',
            '000000000',
            '000000007',
        ])
))

PUZZLES.append(make_puzzle(
    'E55', 'Tight Bounding Crop', 'easy',
    ['cropping', 'bounding box', 'shape isolation'],
    'Do not change the pattern. Just isolate it as tightly as possible.',
    'Find the minimal bounding box that contains all nonzero cells and return that crop unchanged.',
    False, rule_e55,
    [
        grid_from_strings([
                '0000000000',
                '0000000000',
                '0000220000',
                '0000022000',
                '0000002000',
                '0000000000',
                '0000000000',
                '0000000000',
            ]),
        grid_from_strings([
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '030300000',
                '003300000',
                '000300000',
                '000000000',
                '000000000',
            ]),
        grid_from_strings([
                '00000000000',
                '00000044000',
                '00000044400',
                '00000004000',
                '00000000000',
                '00000000000',
                '00000000000',
            ]),
        grid_from_strings([
                '0000000000',
                '0000000000',
                '0000000000',
                '0000000000',
                '0000000000',
                '0022000000',
                '0002200000',
                '0000200000',
                '0000000000',
                '0000000000',
            ]),
    ],
    grid_from_strings([
            '000000000000',
            '000000000000',
            '000000030300',
            '000000003300',
            '000000000300',
            '000000000000',
            '000000000000',
            '000000000000',
            '000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'E56', 'Singleton Multiset Strip', 'easy',
    ['counting', 'sorting by color', 'dynamic output'],
    'Ignore the positions of the dots. Only their colors and counts matter.',
    'Count how many times each nonzero color appears. Output a single row where colors are listed in ascending order, repeated by their counts.',
    False, rule_e56,
    [
        grid_from_strings([
                '00000000',
                '02000000',
                '00000200',
                '00000000',
                '00004000',
                '00000000',
                '70000000',
            ]),
        grid_from_strings([
                '000300000',
                '000000000',
                '000000000',
                '000000050',
                '000000000',
                '050000000',
                '000000800',
                '000000000',
            ]),
        grid_from_strings([
                '0000090000',
                '0000000001',
                '0040000000',
                '0000004000',
                '0000000000',
                '4000000000',
            ]),
        grid_from_strings([
                '0000000',
                '0000000',
                '0600000',
                '0000000',
                '0000060',
                '0000000',
                '0002000',
                '0000000',
                '0000000',
            ]),
    ],
    grid_from_strings([
            '00000000',
            '03000000',
            '00000030',
            '00001000',
            '00000000',
            '00700000',
            '00000000',
            '00000007',
        ])
))

PUZZLES.append(make_puzzle(
    'M50', 'Mirror Target Color Across Guide', 'medium',
    ['selector cell', 'reflection', 'guide line'],
    'The guide line matters, but only one color reacts to it. Use the top-left selector before reflecting.',
    'Read the target color from the top-left cell. Keep the whole grid, and reflect only cells of that color across the 5-colored guide line.',
    True, rule_m50,
    [
        grid_from_strings([
                '2000050000',
                '0200050070',
                '0020050000',
                '0200050000',
                '0000050000',
                '0000050400',
                '0000050000',
                '0000050000',
            ]),
        grid_from_strings([
                '600000000',
                '006000000',
                '006600000',
                '000000000',
                '555555555',
                '000000000',
                '050000000',
                '000000300',
                '000000000',
            ]),
        grid_from_strings([
                '40000050000',
                '00000050000',
                '04000050080',
                '04000050000',
                '00400050000',
                '00000050300',
                '00000050000',
                '00000050000',
            ]),
        grid_from_strings([
                '7000000000',
                '0000700000',
                '0000770000',
                '0000000000',
                '0000000000',
                '0000000000',
                '5555555555',
                '0600000000',
                '0000000020',
                '0000000000',
            ]),
    ],
    grid_from_strings([
            '30000005000',
            '00000005060',
            '03000005000',
            '00300005000',
            '03000005000',
            '00000005000',
            '00000005000',
            '00000005400',
            '00000005000',
        ])
))

PUZZLES.append(make_puzzle(
    'M51', 'Column Packing Inside Frame', 'medium',
    ['frame reasoning', 'column-wise packing', 'order preservation'],
    'Solve the frame first, then handle each interior column independently.',
    'Keep the rectangular frame. Inside it, compress each column upward so the nonzero cells stack from the top of the interior while preserving top-to-bottom order.',
    False, rule_m51,
    [
        grid_from_strings([
                '0000000000',
                '0888888880',
                '0820000080',
                '0800600080',
                '0800000080',
                '0840100080',
                '0830007080',
                '0888888880',
                '0000000000',
            ]),
        grid_from_strings([
                '000000000',
                '008888880',
                '008500080',
                '008009080',
                '008500380',
                '008200080',
                '008888880',
                '000000000',
            ]),
        grid_from_strings([
                '0000000000',
                '0000000000',
                '0888888880',
                '0890007080',
                '0800000080',
                '0800200080',
                '0800200080',
                '0840000080',
                '0888888880',
                '0000000000',
            ]),
        grid_from_strings([
                '00000000000',
                '08888888880',
                '08060002080',
                '08000000080',
                '08000400080',
                '08010000080',
                '08070005080',
                '08888888880',
                '00000000000',
            ]),
    ],
    grid_from_strings([
            '0000000000',
            '0088888800',
            '0087000800',
            '0080009800',
            '0080010800',
            '0080000800',
            '0084000800',
            '0080010800',
            '0088888800',
            '0000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'M52', 'Periodic Tile Fill', 'medium',
    ['motif extraction', 'tiling', 'periodicity'],
    'First crop the seed motif in the corner. Then repeat it over the whole canvas.',
    'Crop the nonzero motif in the corner and tile that exact pattern periodically across the entire output grid.',
    False, rule_m52,
    [
        grid_from_strings([
                '120000000',
                '012000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
            ]),
        grid_from_strings([
                '330000000',
                '303000000',
                '033000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
            ]),
        grid_from_strings([
                '4500000000',
                '0450000000',
                '0000000000',
                '0000000000',
                '0000000000',
                '0000000000',
                '0000000000',
                '0000000000',
            ]),
        grid_from_strings([
                '120000000000',
                '012000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
            ]),
    ],
    grid_from_strings([
            '330000000000',
            '303000000000',
            '033000000000',
            '000000000000',
            '000000000000',
            '000000000000',
            '000000000000',
            '000000000000',
            '000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'M53', 'Command Rotate Crop', 'medium',
    ['command decoding', 'rotation', 'cropping'],
    'Separate the command cell from the object. The command tells you how to rotate the cropped object.',
    'Ignore the command cell at the top-left, crop the remaining nonzero object, and rotate it according to the command: 1=id, 2=90° clockwise, 3=180°, 4=270° clockwise.',
    False, rule_m53,
    [
        grid_from_strings([
                '2000000000',
                '0000000000',
                '0000000000',
                '0000220000',
                '0000022000',
                '0000002000',
                '0000000000',
                '0000000000',
            ]),
        grid_from_strings([
                '300000000',
                '000000000',
                '000000000',
                '000000000',
                '030300000',
                '003300000',
                '000300000',
                '000000000',
                '000000000',
            ]),
        grid_from_strings([
                '40000000000',
                '00000000000',
                '00000044000',
                '00000044400',
                '00000004000',
                '00000000000',
                '00000000000',
                '00000000000',
            ]),
        grid_from_strings([
                '1000000000',
                '0000000000',
                '0000000000',
                '0000000000',
                '0000000000',
                '0000000000',
                '0000303000',
                '0000033000',
                '0000003000',
                '0000000000',
            ]),
    ],
    grid_from_strings([
            '200000000000',
            '000000000000',
            '000000000000',
            '000000000000',
            '000000044000',
            '000000044400',
            '000000004000',
            '000000000000',
            '000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'M54', 'Masked Submatrix Extraction', 'medium',
    ['row/column selection', 'matrix slicing', 'dynamic output'],
    'The top row selects columns and the left column selects rows. The answer is the intersection.',
    'Take the interior matrix. Keep only the rows marked by 8 in the first column and only the columns marked by 8 in the top row, preserving order.',
    False, rule_m54,
    [
        grid_from_strings([
                '00808',
                '81234',
                '05678',
                '89123',
                '04567',
            ]),
        grid_from_strings([
                '08080',
                '02468',
                '81357',
                '08642',
                '87531',
                '81111',
            ]),
        grid_from_strings([
                '008808',
                '812345',
                '867891',
                '023456',
                '878912',
            ]),
        grid_from_strings([
                '08808',
                '09876',
                '05432',
                '81098',
                '07654',
            ]),
    ],
    grid_from_strings([
            '080808',
            '832145',
            '065432',
            '878987',
            '811223',
        ])
))

PUZZLES.append(make_puzzle(
    'M55', 'Area-Sorted Rectangle Strip', 'medium',
    ['component sorting', 'cropping', 'layout'],
    'Split the rectangles first. Then sort them by area before laying them out.',
    'Extract the disconnected solid rectangles, crop each one tightly, sort them by area ascending, and place the crops left to right with one zero column between them.',
    False, rule_m55,
    [
        grid_from_strings([
                '00000000000000',
                '03300000000000',
                '03300000007700',
                '00000000007700',
                '00000555507700',
                '00000555507700',
                '00000555500000',
                '00000000000000',
                '00000000000000',
                '00000000000000',
            ]),
        grid_from_strings([
                '0000000000000',
                '0222000000000',
                '0222000004400',
                '0222000004400',
                '0000000004400',
                '0066666004400',
                '0000000004400',
                '0000000000000',
                '0000000000000',
            ]),
        grid_from_strings([
                '000000000000000',
                '000000000005550',
                '088000000000000',
                '088000000000000',
                '088000000000000',
                '000000000000000',
                '000033333000000',
                '000033333000000',
                '000033333000000',
                '000000000000000',
                '000000000000000',
            ]),
        grid_from_strings([
                '00000000000000',
                '00999900000000',
                '00000000000000',
                '00000000440000',
                '00000000440000',
                '07770000440000',
                '07770000440000',
                '07770000000000',
                '00000000000000',
            ]),
    ],
    grid_from_strings([
            '000000000000000',
            '000000006600000',
            '022200006600000',
            '022200006600000',
            '022200006600000',
            '000000006600000',
            '000000000004444',
            '000000000004444',
            '000000000000000',
            '000000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'M56', 'Colorized Template Transfer', 'medium',
    ['template extraction', 'recoloring', 'component classification'],
    'Decide which object is the color source and which object is the template mask.',
    'One component is a solid rectangle that supplies the target color; the other is the template shape. Crop the template and recolor every nonzero cell with the rectangle’s color.',
    False, rule_m56,
    [
        grid_from_strings([
                '00000000000',
                '00000000000',
                '02200000000',
                '00220000000',
                '00200007700',
                '00000007700',
                '00000000000',
                '00000000000',
                '00000000000',
            ]),
        grid_from_strings([
                '000000000000',
                '000000004440',
                '000000004440',
                '000000000000',
                '000000000000',
                '003300000000',
                '003330000000',
                '000030000000',
                '000000000000',
                '000000000000',
            ]),
        grid_from_strings([
                '0000000000000',
                '0000000000000',
                '0440400000000',
                '0004400000000',
                '0000400000000',
                '0000000006600',
                '0000000006600',
                '0000000006600',
                '0000000000000',
            ]),
        grid_from_strings([
                '000000000000',
                '000000000000',
                '000000033000',
                '000000033000',
                '000000033000',
                '000000000000',
                '022000000000',
                '002200000000',
                '002000000000',
                '000000000000',
                '000000000000',
            ]),
    ],
    grid_from_strings([
            '0000000000000',
            '0000000000000',
            '0000000000000',
            '0033000000000',
            '0033300000000',
            '0000300000000',
            '0000000008880',
            '0000000008880',
            '0000000000000',
            '0000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'H50', 'Quadrant Mirror From Dual Guides', 'hard',
    ['dual-axis symmetry', 'guide detection', 'composed reflection'],
    'Find both guides before moving anything. Then use the same object to generate all reflected copies.',
    'Detect the full vertical 5-guide and the full horizontal 6-guide. Keep the original object and reflect it across the vertical guide, the horizontal guide, and both guides so it appears in all symmetric quadrants.',
    True, rule_h50,
    [
        grid_from_strings([
                '0000005000000',
                '0120005000000',
                '0102005000000',
                '0222005000000',
                '0000005000000',
                '6666665666666',
                '0000005000000',
                '0000005000000',
                '0000005000000',
                '0000005000000',
                '0000005000000',
            ]),
        grid_from_strings([
                '000000050000',
                '000000053400',
                '000000050340',
                '000000050440',
                '666666656666',
                '000000050000',
                '000000050000',
                '000000050000',
                '000000050000',
                '000000050000',
            ]),
        grid_from_strings([
                '00000500000000',
                '00000500000000',
                '00000500000000',
                '00000500000000',
                '00000500000000',
                '00000500000000',
                '66666566666666',
                '07800500000000',
                '07080500000000',
                '08880500000000',
                '00000500000000',
                '00000500000000',
            ]),
        grid_from_strings([
                '00000500000',
                '00000500000',
                '00000500000',
                '00000500000',
                '00000500000',
                '66666566666',
                '00000500000',
                '00000503400',
                '00000500340',
                '00000500440',
                '00000500000',
            ]),
    ],
    grid_from_strings([
            '000000500000',
            '000000501200',
            '000000501020',
            '000000502220',
            '000000500000',
            '000000500000',
            '666666566666',
            '000000500000',
            '000000500000',
            '000000500000',
            '000000500000',
            '000000500000',
        ])
))

PUZZLES.append(make_puzzle(
    'H51', 'Bounding-Box Projection Matrix', 'hard',
    ['relational reasoning', 'component analysis', 'dynamic matrix'],
    'Do not compare pixels directly. Compare the row ranges and column ranges of the rectangles.',
    'Extract the solid rectangles in reading order. Build an n×n matrix where each entry is 3 if the two rectangles’ bounding boxes overlap in both rows and columns, 1 if only row ranges overlap, 2 if only column ranges overlap, and 0 if neither overlaps.',
    False, rule_h51,
    [
        grid_from_strings([
                '00000000000000',
                '02220000000000',
                '02220005500000',
                '02220005500000',
                '00000005500000',
                '00000000000000',
                '00000000000000',
                '00777700000000',
                '00777700000000',
                '00777700000000',
                '00000000000000',
                '00000000000000',
            ]),
        grid_from_strings([
                '0000000000000',
                '0033330004440',
                '0033330004440',
                '0000000004440',
                '0000000000000',
                '0660000888800',
                '0660000888800',
                '0660000888800',
                '0000000888800',
                '0000000000000',
                '0000000000000',
            ]),
        grid_from_strings([
                '099000000000',
                '099000000000',
                '099000000000',
                '000002222000',
                '000002222000',
                '000002222000',
                '777700000000',
                '777700000000',
                '777700000000',
                '000000000000',
            ]),
        grid_from_strings([
                '000000000000000',
                '055550000000000',
                '055550006660000',
                '055550006660000',
                '055550006660000',
                '000000006660000',
                '000000000000000',
                '000333300000000',
                '000333300004440',
                '000333300004440',
                '000000000004440',
                '000000000004440',
                '000000000000000',
            ]),
    ],
    grid_from_strings([
            '0000000000000',
            '0880002222000',
            '0880002222000',
            '0880002222000',
            '0000002222000',
            '0000000000000',
            '0077770000000',
            '0077770044400',
            '0077770044400',
            '0000000044400',
            '0000000044400',
            '0000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'H52', 'Nested Frame Ownership Fill', 'hard',
    ['nesting', 'containment', 'region ownership'],
    'Think region by region, not frame by frame. Every empty cell belongs to the smallest frame that still contains it.',
    'Keep every rectangular border. Fill each zero cell with the color of the innermost border that contains it.',
    False, rule_h52,
    [
        grid_from_strings([
                '00000000000',
                '02222222220',
                '02000000020',
                '02044444020',
                '02040004020',
                '02040004020',
                '02040004020',
                '02044444020',
                '02000000020',
                '02222222220',
                '00000000000',
            ]),
        grid_from_strings([
                '000000000000',
                '033333333330',
                '030000000030',
                '030666666030',
                '030600006030',
                '030609906030',
                '030609906030',
                '030600006030',
                '030666666030',
                '030000000030',
                '033333333330',
                '000000000000',
            ]),
        grid_from_strings([
                '0000000000000',
                '0055555555500',
                '0050000000500',
                '0050777770500',
                '0050700070500',
                '0050700070500',
                '0050777770500',
                '0050000000500',
                '0055555555500',
                '0000000000000',
            ]),
        grid_from_strings([
                '0000000000000',
                '0888888888880',
                '0800000000080',
                '0800000000080',
                '0800222220080',
                '0800200020080',
                '0800200020080',
                '0800200020080',
                '0800222220080',
                '0800000000080',
                '0800000000080',
                '0888888888880',
                '0000000000000',
            ]),
    ],
    grid_from_strings([
            '00000000000000',
            '04444444444440',
            '04000000000040',
            '04077777777040',
            '04070000007040',
            '04070222207040',
            '04070222207040',
            '04070000007040',
            '04077777777040',
            '04000000000040',
            '04444444444440',
            '00000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'H53', 'Rank-Selected Transform In Frame', 'hard',
    ['ranking by area', 'command transform', 'centering'],
    'There are three candidate shapes, one rank command, one transform command, and one destination frame.',
    'Ignore the two command cells. Rank the non-frame components by area, choose the requested rank, transform it by the second command (1=id, 2=90° clockwise, 3=flip vertically across a horizontal axis, 4=flip horizontally across a vertical axis), and center the result inside the empty frame.',
    False, rule_h53,
    [
        grid_from_strings([
                '1000000000000002',
                '0000000000000000',
                '0022000000000000',
                '0020000000888888',
                '0000000000800008',
                '0330000000800008',
                '0333000000800008',
                '0000440000800008',
                '0000444400800008',
                '0000000000800008',
                '0000000000888888',
                '0000000000000000',
            ]),
        grid_from_strings([
                '20000000000000003',
                '00000000000000000',
                '00440000000000000',
                '00444400000000000',
                '00000000000888888',
                '00000000000800008',
                '02200000000800008',
                '02000000000800008',
                '00003300000800008',
                '00003330000800008',
                '00000000000800008',
                '00000000000888888',
                '00000000000000000',
            ]),
        grid_from_strings([
                '300000000000004',
                '000000000000000',
                '000000000888888',
                '000000000800008',
                '033000000800008',
                '033300000800008',
                '000044000800008',
                '000044440800008',
                '002200000800008',
                '002000000888888',
                '000000000000000',
                '000000000000000',
            ]),
        grid_from_strings([
                '200000000000001',
                '002200000000000',
                '002000000000000',
                '000000000888888',
                '000000000800008',
                '044000000800008',
                '044440000800008',
                '000033000800008',
                '000033300800008',
                '000000000888888',
                '000000000000000',
            ]),
    ],
    grid_from_strings([
            '3000000000000002',
            '0000000000000000',
            '0330000000000000',
            '0333000000888888',
            '0000000000800008',
            '0000000000800008',
            '0022000000800008',
            '0020440000800008',
            '0000444400800008',
            '0000000000800008',
            '0000000000888888',
            '0000000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'H54', 'Alternating Rotated Tiling', 'hard',
    ['periodic structure', 'rotation alternation', 'checkerboard logic'],
    'Extract the motif once, then tile by blocks rather than by individual cells.',
    'Crop the corner motif, tile it over the whole output, and rotate every odd checkerboard tile 90° clockwise while leaving even tiles unchanged.',
    False, rule_h54,
    [
        grid_from_strings([
                '120000000',
                '012000000',
                '201000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
            ]),
        grid_from_strings([
                '330000000000',
                '303000000000',
                '033000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
            ]),
        grid_from_strings([
                '450000000000',
                '045000000000',
                '504000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
                '000000000000',
            ]),
        grid_from_strings([
                '120000000',
                '012000000',
                '201000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
                '000000000',
            ]),
    ],
    grid_from_strings([
            '330000000000000',
            '303000000000000',
            '033000000000000',
            '000000000000000',
            '000000000000000',
            '000000000000000',
            '000000000000000',
            '000000000000000',
            '000000000000000',
            '000000000000000',
            '000000000000000',
            '000000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'H55', 'Per-Frame Endpoint Routing', 'hard',
    ['independent subproblems', 'containment', 'path tracing'],
    'Treat each frame as its own small puzzle. Connect only the endpoints that live inside the same frame.',
    'For each rectangular frame, find the two same-colored endpoints inside it and draw a horizontal-then-vertical Manhattan path connecting them with that color, keeping the frame intact.',
    False, rule_h55,
    [
        grid_from_strings([
                '00000000000000',
                '08888800000000',
                '08200800000000',
                '08000800000000',
                '08002800000000',
                '08888800000000',
                '00000008888880',
                '00000008600080',
                '00000008000080',
                '00000008000680',
                '00000008888880',
                '00000000000000',
            ]),
        grid_from_strings([
                '0000000000000',
                '0088888000000',
                '0083008000000',
                '0080038000000',
                '0088888000000',
                '0000000088880',
                '0000000087080',
                '0000000080080',
                '0000000080780',
                '0000000088880',
                '0000000000000',
            ]),
        grid_from_strings([
                '000000000000000',
                '000000000000000',
                '088888000000000',
                '080048000000000',
                '080008000000000',
                '084008000000000',
                '088888000000000',
                '000000008888880',
                '000000008900080',
                '000000008000080',
                '000000008000980',
                '000000008888880',
                '000000000000000',
            ]),
        grid_from_strings([
                '000000000000',
                '088880000000',
                '085080000000',
                '080580000000',
                '088880000000',
                '000000000000',
                '000000888880',
                '000000800280',
                '000000800080',
                '000000820080',
                '000000888880',
                '000000000000',
            ]),
    ],
    grid_from_strings([
            '00000000000000',
            '08888880000000',
            '08007080000000',
            '08000080000000',
            '08700080000000',
            '08888880000000',
            '00000000000000',
            '00000008888880',
            '00000008300080',
            '00000008000080',
            '00000008000380',
            '00000008888880',
            '00000000000000',
        ])
))

PUZZLES.append(make_puzzle(
    'H56', 'Masked Submatrix Then Rotate', 'hard',
    ['compositional reasoning', 'matrix slicing', 'command transform'],
    'First extract the marked submatrix exactly as in a selection task. Only then apply the command transform.',
    'Use the first column and top row to select rows and columns from the interior matrix, then rotate the extracted submatrix according to the top-left command: 1=id, 2=90° clockwise, 3=180°, 4=270° clockwise.',
    False, rule_h56,
    [
        grid_from_strings([
                '20808',
                '81234',
                '05678',
                '89123',
                '04567',
            ]),
        grid_from_strings([
                '38080',
                '02468',
                '81357',
                '08642',
                '87531',
                '81111',
            ]),
        grid_from_strings([
                '408808',
                '812345',
                '867891',
                '023456',
                '878912',
            ]),
        grid_from_strings([
                '18808',
                '09876',
                '05432',
                '81098',
                '07654',
            ]),
    ],
    grid_from_strings([
            '380808',
            '832145',
            '065432',
            '878987',
            '811223',
        ])
))

assert len(PUZZLES)==21

PAYLOAD={
    'set': 8,
    'summary': {
        'set': 8,
        'puzzle_count': 21,
        'train_pair_count': sum(len(p['train']) for p in PUZZLES),
        'avg_train_pairs': round(sum(len(p['train']) for p in PUZZLES)/len(PUZZLES), 2),
        'difficulty_counts': {
            'easy': sum(1 for p in PUZZLES if p['difficulty']=='easy'),
            'medium': sum(1 for p in PUZZLES if p['difficulty']=='medium'),
            'hard': sum(1 for p in PUZZLES if p['difficulty']=='hard'),
        },
        'new_primitive': {
            'name': 'reflect_across_guide',
            'purpose': 'Reflect colored cells across a detected horizontal or vertical guide line while optionally keeping the originals.'
        },
    },
    'puzzles': PUZZLES,
}

def validate():
    ns=globals()
    for p in PUZZLES:
        fn=ns[p['program_name']]
        for i,pair in enumerate(p['train'], start=1):
            inp=grid_from_strings(pair['input'])
            got=strings_from_grid(fn(inp))
            if got!=pair['output']:
                raise AssertionError(f"{p['id']} train {i} mismatch\nGOT={got}\nEXP={pair['output']}")
        tinp=grid_from_strings(p['test']['input'])
        got=strings_from_grid(fn(tinp))
        if got!=p['test']['output']:
            raise AssertionError(f"{p['id']} test mismatch\nGOT={got}\nEXP={p['test']['output']}")
    return True

def write_markdown(payload, out_path):
    lines=[]
    lines.append('# ARC Additional Puzzle Bank — 21 Puzzles (Set 8)')
    lines.append('')
    lines.append('This eighth pack continues the numbering with **`E50–E56`**, **`M50–M56`**, and **`H50–H56`**.')
    lines.append('')
    tp=payload['summary']['train_pair_count']
    avg=payload['summary']['avg_train_pairs']
    lines.append(f'This set contains **{tp} train pairs across 21 puzzles**, averaging **{avg:.2f} train pairs per puzzle**.')
    lines.append('')
    lines.append('It introduces a new helper primitive for solver-facing implementations:')
    lines.append('')
    lines.append('```text')
    lines.append("reflect_across_guide(base_grid, cells, axis, guide_pos, keep_original=True, overlap_color=None)")
    lines.append('```')
    lines.append('')
    lines.append('Intuition: reflect a set of colored cells across a horizontal or vertical guide line while optionally keeping the originals. This primitive is used directly in **E50**, **M50**, and **H50**.')
    lines.append('')
    lines.append('Design goals for this set:')
    lines.append('')
    lines.append('- easy: direct reflections, segment filling, row flooding, compression, rectangle inference, cropping, and color counting')
    lines.append('')
    lines.append('- medium: selector-driven mirroring, frame-local packing, motif tiling, command transforms, matrix slicing, component sorting, and template recoloring')
    lines.append('')
    lines.append('- hard: dual-guide symmetry, relational matrices, nested ownership, rank selection with transforms, alternating tile variants, per-frame routing, and compositional extract-then-rotate tasks')
    lines.append('')
    for difficulty in ['easy','medium','hard']:
        group=[p for p in payload['puzzles'] if p['difficulty']==difficulty]
        lines.append(f'## {difficulty.capitalize()} ({len(group)})')
        lines.append('')
        for p in group:
            lines.append(f"### {p['id']} — {p['title']}")
            lines.append('')
            lines.append(f"**Difficulty:** {p['difficulty']}")
            lines.append('')
            lines.append(f"**Train pairs:** {len(p['train'])}")
            lines.append('')
            lines.append(f"**Skills:** {', '.join(p['skills'])}")
            lines.append('')
            lines.append(f"**Suggested staged path:** {p['staged_hint']}")
            lines.append('')
            for i,pair in enumerate(p['train'], start=1):
                lines.append(f"**Train {i} — input**")
                lines.append('')
                lines.append('```text')
                lines.extend(pair['input'])
                lines.append('```')
                lines.append('')
                lines.append(f"**Train {i} — output**")
                lines.append('')
                lines.append('```text')
                lines.extend(pair['output'])
                lines.append('```')
                lines.append('')
            lines.append('**Test — input**')
            lines.append('')
            lines.append('```text')
            lines.extend(p['test']['input'])
            lines.append('```')
            lines.append('')
            lines.append('**Test — output**')
            lines.append('')
            lines.append('```text')
            lines.extend(p['test']['output'])
            lines.append('```')
            lines.append('')
            lines.append('**Written solution**')
            lines.append('')
            lines.append(p['written_solution'])
            lines.append('')
            lines.append('**Reference program**')
            lines.append('')
            lines.append('```python')
            lines.extend(p['program_source'].splitlines())
            lines.append('```')
            lines.append('')
    Path(out_path).write_text("\n".join(lines))

def write_primitive(out_path):
    lines=[]
    lines.append('# New Primitive Spec — `reflect_across_guide`')
    lines.append('')
    lines.append('```python')
    lines.append("reflect_across_guide(base_grid, cells, axis, guide_pos, keep_original=True, overlap_color=None)")
    lines.append('```')
    lines.append('')
    lines.append('Purpose: reflect colored cells across a detected horizontal or vertical guide line. The primitive can preserve the original cells while painting their reflected counterparts, which makes it useful for one-sided mirror tasks and multi-axis symmetry composition.')
    lines.append('')
    lines.append('Arguments:')
    lines.append('')
    lines.append("- `base_grid`: the canvas to paint on")
    lines.append("- `cells`: iterable of `(row, col, color)` triples to reflect")
    lines.append("- `axis`: `'h'` for a horizontal guide row or `'v'` for a vertical guide column")
    lines.append("- `guide_pos`: row index or column index of the guide")
    lines.append("- `keep_original`: whether the source cells remain after reflection")
    lines.append("- `overlap_color`: optional recolor for landing on an occupied non-guide cell")
    lines.append('')
    lines.append('Why it matters: ARC-style tasks often encode symmetry with an explicit divider. Making that divider a first-class primitive is much cleaner than rebuilding reflection arithmetic from scratch inside every rule.')
    lines.append('')
    lines.append('Used in this set: **E50**, **M50**, and **H50**.')
    Path(out_path).write_text("\n".join(lines))

if __name__ == '__main__':
    validate()
    out_base=Path('/mnt/data')
    py_path=out_base/'arc_additional_puzzles_21_set8.py'
    md_path=out_base/'arc_additional_puzzles_21_set8.md'
    json_path=out_base/'arc_additional_puzzles_21_set8.json'
    prim_path=out_base/'arc_additional_puzzles_21_set8_primitive.md'
    py_path.write_text(Path(__file__).read_text())
    write_markdown(PAYLOAD, md_path)
    json_path.write_text(json.dumps(PAYLOAD, indent=2))
    write_primitive(prim_path)
    print('wrote', md_path)
    print('wrote', py_path)
    print('wrote', json_path)
    print('wrote', prim_path)
