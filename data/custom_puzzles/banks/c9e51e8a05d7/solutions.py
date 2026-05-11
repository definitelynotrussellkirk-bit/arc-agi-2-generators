"""Reference solvers for ARC-style additional puzzle bank volume 4."""
from typing import List

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def parse_grid(s):
    return [[int(ch) for ch in line.strip()] for line in s.strip().splitlines() if line.strip()]

def grid_to_str(g):
    return "\n".join("".join(str(c) for c in row) for row in g)

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w

def safe(g,r,c,d=0):
    return g[r][c] if inb(g,r,c) else d

def components(g, colors=None, bg=0):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            v=g[r][c]
            if v==bg or (colors is not None and v not in colors):
                continue
            stack=[(r,c)]
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color":v, "cells":cells, "bbox":bbox(cells)})
    return out

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize(cells):
    if not cells:
        return set()
    r0,c0,_,_=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}

def crop_to_bbox(g, cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def hmirror_norm(cells):
    cells=normalize(cells)
    if not cells: return set()
    _,_,_,c1 = bbox(list(cells))
    return {(r, c1-c) for r,c in cells}

def vmirror_norm(cells):
    cells=normalize(cells)
    if not cells: return set()
    _,_,r1,_ = bbox(list(cells))
    return {(r1-r, c) for r,c in cells}

def rotate_cw_norm(cells):
    cells = normalize(cells)
    if not cells: return set()
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    h=max(rs)+1; w=max(cs)+1
    rot={(c, h-1-r) for r,c in cells}
    return normalize(rot)

def render_component_crop(comp):
    cells=comp["cells"]
    color=comp["color"]
    r0,c0,r1,c1=bbox(cells)
    out=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in cells:
        out[r-r0][c-c0]=color
    return out

def all_same_row(cells):
    return len({r for r,c in cells})==1

def all_same_col(cells):
    return len({c for r,c in cells})==1

def solve_E22(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==1:
                left = safe(g,r,c-1)==1
                right = safe(g,r,c+1)==1
                up = safe(g,r-1,c)==1
                down = safe(g,r+1,c)==1
                if (left and right and not up and not down) or (up and down and not left and not right):
                    out[r][c]=2
    return out

def solve_E23(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(1,h-1):
        for c in range(w):
            if g[r][c]==0 and g[r-1][c]==3 and g[r+1][c]==3:
                # optional isolation
                out[r][c]=2
    return out

def solve_E24(g):
    out=clone(g)
    h,w=dims(g)
    for comp in components(g, colors={4}):
        borders=set()
        for r,c in comp["cells"]:
            if r==0: borders.add("top")
            if r==h-1: borders.add("bottom")
            if c==0: borders.add("left")
            if c==w-1: borders.add("right")
        if len(borders)==2:
            for r,c in comp["cells"]:
                out[r][c]=8
    return out

def solve_E25(g):
    h,w=dims(g)
    out=clone(g)
    singles=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==6:
                out[r][c]=0
                singles.append((r,c))
    for r,c in singles:
        if r+1<h and c+1<w:
            out[r+1][c+1]=6
    return out

def solve_E26(g):
    out=clone(g)
    for comp in components(g, colors={8}):
        cells=comp["cells"]
        if len(cells)==3 and (all_same_row(cells) or all_same_col(cells)):
            for r,c in cells:
                out[r][c]=7
    return out

def solve_E27(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if vals.count(3)==2 and vals.count(0)==2:
                if g[r][c]==3 and g[r+1][c+1]==3 and g[r][c+1]==0 and g[r+1][c]==0:
                    out[r][c+1]=3
                    out[r+1][c]=3
                if g[r][c+1]==3 and g[r+1][c]==3 and g[r][c]==0 and g[r+1][c+1]==0:
                    out[r][c]=3
                    out[r+1][c+1]=3
    return out

def solve_E28(g):
    out=clone(g)
    comps=components(g, colors={2})
    target=min(comps, key=lambda comp: len(comp["cells"]))
    # unique smallest assumed
    for r,c in target["cells"]:
        out[r][c]=1
    return out

def solve_M22(g):
    out=clone(g)
    for comp in components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        for r,c in comp["cells"]:
            mc = c0 + (c1-c)
            out[r][mc]=color
    return out

def solve_M23(g):
    out=[[0]*len(g[0]) for _ in range(len(g))]
    for comp in components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        norm={(r-r0,c-c0) for r,c in comp["cells"]}
        h=r1-r0+1; w=c1-c0+1
        # expecting square bboxes, but works generally and may swap dims within original anchor if fits
        rot={(c, h-1-r) for r,c in norm}
        for rr,cc in rot:
            nr,nc=r0+rr,c0+cc
            if 0<=nr<len(g) and 0<=nc<len(g[0]):
                out[nr][nc]=color
    return out

def solve_M24(g):
    h,w=dims(g)
    src=dst=None
    object_cells=[]
    color=None
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==2:
                src=(r,c)
            elif v==3:
                dst=(r,c)
            elif v!=0:
                object_cells.append((r,c,v))
                if v not in (2,3):
                    color=v
    dr=dst[0]-src[0]; dc=dst[1]-src[1]
    out=[[0]*w for _ in range(h)]
    for r,c,v in object_cells:
        nr,nc=r+dr,c+dc
        out[nr][nc]=v
    return out

def solve_M25(g):
    comps=components(g)
    target=max(comps, key=lambda comp: (comp["bbox"][3]-comp["bbox"][1]+1, len(comp["cells"])))
    return crop_to_bbox(g, target["cells"])

def solve_M26(g):
    h,w=dims(g)
    cells1={(r,c) for r in range(h) for c in range(w) if g[r][c]==1}
    cells2={(r,c) for r in range(h) for c in range(w) if g[r][c]==2}
    n1=normalize(cells1); n2=normalize(cells2)
    union=n1|n2
    if not union: return [[0]]
    r0,c0,r1,c1=bbox(list(union))
    out=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in union:
        out[r-r0][c-c0]=3
    return out

def solve_M27(g):
    out=clone(g)
    for comp in components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        # assume square bbox
        for r,c in comp["cells"]:
            nr = r0 + (c-c0)
            nc = c0 + (r-r0)
            out[nr][nc]=color
    return out

def solve_M28(g):
    out=clone(g)
    for comp in components(g):
        color=comp["color"]
        r0,c0,r1,c1=comp["bbox"]
        norm={(r-r0,c-c0) for r,c in comp["cells"]}
        rs=[r for r,c in norm]; cs=[c for r,c in norm]
        h=max(rs)+1; w=max(cs)+1
        rots=[]
        cur=set(norm)
        for _ in range(4):
            rots.append(cur)
            cur={(c, h-1-r) for r,c in cur}
            # for square h=w; okay
        for cellset in rots:
            for rr,cc in cellset:
                out[r0+rr][c0+cc]=color
    return out

def solve_H22(g):
    h,w=dims(g)
    rank_ctrl=g[0][0]
    trans_ctrl=g[0][w-1]
    # objects are colors 7,8,9
    obj_grid=[[v if v in (7,8,9) else 0 for v in row] for row in g]
    comps=components(obj_grid)
    comps=sorted(comps, key=lambda comp: len(comp["cells"]))
    if rank_ctrl==1:
        target=comps[0]
    elif rank_ctrl==2:
        target=comps[len(comps)//2]
    elif rank_ctrl==3:
        target=comps[-1]
    else:
        raise ValueError("bad rank")
    color=target["color"]
    norm=normalize(target["cells"])
    if trans_ctrl==4:
        cells=norm
    elif trans_ctrl==5:
        cells=hmirror_norm(norm)
    elif trans_ctrl==6:
        cells=rotate_cw_norm(norm)
    else:
        raise ValueError("bad transform")
    # render cropped
    if not cells: return [[0]]
    r0,c0,r1,c1=bbox(list(cells))
    out=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in cells:
        out[r-r0][c-c0]=color
    return out

def solve_H23(g):
    h,w=dims(g)
    out=[[5 if g[r][c]==5 else 0 for c in range(w)] for r in range(h)]
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]==5 or seen[r][c]:
                continue
            stack=[(r,c)]
            seen[r][c]=True
            cells=[]
            seeds=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                if g[rr][cc] in (1,2,3):
                    seeds.append((rr,cc,g[rr][cc]))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]!=5:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
            if len(seeds)==1:
                color=seeds[0][2]
                for rr,cc in cells:
                    out[rr][cc]=color
            else:
                for rr,cc in cells:
                    if out[rr][cc]!=5:
                        out[rr][cc]=0
    return out

def solve_H24(g):
    out=clone(g)
    h,w=dims(g)
    pivot=None
    seeds=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==2: pivot=(r,c)
            elif v==1: seeds.append((r,c))
    pr,pc=pivot
    for r,c in seeds:
        poss=[(r,c),(2*pr-r,c),(r,2*pc-c),(2*pr-r,2*pc-c)]
        for nr,nc in poss:
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=1
    out[pr][pc]=2
    return out

def solve_H25(g):
    h,w=dims(g)
    A={(r,c) for r in range(h) for c in range(w) if g[r][c]==1}
    B={(r,c) for r in range(h) for c in range(w) if g[r][c]==2}
    A=normalize(A); B=normalize(B)
    C=A-B
    if not C: return [[0]]
    r0,c0,r1,c1=bbox(list(C))
    out=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in C:
        out[r-r0][c-c0]=3
    return out

def solve_H26(g):
    h,w=dims(g)
    template_cells={(r,c) for r in range(h) for c in range(w) if g[r][c]==4}
    template=normalize(template_cells)
    th=max(r for r,c in template)+1 if template else 0
    tw=max(c for r,c in template)+1 if template else 0
    out=[[0]*w for _ in range(h)]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v in (1,2,3):
                if v==1:
                    cells=template
                elif v==2:
                    cells=hmirror_norm(template)
                else:
                    cells=vmirror_norm(template)
                for rr,cc in cells:
                    nr,nc=r+rr,c+cc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=4
    return out

def solve_H27(g):
    frame_comps=components([[5 if v==5 else 0 for v in row] for row in g], colors={5})
    frames=[comp["bbox"] for comp in frame_comps]
    objs=components([[0 if v==5 else v for v in row] for row in g])
    def depth(comp):
        cells=comp["cells"]
        d=0
        for r0,c0,r1,c1 in frames:
            if all(r0<r<r1 and c0<c<c1 for r,c in cells):
                d+=1
        return d
    target=max(objs, key=lambda comp: (depth(comp), len(comp["cells"])))
    return render_component_crop(target)

def solve_H28(g):
    h,w=dims(g)
    out=[[0]*w for _ in range(h)]
    row_marks={}
    col_marks={}
    for r in range(1,h):
        if g[r][0] in (1,2,3):
            row_marks[r]=g[r][0]
            out[r][0]=g[r][0]
    for c in range(1,w):
        if g[0][c] in (1,2,3):
            col_marks[c]=g[0][c]
            out[0][c]=g[0][c]
    for r,rv in row_marks.items():
        for c,cv in col_marks.items():
            if rv==cv:
                out[r][c]=rv
    return out

SOLVERS = {
    'E22': solve_E22,
    'E23': solve_E23,
    'E24': solve_E24,
    'E25': solve_E25,
    'E26': solve_E26,
    'E27': solve_E27,
    'E28': solve_E28,
    'M22': solve_M22,
    'M23': solve_M23,
    'M24': solve_M24,
    'M25': solve_M25,
    'M26': solve_M26,
    'M27': solve_M27,
    'M28': solve_M28,
    'H22': solve_H22,
    'H23': solve_H23,
    'H24': solve_H24,
    'H25': solve_H25,
    'H26': solve_H26,
    'H27': solve_H27,
    'H28': solve_H28,
}

if __name__ == '__main__':
    print('Available solvers:', ', '.join(sorted(SOLVERS)))
