"""
ARC-style puzzle bank continuation 22: 21 more puzzles (E148-E154, M148-M154, H148-H154).

This batch leans into header-driven emitters, stencil extraction, anchor-relative motion,
transform analogy, support-delta transfer, embedded operation inference,
family matching under symmetry, and transform-shadow unions.

Notable motifs:
- anchor_rebase(shape, src, dst): M148
- support_delta_transfer(A, B, C): H149
- embedded_op_dispatch(example_left, example_right, example_out, target_left, target_right): H152
- family_match_under_symmetry(query, candidates): H151
- shadow_union_analogy(A, B, C): H154
"""

from __future__ import annotations
from collections import deque, Counter
from typing import List

Grid = List[List[int]]

def blank(h,w,v=0): return [[v]*w for _ in range(h)]

def clone(g): return [row[:] for row in g]

def dims(g): return len(g), len(g[0])

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def crop_bbox(g, ignore=(0,)):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v not in ignore]
    if not cells: return [[0]]
    r0,r1,c0,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_component(g, cells):
    r0,r1,c0,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in cells: out[r-r0][c-c0]=g[r][c]
    return out

def cc(g, ignore=(0,), same_color=True):
    h,w=dims(g)
    seen=set(); out=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in seen or g[r][c] in ignore: continue
            color=g[r][c]
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and (nx,ny) not in seen and g[nx][ny] not in ignore and ((not same_color) or g[nx][ny]==color):
                        seen.add((nx,ny)); q.append((nx,ny))
            out.append((color,cells))
    return out

def rot90(g): return [list(row) for row in zip(*g[::-1])]
def rot180(g): return [row[::-1] for row in g[::-1]]
def rot270(g): return [list(row) for row in zip(*g)][::-1]
def flip_h(g): return [row[::-1] for row in g]
def flip_v(g): return g[::-1]
def transpose(g): return [list(row) for row in zip(*g)]

def anti_transpose(g):
    h,w=dims(g); out=blank(w,h)
    for r in range(h):
        for c in range(w):
            out[w-1-c][h-1-r]=g[r][c]
    return out

def all_transforms(g):
    return {
        "id": g,
        "rot90": rot90(g),
        "rot180": rot180(g),
        "rot270": rot270(g),
        "flip_h": flip_h(g),
        "flip_v": flip_v(g),
        "transpose": transpose(g),
        "anti_transpose": anti_transpose(g),
    }

def split_by_full_sep_cols(g, sep=8):
    h,w=dims(g)
    seps=[c for c in range(w) if all(g[r][c]==sep for r in range(h))]
    parts=[]; start=0
    for c in seps+[w]:
        parts.append([row[start:c] for row in g])
        start=c+1
    return parts

def normalize_support(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells: return frozenset()
    r0,r1,c0,c1=bbox(cells)
    return frozenset((r-r0,c-c0) for r,c in cells)

def recolor(g,mapping):
    return [[mapping.get(v,v) if v!=0 else 0 for v in row] for row in g]

def dominant_nonzero_color(g):
    cnt=Counter(v for row in g for v in row if v!=0)
    return cnt.most_common(1)[0][0] if cnt else 1

def op_union(A,B,color=1):
    h,w=dims(A); out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if A[r][c]!=0 or B[r][c]!=0: out[r][c]=color
    return out

def op_intersection(A,B,color=1):
    h,w=dims(A); out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if A[r][c]!=0 and B[r][c]!=0: out[r][c]=color
    return out

def op_xor(A,B,color=1):
    h,w=dims(A); out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if (A[r][c]!=0) ^ (B[r][c]!=0): out[r][c]=color
    return out

OPS = {"union": op_union, "intersection": op_intersection, "xor": op_xor}

def join_panels(parts, sep=8):
    h=max(len(p) for p in parts)
    out=[]
    for r in range(h):
        row=[]
        for i,p in enumerate(parts):
            prow=p[r] if r < len(p) else [0]*len(p[0])
            row+=prow
            if i!=len(parts)-1: row+=[sep]
        out.append(row)
    return out


def solve_E148(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for c,color in enumerate(grid[0]):
        if color!=0:
            k=0
            while k<h and c+k<w:
                out[k][c+k]=color
                k+=1
    return out



def solve_E149(grid):
    h,w=dims(grid)
    out=clone(grid)
    fills=[]
    for r in range(h-1):
        for c in range(w-1):
            cells=[grid[r+i][c+j] for i in range(2) for j in range(2)]
            nz=[v for v in cells if v!=0]
            if len(nz)==3 and len(set(nz))==1 and cells.count(0)==1:
                idx=cells.index(0)
                dr,dc=divmod(idx,2)
                fills.append((r+dr,c+dc,nz[0]))
    for r,c,v in fills:
        out[r][c]=v
    return out



def solve_E150(grid):
    h,w=dims(grid)
    cells=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    if not cells: return clone(grid)
    shift=(h-1)-max(r for r,c,v in cells)
    out=blank(h,w)
    for r,c,v in cells:
        out[r+shift][c]=v
    return out



def solve_E151(grid):
    h,w=dims(grid)
    key=None
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                key=grid[r][c]
                break
        if key is not None: break
    out=blank(h,w)
    if key is None: return out
    for r in range(h):
        for c in range(w):
            if grid[r][c]==key: out[r][c]=key
    return out



def solve_E152(grid):
    cells=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    if not cells: return clone(grid)
    r0,r1,c0,c1=bbox(cells)
    color=next(v for row in grid for v in row if v!=0)
    out=blank(*dims(grid))
    for c in range(c0,c1+1):
        out[r0][c]=color
        out[r1][c]=color
    for r in range(r0,r1+1):
        out[r][c0]=color
        out[r][c1]=color
    return out



def solve_E153(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r,row in enumerate(grid):
        vals=[v for v in row if v!=0]
        for i,v in enumerate(vals):
            out[r][i]=v
    return out



def solve_E154(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                for dr,dc in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out



def solve_M148(grid):
    h,w=dims(grid)
    src=dst=None
    obj=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==1: src=(r,c)
            elif v==2: dst=(r,c)
            elif v!=0: obj.append((r,c,v))
    dr,dc=dst[0]-src[0], dst[1]-src[1]
    out=blank(h,w)
    for r,c,v in obj:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out



def solve_M149(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    for name,T in all_transforms(A).items():
        if T==B:
            return all_transforms(C)[name]
    raise ValueError("no transform match")



def solve_M150(grid):
    k=sum(1 for v in grid[0] if v!=0)
    body=[row[:] for row in grid[1:]]
    comps=cc(body, ignore=(0,), same_color=True)
    comps_sorted=sorted(comps, key=lambda t: (-len(t[1]), bbox(t[1])[0], bbox(t[1])[2]))
    color,cells=comps_sorted[k-1]
    return crop_component(body, cells)



def solve_M151(grid):
    left,right = split_by_full_sep_cols(grid, sep=8)
    h,w=dims(left)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if left[r][c]!=0 and right[r][c]!=0:
                out[r][c]=right[r][c]
    return crop_bbox(out)



def solve_M152(grid):
    h,w=dims(grid)
    anchor=None
    objs=[]
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v==9: anchor=(r,c)
            elif v!=0: objs.append((r,c,v))
    ar,ac=anchor
    out=blank(h,w)
    out[ar][ac]=9
    for r,c,v in objs:
        dr,dc = r-ar, c-ac
        nr,nc = ar+dc, ac-dr
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out



def solve_M153(grid):
    A,B = split_by_full_sep_cols(grid, sep=8)
    h,w=dims(A)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            av,bv=A[r][c], B[r][c]
            if (av!=0) ^ (bv!=0):
                out[r][c]=av if av!=0 else bv
    return out



def solve_M154(grid):
    h,w=dims(grid)
    seeds=[]; out=blank(h,w)
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0 and v!=5:
                seeds.append((r,c,v))
                out[r][c]=v
    for r in range(h):
        for c in range(w):
            if grid[r][c]==5:
                best=min(seeds, key=lambda t: (abs(r-t[0])+abs(c-t[1]), t[2], t[0], t[1]))
                out[r][c]=best[2]
    return out



def solve_H148(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    for name,TA in all_transforms(A).items():
        if dims(TA)!=dims(B): continue
        mapping={}; ok=True
        for r in range(len(TA)):
            for c in range(len(TA[0])):
                a,b = TA[r][c], B[r][c]
                if a==0 and b==0: continue
                if (a==0)!=(b==0):
                    ok=False; break
                if a in mapping and mapping[a]!=b:
                    ok=False; break
                mapping[a]=b
            if not ok: break
        if ok:
            return recolor(all_transforms(C)[name], mapping)
    raise ValueError("no transform/color-map match")



def solve_H149(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    Acells=[(r,c) for r,row in enumerate(A) for c,v in enumerate(row) if v!=0]
    Ccells=[(r,c) for r,row in enumerate(C) for c,v in enumerate(row) if v!=0]
    if not Acells or not Ccells: return clone(C)
    ar0,ar1,ac0,ac1 = bbox(Acells)
    cr0,cr1,cc0,cc1 = bbox(Ccells)
    ah,aw = ar1-ar0+1, ac1-ac0+1
    ch,cw = cr1-cr0+1, cc1-cc0+1
    if (ah,aw)!=(ch,cw):
        raise ValueError("bbox mismatch")
    tcolor=dominant_nonzero_color([row[cc0:cc1+1] for row in C[cr0:cr1+1]])
    out=clone(C)
    for dr in range(ah):
        for dc in range(aw):
            a_non = A[ar0+dr][ac0+dc] != 0
            b_non = B[ar0+dr][ac0+dc] != 0
            if a_non and not b_non:
                out[cr0+dr][cc0+dc]=0
            elif (not a_non) and b_non:
                out[cr0+dr][cc0+dc]=tcolor
    return out



def solve_H150(grid):
    tokens=[v for v in grid[0] if v!=0]
    shape=crop_bbox([row[:] for row in grid[1:]])
    for t in tokens:
        if t==1: shape=rot90(shape)
        elif t==2: shape=flip_h(shape)
        elif t==3: shape=flip_v(shape)
        elif t==4: shape=transpose(shape)
        else: raise ValueError("unknown token")
    return shape



def solve_H151(grid):
    query,cands = split_by_full_sep_cols(grid, sep=8)
    qcolor=next(v for row in query for v in row if v!=0)
    qcrop=crop_bbox(query)
    qsupports={normalize_support(T) for T in all_transforms(qcrop).values()}
    comps=cc(cands, ignore=(0,), same_color=True)
    for color,cells in comps:
        cand_crop=crop_component(cands, cells)
        if normalize_support(cand_crop) in qsupports:
            return [[qcolor if v!=0 else 0 for v in row] for row in cand_crop]
    raise ValueError("no matching candidate")



def solve_H152(grid):
    EA,EB,EO,TA,TB = split_by_full_sep_cols(grid, sep=8)
    opname=None
    ex_color=dominant_nonzero_color(EO)
    for name,fn in OPS.items():
        if fn(EA,EB,ex_color)==EO:
            opname=name
            break
    if opname is None: raise ValueError("no embedded operation match")
    tcolor=dominant_nonzero_color(TA)
    return OPS[opname](TA,TB,tcolor)



def solve_H153(grid):
    k=sum(1 for v in grid[0] if v!=0)
    body=[row[:] for row in grid[1:]]
    h,w=dims(body)
    anchor=None; objs=[]
    for r in range(h):
        for c in range(w):
            v=body[r][c]
            if v==9: anchor=(r,c)
            elif v!=0: objs.append((r,c,v))
    ar,ac=anchor
    out=blank(h,w); out[ar][ac]=9
    for r,c,v in objs:
        dr,dc=r-ar,c-ac
        pos=[(dr,dc),(dc,-dr),(-dr,-dc),(-dc,dr)]
        for idx in range(min(k,4)):
            rr,cc=pos[idx]
            nr,nc=ar+rr, ac+cc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out



def solve_H154(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    A_sup=[[1 if v!=0 else 0 for v in row] for row in A]
    B_sup=[[1 if v!=0 else 0 for v in row] for row in B]
    match=None
    for name,T in all_transforms(A_sup).items():
        if T==B_sup:
            match=name
            break
    if match is None: raise ValueError("no support transform match")
    TC=all_transforms(C)[match]
    out=clone(C)
    for r in range(len(C)):
        for c in range(len(C[0])):
            if TC[r][c]!=0:
                out[r][c]=TC[r][c]
    return out
