"""Reference helper library and 21 reference solve functions for the thirteenth custom ARC puzzle bank.

New primitive introduced in this set:
  describe_components(grid, connectivity=4)
Return the non-zero connected components together with feature records such as
area, bounding-box size, hole count, symmetry flags, perimeter, and whether
the component touches the border. This makes feature-driven ARC tasks explicit:
selection by holes or symmetry, area/perimeter ranking, feature analogies, and
small symbolic outputs built from object descriptors.

All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 13.
"""
from typing import List
from collections import Counter

Grid = List[List[int]]
dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]
dirs8 = dirs4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def copyg(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def components(grid, colors=None, connectivity=4, include_zero=False):
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    dirs = dirs4 if connectivity==4 else dirs8
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            v=grid[r][c]
            if v==0 and not include_zero:
                continue
            if colors is not None and v not in colors:
                continue
            stack=[(r,c)]
            cells=[(r,c)]
            while stack:
                rr,cc=stack.pop()
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and grid[nr][nc]==v:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color":v,"cells":cells})
    return out

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_mask(cells):
    r1,c1,r2,c2=bbox(cells)
    h,w=r2-r1+1,c2-c1+1
    m=blank(h,w,0)
    for r,c in cells:
        m[r-r1][c-c1]=1
    return m

def count_holes_mask(mask):
    h,w=dims(mask)
    seen=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if seen[r][c] or mask[r][c]==1:
                continue
            seen[r][c]=True
            q=[(r,c)]
            cells=[(r,c)]
            border = r in (0,h-1) or c in (0,w-1)
            while q:
                rr,cc=q.pop()
                for dr,dc in dirs4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and mask[nr][nc]==0:
                        seen[nr][nc]=True
                        q.append((nr,nc))
                        cells.append((nr,nc))
                        if nr in (0,h-1) or nc in (0,w-1):
                            border=True
            if not border:
                holes += 1
    return holes

def perimeter(cells):
    s=set(cells)
    p=0
    for r,c in s:
        for dr,dc in dirs4:
            if (r+dr,c+dc) not in s:
                p+=1
    return p

def symmetry_bits(cells):
    m=crop_mask(cells)
    h,w=dims(m)
    sym_h = all(m[r][c]==m[h-1-r][c] for r in range(h) for c in range(w))
    sym_v = all(m[r][c]==m[r][w-1-c] for r in range(h) for c in range(w))
    return sym_h, sym_v

def describe_components(grid, connectivity=4):
    h,w=dims(grid)
    comps=components(grid, connectivity=connectivity)
    out=[]
    for comp in comps:
        cells=comp["cells"]
        r1,c1,r2,c2=bbox(cells)
        mask=crop_mask(cells)
        holes=count_holes_mask(mask)
        sym_h,sym_v=symmetry_bits(cells)
        out.append({
            "color": comp["color"],
            "cells": cells,
            "area": len(cells),
            "bbox": (r1,c1,r2,c2),
            "height": r2-r1+1,
            "width": c2-c1+1,
            "holes": holes,
            "sym_h": sym_h,
            "sym_v": sym_v,
            "sym_count": int(sym_h)+int(sym_v),
            "touches_border": any(r in (0,h-1) or c in (0,w-1) for r,c in cells),
            "perimeter": perimeter(cells),
        })
    return out

def blank_like(g,v=0):
    h,w=dims(g); return blank(h,w,v)

def filter_same_size(grid, pred, recolor=None):
    desc=describe_components(grid)
    out=blank_like(grid,0)
    for comp in desc:
        if pred(comp):
            color = recolor if recolor is not None else comp["color"]
            for r,c in comp["cells"]:
                out[r][c]=color
    return out

def recolor_same_size(grid, pred, new_color):
    out=copyg(grid)
    desc=describe_components(grid)
    for comp in desc:
        if pred(comp):
            for r,c in comp["cells"]:
                out[r][c]=new_color
    return out

def crop_component(comp, recolor=8):
    r1,c1,r2,c2 = comp["bbox"]
    out=blank(r2-r1+1, c2-c1+1, 0)
    for r,c in comp["cells"]:
        out[r-r1][c-c1]=recolor
    return out

def top_left(comp):
    r1,c1,_,_=comp['bbox']; return (r1,c1)

def sym_class(comp):
    if comp["sym_h"] and comp["sym_v"]:
        return "both"
    if comp["sym_h"]:
        return "h"
    if comp["sym_v"]:
        return "v"
    return "none"

def feature_triple(comp):
    return (comp["area"], comp["holes"], sym_class(comp))

def split_panels(grid, sep_color=5):
    h,w=dims(grid)
    sep_cols=[c for c in range(w) if all(grid[r][c]==sep_color for r in range(h))]
    # assume vertical separators only
    starts=[0]
    for c in sep_cols:
        if starts[-1]!=c+1:
            starts.append(c+1)
    # easier: intervals between sep cols
    cols=[-1]+sep_cols+[w]
    panels=[]
    for a,b in zip(cols, cols[1:]):
        l=a+1; r=b-1
        if l<=r:
            panels.append([row[l:r+1] for row in grid])
    return panels, [(a+1,b-1) for a,b in zip(cols, cols[1:]) if a+1<=b-1]

def solve_S13_E1(grid):
    return recolor_same_size(grid, lambda comp: comp["holes"] > 0, 8)

def solve_S13_E2(grid):
    return filter_same_size(grid, lambda comp: comp["touches_border"])

def solve_S13_E3(grid):
    desc=describe_components(grid)
    target=max(desc, key=lambda comp: (comp["width"], comp["area"], -top_left(comp)[0], -top_left(comp)[1]))
    return crop_component(target, 8)

def solve_S13_E4(grid):
    return recolor_same_size(grid, lambda comp: comp["sym_h"], 8)

def solve_S13_E5(grid):
    desc=describe_components(grid)
    target=next(comp for comp in sorted(desc, key=top_left) if comp["holes"]==1)
    return crop_component(target, 8)

def solve_S13_E6(grid):
    desc=[comp for comp in describe_components(grid) if comp["sym_count"]==0]
    target=min(desc, key=lambda comp: (comp["area"], comp["perimeter"], top_left(comp)))
    return crop_component(target, 8)

def solve_S13_E7(grid):
    return recolor_same_size(grid, lambda comp: comp["height"] > comp["width"], 8)

def solve_S13_M1(grid):
    k = sum(1 for v in grid[0] if v == 1)
    body = [row[:] for row in grid[1:]]
    desc=describe_components(body)
    desc=sorted(desc, key=lambda comp: (-comp["area"], top_left(comp)))
    target=desc[k-1]
    return crop_component(target, 8)

def solve_S13_M2(grid):
    desc=describe_components(grid)
    seed=next(comp for comp in desc if comp["color"]==1)
    feat=feature_triple(seed)
    out=copyg(grid)
    for comp in desc:
        if comp is seed:
            continue
        if feature_triple(comp)==feat:
            for r,c in comp["cells"]:
                out[r][c]=8
    return out

def solve_S13_M3(grid):
    code=sum(1 for v in grid[0] if v==1)
    wanted = {1:"v", 2:"h", 3:"both", 4:"none"}[code]
    body=[row[:] for row in grid[1:]]
    desc=describe_components(body)
    target=next(comp for comp in sorted(desc, key=top_left) if sym_class(comp)==wanted)
    return crop_component(target, 8)

def solve_S13_M4(grid):
    desc=sorted(describe_components(grid), key=top_left)
    return [[comp["area"] for comp in desc]]

def solve_S13_M5(grid):
    desc=describe_components(grid)
    target=max(desc, key=lambda comp: (comp["perimeter"], comp["area"], -top_left(comp)[0], -top_left(comp)[1]))
    return crop_component(target, 8)

def solve_S13_M6(grid):
    desc=describe_components(grid)
    anchor=next(comp for comp in desc if comp["color"]==2)
    feat=(anchor["touches_border"], sym_class(anchor))
    out=copyg(grid)
    for comp in desc:
        if comp is anchor:
            continue
        if (comp["touches_border"], sym_class(comp))==feat:
            for r,c in comp["cells"]:
                out[r][c]=8
    return out

def solve_S13_M7(grid):
    panels,_=split_panels(grid, sep_color=5)
    sigs=[]
    for panel in panels:
        hs=sorted(comp["holes"] for comp in describe_components(panel))
        sigs.append(tuple(hs))
    counts=Counter(sigs)
    odd_index=next(i for i,s in enumerate(sigs) if counts[s]==1)
    out=[[0,0,0]]
    out[0][odd_index]=8
    return out

def solve_S13_H1(grid):
    holes_target = max(sum(1 for v in grid[0] if v==1)-1, 0)
    sym_target = {1:"v", 2:"h", 3:"both", 4:"none"}[sum(1 for v in grid[1] if v==2)]
    body=[row[:] for row in grid[2:]]
    desc=describe_components(body)
    target=next(comp for comp in sorted(desc, key=top_left) if comp["holes"]==holes_target and sym_class(comp)==sym_target)
    return crop_component(target, 8)

def solve_S13_H2(grid):
    desc=sorted(describe_components(grid), key=top_left)
    n=len(desc)
    out=blank(n,n,0)
    for i in range(n):
        out[i][i]=1
    for i,a in enumerate(desc):
        for j,b in enumerate(desc):
            if i==j:
                continue
            if sym_class(a)==sym_class(b):
                out[i][j]=8
            elif a["holes"]==b["holes"]:
                out[i][j]=4
    return out

def solve_S13_H3(grid):
    panels,_ = split_panels(grid, sep_color=5)
    ref, cand = panels[0], panels[1]
    ref_desc=describe_components(ref)
    target_feat = feature_triple(next(comp for comp in ref_desc if comp["color"]==2))
    cand_desc=describe_components(cand)
    target=next(comp for comp in sorted(cand_desc, key=top_left) if feature_triple(comp)==target_feat)
    return crop_component(target, 8)

def solve_S13_H4(grid):
    sym_target = {1:"v", 2:"h", 3:"both", 4:"none"}[sum(1 for v in grid[0] if v==1)]
    k = sum(1 for v in grid[1] if v==2)
    body=[row[:] for row in grid[2:]]
    desc=[comp for comp in describe_components(body) if sym_class(comp)==sym_target]
    desc=sorted(desc, key=lambda comp: (-comp["area"], top_left(comp)))
    target=desc[k-1]
    return crop_component(target, 8)

def solve_S13_H5(grid):
    desc=describe_components(grid)
    counts=Counter(feature_triple(comp) for comp in desc)
    out=copyg(grid)
    for comp in desc:
        if counts[feature_triple(comp)] > 1:
            for r,c in comp["cells"]:
                out[r][c]=8
    return out

def solve_S13_H6(grid):
    desc=describe_components(grid)
    blue=next(comp for comp in desc if comp["color"]==1)
    red=next(comp for comp in desc if comp["color"]==2)
    holes_target = blue["holes"]
    sym_target = sym_class(red)
    candidates=[comp for comp in desc if comp["color"] not in (1,2)]
    target=next(comp for comp in sorted(candidates, key=top_left) if comp["holes"]==holes_target and sym_class(comp)==sym_target)
    return crop_component(target, 8)

def solve_S13_H7(grid):
    desc=describe_components(grid)
    target=max(desc, key=lambda comp: (comp["holes"], comp["sym_count"], comp["area"], -top_left(comp)[0], -top_left(comp)[1]))
    return crop_component(target, 8)
