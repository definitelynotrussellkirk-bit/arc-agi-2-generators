"""
ARC-style puzzle bank continuation 16: 21 more puzzles (E106-E112, M106-M112, H106-H112).

This batch leans into vertical completion, local object growth, guide-vector copying, border-contact classification, frame transplantation, prototype dispatch, edit-stencil transfer, mask composition, roomwise seed filling, and binary-operation inference.

Notable motifs:
- vector_shadow_copy(object, marker8, marker9): M106
- room_seed_fill(walls, seeds): M112
- prototype_label_dispatch(prototypes, query): H107
- edit_stencil_transfer(example_before, example_after, query): H108
- panel_mask_compose(mask, a, b): H110
- binary_op_infer(exampleA, exampleB, exampleC, queryD, queryE): H112
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import List

Grid = List[List[int]]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]


def dims(grid: Grid):
    return len(grid), len(grid[0])


def clone(grid):
    return [row[:] for row in grid]


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)


def connected_components(gd: Grid, ignore=(0,), same_color=True):
    h,w=dims(gd)
    seen=set()
    out=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in seen or gd[r][c] in ignore:
                continue
            color=gd[r][c]
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and gd[nx][ny] not in ignore and ((not same_color) or gd[nx][ny]==color):
                        seen.add((nx,ny)); q.append((nx,ny))
            out.append((color,cells))
    return out


def rot90(gd: Grid) -> Grid:
    return [list(row) for row in zip(*gd[::-1])]


def rot180(gd): return [row[::-1] for row in gd[::-1]]


def rot270(gd): return [list(row) for row in zip(*gd)][::-1]


def flip_h(gd): return [row[::-1] for row in gd]


def flip_v(gd): return gd[::-1]


def transpose(gd): return [list(row) for row in zip(*gd)]


def anti_transpose(gd):
    h,w=dims(gd)
    out=[[0]*h for _ in range(w)]
    for r in range(h):
        for c in range(w):
            out[w-1-c][h-1-r]=gd[r][c]
    return out


def split_panels_row(grid: Grid, panel_w: int, count: int, sep_color=5):
    panels=[]
    start=0
    for i in range(count):
        panels.append([row[start:start+panel_w] for row in grid])
        start += panel_w
        if i<count-1:
            start += 1
    return panels


def normalize_occ(occ):
    occ=set(occ)
    if not occ:
        return frozenset()
    minr=min(r for r,c in occ); minc=min(c for r,c in occ)
    return frozenset((r-minr,c-minc) for r,c in occ)


def transform_occ(occ, name):
    occ=set(occ)
    if not occ:
        return frozenset()
    maxr=max(r for r,c in occ); maxc=max(c for r,c in occ)
    grid=blank(maxr+1,maxc+1,0)
    for r,c in occ: grid[r][c]=1
    tg=TRANSFORMS[name](grid)
    return normalize_occ({(r,c) for r,row in enumerate(tg) for c,v in enumerate(row) if v})


def all_occ_transforms(occ):
    return {name: transform_occ(occ,name) for name in TRANSFORMS}


def infer_transform(example_in: Grid, example_out: Grid, candidates=None):
    if candidates is None:
        candidates=list(TRANSFORMS)
    matches=[]
    for name in candidates:
        if TRANSFORMS[name](example_in)==example_out:
            matches.append(name)
    if not matches:
        raise ValueError("no transform match")
    return matches[0]


def panel_label_and_occ(panel: Grid):
    label=panel[0][0]
    occ={(r,c) for r,row in enumerate(panel) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0)}
    return label, normalize_occ(occ)


def main_object_bbox(panel: Grid, ignore_colors=(0,8)):
    cells=[(r,c) for r,row in enumerate(panel) for c,v in enumerate(row) if v not in ignore_colors]
    if not cells:
        raise ValueError("no main object")
    return bbox(cells), cells


def geodesic_room_fill(grid):
    h,w=dims(grid)
    out=clone(grid)
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen:
                continue
            # collect room
            q=deque([(r,c)]); seen.add((r,c)); room=[]
            seeds=[]
            while q:
                x,y=q.popleft(); room.append((x,y))
                if grid[x][y] not in (0,5):
                    seeds.append((x,y,grid[x][y]))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            # multi-source bfs distances within room
            room_set=set(room)
            # precompute distances from each seed
            distmaps=[]
            for sx,sy,color in seeds:
                dq=deque([(sx,sy)])
                dist={(sx,sy):0}
                while dq:
                    x,y=dq.popleft()
                    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nx,ny=x+dx,y+dy
                        if (nx,ny) in room_set and (nx,ny) not in dist:
                            dist[(nx,ny)]=dist[(x,y)]+1
                            dq.append((nx,ny))
                distmaps.append((color,dist,(sx,sy)))
            for x,y in room:
                if grid[x][y]==5:
                    continue
                if grid[x][y]!=0:
                    continue
                best=None
                tie=False
                for color,dist,seed in distmaps:
                    d=dist.get((x,y))
                    if d is None:
                        continue
                    if best is None or d<best[0]:
                        best=(d,color)
                        tie=False
                    elif d==best[0] and color!=best[1]:
                        tie=True
                if best is not None and not tie:
                    out[x][y]=best[1]
                else:
                    out[x][y]=0
    return out


def op_union(a,b,color=2):
    n=len(a); m=len(a[0])
    out=blank(n,m)
    for r in range(n):
        for c in range(m):
            if a[r][c]!=0 or b[r][c]!=0:
                out[r][c]=color
    return out


def op_intersection(a,b,color=2):
    n=len(a); m=len(a[0])
    out=blank(n,m)
    for r in range(n):
        for c in range(m):
            if a[r][c]!=0 and b[r][c]!=0:
                out[r][c]=color
    return out


def op_xor(a,b,color=2):
    n=len(a); m=len(a[0])
    out=blank(n,m)
    for r in range(n):
        for c in range(m):
            if (a[r][c]!=0) ^ (b[r][c]!=0):
                out[r][c]=color
    return out


TRANSFORMS = {
    "id": lambda x: [row[:] for row in x],
    "rot90": rot90,
    "rot180": rot180,
    "rot270": rot270,
    "flip_h": flip_h,
    "flip_v": flip_v,
    "transpose": transpose,
    "anti_transpose": anti_transpose,
}

OPS = {"union": op_union, "intersection": op_intersection, "xor": op_xor}

def solve_E106(grid):
    out=clone(grid)
    h,w=dims(grid)
    by=defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2 and cells[0][1]==cells[1][1]:
            c=cells[0][1]
            a,b=sorted([cells[0][0],cells[1][0]])
            if all(grid[r][c]==0 for r in range(a+1,b)):
                for r in range(a,b+1):
                    out[r][c]=color
    return out


def solve_E107(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h-1):
        for c in range(w-1):
            vals=[grid[r][c],grid[r][c+1],grid[r+1][c],grid[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                color=nz[0]
                if grid[r][c]==0: out[r][c]=color
                if grid[r][c+1]==0: out[r][c+1]=color
                if grid[r+1][c]==0: out[r+1][c]=color
                if grid[r+1][c+1]==0: out[r+1][c+1]=color
    return out


def solve_E108(grid):
    out=clone(grid)
    h,w=dims(grid)
    # horizontal
    for r in range(h):
        for c in range(w-2):
            a,b,d=grid[r][c],grid[r][c+1],grid[r][c+2]
            if a!=0 and a==d and b==0:
                out[r][c+1]=a
    # vertical
    for r in range(h-2):
        for c in range(w):
            a,b,d=grid[r][c],grid[r+1][c],grid[r+2][c]
            if a!=0 and a==d and b==0:
                out[r+1][c]=a
    return out


def solve_E109(grid):
    out=blank(*dims(grid))
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                for dr,dc in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out


def solve_E110(grid):
    out=clone(grid)
    h,w=dims(grid)
    assert h==w
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                out[c][r]=v
    return out


def solve_E111(grid):
    out=clone(grid)
    h,w=dims(grid)
    for r in range(h):
        c=0
        while c<w-1:
            v=grid[r][c]
            if v!=0 and c+1<w and grid[r][c+1]==v:
                left_same = c-1>=0 and grid[r][c-1]==v
                right_same = c+2<w and grid[r][c+2]==v
                if not left_same and not right_same and c+2<w and grid[r][c+2]==0:
                    out[r][c+2]=v
                c += 2
            else:
                c += 1
    return out


def solve_E112(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for c in range(w):
        cells=[grid[r][c] for r in range(h) if grid[r][c]!=0]
        if len(cells)==1:
            color=cells[0]
            for r in range(h):
                out[r][c]=color
    return out


def solve_M106(grid):
    h,w=dims(grid)
    out=blank(h,w)
    src=dst=None
    for r in range(h):
        for c in range(w):
            if grid[r][c]==8:
                src=(r,c)
            elif grid[r][c]==9:
                dst=(r,c)
    assert src and dst
    dr,dc=dst[0]-src[0], dst[1]-src[1]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0 and v not in (8,9):
                out[r][c]=v
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w:
                    out[nr][nc]=v
    return out


def solve_M107(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in connected_components(grid, ignore=(0,), same_color=True):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c]=8
    return out


def solve_M108(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in connected_components(grid, ignore=(0,), same_color=True):
        r0,r1,c0,c1=bbox(cells)
        for c in range(c0,c1+1):
            out[r0][c]=color
            out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color
            out[r][c1]=color
    return out


def solve_M109(grid):
    h,w=dims(grid)
    out=blank(h,w)
    anchor=None
    cells=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9:
                anchor=(r,c)
            elif v!=0:
                cells.append((r,c,v))
    assert anchor
    ar,ac=anchor
    for r,c,v in cells:
        dr,dc=r-ar,c-ac
        nr,nc=ar+dc, ac-dr
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out


def solve_M110(grid):
    h,w=dims(grid)
    # frame cells are color 5
    frame_cells=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==5]
    obj_cells=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,5)]
    assert frame_cells and obj_cells
    fr0,fr1,fc0,fc1=bbox([(r,c) for r,c in frame_cells])
    target=(fr0+1, fc0+1)
    or0,or1,oc0,oc1=bbox([(r,c) for r,c,v in obj_cells])
    out=blank(h,w)
    dr,dc=target[0]-or0, target[1]-oc0
    for r,c,v in obj_cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out


def solve_M111(grid):
    h,w=dims(grid)
    comps=connected_components(grid, ignore=(0,), same_color=True)
    assert len(comps)==3
    comps_sorted=sorted(comps, key=lambda x: len(x[1]))
    palette=[2,4,8]
    out=blank(h,w)
    for new_color, (_,cells) in zip(palette, comps_sorted):
        for r,c in cells:
            out[r][c]=new_color
    return out


def solve_M112(grid):
    h,w=dims(grid)
    out=clone(grid)
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5 or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); region=[]
            seeds=[]
            while q:
                x,y=q.popleft(); region.append((x,y))
                if grid[x][y] not in (0,5):
                    seeds.append(grid[x][y])
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and grid[nx][ny]!=5 and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            uniq=set(seeds)
            if len(uniq)==1 and len(seeds)==1:
                color=next(iter(uniq))
                for x,y in region:
                    if grid[x][y]!=5:
                        out[x][y]=color
    return out


def solve_H106(grid):
    h,w=dims(grid)
    n=h
    p1,p2,p3=split_panels_row(grid, n, 3, sep_color=5)
    name=infer_transform(p1,p2, candidates=["rot90","rot180","rot270","flip_h","flip_v","transpose","anti_transpose","id"])
    return TRANSFORMS[name](p3)


def solve_H107(grid):
    h,w=dims(grid)
    n=h
    p1,p2,p3=split_panels_row(grid, n, 3, sep_color=5)
    label1, occ1 = panel_label_and_occ(p1)
    label2, occ2 = panel_label_and_occ(p2)
    _, query_occ = panel_label_and_occ(p3)
    q_transforms=set(all_occ_transforms(query_occ).values())
    if occ1 in q_transforms and occ2 not in q_transforms:
        label=label1
    elif occ2 in q_transforms and occ1 not in q_transforms:
        label=label2
    elif occ1 in q_transforms:
        label=label1
    elif occ2 in q_transforms:
        label=label2
    else:
        raise ValueError("no prototype match")
    out=blank(n,n)
    for r,row in enumerate(p3):
        for c,v in enumerate(row):
            if v!=0 and not (r==0 and c==0):
                out[r][c]=label
    return out


def solve_H108(grid):
    h,w=dims(grid)
    n=h
    before, after, query = split_panels_row(grid, n, 3, sep_color=5)
    (br0,br1,bc0,bc1), before_cells = main_object_bbox(before, ignore_colors=(0,8))
    # Added stencil = cells that are 8 in after but 0 in before
    added=[(r-br0,c-bc0) for r in range(n) for c in range(n) if after[r][c]==8 and before[r][c]==0]
    (qr0,qr1,qc0,qc1), query_cells = main_object_bbox(query, ignore_colors=(0,8))
    out=clone(query)
    for dr,dc in added:
        nr,nc=qr0+dr,qc0+dc
        if 0<=nr<n and 0<=nc<n:
            out[nr][nc]=8
    return out


def solve_H109(grid):
    h,w=dims(grid)
    out=blank(h,w)
    anchor=None
    cells=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9:
                anchor=(r,c)
            elif v!=0:
                cells.append((r,c,v))
    ar,ac=anchor
    for r,c,v in cells:
        dr,dc=r-ar,c-ac
        for _ in range(4):
            nr,nc=ar+dr, ac+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
            dr,dc=dc,-dr
    return out


def solve_H110(grid):
    h,w=dims(grid)
    n=h
    mask,a,b=split_panels_row(grid, n, 3, sep_color=5)
    out=blank(n,n)
    for r in range(n):
        for c in range(n):
            out[r][c]=a[r][c] if mask[r][c]!=0 else b[r][c]
    return out


def solve_H111(grid):
    return geodesic_room_fill(grid)


def solve_H112(grid):
    h,w=dims(grid)
    n=h
    p1,p2,p3,p4,p5=split_panels_row(grid,n,5,sep_color=5)
    op_name=None
    for name,fn in OPS.items():
        if fn(p1,p2)==p3:
            op_name=name
            break
    if op_name is None:
        raise ValueError("no binary op match")
    return OPS[op_name](p4,p5)


