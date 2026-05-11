"""Reference solvers for the 21-puzzle ARC-style additional bank."""
from pathlib import Path
import json
from typing import List

Grid = List[List[int]]

def parse_grid(s:str)->Grid:
    lines=[line.strip() for line in s.strip().splitlines() if line.strip()]
    return [[int(ch) for ch in line] for line in lines]

def grid_to_str(g:Grid)->str:
    return "\n".join("".join(str(c) for c in row) for row in g)

def clone(g:Grid)->Grid:
    return [row[:] for row in g]

def components(g:Grid, color=None):
    h,w=len(g),len(g[0])
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            val=g[r][c]
            if val==0:
                seen[r][c]=True
                continue
            if color is not None and val!=color:
                seen[r][c]=True
                continue
            target=val if color is None else color
            stack=[(r,c)]
            seen[r][c]=True
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==target:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
            comps.append((target,cells))
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs),max(rs),min(cs),max(cs)

def crop_to_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    r0,r1,c0,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def is_rect_border(cells):
    r0,r1,c0,c1=bbox(cells)
    border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
    return set(cells)==border

def solve_e1(g):
    h,w=len(g),len(g[0]); out=clone(g); mark=set()
    for r in range(h-1):
        for c in range(w-1):
            if g[r][c]==g[r+1][c]==g[r][c+1]==g[r+1][c+1]==2:
                mark.update([(r,c),(r+1,c),(r,c+1),(r+1,c+1)])
    for r,c in mark: out[r][c]=3
    return out

def solve_e2(g):
    out=clone(g)
    for _,cells in components(g, color=1):
        if any(r==0 for r,c in cells):
            for r,c in cells: out[r][c]=4
    return out

def solve_e3(g):
    out=clone(g)
    for _,cells in components(g, color=6):
        if is_rect_border(cells):
            r0,r1,c0,c1=bbox(cells)
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=6
    return out

def solve_e4(g):
    h,w=len(g),len(g[0]); out=clone(g)
    div=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]
    d=div[0]
    for r in range(h):
        for c in range(d+1,w):
            if out[r][c]!=5: out[r][c]=0
    for r in range(h):
        for c in range(d):
            v=g[r][c]
            if v!=0 and v!=5:
                mc=2*d-c
                if 0<=mc<w: out[r][mc]=v
    return out

def solve_e5(g):
    out=clone(g)
    for _,cells in components(g, color=8):
        rows={r for r,c in cells}
        cols=sorted(c for r,c in cells)
        if len(rows)==1 and len(cells)==3 and cols==list(range(min(cols), max(cols)+1)):
            r=next(iter(rows))
            left=min(cols)-1; right=max(cols)+1
            if 0<=left<len(g[0]) and g[r][left]==0: out[r][left]=8
            if 0<=right<len(g[0]) and g[r][right]==0: out[r][right]=8
    return out

def solve_e6(g):
    return crop_to_nonzero(g)

def solve_e7(g):
    comps=[cells for _,cells in components(g, color=7)]
    largest=max(comps, key=len)
    out=clone(g)
    for r,c in largest: out[r][c]=2
    return out

def solve_m1(g):
    out=clone(g)
    for _,cells in components(g, color=3):
        rs={r for r,c in cells}; cs={c for r,c in cells}
        new=1 if len(rs)==1 else 8 if len(cs)==1 else 3
        for r,c in cells: out[r][c]=new
    return out

def solve_m2(g):
    h,w=len(g),len(g[0]); out=clone(g)
    markers=sorted((r,c) for r in range(h) for c in range(w) if g[r][c]==9)
    (r1,c1),(r2,c2)=markers
    dr,dc=r2-r1,c2-c1
    for r,c in markers: out[r][c]=0
    cells=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c]!=0 and g[r][c]!=9]
    for r,c,v in cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w: out[nr][nc]=v
    return out

def solve_m3(g):
    h,w=len(g),len(g[0]); out=clone(g)
    div=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]
    d=div[0]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=5:
                mc=2*d-c
                if 0<=mc<w: out[r][mc]=v
    return out

def solve_m4(g):
    out=clone(g)
    for _,cells in components(g, color=7):
        r0,r1,c0,c1=bbox(cells)
        cellset=set(cells)
        hollow=False
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if (r,c) not in cellset and g[r][c]==0:
                    hollow=True
        new=4 if hollow else 2
        for r,c in cells: out[r][c]=new
    return out

def solve_m5(g):
    h,w=len(g),len(g[0]); out=clone(g)
    colors={g[r][c] for r in range(h) for c in range(w)} - {0}
    for color in colors:
        pts=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        n=len(pts)
        for i in range(n):
            for j in range(i+1,n):
                r1,c1=pts[i]; r2,c2=pts[j]
                if r1==r2:
                    for c in range(min(c1,c2), max(c1,c2)+1): out[r1][c]=color
                elif c1==c2:
                    for r in range(min(r1,r2), max(r1,r2)+1): out[r][c1]=color
    return out

def solve_m6(g):
    comps=[]
    for color,cells in components(g, color=None):
        comps.append((len(cells), color))
    comps.sort(key=lambda x:(-x[0], x[1]))
    row=[]
    for i,(size,color) in enumerate(comps):
        row.extend([color]*size)
        if i!=len(comps)-1: row.append(0)
    return [row]

def solve_m7(g):
    out=clone(g)
    for _,cells in components(g, color=5):
        if is_rect_border(cells):
            r0,r1,c0,c1=bbox(cells)
            marks=[(r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c]!=0 and g[r][c]!=5]
            if len(marks)==1:
                _,_,color=marks[0]
                for r,c in cells: out[r][c]=color
                mr,mc,_=marks[0]; out[mr][mc]=0
    return out

def solve_h1(g):
    h,w=len(g),len(g[0]); out=clone(g)
    control=g[0][0]
    out[0][0]=0
    cells=[(r,c,g[r][c]) for r in range(h) for c in range(w) if not (r==0 and c==0) and g[r][c]!=0]
    for r,c,v in cells:
        if control==1:
            out[r][w-1-c]=v
        elif control==2:
            out[h-1-r][c]=v
    return out

def solve_h2(g):
    h,w=len(g),len(g[0]); out=clone(g)
    markers=sorted((r,c) for r in range(h) for c in range(w) if g[r][c]==9)
    (r1,c1),(r2,c2)=markers
    dr,dc=r2-r1,c2-c1
    for r,c in markers: out[r][c]=0
    g2=[[0 if v==9 else v for v in row] for row in g]
    comps=[(len(cells), bbox(cells), color, cells) for color,cells in components(g2, color=None)]
    comps.sort(key=lambda t:(t[0], t[1][0], t[1][2], t[2]))
    _,_,color,cells = comps[0]
    for r,c in cells:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=color
    return out

def solve_h3(g):
    h,w=len(g),len(g[0]); out=clone(g)
    seeds=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    for r,c in seeds:
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc=r+dr,c+dc
            while 0<=nr<h and 0<=nc<w and g[nr][nc]!=1:
                if out[nr][nc]==0: out[nr][nc]=4
                nr+=dr; nc+=dc
    return out

def solve_h4(g):
    counts={}
    for col in [2,3,4]:
        counts[col]=len([cells for _,cells in components(g, color=col)])
    width=max(counts.values()) if counts else 0
    out=[[0]*width for _ in range(3)]
    for i,col in enumerate([2,3,4]):
        for c in range(counts[col]): out[i][c]=col
    return out

def solve_h5(g):
    h,w=len(g),len(g[0])
    marker=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2][0]
    candidates=[]
    for color,cells in components(g, color=None):
        if color not in (0,2) and is_rect_border(cells):
            r0,r1,c0,c1=bbox(cells)
            if r0 < marker[0] < r1 and c0 < marker[1] < c1:
                area=(r1-r0+1)*(c1-c0+1)
                candidates.append((area,color,r0,r1,c0,c1))
    area,color,r0,r1,c0,c1=min(candidates)
    return [[color]*(c1-c0+1) for _ in range(r1-r0+1)]

def solve_h6(g):
    horiz=[]; vert=[]
    for color,cells in components(g, color=None):
        rs={r for r,c in cells}; cs={c for r,c in cells}
        if len(rs)==1:
            horiz.append((len(cells), color))
        elif len(cs)==1:
            vert.append((len(cells), color))
    horiz.sort(key=lambda x:(-x[0], x[1]))
    vert.sort(key=lambda x:(-x[0], x[1]))
    def make_row(items):
        row=[]
        for i,(size,color) in enumerate(items):
            row.extend([color]*size)
            if i!=len(items)-1: row.append(0)
        return row
    row1=make_row(horiz); row2=make_row(vert)
    width=max(len(row1), len(row2))
    row1=row1+[0]*(width-len(row1))
    row2=row2+[0]*(width-len(row2))
    return [row1,row2]

def solve_h7(g):
    control=g[0][0]
    out=clone(g)
    out[0][0]=0
    g2=[[0 if (r==0 and c==0) else v for c,v in enumerate(row)] for r,row in enumerate(g)]
    for _,cells in components(g2, color=7):
        r0,r1,c0,c1=bbox(cells)
        cellset=set(cells)
        hollow=False
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if (r,c) not in cellset and g[r][c]==0:
                    hollow=True
        if (control==1 and hollow) or (control==2 and not hollow):
            for r,c in cells: out[r][c]=8
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
    "H7": solve_h7,
}

def load_tasks(json_path: str | None = None):
    path = Path(json_path) if json_path else Path(__file__).with_name("arc_additional_puzzle_bank.json")
    return json.loads(path.read_text())
