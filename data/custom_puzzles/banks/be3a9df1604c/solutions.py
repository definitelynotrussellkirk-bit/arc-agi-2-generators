"""Reference helper library and 21 reference solve functions for the ninth custom ARC puzzle bank.

New primitive introduced in this set:
  frontier_layers(grid, seeds, passable=None, blockers=None, connectivity=4)
Return BFS distance layers expanding from one or more seed cells through passable cells, either by passable colors or by an explicit set of allowed coordinates.
"""
from typing import List, Dict, Tuple
from collections import deque

Grid = List[List[int]]
dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def copyg(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w

def components(grid, colors=None, connectivity=4, include_zero=False, ignore=None):
    if ignore is None:
        ignore=set()
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    dirs = dirs4 if connectivity==4 else dirs4+[(-1,-1),(-1,1),(1,-1),(1,1)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or (r,c) in ignore:
                continue
            seen[r][c]=True
            v=grid[r][c]
            if v==0 and not include_zero:
                continue
            if colors is not None and v not in colors:
                continue
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and (nr,nc) not in ignore and grid[nr][nc]==v:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            out.append({'color':v,'cells':sorted(cells)})
    return out

def bbox(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def norm_cells(cells):
    r1,c1,r2,c2=bbox(cells)
    return sorted((r-r1,c-c1) for r,c in cells)

def rotate_norm(cells, k=1):
    pts=norm_cells(cells)
    for _ in range(k%4):
        maxr=max(r for r,c in pts)
        pts=[(c, maxr-r) for r,c in pts]
        rmin=min(r for r,c in pts)
        cmin=min(c for r,c in pts)
        pts=[(r-rmin,c-cmin) for r,c in pts]
    return sorted(pts)

def mirror_h_norm(cells):
    pts=norm_cells(cells)
    maxc=max(c for r,c in pts)
    return sorted((r,maxc-c) for r,c in pts)

def mirror_v_norm(cells):
    pts=norm_cells(cells)
    maxr=max(r for r,c in pts)
    return sorted((maxr-r,c) for r,c in pts)

def frontier_layers(grid, seeds, passable=None, blockers=None, connectivity=4):
    """
    Expand from seed cells in BFS layers.
    `passable` may be:
      - None: cells with color 0 are passable
      - a set of colors
      - a set of coordinate tuples (r,c)
    Seeds are always included regardless of passable.
    Returns {'layers': {dist:[cells]}, 'dist': {(r,c):dist}}.
    """
    if blockers is None:
        blockers=set()
    else:
        blockers=set(blockers)

    passable_coords=None
    passable_colors=None
    if passable is None:
        passable_colors={0}
    else:
        items=list(passable)
        if items and isinstance(items[0], tuple):
            passable_coords=set(passable)
        else:
            passable_colors=set(passable)

    dirs = dirs4 if connectivity==4 else dirs4+[(-1,-1),(-1,1),(1,-1),(1,1)]
    q=deque()
    dist={}
    for r,c in seeds:
        dist[(r,c)] = 0
        q.append((r,c))
    while q:
        r,c=q.popleft()
        d=dist[(r,c)]
        for dr,dc in dirs:
            nr,nc=r+dr,c+dc
            if not inb(grid,nr,nc):
                continue
            if (nr,nc) in dist or (nr,nc) in blockers:
                continue
            allowed=False
            if passable_coords is not None:
                allowed=(nr,nc) in passable_coords
            else:
                allowed=grid[nr][nc] in passable_colors
            if not allowed:
                continue
            dist[(nr,nc)] = d+1
            q.append((nr,nc))
    layers={}
    for cell,d in dist.items():
        layers.setdefault(d,[]).append(cell)
    for d in layers:
        layers[d]=sorted(layers[d])
    return {'layers': layers, 'dist': dist}

def solve_S9_E1(grid):
    out=copyg(grid)
    seeds=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    for seed in seeds:
        layers=frontier_layers(grid, [seed], passable={0}, connectivity=4)['layers']
        for r,c in layers.get(1, []):
            if out[r][c]==0:
                out[r][c]=8
    return out

def solve_S9_E2(grid):
    by={}
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v!=0:
                by.setdefault(v, []).append((r,c))
    color, cells = next((color,cells) for color,cells in by.items() if len(cells)==2)
    r1,c1,r2,c2=bbox(cells)
    out=blank(len(grid), len(grid[0]), 0)
    for r in range(r1, r2+1):
        for c in range(c1, c2+1):
            out[r][c]=color
    return out

def solve_S9_E3(grid):
    h,w=dims(grid)
    out=copyg(grid)
    for r in range(h):
        c=0
        while c<w:
            if grid[r][c]==0:
                c+=1
                continue
            v=grid[r][c]
            c0=c
            while c+1<w and grid[r][c+1]==v:
                c+=1
            c1=c
            out[r][c0]=1
            out[r][c1]=1
            c+=1
    return out

def solve_S9_E4(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for comp in components(grid):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=comp['color']
    return out

def solve_S9_E5(grid):
    h,w=dims(grid)
    divider = next(c for c in range(w) if all(grid[r][c]==5 for r in range(h)))
    out=copyg(grid)
    for r in range(h):
        for c in range(divider):
            v=grid[r][c]
            if v not in (0,5):
                mc = 2*divider - c
                if 0<=mc<w:
                    out[r][mc]=v
    return out

def solve_S9_E6(grid):
    h,w=dims(grid)
    pts=[v for row in grid for v in row if v!=0]
    color=pts[0]
    n=len(pts)
    out=blank(h,w,0)
    for c in range(min(n,w)):
        out[h-1][c]=color
    return out

def solve_S9_E7(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        by={}
        for c,v in enumerate(grid[r]):
            if v!=0:
                by.setdefault(v, []).append(c)
        for color, cols in by.items():
            if len(cols)==2:
                a,b=min(cols), max(cols)
                for c in range(a,b+1):
                    out[r][c]=color
    return out

def solve_S9_M1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    p2=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    p3=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3][0]
    d2=frontier_layers(grid, [p2], passable={0,2,3})['dist']
    d3=frontier_layers(grid, [p3], passable={0,2,3})['dist']
    for r in range(h):
        for c in range(w):
            if (r,c)==p2:
                out[r][c]=2
            elif (r,c)==p3:
                out[r][c]=3
            else:
                a=d2.get((r,c))
                b=d3.get((r,c))
                if a is None or b is None or a==b:
                    out[r][c]=0
                elif a<b:
                    out[r][c]=2
                else:
                    out[r][c]=3
    return out

def solve_S9_M2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                out[r][c]=9
    seed=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    out[seed[0]][seed[1]]=2
    dist=frontier_layers(grid, [seed], passable={0,2}, blockers={})['dist']
    for (r,c),d in dist.items():
        if (r,c)==seed or grid[r][c]==9:
            continue
        if d%2==1:
            out[r][c]=8
    return out

def solve_S9_M3(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comp=components(grid, colors={2})[0]['cells']
    s=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3][0]
    t=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==4][0]
    dr,dc=t[0]-s[0], t[1]-s[1]
    out[t[0]][t[1]]=4
    for r,c in comp:
        nr,nc=r+dr,c+dc
        if inb(out,nr,nc):
            out[nr][nc]=8
    return out

def solve_S9_M4(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comps=components(grid)
    comps=sorted(comps, key=lambda comp: len(comp['cells']))
    rank_colors=[2,3,4]
    for comp,newc in zip(comps, rank_colors):
        for r,c in comp['cells']:
            out[r][c]=newc
    return out

def solve_S9_M5(grid):
    h,w=dims(grid)
    target=sum(1 for v in grid[0] if v==1)
    out=blank(h,w,0)
    for comp in components(grid):
        if comp['color']==1:
            continue
        if any(r==0 for r,c in comp['cells']):
            continue
        if len(comp['cells'])==target:
            for r,c in comp['cells']:
                out[r][c]=8
            break
    return out

def solve_S9_M6(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for comp in components(grid):
        r1,c1,r2,c2=bbox(comp['cells'])
        for cell in [(r1,c1),(r1,c2),(r2,c1),(r2,c2)]:
            out[cell[0]][cell[1]]=8
    return out

def solve_S9_M7(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    by={}
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v!=0:
                by.setdefault(v, []).append((r,c))
    for color,cells in by.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            a,b=sorted([c1,c2])
            for c in range(a,b+1):
                out[r1][c]=color
        elif c1==c2:
            a,b=sorted([r1,r2])
            for r in range(a,b+1):
                out[r][c1]=color
    return out

def solve_S9_H1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    allowed={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==7 or v in (2,3)}
    s2=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    s3=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3][0]
    d2=frontier_layers(grid, [s2], passable=allowed)['dist']
    d3=frontier_layers(grid, [s3], passable=allowed)['dist']
    for r,c in allowed:
        if (r,c)==s2:
            out[r][c]=2
        elif (r,c)==s3:
            out[r][c]=3
        else:
            a=d2.get((r,c))
            b=d3.get((r,c))
            if a==b:
                out[r][c]=8
            elif a<b:
                out[r][c]=2
            else:
                out[r][c]=3
    return out

def solve_S9_H2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    legend={(0,0):0,(0,1):1,(1,1):2,(1,0):3}
    pos=next((r,c) for r in range(2) for c in range(2) if grid[r][c]==1)
    k=legend[pos]
    shape=components(grid, colors={2})[0]['cells']
    pts=rotate_norm(shape, k)
    anchor=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==4][0]
    for dr,dc in pts:
        nr,nc=anchor[0]+dr, anchor[1]+dc
        if inb(out,nr,nc):
            out[nr][nc]=8
    return out

def solve_S9_H3(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comps=components(grid)
    sigs={}
    for idx,comp in enumerate(comps):
        sig=tuple(norm_cells(comp['cells']))
        sigs.setdefault(sig, []).append(idx)
    keep_idx=next(indices[0] for sig,indices in sigs.items() if len(indices)==1)
    for r,c in comps[keep_idx]['cells']:
        out[r][c]=8
    return out

def solve_S9_H4(grid):
    h,w=dims(grid)
    area_target=sum(1 for v in grid[0] if v==1)
    width_target=sum(1 for r in range(h) if grid[r][0]==3)
    out=blank(h,w,0)
    for comp in components(grid):
        if comp['color'] in (1,3):
            continue
        if any(r==0 or c==0 for r,c in comp['cells']):
            continue
        r1,c1,r2,c2=bbox(comp['cells'])
        area=len(comp['cells'])
        width=c2-c1+1
        if area==area_target and width==width_target:
            for r,c in comp['cells']:
                out[r][c]=8
            break
    return out

def solve_S9_H5(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    frame=components(grid, colors={4})[0]['cells']
    for r,c in frame:
        out[r][c]=4
    template=components(grid, colors={2})[0]['cells']
    t0=norm_cells(template)
    t1=mirror_h_norm(template)
    t2=mirror_v_norm(template)
    t3=rotate_norm(template, 2)
    fh1,fw1,fh2,fw2=bbox(frame)
    inner_r1, inner_c1 = fh1+1, fw1+1
    inner_r2, inner_c2 = fh2-1, fw2-1

    def place(pts, top, left):
        for dr,dc in pts:
            out[top+dr][left+dc]=8

    h0=max(r for r,c in t0)+1; w0=max(c for r,c in t0)+1
    h1=max(r for r,c in t1)+1; w1=max(c for r,c in t1)+1
    h2=max(r for r,c in t2)+1; w2=max(c for r,c in t2)+1
    h3=max(r for r,c in t3)+1; w3=max(c for r,c in t3)+1

    place(t0, inner_r1, inner_c1)
    place(t1, inner_r1, inner_c2-w1+1)
    place(t2, inner_r2-h2+1, inner_c1)
    place(t3, inner_r2-h3+1, inner_c2-w3+1)
    return out

def solve_S9_H6(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    allowed={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==7 or v in (2,3)}
    s2=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    s3=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3][0]
    d2=frontier_layers(grid, [s2], passable=allowed)['dist']
    d3=frontier_layers(grid, [s3], passable=allowed)['dist']
    for r,c in allowed:
        if (r,c)==s2:
            out[r][c]=2
        elif (r,c)==s3:
            out[r][c]=3
        else:
            a=d2.get((r,c))
            b=d3.get((r,c))
            if a==b:
                out[r][c]=8
            elif a<b and a%2==1:
                out[r][c]=2
            elif b<a and b%2==1:
                out[r][c]=3
    return out

def solve_S9_H7(grid):
    h,w=dims(grid)
    divs=[c for c in range(w) if all(grid[r][c]==5 for r in range(h))]
    assert len(divs)==2
    d1,d2=divs
    panels=[
        [row[:d1] for row in grid],
        [row[d1+1:d2] for row in grid],
        [row[d2+1:] for row in grid],
    ]
    ph,pw=dims(panels[0])
    out=blank(ph,pw,0)
    for r in range(ph):
        for c in range(pw):
            occ=sum(1 for p in panels if p[r][c]!=0)
            if occ>=2:
                out[r][c]=8
    return out

