
"""Reference solvers for ARC-style additional puzzle bank volume 18.

This volume keeps the 4-train-pairs format and emphasizes midpoint marking,
rectangle completion, object cropping, border-touch detection, divider mirrors,
span filling, vector translation, chamber fills, count abstractions,
band selection in nested frames, shortest-path cores, maze equidistance,
beam tracing, dihedral odd-one-out detection, and transform+translation stamping.

Helper ideas emphasized here:
- segment_midpoint
- missing_rectangle_corner
- translate_by_marker_vector
- chamber_fill_from_seed
- mandatory_shortest_path_cells
- equidistant_maze_cells
- frame_band_by_depth
- beam_trace
- canonical_under_dihedral
- transform_and_stamp
"""
from __future__ import annotations
from typing import List, Tuple, Iterable, Dict, Set
from collections import deque, Counter

Grid = List[List[int]]
Cell = Tuple[int, int]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = DIR4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

def blank(h:int,w:int,v:int=0)->Grid:
    return [[v for _ in range(w)] for _ in range(h)]

def clone(g:Grid)->Grid:
    return [row[:] for row in g]

def dims(g:Grid):
    return len(g), len(g[0])

def inb(g:Grid, r:int, c:int)->bool:
    h,w=dims(g)
    return 0<=r<h and 0<=c<w

def paint(g:Grid, cells:Iterable[Cell], color:int):
    for r,c in cells:
        if inb(g,r,c):
            g[r][c]=color

def find_cells(g:Grid, color:int)->List[Cell]:
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]

def bbox(cells:Iterable[Cell]):
    cells=list(cells)
    rs=[r for r,_ in cells]
    cs=[c for _,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g:Grid, box)->Grid:
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def normalize(cells:Iterable[Cell])->List[Cell]:
    cells=list(cells)
    if not cells:
        return []
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def crop_cells(cells:Iterable[Cell], color:int=8)->Grid:
    cells=list(cells)
    if not cells:
        return [[0]]
    norm=normalize(cells)
    rmax=max(r for r,_ in norm)
    cmax=max(c for _,c in norm)
    g=blank(rmax+1,cmax+1,0)
    paint(g,norm,color)
    return g

def components(g:Grid, color:int, dirs=DIR4)->List[List[Cell]]:
    h,w=dims(g)
    seen=set()
    out=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=color or (r,c) in seen:
                continue
            comp=[]
            q=[(r,c)]
            seen.add((r,c))
            while q:
                cr,cc=q.pop()
                comp.append((cr,cc))
                for dr,dc in dirs:
                    nr,nc=cr+dr,cc+dc
                    if inb(g,nr,nc) and g[nr][nc]==color and (nr,nc) not in seen:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            out.append(sorted(comp))
    return out

def all_components(g:Grid)->List[Tuple[int,List[Cell]]]:
    seen=set()
    out=[]
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            col=g[r][c]
            if col==0 or (r,c) in seen:
                continue
            comp=[]
            q=[(r,c)]
            seen.add((r,c))
            while q:
                cr,cc=q.pop()
                comp.append((cr,cc))
                for dr,dc in DIR4:
                    nr,nc=cr+dr,cc+dc
                    if inb(g,nr,nc) and g[nr][nc]==col and (nr,nc) not in seen:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            out.append((col,sorted(comp)))
    return out

def translate(cells:Iterable[Cell], dr:int, dc:int)->List[Cell]:
    return sorted((r+dr,c+dc) for r,c in cells)

def hcat(grids:List[Grid], sep:int=1)->Grid:
    if not grids:
        return [[0]]
    maxh=max(len(g) for g in grids)
    totalw=sum(len(g[0]) for g in grids)+sep*(len(grids)-1)
    out=blank(maxh,totalw,0)
    off=0
    for i,g in enumerate(grids):
        for r,row in enumerate(g):
            for c,v in enumerate(row):
                out[r][off+c]=v
        off += len(g[0]) + (sep if i+1<len(grids) else 0)
    return out

def rot90(cells:Iterable[Cell])->List[Cell]:
    norm=normalize(cells)
    if not norm:
        return []
    rmax=max(r for r,_ in norm)
    return normalize((c, rmax-r) for r,c in norm)

def rot180(cells:Iterable[Cell])->List[Cell]:
    return rot90(rot90(cells))

def rot270(cells:Iterable[Cell])->List[Cell]:
    return rot90(rot180(cells))

def flip_h(cells:Iterable[Cell])->List[Cell]:
    norm=normalize(cells)
    if not norm:
        return []
    rmax=max(r for r,_ in norm)
    return normalize((rmax-r,c) for r,c in norm)

def flip_v(cells:Iterable[Cell])->List[Cell]:
    norm=normalize(cells)
    if not norm:
        return []
    cmax=max(c for _,c in norm)
    return normalize((r,cmax-c) for r,c in norm)

def apply_rot(cells:Iterable[Cell], code:int)->List[Cell]:
    code%=4
    if code==0:
        return normalize(cells)
    if code==1:
        return rot90(cells)
    if code==2:
        return rot180(cells)
    return rot270(cells)

def dihedral_variants(cells:Iterable[Cell])->List[List[Cell]]:
    n=normalize(cells)
    vars=[normalize(n), rot90(n), rot180(n), rot270(n)]
    f=flip_v(n)
    vars += [normalize(f), rot90(f), rot180(f), rot270(f)]
    # dedupe
    seen=[]
    out=[]
    for v in vars:
        t=tuple(v)
        if t not in seen:
            seen.append(t)
            out.append(v)
    return out

def canonical(cells:Iterable[Cell])->List[Cell]:
    vars=dihedral_variants(cells)
    return list(min(tuple(v) for v in vars))

def flood_region(g:Grid, starts:Iterable[Cell], passable:Set[int])->Set[Cell]:
    q=deque(starts)
    seen=set(starts)
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc) and (nr,nc) not in seen and g[nr][nc] in passable:
                seen.add((nr,nc))
                q.append((nr,nc))
    return seen

def dist_map(g:Grid, starts:Iterable[Cell], passable:Set[int])->List[List[int]]:
    h,w=dims(g)
    INF=10**9
    dist=[[INF]*w for _ in range(h)]
    q=deque()
    for r,c in starts:
        dist[r][c]=0
        q.append((r,c))
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc) and g[nr][nc] in passable and dist[nr][nc]==INF:
                dist[nr][nc]=dist[r][c]+1
                q.append((nr,nc))
    return dist

def shortest_path_counts(g:Grid, start:Cell, passable:Set[int], dist)->Dict[Cell,int]:
    h,w=dims(g)
    cells=[(dist[r][c],r,c) for r in range(h) for c in range(w) if dist[r][c] < 10**9]
    cells.sort()
    cnt={start:1}
    for _,r,c in cells:
        if (r,c)==start:
            continue
        total=0
        for dr,dc in DIR4:
            pr,pc=r-dr,c-dc
            if inb(g,pr,pc) and g[pr][pc] in passable and dist[pr][pc]+1==dist[r][c]:
                total += cnt.get((pr,pc),0)
        cnt[(r,c)] = total
    return cnt

def full_line_color(g:Grid, color:int):
    h,w=dims(g)
    for r in range(h):
        if all(g[r][c]==color for c in range(w)):
            return ('h', r)
    for c in range(w):
        if all(g[r][c]==color for r in range(h)):
            return ('v', c)
    return None

def rectangle_fill_cells(box):
    r0,c0,r1,c1=box
    return [(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1)]

def rectangle_interior_cells(box):
    r0,c0,r1,c1=box
    return [(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)]

def is_hollow_rect(comp:List[Cell])->bool:
    r0,c0,r1,c1=bbox(comp)
    rect=set()
    for r in range(r0,r1+1):
        rect.add((r,c0)); rect.add((r,c1))
    for c in range(c0,c1+1):
        rect.add((r0,c)); rect.add((r1,c))
    return set(comp)==rect and r1-r0>=2 and c1-c0>=2

def beam_trace(g:Grid)->List[Cell]:
    h,w=dims(g)
    src=find_cells(g,2)
    if len(src)!=1:
        return []
    r,c=src[0]
    if r==0: dr,dc=1,0
    elif r==h-1: dr,dc=-1,0
    elif c==0: dr,dc=0,1
    elif c==w-1: dr,dc=0,-1
    else:
        # fallback: use adjacent 1 marker
        dirs={(r-1,c):(-1,0),(r+1,c):(1,0),(r,c-1):(0,-1),(r,c+1):(0,1)}
        dr,dc=0,1
        for (nr,nc),vec in dirs.items():
            if inb(g,nr,nc) and g[nr][nc]==1:
                dr,dc=vec
                break
    out=[]
    cr,cc=r,c
    while True:
        nr,nc=cr+dr,cc+dc
        if not inb(g,nr,nc) or g[nr][nc]==5:
            break
        cr,cc=nr,nc
        out.append((cr,cc))
        cell=g[cr][cc]
        if cell==6:  # backslash
            dr,dc=dc,dr
        elif cell==7:  # slash
            dr,dc=-dc,-dr
    return out

# Easy solvers

def solve_E120(grid:Grid)->Grid:
    g=clone(grid)
    for comp in components(grid,1,DIR4):
        rs={r for r,_ in comp}; cs={c for _,c in comp}
        if len(comp)>=3 and len(comp)%2==1 and (len(rs)==1 or len(cs)==1):
            if len(rs)==1:
                r=next(iter(rs))
                cells=sorted(comp, key=lambda x:x[1])
            else:
                c=next(iter(cs))
                cells=sorted(comp, key=lambda x:x[0])
            mr,mc=cells[len(cells)//2]
            g[mr][mc]=2
    return g

def solve_E121(grid:Grid)->Grid:
    g=clone(grid)
    reds=find_cells(grid,2)
    rows=sorted(set(r for r,_ in reds))
    cols=sorted(set(c for _,c in reds))
    if len(reds)==3 and len(rows)==2 and len(cols)==2:
        allcorn={(rows[0],cols[0]),(rows[0],cols[1]),(rows[1],cols[0]),(rows[1],cols[1])}
        missing=list(allcorn-set(reds))[0]
        g[missing[0]][missing[1]]=8
    return g

def solve_E122(grid:Grid)->Grid:
    comps=all_components(grid)
    col,comp=min(comps, key=lambda x:(len(x[1]), x[0], bbox(x[1])))
    return crop_bbox(grid, bbox(comp))

def solve_E123(grid:Grid)->Grid:
    g=clone(grid)
    h,w=dims(g)
    for comp in components(grid,3,DIR4):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in comp):
            for r,c in comp:
                g[r][c]=4
    return g

def solve_E124(grid:Grid)->Grid:
    g=clone(grid)
    line=full_line_color(grid,7)
    if line is None:
        return g
    orient,k=line
    for r,c in find_cells(grid,6):
        if orient=='v':
            mc=2*k-c
            if inb(g,r,mc):
                g[r][mc]=8
        else:
            mr=2*k-r
            if inb(g,mr,c):
                g[mr][c]=8
    return g

def solve_E125(grid:Grid)->Grid:
    g=clone(grid)
    colors=sorted({v for row in grid for v in row if v!=0})
    for color in colors:
        cells=find_cells(grid,color)
        if len(cells)==2:
            (r1,c1),(r2,c2)=sorted(cells)
            if r1==r2:
                for c in range(min(c1,c2), max(c1,c2)+1):
                    g[r1][c]=color
            elif c1==c2:
                for r in range(min(r1,r2), max(r1,r2)+1):
                    g[r][c1]=color
    return g

def solve_E126(grid:Grid)->Grid:
    g=clone(grid)
    blue=find_cells(grid,1)
    if not blue:
        return g
    r0,c0,r1,c1=bbox(blue)
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            g[r][c]=8
    return g

# Medium solvers

def solve_M120(grid:Grid)->Grid:
    h,w=dims(grid)
    out=clone(grid)
    src=components(grid,2,DIR4)[0]
    for r,c in src:
        out[r][c]=0
    b=find_cells(grid,1)[0]
    g=find_cells(grid,3)[0]
    dr,dc=g[0]-b[0], g[1]-b[1]
    paint(out, translate(src,dr,dc), 8)
    return out

def solve_M121(grid:Grid)->Grid:
    h,w=dims(grid)
    ctrl=find_cells(grid,1)[0]
    if ctrl==(0,0):
        code=0
    elif ctrl==(0,w-1):
        code=1
    elif ctrl==(h-1,w-1):
        code=2
    else:
        code=3
    shape=components(grid,2,DIR4)[0]
    transformed=apply_rot(shape, code)
    return crop_cells(transformed, 8)

def solve_M122(grid:Grid)->Grid:
    g=clone(grid)
    seed=find_cells(grid,2)[0]
    region=flood_region(grid,[seed],{0,2})
    for r,c in region:
        if g[r][c]==0:
            g[r][c]=8
    return g

def solve_M123(grid:Grid)->Grid:
    counts=[]
    for color in [2,3,4]:
        counts.append(len(components(grid,color,DIR4)))
    row=[2]*counts[0]+[0]+[3]*counts[1]+[0]+[4]*counts[2]
    return [row]

def solve_M124(grid:Grid)->Grid:
    g=clone(grid)
    frames=components(grid,4,DIR4)
    markers=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v not in (0,4)]
    chosen=None
    fill=None
    for comp in frames:
        r0,c0,r1,c1=bbox(comp)
        for r,c,v in markers:
            if ((r==r0-1 and c0<=c<=c1) or (r==r1+1 and c0<=c<=c1) or
                (c==c0-1 and r0<=r<=r1) or (c==c1+1 and r0<=r<=r1)):
                chosen=(r0,c0,r1,c1)
                fill=v
                break
        if chosen:
            break
    if chosen:
        for r,c in rectangle_interior_cells(chosen):
            if g[r][c]==0:
                g[r][c]=fill
    return g

def solve_M125(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    row_spans=[]
    col_spans=[]
    # red row spans
    reds=find_cells(grid,2)
    by_row={}
    for r,c in reds:
        by_row.setdefault(r,[]).append(c)
    for r,cs in by_row.items():
        if len(cs)>=2:
            row_spans.append((r,min(cs),max(cs)))
    blues=find_cells(grid,3)
    by_col={}
    for r,c in blues:
        by_col.setdefault(c,[]).append(r)
    for c,rs in by_col.items():
        if len(rs)>=2:
            col_spans.append((c,min(rs),max(rs)))
    for r,c0,c1 in row_spans:
        for c, r0, r1 in col_spans:
            if c0<=c<=c1 and r0<=r<=r1:
                out[r][c]=8
    return out

def solve_M126(grid:Grid)->Grid:
    objs=[]
    for color,comp in all_components(grid):
        box=bbox(comp)
        crop=blank(box[2]-box[0]+1, box[3]-box[1]+1, 0)
        for r,c in comp:
            crop[r-box[0]][c-box[1]]=color
        objs.append((len(comp), color, crop))
    objs.sort(key=lambda x:(x[0], x[1]))
    return hcat([crop for _,_,crop in objs], sep=1)

# Hard solvers

def solve_H120(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    s=find_cells(grid,2)[0]
    t=find_cells(grid,3)[0]
    passable={0,2,3}
    ds=dist_map(grid,[s],passable)
    dt=dist_map(grid,[t],passable)
    D=ds[t[0]][t[1]]
    cnts=shortest_path_counts(grid,s,passable,ds)
    cntt=shortest_path_counts(grid,t,passable,dt)
    total=cnts.get(t,0)
    for r in range(h):
        for c in range(w):
            if grid[r][c] in passable and ds[r][c]+dt[r][c]==D:
                if cnts.get((r,c),0) * cntt.get((r,c),0) == total:
                    out[r][c]=8
    return out

def solve_H121(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    a=find_cells(grid,2)[0]
    b=find_cells(grid,3)[0]
    passable={0,2,3}
    da=dist_map(grid,[a],passable)
    db=dist_map(grid,[b],passable)
    INF=10**9
    for r in range(h):
        for c in range(w):
            if grid[r][c] in passable and da[r][c]<INF and db[r][c]<INF and da[r][c]==db[r][c]:
                out[r][c]=8
    return out

def solve_H122(grid:Grid)->Grid:
    h,w=dims(grid)
    ctrl=find_cells(grid,1)[0]
    if ctrl==(0,0): code=0
    elif ctrl==(0,w-1): code=1
    elif ctrl==(h-1,w-1): code=2
    else: code=3
    a=normalize(components(grid,2,DIR4)[0])
    b=apply_rot(components(grid,3,DIR4)[0], code)
    aset=set(a); bset=set(b)
    xor=sorted(aset ^ bset)
    return crop_cells(xor, 8)

def solve_H123(grid:Grid)->Grid:
    g=clone(grid)
    frames=[bbox(comp) for comp in components(grid,4,DIR4) if is_hollow_rect(comp)]
    frames=sorted(frames, key=lambda box: ((box[2]-box[0])*(box[3]-box[1])), reverse=True)
    k=len(find_cells(grid,1))
    if not frames:
        return g
    if k<1:
        return g
    if k < len(frames):
        outer=frames[k-1]
        inner=frames[k]
        outer_in=set(rectangle_interior_cells(outer))
        inner_all=set(rectangle_fill_cells(inner))
        band=[cell for cell in outer_in if cell not in inner_all and g[cell[0]][cell[1]]==0]
    else:
        inner=frames[-1]
        band=[cell for cell in rectangle_interior_cells(inner) if g[cell[0]][cell[1]]==0]
    paint(g, band, 8)
    return g

def solve_H124(grid:Grid)->Grid:
    h,w=dims(grid)
    out=blank(h,w,0)
    paint(out, beam_trace(grid), 8)
    return out

def solve_H125(grid:Grid)->Grid:
    comps=components(grid,2,DIR4)
    sigs=[tuple(canonical(comp)) for comp in comps]
    freq=Counter(sigs)
    odd_idx=[i for i,s in enumerate(sigs) if freq[s]==1][0]
    return crop_cells(canonical(comps[odd_idx]), 8)

def solve_H126(grid:Grid)->Grid:
    h,w=dims(grid)
    ctrl=find_cells(grid,1)[0]
    if ctrl==(0,0): code=0
    elif ctrl==(0,w-1): code=1
    elif ctrl==(h-1,w-1): code=2
    else: code=3
    vec_a=find_cells(grid,3)[0]
    vec_b=find_cells(grid,6)[0]
    dr,dc=vec_b[0]-vec_a[0], vec_b[1]-vec_a[1]
    shape=components(grid,2,DIR4)[0]
    r0,c0,r1,c1=bbox(shape)
    transformed=apply_rot(shape, code)
    target=translate(transformed, r0+dr, c0+dc)
    out=blank(h,w,0)
    paint(out, target, 8)
    return out

SOLVERS = {
    'E120': solve_E120,
    'E121': solve_E121,
    'E122': solve_E122,
    'E123': solve_E123,
    'E124': solve_E124,
    'E125': solve_E125,
    'E126': solve_E126,
    'M120': solve_M120,
    'M121': solve_M121,
    'M122': solve_M122,
    'M123': solve_M123,
    'M124': solve_M124,
    'M125': solve_M125,
    'M126': solve_M126,
    'H120': solve_H120,
    'H121': solve_H121,
    'H122': solve_H122,
    'H123': solve_H123,
    'H124': solve_H124,
    'H125': solve_H125,
    'H126': solve_H126,
}
