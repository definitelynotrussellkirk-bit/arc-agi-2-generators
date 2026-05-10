"""Reference solvers for ARC-style additional puzzle bank volume 6.

This volume adds a new explicit helper primitive:
`apply_dihedral(shape, code)`, which applies one of the 8 dihedral
transforms to a normalized shape.
"""
from typing import List, Dict, Tuple, Set

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def clone(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w


def safe(g,r,c,d=0):
    return g[r][c] if inb(g,r,c) else d


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


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
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color":v, "cells":cells, "bbox":bbox(cells)})
    return out


def normalize_cells(cells):
    if not cells:
        return set()
    r0,c0,_,_=bbox(cells)
    return {(r-r0, c-c0) for r,c in cells}


def component_degree_map(cells):
    S=set(cells)
    deg={}
    for p in S:
        deg[p] = sum(((p[0]+dr,p[1]+dc) in S) for dr,dc in DIR4)
    return deg


def holes_of_component(comp):
    cells=set(comp["cells"])
    r0,c0,r1,c1=comp["bbox"]
    seen=set()
    stack=[]
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if r in (r0,r1) or c in (c0,c1):
                if (r,c) not in cells and (r,c) not in seen:
                    seen.add((r,c)); stack.append((r,c))
    while stack:
        rr,cc=stack.pop()
        for dr,dc in DIR4:
            nr,nc=rr+dr,cc+dc
            if r0<=nr<=r1 and c0<=nc<=c1 and (nr,nc) not in cells and (nr,nc) not in seen:
                seen.add((nr,nc)); stack.append((nr,nc))
    hole_cells={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if (r,c) not in cells and (r,c) not in seen}
    return hole_cells


def hole_components(comp):
    holes = holes_of_component(comp)
    seen=set()
    out=[]
    for cell in list(holes):
        if cell in seen:
            continue
        stack=[cell]
        seen.add(cell)
        cc=[cell]
        while stack:
            r,c=stack.pop()
            for dr,dc in DIR4:
                nb=(r+dr,c+dc)
                if nb in holes and nb not in seen:
                    seen.add(nb); stack.append(nb); cc.append(nb)
        out.append(cc)
    return out


def normalize_shape_dims(shape):
    if not shape:
        return set(),0,0
    rs=[r for r,c in shape]; cs=[c for r,c in shape]
    r0,c0=min(rs), min(cs)
    sh={(r-r0,c-c0) for r,c in shape}
    h=max(r for r,c in sh)+1
    w=max(c for r,c in sh)+1
    return sh,h,w


def rot90(shape, h, w):
    return {(c, h-1-r) for r,c in shape}, w, h


def rot180(shape, h, w):
    return {(h-1-r, w-1-c) for r,c in shape}, h, w


def rot270(shape, h, w):
    return {(w-1-c, r) for r,c in shape}, w, h


def flip_h(shape, h, w):  # mirror left-right across vertical axis
    return {(r, w-1-c) for r,c in shape}, h, w


def flip_v(shape, h, w):
    return {(h-1-r, c) for r,c in shape}, h, w


def flip_diag(shape, h, w):  # transpose main diagonal
    return {(c, r) for r,c in shape}, w, h


def flip_anti(shape, h, w):
    return {(w-1-c, h-1-r) for r,c in shape}, w, h


def apply_dihedral(shape, code, h=None, w=None):
    """code 1..8: id, rot90, rot180, rot270, flip_h, flip_v, flip_diag, flip_anti"""
    if h is None or w is None:
        shape,h,w = normalize_shape_dims(shape)
    if code==1:
        out,hh,ww = set(shape),h,w
    elif code==2:
        out,hh,ww = rot90(shape,h,w)
    elif code==3:
        out,hh,ww = rot180(shape,h,w)
    elif code==4:
        out,hh,ww = rot270(shape,h,w)
    elif code==5:
        out,hh,ww = flip_h(shape,h,w)
    elif code==6:
        out,hh,ww = flip_v(shape,h,w)
    elif code==7:
        out,hh,ww = flip_diag(shape,h,w)
    elif code==8:
        out,hh,ww = flip_anti(shape,h,w)
    else:
        raise ValueError(code)
    out,hh2,ww2 = normalize_shape_dims(out)
    return out,hh2,ww2


def slide_component(cells, occupied, h, w, dr, dc):
    cur=set(cells)
    while True:
        nxt={(r+dr,c+dc) for r,c in cur}
        if any(not (0<=r<h and 0<=c<w) for r,c in nxt):
            return cur
        if nxt & occupied:
            return cur
        cur=nxt


def bfs_multi(grid, starts, passable={0,2}):
    from collections import deque
    h,w=dims(grid)
    q=deque()
    dist={}
    for s in starts:
        q.append(s); dist[s]=0
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in dist and grid[nr][nc] in passable:
                dist[(nr,nc)] = dist[(r,c)] + 1
                q.append((nr,nc))
    return dist


def solve_E36(g):
    out=clone(g)
    for comp in components(g, colors={2}):
        cells=set(comp["cells"])
        r0,c0,r1,c1=comp["bbox"]
        norm={(r-r0,c-c0) for r,c in cells}
        w=c1-c0+1
        mir={(r,w-1-c) for r,c in norm}
        if norm==mir:
            for r,c in cells:
                out[r][c]=3
    return out


def solve_E37(g):
    out=clone(g)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            if safe(g,r-1,c-1)==4 and safe(g,r+1,c+1)==4:
                out[r][c]=8
            if safe(g,r-1,c+1)==4 and safe(g,r+1,c-1)==4:
                out[r][c]=8
    return out


def solve_E38(g):
    out=clone(g)
    for comp in components(g, colors={1}):
        cells=set(comp["cells"])
        r0,c0,r1,c1=comp["bbox"]
        # assume filled rectangle
        for r,c in cells:
            if not (r in (r0,r1) or c in (c0,c1)):
                out[r][c]=0
    return out


def solve_E39(g):
    out=clone(g)
    for comp in components(g, colors={3}):
        cells=comp["cells"]
        if len(cells)!=3:
            continue
        r0,c0,r1,c1=comp["bbox"]
        if (r1-r0+1, c1-c0+1)!=(2,2):
            continue
        deg=component_degree_map(cells)
        corner=[p for p,d in deg.items() if d==2]
        if len(corner)==1:
            out[corner[0][0]][corner[0][1]]=2
    return out


def solve_E40(g):
    h,w=dims(g)
    corners={(0,0),(0,w-1),(h-1,0),(h-1,w-1)}
    out=clone(g)
    for comp in components(g, colors={7}):
        if set(comp["cells"]) & corners:
            for r,c in comp["cells"]:
                out[r][c]=1
    return out


def solve_E41(g):
    reds=components(g, colors={2})
    target=min(reds, key=lambda comp: len(comp["cells"]))
    out=clone(g)
    for r,c in target["cells"]:
        out[r][c]=8
    return out


def solve_E42(g):
    out=clone(g)
    for comp in components(g, colors={2}):
        if len(comp["cells"])!=1:
            continue
        r,c=comp["cells"][0]
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc) and g[nr][nc]==0:
                out[nr][nc]=1
    return out


def solve_M36(g):
    out=clone(g)
    h,w=dims(g)
    mapping={}
    for c in range(w):
        src=g[0][c]; dst=g[1][c]
        if src!=0 and dst!=0:
            mapping[src]=dst
    for r in range(2,h):
        for c in range(w):
            if g[r][c] in mapping:
                out[r][c]=mapping[g[r][c]]
    return out


def solve_M37(g):
    out=clone(g)
    temps=components(g, colors={8})
    if len(temps)!=1:
        raise ValueError("expected one template")
    template=normalize_cells(temps[0]["cells"])
    for comp in components(g, colors={2}):
        if normalize_cells(comp["cells"])==template:
            for r,c in comp["cells"]:
                out[r][c]=3
    return out


def solve_M38(g):
    out=clone(g)
    h,w=dims(g)
    colors=sorted({g[r][c] for r in range(h) for c in range(w) if g[r][c]!=0})
    for color in colors:
        pts=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        if len(pts)!=2:
            continue
        (r0,c0),(r1,c1)=pts
        ra,rb=sorted([r0,r1]); ca,cb=sorted([c0,c1])
        for r in range(ra,rb+1):
            out[r][ca]=color; out[r][cb]=color
        for c in range(ca,cb+1):
            out[ra][c]=color; out[rb][c]=color
    return out


def solve_M39(g):
    h,w=dims(g)
    wall={(r,c) for r in range(h) for c in range(w) if g[r][c]==5}
    movable=components(g, colors={2,3,4})
    out=clone(g)
    for comp in movable:
        for r,c in comp["cells"]:
            out[r][c]=0
    occupied=set(wall)
    # sort by rightmost bbox edge descending, then row
    movable=sorted(movable, key=lambda comp:(comp["bbox"][3], comp["bbox"][0]), reverse=True)
    for comp in movable:
        landed=slide_component(comp["cells"], occupied, h, w, 0, 1)
        for r,c in landed:
            out[r][c]=comp["color"]
        occupied |= set(landed)
    return out


def solve_M40(g):
    h,w=dims(g)
    out=clone(g)
    comps=components(g, colors={6})
    for comp in comps:
        r0,c0,r1,c1=comp["bbox"]
        n=r1-r0+1; m=c1-c0+1
        if n!=m:
            raise ValueError("bbox not square")
        code=safe(g,r0-1,c0,0)
        if code not in {1,2,3,4}:
            raise ValueError(f"missing control {code} at {(r0-1,c0)}")
        for r,c in comp["cells"]:
            out[r][c]=0
        shape={(r-r0,c-c0) for r,c in comp["cells"]}
        hh=n; ww=m
        if code==1:
            tsh=shape
        elif code==2:
            tsh,_hh,_ww=apply_dihedral(shape,2,hh,ww)
        elif code==3:
            tsh,_hh,_ww=apply_dihedral(shape,3,hh,ww)
        else:
            tsh,_hh,_ww=apply_dihedral(shape,4,hh,ww)
        for dr,dc in tsh:
            out[r0+dr][c0+dc]=6
    return out


def solve_M41(g):
    out=clone(g)
    for comp in components(g, colors={6}):
        nh=len(hole_components(comp))
        newc={0:2,1:3}.get(nh,4)
        for r,c in comp["cells"]:
            out[r][c]=newc
    return out


def solve_M42(g):
    out=clone(g)
    target=sum(1 for x in g[0] if x==1)
    for comp in components(g, colors={2}):
        if len(comp["cells"])==target:
            for r,c in comp["cells"]:
                out[r][c]=3
    return out


def solve_H36(g):
    out=clone(g)
    frame_comps=[]
    for comp in components(g, colors=set(range(1,10))-{8}):
        cells=set(comp["cells"])
        r0,c0,r1,c1=comp["bbox"]
        box={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1)}
        if len(cells)>=2*(r1-r0+1)+2*(c1-c0+1)-4 and cells=={(r,c) for r,c in box if r in (r0,r1) or c in (c0,c1)}:
            frame_comps.append(comp)
    if not frame_comps:
        return out
    interiors=[]
    for comp in frame_comps:
        r0,c0,r1,c1=comp["bbox"]
        interiors.append({(r,c) for r in range(r0+1,r1) for c in range(c0+1,c1)})
    inter=set.intersection(*interiors) if interiors else set()
    for r,c in inter:
        out[r][c]=2
    return out


def solve_H37(g):
    h,w=dims(g)
    starts=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    dist=bfs_multi(g, starts, passable={0,2})
    out=clone(g)
    for (r,c),d in dist.items():
        out[r][c]={0:3,1:4,2:5}[d%3]
    return out


def solve_H38(g):
    h,w=dims(g)
    shapes=[normalize_cells(comp["cells"]) for comp in components(g, colors={2})]
    inter=set.intersection(*map(set, shapes)) if shapes else set()
    anchor=next((r,c) for r in range(h) for c in range(w) if g[r][c]==9)
    out=blank(h,w)
    for dr,dc in inter:
        r,c=anchor[0]+dr, anchor[1]+dc
        if 0<=r<h and 0<=c<w:
            out[r][c]=3
    return out


def solve_H39(g):
    h,w=dims(g)
    template_comp=components(g, colors={2})[0]
    shape={(r-template_comp["bbox"][0], c-template_comp["bbox"][1]) for r,c in template_comp["cells"]}
    hh=template_comp["bbox"][2]-template_comp["bbox"][0]+1
    ww=template_comp["bbox"][3]-template_comp["bbox"][1]+1
    ops=[x for x in g[h-1] if x in {1,2,3,4}]
    cur=shape; ch,chh,cww = None,None,None
    cur=shape; ch=hh; cw=ww
    for op in ops:
        if op==1:
            cur,ch,cw = apply_dihedral(cur,2,ch,cw)
        elif op==2:
            cur,ch,cw = apply_dihedral(cur,3,ch,cw)
        elif op==3:
            cur,ch,cw = apply_dihedral(cur,5,ch,cw)
        elif op==4:
            cur,ch,cw = apply_dihedral(cur,6,ch,cw)
    anchor=next((r,c) for r in range(h) for c in range(w) if g[r][c]==9)
    out=blank(h,w)
    for dr,dc in cur:
        r,c=anchor[0]+dr, anchor[1]+dc
        if 0<=r<h and 0<=c<w:
            out[r][c]=3
    return out


def solve_H40(g):
    h,w=dims(g)
    selector=None
    for c,v in enumerate(g[0]):
        if v in {2,3,4,5,6,7}:
            selector=v; break
    if selector is None:
        raise ValueError("no selector")
    candidates=[comp for comp in components(g, colors={selector}) if len(comp["cells"])>1]
    if len(candidates)!=1:
        raise ValueError(f"need one non-singleton target comp of color {selector}, got {len(candidates)}")
    holes=holes_of_component(candidates[0])
    sh=normalize_cells(holes)
    anchor=next((r,c) for r in range(h) for c in range(w) if g[r][c]==9)
    out=blank(h,w)
    for dr,dc in sh:
        r,c=anchor[0]+dr, anchor[1]+dc
        if 0<=r<h and 0<=c<w:
            out[r][c]=8
    return out


def solve_H41(g):
    h,w=dims(g)
    template=components(g, colors={2})[0]
    r0,c0,r1,c1=template["bbox"]
    base={(r-r0,c-c0) for r,c in template["cells"]}
    hh=r1-r0+1; ww=c1-c0+1
    out=blank(h,w)
    anchors=[(r,c) for r in range(h) for c in range(w) if g[r][c]==9]
    for ar,ac in anchors:
        code=safe(g, ar, ac-1, 0)
        if code not in range(1,9):
            raise ValueError(f"anchor at {(ar,ac)} missing left control")
        tsh,th,tw=apply_dihedral(base, code, hh, ww)
        for dr,dc in tsh:
            r,c=ar+dr, ac+dc
            if 0<=r<h and 0<=c<w:
                out[r][c]=3
    return out


def solve_H42(g):
    h,w=dims(g)
    comps2=components(g, colors={2})
    comps4=components(g, colors={4})
    if len(comps2)!=1 or len(comps4)!=1:
        raise ValueError("need one A and one B")
    A=normalize_cells(comps2[0]["cells"])
    B=normalize_cells(comps4[0]["cells"])
    diff=A-B
    anchor=next((r,c) for r in range(h) for c in range(w) if g[r][c]==9)
    out=blank(h,w)
    for dr,dc in diff:
        r,c=anchor[0]+dr, anchor[1]+dc
        if 0<=r<h and 0<=c<w:
            out[r][c]=6
    return out


SOLVERS = {
    'E36': solve_E36,
    'E37': solve_E37,
    'E38': solve_E38,
    'E39': solve_E39,
    'E40': solve_E40,
    'E41': solve_E41,
    'E42': solve_E42,
    'M36': solve_M36,
    'M37': solve_M37,
    'M38': solve_M38,
    'M39': solve_M39,
    'M40': solve_M40,
    'M41': solve_M41,
    'M42': solve_M42,
    'H36': solve_H36,
    'H37': solve_H37,
    'H38': solve_H38,
    'H39': solve_H39,
    'H40': solve_H40,
    'H41': solve_H41,
    'H42': solve_H42,
}

def solve_by_id(task_id: str, grid: Grid) -> Grid:
    return SOLVERS[task_id](grid)
