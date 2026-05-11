"""Reference solvers for ARC-style additional puzzle bank volume 7.

This volume introduces two especially useful helper primitives:
`orthogonal_closure(cells)` for row/column closure inside a component bbox,
and `manhattan_shell(cells, k)` for exact-distance shells around a source object.
It also includes stateful beam tracing for the mirror task.
"""

from typing import List
from collections import deque

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]


def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def clone(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def inb(g,r,c):
    h,w=dims(g); return 0<=r<h and 0<=c<w


def safe(g,r,c,d=0):
    return g[r][c] if inb(g,r,c) else d


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def frame_cells(r0,c0,r1,c1):
    cells=set()
    for c in range(c0,c1+1):
        cells.add((r0,c)); cells.add((r1,c))
    for r in range(r0,r1+1):
        cells.add((r,c0)); cells.add((r,c1))
    return cells


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
            out.append({"color":v,"cells":cells,"bbox":bbox(cells)})
    return out


def components_multicolor(g, allowed):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            if g[r][c] not in allowed:
                continue
            stack=[(r,c)]
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc] in allowed:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"cells":cells,"bbox":bbox(cells)})
    return out


def holes_for_component(comp):
    cells=set(comp["cells"])
    r0,c0,r1,c1=comp["bbox"]
    outside=set()
    stack=[]
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            if r in (r0,r1) or c in (c0,c1):
                if (r,c) not in cells and (r,c) not in outside:
                    outside.add((r,c)); stack.append((r,c))
    while stack:
        r,c=stack.pop()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if r0<=nr<=r1 and c0<=nc<=c1 and (nr,nc) not in cells and (nr,nc) not in outside:
                outside.add((nr,nc)); stack.append((nr,nc))
    holes={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if (r,c) not in cells and (r,c) not in outside}
    # split into comps
    seen=set(); out=[]
    for cell in list(holes):
        if cell in seen: continue
        stack=[cell]; seen.add(cell); cc=[cell]
        while stack:
            r,c=stack.pop()
            for dr,dc in DIR4:
                nb=(r+dr,c+dc)
                if nb in holes and nb not in seen:
                    seen.add(nb); stack.append(nb); cc.append(nb)
        out.append(cc)
    return out


def normalize_top_left(cells):
    if not cells: return set()
    r0,c0,r1,c1=bbox(cells)
    return {(r-r0,c-c0) for r,c in cells}


def rot_offsets(offsets, k):
    # offsets as set of (r,c) relative to anchor
    res=set(offsets)
    for _ in range(k%4):
        res={(c,-r) for r,c in res}
    return res


def orthogonal_closure(cells):
    rs=sorted({r for r,c in cells})
    cs=sorted({c for r,c in cells})
    r0,c0,r1,c1=bbox(cells)
    return {(r,c) for r in rs for c in cs if r0<=r<=r1 and c0<=c<=c1}


def manhattan_shell(cells, k, h, w):
    S=set(cells)
    out=set()
    for r in range(h):
        for c in range(w):
            if (r,c) in S:
                continue
            d=min(abs(r-r0)+abs(c-c0) for r0,c0 in S)
            if d==k:
                out.add((r,c))
    return out


def transform_shape(shape, t):
    # shape normalized top-left
    sh=set(shape)
    if t==1:
        out=sh
    elif t==2:
        # rot90 cw around bbox
        h=max(r for r,c in sh)+1; w=max(c for r,c in sh)+1
        out={(c, h-1-r) for r,c in sh}
    elif t==3:
        h=max(r for r,c in sh)+1; w=max(c for r,c in sh)+1
        out={(h-1-r, w-1-c) for r,c in sh}
    elif t==4:
        h=max(r for r,c in sh)+1; w=max(c for r,c in sh)+1
        out={(r, w-1-c) for r,c in sh}
    else:
        raise ValueError(t)
    # renormalize
    return normalize_top_left(out)


def bfs_dist(g, start):
    h,w=dims(g)
    q=deque([start]); dist={start:0}
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in dist and g[nr][nc] != 5:
                dist[(nr,nc)] = dist[(r,c)] + 1
                q.append((nr,nc))
    return dist


def slash_reflect(dr,dc):
    # / mirror
    if (dr,dc)==(0,1): return (-1,0)
    if (dr,dc)==(0,-1): return (1,0)
    if (dr,dc)==(1,0): return (0,-1)
    if (dr,dc)==(-1,0): return (0,1)
    raise ValueError((dr,dc))


def backslash_reflect(dr,dc):
    # \ mirror
    if (dr,dc)==(0,1): return (1,0)
    if (dr,dc)==(0,-1): return (-1,0)
    if (dr,dc)==(1,0): return (0,1)
    if (dr,dc)==(-1,0): return (0,-1)
    raise ValueError((dr,dc))


def solve_E43(g):
    h,w=dims(g)
    out=clone(g)
    for comp in components(g, colors={2}):
        S=set()
        for r,c in comp["cells"]:
            if r==0: S.add('T')
            if r==h-1: S.add('B')
            if c==0: S.add('L')
            if c==w-1: S.add('R')
        if len(S)==2:
            for r,c in comp["cells"]:
                out[r][c]=3
    return out


def solve_E44(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]==0 and safe(g,r-1,c-1)==4 and safe(g,r-1,c+1)==4 and safe(g,r+1,c-1)==4 and safe(g,r+1,c+1)==4:
                if safe(g,r-1,c)==0 and safe(g,r+1,c)==0 and safe(g,r,c-1)==0 and safe(g,r,c+1)==0:
                    out[r][c]=8
    return out


def solve_E45(g):
    out=clone(g)
    for comp in components(g, colors={1}):
        cells=comp["cells"]
        rs={r for r,c in cells}; cs={c for r,c in cells}
        if len(rs)==1:
            row=next(iter(rs))
            mn=min(c for r,c in cells); mx=max(c for r,c in cells)
            out[row][mn]=7; out[row][mx]=7
        elif len(cs)==1:
            col=next(iter(cs))
            mn=min(r for r,c in cells); mx=max(r for r,c in cells)
            out[mn][col]=7; out[mx][col]=7
    return out


def solve_E46(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(1,w-1):
            if g[r][c]==0 and g[r][c-1]==6 and g[r][c+1]==6:
                out[r][c]=6
    return out


def solve_E47(g):
    out=clone(g)
    comps=components(g, colors={3})
    if not comps: return out
    best=min(comps, key=lambda comp: len(comp["cells"]))
    for r,c in best["cells"]:
        out[r][c]=4
    return out


def solve_E48(g):
    out=clone(g)
    for comp in components(g, colors={2}):
        cells=set(comp["cells"])
        r0,c0,r1,c1=comp["bbox"]
        if (r1-r0+1)%2==1 and (c1-c0+1)%2==1 and cells==frame_cells(r0,c0,r1,c1):
            out[(r0+r1)//2][(c0+c1)//2]=8
    return out


def solve_E49(g):
    h,w=dims(g)
    out=clone(g)
    # find divider column with all 9s
    div=None
    for c in range(w):
        if all(g[r][c]==9 for r in range(h)):
            div=c; break
    if div is None: return out
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=9:
                mc=2*div-c
                if 0<=mc<w and mc!=div and out[r][mc]==0:
                    out[r][mc]=v
    return out


def solve_M43(g):
    out=clone(g)
    red=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    blue=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==1]
    if len(red)!=1 or len(blue)!=1: return out
    (r0,c0)=red[0]; (r1,c1)=blue[0]
    dr,dc=r1-r0,c1-c0
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v==3:
                nr,nc=r+dr,c+dc
                if inb(g,nr,nc):
                    out[nr][nc]=7
    return out


def solve_M44(g):
    out=clone(g)
    k=sum(v==2 for row in g for v in row)
    for comp in components(g, colors={4}):
        cells=set(comp["cells"])
        r0,c0,r1,c1=comp["bbox"]
        if cells==frame_cells(r0,c0,r1,c1) and (c1-c0+1)==k:
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=8
    return out


def solve_M45(g):
    out=clone(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v in {2,3,4,6,7,8}]
    # choose first non-wall marker, assume exactly one
    if not seeds:
        return out
    sr,sc,color=seeds[0]
    stack=[(sr,sc)]
    seen={(sr,sc)}
    while stack:
        r,c=stack.pop()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]==0:
                seen.add((nr,nc)); stack.append((nr,nc))
    for r,c in seen:
        if out[r][c]==0:
            out[r][c]=color
    return out


def solve_M46(g):
    out=clone(g)
    comps=components(g, colors={1})
    if not comps: return out
    comp=max(comps, key=lambda comp: len(comp["cells"]))
    r0,c0,r1,c1=comp["bbox"]
    for r,c in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
        out[r][c]=2
    return out


def solve_M47(g):
    out=clone(g)
    for comp in components(g, colors={2}):
        clo=orthogonal_closure(set(comp["cells"]))
        for r,c in clo:
            out[r][c]=3
    return out


def solve_M48(g):
    out=clone(g)
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    targets=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    k=sum(v==1 for row in g for v in row)
    if len(anchors)!=1 or len(targets)!=1 or k<1:
        return out
    ar,ac=anchors[0]; tr,tc=targets[0]
    comp=None
    for cc in components_multicolor(g,{2,3}):
        if (ar,ac) in cc["cells"]:
            comp=cc["cells"]; break
    if comp is None: return out
    offsets={(r-ar,c-ac) for r,c in comp}
    offsets=rot_offsets(offsets, k-1)
    for dr,dc in offsets:
        nr,nc=tr+dr, tc+dc
        if inb(g,nr,nc):
            out[nr][nc]=7
    return out


def solve_M49(g):
    h,w=dims(g)
    out=blank(h,w)
    candidates=[]
    for comp in components(g, colors={2}):
        holes=holes_for_component(comp)
        if len(holes)==1:
            candidates.append((len(comp["cells"]), holes[0]))
    if not candidates:
        return out
    # if multiple, choose largest one-hole component
    hole=max(candidates, key=lambda x:x[0])[1]
    for r,c in hole:
        out[r][c]=8
    return out


def solve_H43(g):
    h,w=dims(g)
    comps=components(g, colors={1})
    if not comps:
        return blank(h,w)
    k=sum(v==2 for row in g for v in row)
    t=sum(v==3 for row in g for v in row)
    targets=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    if not targets or not (1 <= k <= len(comps)) or not (1 <= t <= 4):
        return blank(h,w)
    tr,tc=targets[0]
    comps_sorted=sorted(comps, key=lambda comp: len(comp["cells"]))
    shape=normalize_top_left(comps_sorted[k-1]["cells"])
    shape=transform_shape(shape, t)
    out=blank(h,w)
    for r,c in shape:
        nr,nc=tr+r, tc+c
        if inb(out,nr,nc):
            out[nr][nc]=7
    return out


def solve_H44(g):
    out=clone(g)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v in {2,3}]
    dists={(r,c,v): bfs_dist(g,(r,c)) for r,c,v in seeds}
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==0:
                bestd=None; bestcolors=[]
                for sr,sc,color in seeds:
                    d=dists[(sr,sc,color)].get((r,c))
                    if d is None: 
                        continue
                    if bestd is None or d<bestd:
                        bestd=d; bestcolors=[color]
                    elif d==bestd:
                        bestcolors.append(color)
                if bestd is not None and len(set(bestcolors))==1:
                    out[r][c]=bestcolors[0]
    return out


def solve_H45(g):
    h,w=dims(g)
    out=blank(h,w)
    target=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8]
    if not target:
        return out
    tr,tc=target[0]
    red_comp=None; blue_comp=None; red_anchor=None; blue_anchor=None
    # find components with 9 and 2 or 1
    # components over {1,2,9} separated by zeros if distinct
    for comp in components_multicolor(g,{1,2,9}):
        vals={g[r][c] for r,c in comp["cells"]}
        if 9 in vals and 2 in vals and 1 not in vals:
            red_comp=comp["cells"]
            red_anchor=[(r,c) for r,c in comp["cells"] if g[r][c]==9][0]
        elif 9 in vals and 1 in vals and 2 not in vals:
            blue_comp=comp["cells"]
            blue_anchor=[(r,c) for r,c in comp["cells"] if g[r][c]==9][0]
    if red_comp is None or blue_comp is None:
        return out
    R={(r-red_anchor[0], c-red_anchor[1]) for r,c in red_comp}
    B={(r-blue_anchor[0], c-blue_anchor[1]) for r,c in blue_comp}
    X=(R ^ B)
    if (0,0) in X:
        X.remove((0,0))  # anchors cancel visually even if not
    for dr,dc in X:
        nr,nc=tr+dr, tc+dc
        if inb(out,nr,nc):
            out[nr][nc]=3
    return out


def solve_H46(g):
    out=clone(g)
    comps=[comp for comp in components(g, colors={4}) if set(comp["cells"])==frame_cells(*comp["bbox"])]
    if not comps:
        return out
    k=sum(v==2 for row in g for v in row)
    comps=sorted(comps, key=lambda comp: (comp["bbox"][2]-comp["bbox"][0]+1)*(comp["bbox"][3]-comp["bbox"][1]+1), reverse=True)
    if not (1 <= k <= len(comps)):
        return out
    cur=comps[k-1]["bbox"]
    nxt=comps[k]["bbox"] if k < len(comps) else None
    r0,c0,r1,c1=cur
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            if nxt is not None:
                nr0,nc0,nr1,nc1=nxt
                if nr0 <= r <= nr1 and nc0 <= c <= nc1:
                    continue
            if out[r][c]==0:
                out[r][c]=8
    return out


def solve_H47(g):
    out=clone(g)
    h,w=dims(g)
    k=sum(v==2 for row in g for v in row)
    cells={(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3}
    if not cells or k<1:
        return out
    shell=manhattan_shell(cells, k, h, w)
    for r,c in shell:
        if out[r][c]==0:
            out[r][c]=8
    return out


def solve_H48(g):
    out=clone(g)
    src=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    arr=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==1]
    if len(src)!=1 or len(arr)!=1:
        return out
    sr,sc=src[0]; ar,ac=arr[0]
    dr,dc=ar-sr, ac-sc
    # require adjacent orthogonal
    if abs(dr)+abs(dc)!=1:
        return out
    r,c=ar+dr, ac+dc
    steps=0
    while inb(g,r,c) and steps<500:
        steps+=1
        v=g[r][c]
        if v==5:
            break
        if v==3:
            dr,dc=slash_reflect(dr,dc)
        elif v==4:
            dr,dc=backslash_reflect(dr,dc)
        elif v==0:
            out[r][c]=8
        # cells 1/2/3/4 just pass through / reflect without coloring
        r,c=r+dr,c+dc
    return out


def solve_H49(g):
    out=clone(g)
    h,w=dims(g)
    mapping={}
    if h<3: return out
    for c in range(w):
        if g[0][c] !=0 and g[1][c] !=0:
            mapping[g[0][c]]=g[1][c]
    seen_global=set()
    for r in range(2,h):
        for c in range(w):
            v=g[r][c]
            if v in mapping and (r,c) not in seen_global:
                fill=mapping[v]
                stack=[(r,c)]
                seen={(r,c)}
                seen_global.add((r,c))
                while stack:
                    rr,cc=stack.pop()
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 2<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc] !=5:
                            # allow zeros and same label only; avoid spilling into other label colors maybe
                            if g[nr][nc]==0 or g[nr][nc]==v:
                                seen.add((nr,nc)); seen_global.add((nr,nc)); stack.append((nr,nc))
                for rr,cc in seen:
                    if out[rr][cc]==0:
                        out[rr][cc]=fill
    return out


SOLVERS = {
    'E43': solve_E43,
    'E44': solve_E44,
    'E45': solve_E45,
    'E46': solve_E46,
    'E47': solve_E47,
    'E48': solve_E48,
    'E49': solve_E49,
    'M43': solve_M43,
    'M44': solve_M44,
    'M45': solve_M45,
    'M46': solve_M46,
    'M47': solve_M47,
    'M48': solve_M48,
    'M49': solve_M49,
    'H43': solve_H43,
    'H44': solve_H44,
    'H45': solve_H45,
    'H46': solve_H46,
    'H47': solve_H47,
    'H48': solve_H48,
    'H49': solve_H49,
}



def solve_by_id(task_id: str, grid: Grid) -> Grid:
    return SOLVERS[task_id](grid)
