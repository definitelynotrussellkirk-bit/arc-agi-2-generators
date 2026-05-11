"""
ARC-style puzzle bank continuation 11: 21 more puzzles (E71-E77, M71-M77, H71-H77).

This batch leans into local completion, guide-vector motion, legend dispatch,
crop-and-rotate extraction, keyed prototype dictionaries, counted orbits,
dual-example composition, and path-distance coloring.

Notable motifs:
- guide_translate(object, marker_a, marker_b): M71
- prototype_dictionary_stamp(dictionary, query_keys): H72
- counted_orbit(anchor, shape, k): H73
- frame_library_dispatch(source_frames, target_keys): H74
- dual_example_compose(geom_pair, color_pair, query): H76
- nearest_seed_path(path, seed_a, seed_b): H77
"""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Callable, Iterable, List, Tuple

Grid = List[List[int]]

def blank(h:int,w:int,v:int=0)->Grid:
    return [[v]*w for _ in range(h)]

def dims(g:Grid)->Tuple[int,int]:
    return len(g), len(g[0])

def clone(g:Grid)->Grid:
    return [row[:] for row in g]

def bbox(cells):
    pts=list(cells); rs=[r for r,c in pts]; cs=[c for r,c in pts]
    return min(rs),max(rs),min(cs),max(cs)

def components(g:Grid, ignore=(0,)):
    h,w=dims(g); seen=set(); out=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in ignore or (r,c) in seen: 
                continue
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and g[nx][ny]==v:
                        seen.add((nx,ny)); q.append((nx,ny))
            out.append((v,cells))
    return out

def identity(g:Grid)->Grid:
    return clone(g)

def rot90(g:Grid)->Grid:
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rot180(g:Grid)->Grid:
    return [row[::-1] for row in g[::-1]]

def rot270(g:Grid)->Grid:
    return rot90(rot180(g))

def flip_h(g:Grid)->Grid:
    return [row[::-1] for row in g]

def flip_v(g:Grid)->Grid:
    return g[::-1]

def transpose(g:Grid)->Grid:
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]

def join_h(panels:List[Grid], sep:int=9)->Grid:
    h=max(len(p) for p in panels)
    pans=[]
    for p in panels:
        ph,pw=dims(p)
        if ph<h:
            q=blank(h,pw,0); q[:ph]=[row[:] for row in p]
            p=q
        pans.append(p)
    rows=[]
    for r in range(h):
        row=[]
        for i,p in enumerate(pans):
            row += p[r]
            if i!=len(pans)-1:
                row += [sep]
        rows.append(row)
    return rows

def split_by_sep_cols(g:Grid, sep:int=9)->List[Grid]:
    h,w=dims(g)
    sepcols=[c for c in range(w) if all(g[r][c]==sep for r in range(h))]
    parts=[]; start=0
    for c in sepcols+[w]:
        if c>start:
            parts.append([row[start:c] for row in g])
        start=c+1
    return parts

def split_by_sep_rows(g:Grid, sep:int=9)->List[Grid]:
    h,w=dims(g)
    seprows=[r for r in range(h) if all(v==sep for v in g[r])]
    parts=[]; start=0
    for r in seprows+[h]:
        if r>start:
            parts.append([row[:] for row in g[start:r]])
        start=r+1
    return parts

def infer_transform(a,b):
    for name,fn in TRANSFORMS.items():
        if fn(a)==b:
            return name
    raise ValueError("no transform")

def rotate_offset(dr,dc,k):
    for _ in range(k%4):
        dr,dc=dc,-dr
    return dr,dc

def apply_binop(a,b,op):
    h,w=dims(a)
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            aa=a[r][c]!=0; bb=b[r][c]!=0
            keep=False
            if op=="union":
                keep=aa or bb
            elif op=="intersection":
                keep=aa and bb
            elif op=="xor":
                keep=(aa != bb)
            elif op=="a_minus_b":
                keep=aa and not bb
            elif op=="b_minus_a":
                keep=bb and not aa
            if keep: out[r][c]=2
    return out

def infer_binop(a,b,out):
    for op in ["union","intersection","xor","a_minus_b","b_minus_a"]:
        if apply_binop(a,b,op)==out:
            return op
    raise ValueError("no op")

def infer_color_map(a,b):
    mapping={}
    h,w=dims(a)
    for r in range(h):
        for c in range(w):
            va,vb=a[r][c],b[r][c]
            if va!=0:
                mapping[va]=vb
    return mapping

def recolor(g,m):
    return [[m.get(v,v) if v!=0 else 0 for v in row] for row in g]

TRANSFORMS: dict[str, Callable[[Grid], Grid]] = {
    "identity": identity,
    "rot90": rot90,
    "rot180": rot180,
    "rot270": rot270,
    "flip_h": flip_h,
    "flip_v": flip_v,
    "transpose": transpose,
}

def solve_E71(g):
    out=clone(g)
    by=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==3:
            rs=sorted({r for r,c in cells}); cs=sorted({c for r,c in cells})
            if len(rs)==2 and len(cs)==2 and rs[1]-rs[0]==1 and cs[1]-cs[0]==1:
                for rr in rs:
                    for cc in cs:
                        out[rr][cc]=color
    return out

def solve_E72(g):
    out=clone(g); h,w=dims(g)
    for r in range(h):
        by=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                by[v].append(c)
        for color,cols in by.items():
            if len(cols)==2:
                a,b=min(cols),max(cols)
                if all(g[r][c]==0 for c in range(a+1,b)):
                    for c in range(a,b+1):
                        out[r][c]=color
    return out

def solve_E73(g):
    out=clone(g); h,w=dims(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0: continue
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            if vals[0]!=0 and all(v==vals[0] for v in vals):
                out[r][c]=vals[0]
    return out

def solve_E74(g):
    out=clone(g); h,w=dims(g)
    for r in range(h):
        for c in range(w):
            color=g[r][c]
            if color==0: continue
            nbrs=[]
            for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                rr,cc=r+dr,c+dc
                if 0<=rr<h and 0<=cc<w:
                    nbrs.append((rr,cc,g[rr][cc],dr,dc))
            same=[(rr,cc,dr,dc) for rr,cc,v,dr,dc in nbrs if v==color]
            if len(same)==3:
                dirs={(dr,dc) for rr,cc,dr,dc in same}
                for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    rr,cc=r+dr,c+dc
                    if 0<=rr<h and 0<=cc<w and (dr,dc) not in dirs and g[rr][cc]==0:
                        out[rr][cc]=color
    return out

def solve_E75(g):
    out=clone(g); h,w=dims(g)
    for r in range(1,h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][c]=g[0][c]
    return out

def solve_E76(g):
    comps=components(g)
    if not comps: return clone(g)
    v,cells=min(comps, key=lambda vc:(len(vc[1]), min(vc[1])))
    out=blank(*dims(g),0)
    for r,c in cells:
        out[r][c]=v
    return out

def solve_E77(g):
    out=clone(g)
    by=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                by[v].append((r,c))
    for color,cells in by.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            dr=r2-r1; dc=c2-c1
            if abs(dr)==abs(dc) and dr!=0:
                sr=1 if dr>0 else -1
                sc=1 if dc>0 else -1
                ok=True
                rr,cc=r1+sr,c1+sc
                while (rr,cc)!=(r2,c2):
                    if g[rr][cc]!=0:
                        ok=False; break
                    rr+=sr; cc+=sc
                if ok:
                    rr,cc=r1,c1
                    while True:
                        out[rr][cc]=color
                        if (rr,cc)==(r2,c2): break
                        rr+=sr; cc+=sc
    return out

def solve_M71(g):
    h,w=dims(g)
    pos8=pos9=None
    out=blank(h,w,0)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==8: pos8=(r,c)
            elif v==9: pos9=(r,c)
    dr=pos9[0]-pos8[0]; dc=pos9[1]-pos8[1]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,8,9):
                rr,cc=r+dr,c+dc
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=v
    return out

def solve_M72(g):
    out=clone(g); h,w=dims(g)
    palette=[v for v in g[0] if v!=0]
    body=[row[:] for row in g[1:]]
    comps=components(body, ignore=(0,))
    # comps coords in body space
    for v,cells in comps:
        if v!=7: 
            continue
        size=len(cells)
        if 1<=size<=len(palette):
            color=palette[size-1]
            for r,c in cells:
                out[r+1][c]=color
    return out

def solve_M73(g):
    code=g[0][0]
    # find frame color 5 bbox
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5]
    r0,r1,c0,c1=bbox(cells)
    inner=[row[c0+1:c1] for row in g[r0+1:r1]]
    if code==1:
        return inner
    elif code==2:
        return rot90(inner)
    elif code==3:
        return rot180(inner)
    elif code==4:
        return rot270(inner)
    else:
        return inner

def solve_M74(g):
    parts=split_by_sep_cols(g,9)
    mask,panel=parts
    h,w=dims(mask)
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            if mask[r][c]!=0:
                out[r][c]=panel[r][c]
    return out

def solve_M75(g):
    out=clone(g); h,w=dims(g)
    ar=ac=None
    cells=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==8: ar,ac=r,c
            elif v!=0:
                cells.append((r,c,v))
    for r,c,v in cells:
        rr,cc=2*ar-r, 2*ac-c
        if 0<=rr<h and 0<=cc<w:
            out[rr][cc]=v
    return out

def solve_M76(g):
    h,w=dims(g)
    anchor=None
    targets=[]
    offsets=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==8: anchor=(r,c)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v==1:
                targets.append((r,c))
            elif v not in (0,8):
                offsets.append((r-anchor[0], c-anchor[1], v))
    out=blank(h,w,0)
    for tr,tc in targets:
        for dr,dc,v in offsets:
            rr,cc=tr+dr, tc+dc
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=v
    return out

def solve_M77(g):
    cols=[c for c,v in enumerate(g[0]) if v==1]
    return [[row[c] for c in cols] for row in g[1:]]

def solve_H71(g):
    a,b,q=split_by_sep_cols(g,9)
    name=infer_transform(a,b)
    return TRANSFORMS[name](q)

def solve_H72(g):
    top,bottom=split_by_sep_rows(g,9)
    protos=split_by_sep_cols(top,9)
    patterns={}
    for p in protos:
        cells=[(r,c,v) for r,row in enumerate(p) for c,v in enumerate(row) if v!=0]
        # key is smallest color among cells? assume one key in {1,2,3}
        key=min(v for r,c,v in cells)
        anchors=[(r,c) for r,c,v in cells if v==key]
        assert len(anchors)==1
        ar,ac=anchors[0]
        patterns[key]=[(r-ar,c-ac,v) for r,c,v in cells]
    out=blank(*dims(bottom),0)
    h,w=dims(bottom)
    for r in range(h):
        for c,v in enumerate(bottom[r]):
            if v in patterns:
                for dr,dc,col in patterns[v]:
                    rr,cc=r+dr,c+dc
                    if 0<=rr<h and 0<=cc<w:
                        out[rr][cc]=col
    return out

def solve_H73(g):
    h,w=dims(g)
    k=sum(1 for v in g[0] if v==1)
    ar=ac=None
    cells=[]
    for r in range(1,h):
        for c,v in enumerate(g[r]):
            if v==9: ar,ac=r,c
            elif v!=0:
                cells.append((r,c,v))
    out=blank(h,w,0)
    out[ar][ac]=9
    for r,c,v in cells:
        dr,dc=r-ar,c-ac
        for t in range(k):
            rr_off,cc_off=rotate_offset(dr,dc,t)
            rr,cc=ar+rr_off, ac+cc_off
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=v
    return out

def solve_H74(g):
    top,bottom=split_by_sep_rows(g,9)
    src_panels=split_by_sep_cols(top,9)
    tgt_panels=split_by_sep_cols(bottom,9)
    patterns={}
    for p in src_panels:
        key=next(v for v in p[0] if v!=0)
        frame=p[1:]
        frame_cells=[(r,c) for r,row in enumerate(frame) for c,v in enumerate(row) if v==5]
        r0,r1,c0,c1=bbox(frame_cells)
        interior=[row[c0+1:c1] for row in frame[r0+1:r1]]
        patterns[key]=interior
    filled=[]
    for p in tgt_panels:
        key=next(v for v in p[0] if v!=0)
        frame=clone(p[1:])
        frame_cells=[(r,c) for r,row in enumerate(frame) for c,v in enumerate(row) if v==5]
        r0,r1,c0,c1=bbox(frame_cells)
        interior=patterns[key]
        # place interior into frame
        for r in range(len(interior)):
            for c in range(len(interior[0])):
                frame[r0+1+r][c0+1+c]=interior[r][c]
        filled.append(frame)
    return join_h(filled, sep=9)

def solve_H75(g):
    a,b,o,q1,q2=split_by_sep_cols(g,9)
    op=infer_binop(a,b,o)
    return apply_binop(q1,q2,op)

def solve_H76(g):
    gin,gout,cin,cout,q=split_by_sep_cols(g,9)
    tname=infer_transform(gin,gout)
    cmap=infer_color_map(cin,cout)
    return recolor(TRANSFORMS[tname](q), cmap)

def solve_H77(g):
    h,w=dims(g)
    # path cells are 1 plus seed cells 2 and 3 are part of graph
    seeds={}
    graph_cells=[]
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v in (1,2,3):
                graph_cells.append((r,c))
                if v in (2,3): seeds[v]=(r,c)
    # bfs distances along graph where traversable if cell in 1,2,3
    def bfs(start):
        dist={start:0}
        q=deque([start])
        while q:
            r,c=q.popleft()
            for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                rr,cc=r+dr,c+dc
                if 0<=rr<h and 0<=cc<w and (rr,cc) not in dist and g[rr][cc] in (1,2,3):
                    dist[(rr,cc)]=dist[(r,c)]+1
                    q.append((rr,cc))
        return dist
    d2=bfs(seeds[2]); d3=bfs(seeds[3])
    out=blank(h,w,0)
    for r,c in graph_cells:
        if g[r][c]==2: out[r][c]=2
        elif g[r][c]==3: out[r][c]=3
        else:
            a,b=d2[(r,c)],d3[(r,c)]
            out[r][c]=2 if a<b else 3 if b<a else 4
    return out

SOLVERS = {

    "E71": solve_E71,

    "E72": solve_E72,

    "E73": solve_E73,

    "E74": solve_E74,

    "E75": solve_E75,

    "E76": solve_E76,

    "E77": solve_E77,

    "M71": solve_M71,

    "M72": solve_M72,

    "M73": solve_M73,

    "M74": solve_M74,

    "M75": solve_M75,

    "M76": solve_M76,

    "M77": solve_M77,

    "H71": solve_H71,

    "H72": solve_H72,

    "H73": solve_H73,

    "H74": solve_H74,

    "H75": solve_H75,

    "H76": solve_H76,

    "H77": solve_H77,

}
