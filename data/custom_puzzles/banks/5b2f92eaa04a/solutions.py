"""
ARC-style puzzle bank continuation: 21 more puzzles (7 easy, 7 medium, 7 hard).
Each solve_* function is a reference program for one puzzle.
"""
from __future__ import annotations
from typing import List, Tuple
from collections import deque, defaultdict

Grid = List[List[int]]


def parse_grid(lines: List[str]) -> Grid:
    return [[int(ch) for ch in line.strip()] for line in lines]

def grid_to_strings(g: Grid) -> List[str]:
    return ["".join(str(x) for x in row) for row in g]

def dims(g): return len(g), len(g[0])


def clone(g): return [row[:] for row in g]


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs),max(rs),min(cs),max(cs)


def components(g):
    h,w=dims(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in seen or g[r][c]==0: continue
            col=g[r][c]
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and g[nx][ny]==col:
                        seen.add((nx,ny)); q.append((nx,ny))
            comps.append((col,cells))
    return comps


def crop_cells(cells):
    r0,r1,c0,c1=bbox(cells)
    return [(r-r0,c-c0) for r,c in cells], (r1-r0+1,c1-c0+1)


def hole_cells_of_component(g,cells):
    r0,r1,c0,c1=bbox(cells)
    comp=set(cells)
    seen=set()
    q=deque()
    for r in range(r0,r1+1):
        for c in [c0,c1]:
            if (r,c) not in comp and (r,c) not in seen:
                seen.add((r,c)); q.append((r,c))
    for c in range(c0,c1+1):
        for r in [r0,r1]:
            if (r,c) not in comp and (r,c) not in seen:
                seen.add((r,c)); q.append((r,c))
    while q:
        x,y=q.popleft()
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny=x+dx,y+dy
            if r0<=nx<=r1 and c0<=ny<=c1 and (nx,ny) not in comp and (nx,ny) not in seen:
                seen.add((nx,ny)); q.append((nx,ny))
    holes=[]
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if (r,c) not in comp and (r,c) not in seen:
                holes.append((r,c))
    return holes


def draw_rect_border(out, r0,r1,c0,c1,col):
    for c in range(c0,c1+1):
        out[r0][c]=col; out[r1][c]=col
    for r in range(r0,r1+1):
        out[r][c0]=col; out[r][c1]=col


def is_vert_sym(cells):
    local,(H,W)=crop_cells(cells)
    s=set(local)
    return all((r,W-1-c) in s for r,c in s)


def solve_E8(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]!=0 and g[r][c-1]==g[r][c+1]:
                out[r][c]=g[r][c-1]
    return out


def solve_E9(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                if g[r][c]==0: out[r][c]=nz[0]
                if g[r][c+1]==0: out[r][c+1]=nz[0]
                if g[r+1][c]==0: out[r+1][c]=nz[0]
                if g[r+1][c+1]==0: out[r+1][c+1]=nz[0]
    return out


def solve_E10(g):
    out=clone(g)
    for r,row in enumerate(g):
        nz=[(c,v) for c,v in enumerate(row) if v!=0]
        if len(nz)==2 and nz[0][1]==nz[1][1]:
            c0,v=nz[0]; c1,_=nz[1]
            if all(row[c]==0 for c in range(c0+1,c1)):
                for c in range(c0,c1+1):
                    out[r][c]=v
    return out


def solve_E11(g):
    h,w=dims(g); out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            if g[r][c]==0 and vals[0]!=0 and len(set(vals))==1:
                out[r][c]=vals[0]
    return out


def solve_E12(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]!=0:
                val=g[r][c]; start=c
                while c+1<w and g[r][c+1]==val: c+=1
                end=c
                if end-start+1==2 and end+1<w and g[r][end+1]==0:
                    out[r][end+1]=val
            c+=1
    return out


def solve_E13(g):
    h,w=dims(g); out=clone(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if vals[0]!=0 and len(set(vals))==1:
                out[r][c]=8
    return out


def solve_E14(g):
    h,w=dims(g); out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[h-1-r][c]=g[r][c]
    return out


def solve_M8(g):
    comps=components(g)
    # choose comp with largest max col; tie by area then min row
    chosen=max(comps, key=lambda x: (max(c for r,c in x[1]), len(x[1]), -min(r for r,c in x[1])))
    out=clone(g)
    for r,c in chosen[1]:
        out[r][c]=8
    return out


def solve_M9(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        draw_rect_border(out,r0,r1,c0,c1,col)
    return out


def solve_M10(g):
    out=clone(g)
    by_color=defaultdict(list)
    for col,cells in components(g):
        by_color[col].append(cells)
    for col, comps in by_color.items():
        if len(comps)==2:
            bbs=[bbox(cells) for cells in comps]
            # sort left to right
            (r0a,r1a,c0a,c1a),(r0b,r1b,c0b,c1b)=sorted(bbs,key=lambda b:b[2])
            overlap_r0=max(r0a,r0b); overlap_r1=min(r1a,r1b)
            if overlap_r0<=overlap_r1 and c1a+1<=c0b-1:
                for r in range(overlap_r0,overlap_r1+1):
                    for c in range(c1a+1,c0b):
                        out[r][c]=col
    return out


def solve_M11(g):
    comps=[(col,cells) for col,cells in components(g) if col!=9]
    marker=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    assert len(comps)==1 and len(marker)==1
    col,cells=comps[0]
    mr,mc=marker[0]
    r0,r1,c0,c1=bbox(cells)
    out=[[0]*len(g[0]) for _ in range(len(g))]
    for r,c in cells:
        out[mr+(r-r0)][mc+(c-c0)] = col
    return out


def solve_M12(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        if is_vert_sym(cells):
            for r,c in cells:
                out[r][c]=col
    return out


def solve_M13(g):
    out=clone(g)
    for col,cells in components(g):
        rows=defaultdict(list)
        for r,c in cells:
            rows[r].append(c)
        for r, cs in rows.items():
            for c in range(min(cs), max(cs)+1):
                out[r][c]=col
    return out


def solve_M14(g):
    out=clone(g)
    hollow=[]
    for col,cells in components(g):
        holes=hole_cells_of_component(g,cells)
        if holes:
            hollow.append((len(cells), col, cells, holes))
    if not hollow:
        return out
    _, col, cells, holes = max(hollow, key=lambda x:x[0])
    for r,c in holes:
        out[r][c]=col
    return out


def solve_H8(g):
    comps=components(g)
    items=[]
    for col,cells in comps:
        local,(H,W)=crop_cells(cells)
        items.append((W,H,col,set(local)))
    items.sort(key=lambda x:(-x[0], -x[1], x[2]))
    out_h=sum(H for W,H,col,s in items) + max(0, len(items)-1)
    out_w=max(W for W,H,col,s in items) if items else 0
    out=[[0]*out_w for _ in range(out_h)]
    r_off=0
    for W,H,col,s in items:
        for r,c in s:
            out[r_off+r][c]=col
        r_off += H + 1
    return out


def solve_H9(g):
    comps=components(g)
    # choose first color2 and first color3
    c2=[cells for col,cells in comps if col==2][0]
    c3=[cells for col,cells in comps if col==3][0]
    s2,(H2,W2)=crop_cells(c2); s2=set(s2)
    s3,(H3,W3)=crop_cells(c3); s3=set(s3)
    H=max(H2,H3); W=max(W2,W3)
    out=[[0]*W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            in2=(r,c) in s2
            in3=(r,c) in s3
            if in2 ^ in3:
                out[r][c]=8
    return out


def solve_H10(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    for col,cells in components(g):
        r0,r1,c0,c1=bbox(cells)
        H=r1-r0+1; W=c1-c0+1
        local,_=crop_cells(cells)
        for r,c in local:
            rr = H-1-r
            cc = W-1-c
            out[r0+rr][c0+cc]=col
    return out


def solve_H11(g):
    comps=components(g)
    groups=defaultdict(list)
    dims_map={}
    for col,cells in comps:
        local,(H,W)=crop_cells(cells)
        key=tuple(sorted(local))
        groups[key].append((col,cells,H,W))
        dims_map[key]=(H,W)
    key=max(groups.keys(), key=lambda k: (len(groups[k]), len(k)))
    H,W=dims_map[key]
    out=[[0]*W for _ in range(H)]
    for r,c in key:
        out[r][c]=8
    return out


def solve_H12(g):
    comps=components(g)
    items=[]
    for col,cells in comps:
        local,(H,W)=crop_cells(cells)
        items.append((len(cells), W, H, col, set(local)))
    items.sort(key=lambda x:(x[0], x[1], x[2], x[3]))
    # take first four
    items=items[:4]
    (a_area,aW,aH,aCol,aS),(b_area,bW,bH,bCol,bS),(c_area,cW,cH,cCol,cS),(d_area,dW,dH,dCol,dS)=items
    left_w=max(aW,cW); right_w=max(bW,dW)
    top_h=max(aH,bH); bot_h=max(cH,dH)
    H=top_h+1+bot_h; W=left_w+1+right_w
    out=[[0]*W for _ in range(H)]
    # TL
    for r,c in aS: out[r][c]=aCol
    # TR
    for r,c in bS: out[r][left_w+1+c]=bCol
    # BL
    for r,c in cS: out[top_h+1+r][c]=cCol
    # BR
    for r,c in dS: out[top_h+1+r][left_w+1+c]=dCol
    return out


def solve_H13(g):
    # extract hole patterns, crop them to hole bbox, pack left->right with gap 1 by original left order
    items=[]
    for col,cells in components(g):
        holes=hole_cells_of_component(g,cells)
        if holes:
            hr0,hr1,hc0,hc1=bbox(holes)
            local=[(r-hr0,c-hc0) for r,c in holes]
            H=hr1-hr0+1; W=hc1-hc0+1
            comp_bb=bbox(cells)
            items.append((comp_bb[2], H, W, col, set(local)))
    items.sort(key=lambda x:x[0])
    if not items:
        return [[]]
    H=max(item[1] for item in items)
    W=sum(item[2] for item in items)+max(0,len(items)-1)
    out=[[0]*W for _ in range(H)]
    off=0
    for _,h,w,col,s in items:
        for r,c in s: out[r][off+c]=col
        off += w+1
    return out


def solve_H14(g):
    comps=components(g)
    hollow=[]; solid=[]
    for col,cells in comps:
        holes=hole_cells_of_component(g,cells)
        bb=bbox(cells)
        if holes:
            hollow.append((col,cells,holes,bb))
        else:
            solid.append((col,cells,bb))
    # match by bbox dims
    out=clone(g)
    for hcol,hcells,holes,hbb in hollow:
        hH=hbb[1]-hbb[0]+1; hW=hbb[3]-hbb[2]+1
        rel=[(r-hbb[0], c-hbb[2]) for r,c in holes]
        for scol,scells,sbb in solid:
            sH=sbb[1]-sbb[0]+1; sW=sbb[3]-sbb[2]+1
            if (sH,sW)==(hH,hW):
                for rr,cc in rel:
                    out[sbb[0]+rr][sbb[2]+cc]=0
                return out
    return out


