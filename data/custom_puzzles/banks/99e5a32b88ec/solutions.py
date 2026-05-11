"""
ARC-style puzzle bank continuation 23: 21 more puzzles (E155-E161, M155-M161, H155-H161).

This batch leans into row/anchor emitters, hinge reflection, palette-by-size recoloring,
corridor sweeps, room filling, cutout transfer, panel-transform inference,
support-edit transfer, binary-op inference, counted orbits, recolor-stencil replay,
and two-stage transform composition.

Notable motifs:
- hinge_reflect(object, pivot): M155
- corridor_sweep_right(shape, walls): M157
- support_edit_transfer(A, B, C): H156
- counted_orbit(shape, pivot, k): H159
- recolor_stencil_replay(A, B, C): H160
- two_stage_dispatch(A_to_B, C_to_D, X): H161
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

TRANSFORM_NAMES = ["id","rot90","rot180","rot270","flip_h","flip_v","transpose","anti_transpose"]

def transform_by_name(name, g):
    return all_transforms(g)[name]

def split_by_full_sep_cols(g, sep=8):
    h,w=dims(g)
    seps=[c for c in range(w) if all(g[r][c]==sep for r in range(h))]
    parts=[]; start=0
    for c in seps+[w]:
        parts.append([row[start:c] for row in g])
        start=c+1
    return parts

def join_panels(parts, sep=8):
    h=max(len(p) for p in parts)
    out=[]
    for r in range(h):
        row=[]
        for i,p in enumerate(parts):
            prow=p[r] if r < len(p) else [0]*len(p[0])
            row += prow
            if i != len(parts)-1:
                row += [sep]
        out.append(row)
    return out

def normalize_support(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells: return frozenset()
    r0,r1,c0,c1=bbox(cells)
    return frozenset((r-r0,c-c0) for r,c in cells)

def dominant_nonzero_color(g):
    cnt=Counter(v for row in g for v in row if v!=0)
    return cnt.most_common(1)[0][0] if cnt else 1

def recolor(g, color):
    return [[color if v!=0 else 0 for v in row] for row in g]

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

def op_left_minus(A,B,color=1):
    h,w=dims(A); out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if A[r][c]!=0 and B[r][c]==0: out[r][c]=color
    return out

OPS = {
    "union": op_union,
    "intersection": op_intersection,
    "xor": op_xor,
    "left_minus": op_left_minus,
}


def solve_E155(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r in range(h):
        color=grid[r][0]
        if color!=0:
            for c in range(w):
                out[r][c]=color
    return out



def solve_E156(grid):
    h,w=dims(grid)
    out=clone(grid)
    for r in range(h):
        for c in range(w-2):
            a,b,d=grid[r][c],grid[r][c+1],grid[r][c+2]
            if a!=0 and a==d and b==0:
                out[r][c+1]=a
    return out



def solve_E157(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for c,color in enumerate(grid[h-1]):
        if color!=0:
            k=0
            while h-1-k>=0 and c-k>=0:
                out[h-1-k][c-k]=color
                k+=1
    return out



def solve_E158(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for color,cells in cc(grid, ignore=(0,), same_color=True):
        if any(r in (0,h-1) or c in (0,w-1) for r,c in cells):
            for r,c in cells:
                out[r][c]=color
    return out



def solve_E159(grid):
    h,w=dims(grid)
    out=clone(grid)
    for r,row in enumerate(grid):
        pos={}
        for c,v in enumerate(row):
            if v!=0:
                pos.setdefault(v,[]).append(c)
        for color,cols in pos.items():
            if len(cols)>=2:
                for c in range(min(cols), max(cols)+1):
                    out[r][c]=color
    return out



def solve_E160(grid):
    h,w=dims(grid)
    out=blank(h,w)
    for r,row in enumerate(grid):
        header=row[0]
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=header if header!=0 else v
    return out



def solve_E161(grid):
    h,w=dims(grid)
    out=clone(grid)
    for r,row in enumerate(grid):
        anchors=[c for c,v in enumerate(row) if v==9]
        if not anchors:
            continue
        a=anchors[0]
        for c,v in enumerate(row):
            if v!=0 and v!=9:
                mc=2*a-c
                if 0<=mc<w:
                    out[r][mc]=v
        out[r][a]=9
    return out



def solve_M155(grid):
    h,w=dims(grid)
    pivot=None
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                pivot=(r,c); break
        if pivot is not None: break
    pr,pc=pivot
    obj=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c] not in (0,9)]
    out=clone(grid)
    if not obj:
        return out
    rs=[r for r,c,v in obj]; cs=[c for r,c,v in obj]
    if max(cs) < pc:
        for r,c,v in obj:
            mc=2*pc-c
            if 0<=mc<w: out[r][mc]=v
    elif min(cs) > pc:
        for r,c,v in obj:
            mc=2*pc-c
            if 0<=mc<w: out[r][mc]=v
    elif max(rs) < pr:
        for r,c,v in obj:
            mr=2*pr-r
            if 0<=mr<h: out[mr][c]=v
    elif min(rs) > pr:
        for r,c,v in obj:
            mr=2*pr-r
            if 0<=mr<h: out[mr][c]=v
    return out



def solve_M156(grid):
    h,w=dims(grid)
    palette=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    comps=cc(body, ignore=(0,), same_color=True)
    comps=sorted(comps, key=lambda x: len(x[1]))
    out=blank(h,w)
    out[0]=grid[0][:]
    for (old_color,cells), new_color in zip(comps, palette):
        for r,c in cells:
            out[r+1][c]=new_color
    return out



def solve_M157(grid):
    h,w=dims(grid)
    out=clone(grid)
    for r in range(h):
        wall_cols=[c for c,v in enumerate(grid[r]) if v==8]
        for c,v in enumerate(grid[r]):
            if v!=0 and v!=8:
                stop=min([wc for wc in wall_cols if wc>c], default=w)
                for x in range(c, stop):
                    if out[r][x]==0:
                        out[r][x]=v
    return out



def solve_M158(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    tname=None
    for name in TRANSFORM_NAMES:
        if transform_by_name(name, A)==B:
            tname=name; break
    return transform_by_name(tname, C)



def solve_M159(grid):
    h,w=dims(grid)
    src=dst=None
    obj=[]
    for r in range(h):
        for c,v in enumerate(grid[r]):
            if v==3: src=(r,c)
            elif v==4: dst=(r,c)
            elif v not in (0,3,4):
                obj.append((r,c,v))
    dr,dc=dst[0]-src[0], dst[1]-src[1]
    out=blank(h,w)
    sr,sc=src; tr,tc=dst
    out[sr][sc]=3; out[tr][tc]=4
    for r,c,v in obj:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            out[nr][nc]=v
    return out



def solve_M160(grid):
    h,w=dims(grid)
    out=clone(grid)
    seeds=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v not in (0,8)]
    for sr,sc,color in seeds:
        q=deque([(sr,sc)]); seen={(sr,sc)}
        while q:
            r,c=q.popleft()
            out[r][c]=color
            for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and grid[nr][nc]!=8:
                    seen.add((nr,nc)); q.append((nr,nc))
    return out



def solve_M161(grid):
    comps=cc(grid, ignore=(0,), same_color=True)
    if len(comps)!=2:
        return clone(grid)
    comps_sorted=sorted(comps, key=lambda x: min(c for r,c in x[1]))
    (c1,cells1),(c2,cells2)=comps_sorted
    r01,r11,c01,c11=bbox(cells1)
    r02,r12,c02,c12=bbox(cells2)
    mask={(r-r01,c-c01) for r,c in cells1}
    out=blank(*dims(grid))
    for r,c in cells1:
        out[r][c]=c1
    for r in range(r02,r12+1):
        for c in range(c02,c12+1):
            if (r-r02,c-c02) in mask:
                out[r][c]=c2
    return out



def solve_H155(grid):
    target=next(v for v in grid[0] if v!=0)
    body=grid[1:]
    A,B,C = split_by_full_sep_cols(body, sep=8)
    tname=None
    for name in TRANSFORM_NAMES:
        if transform_by_name(name, A)==B:
            tname=name; break
    out=transform_by_name(tname, C)
    return recolor(out, target)



def solve_H156(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    A0=crop_bbox(A); B0=crop_bbox(B); C0=crop_bbox(C)
    ha,wa=dims(A0); hb,wb=dims(B0); hc,wc=dims(C0)
    if (ha,wa)!=(hb,wb) or (ha,wa)!=(hc,wc):
        return C0
    SA={(r,c) for r,row in enumerate(A0) for c,v in enumerate(row) if v!=0}
    SB={(r,c) for r,row in enumerate(B0) for c,v in enumerate(row) if v!=0}
    SC={(r,c) for r,row in enumerate(C0) for c,v in enumerate(row) if v!=0}
    add=SB-SA
    remove=SA-SB
    new=(SC-remove)|add
    color=dominant_nonzero_color(C0)
    out=blank(ha,wa)
    for r,c in new:
        out[r][c]=color
    return out



def solve_H157(grid):
    A,B,O,X,Y = split_by_full_sep_cols(grid, sep=8)
    opname=None
    for name,op in OPS.items():
        if op(A,B)==O:
            opname=name; break
    return OPS[opname](X,Y)



def solve_H158(grid):
    target=next(v for v in grid[0] if v!=0)
    body=grid[1:]
    Q,C1,C2,C3 = split_by_full_sep_cols(body, sep=8)
    q_support=normalize_support(Q)
    for cand in [C1,C2,C3]:
        for name in TRANSFORM_NAMES:
            tc=transform_by_name(name, cand)
            if normalize_support(tc)==q_support:
                return recolor(tc, target)
    return [[0]]



def solve_H159(grid):
    h,w=dims(grid)
    k=sum(1 for v in grid[0] if v!=0)
    body=[row[:] for row in grid[1:]]
    pr=pc=None
    obj=[]
    for r in range(len(body)):
        for c,v in enumerate(body[r]):
            if v==9:
                pr,pc=r,c
            elif v not in (0,1):
                obj.append((r,c,v))
    out=blank(h,w)
    out[0]=grid[0][:]
    out[pr+1][pc]=9
    def rot(dr,dc,t):
        for _ in range(t):
            dr,dc = dc,-dr
        return dr,dc
    for t in range(k):
        for r,c,v in obj:
            dr,dc=r-pr,c-pc
            nr,nc=rot(dr,dc,t)
            rr,cc=pr+nr,pc+nc
            if 0<=rr<len(body) and 0<=cc<w:
                out[rr+1][cc]=v
    return out



def solve_H160(grid):
    A,B,C = split_by_full_sep_cols(grid, sep=8)
    A0=crop_bbox(A); B0=crop_bbox(B); C0=crop_bbox(C)
    ha,wa=dims(A0); hb,wb=dims(B0); hc,wc=dims(C0)
    if (ha,wa)!=(hb,wb) or (ha,wa)!=(hc,wc):
        return C0
    accent_positions=[]
    accent_color=None
    for r in range(ha):
        for c in range(wa):
            if A0[r][c]!=0 and B0[r][c]!=0 and A0[r][c]!=B0[r][c]:
                accent_positions.append((r,c))
                accent_color=B0[r][c]
    base=dominant_nonzero_color(C0)
    out=[[base if v!=0 else 0 for v in row] for row in C0]
    for r,c in accent_positions:
        if out[r][c]!=0:
            out[r][c]=accent_color
    return out



def solve_H161(grid):
    A,B,C,D,X = split_by_full_sep_cols(grid, sep=8)
    t1=t2=None
    for name in TRANSFORM_NAMES:
        if transform_by_name(name, A)==B:
            t1=name; break
    first=transform_by_name(t1, X)
    for name in TRANSFORM_NAMES:
        if transform_by_name(name, C)==D:
            t2=name; break
    return transform_by_name(t2, first)
