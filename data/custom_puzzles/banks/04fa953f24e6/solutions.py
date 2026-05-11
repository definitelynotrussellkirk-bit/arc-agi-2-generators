"""Reference helper library and 21 reference solve functions for the seventeenth custom ARC puzzle bank.

New primitive introduced in this set:

  expand_with_stencil(cells, offsets, bounds)


Take a set of source cells and a small offset stencil, translate the stencil
around every source cell, union the translated copies, and clip to the grid.
This makes plus growth, X growth, square halos, contact tests, layer
differences, and library-based stamping explicit.

All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 17.
"""
from typing import List, Tuple
from collections import defaultdict, Counter

Grid = List[List[int]]

PLUS = [(0,0),(-1,0),(1,0),(0,-1),(0,1)]
XST = [(0,0),(-1,-1),(-1,1),(1,-1),(1,1)]
SQ1 = [(dr,dc) for dr in (-1,0,1) for dc in (-1,0,1)]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def dims(g):
    return len(g), len(g[0])

def place(g, cells, color):
    h,w=dims(g)
    for r,c in cells:
        if 0 <= r < h and 0 <= c < w:
            g[r][c]=color
    return g

def nonzero(g):
    return [(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]

def components(g, include_zero=False, connectivity=4):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    if connectivity==4:
        dirs=[(-1,0),(1,0),(0,-1),(0,1)]
    else:
        dirs=[(dr,dc) for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc)!=(0,0)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]: continue
            seen[r][c]=True
            v=g[r][c]
            if v==0 and not include_zero: continue
            st=[(r,c)]
            cells=[(r,c)]
            while st:
                rr,cc=st.pop()
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        st.append((nr,nc))
                        cells.append((nr,nc))
            out.append({"color":v,"cells":cells})
    return out

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_cells(cells, color=8):
    r1,c1,r2,c2=bbox(cells)
    out=blank(r2-r1+1, c2-c1+1, 0)
    for r,c in cells:
        out[r-r1][c-c1]=color
    return out

def expand_with_stencil(cells, offsets, bounds):
    h,w=bounds
    out=set()
    for r,c in cells:
        for dr,dc in offsets:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out.add((nr,nc))
    return out

def panel_split_vertical(g, sep=9):
    h,w=dims(g)
    cols=[]
    start=0
    for c in range(w):
        if all(g[r][c]==sep for r in range(h)):
            cols.append((start,c))
            start=c+1
    cols.append((start,w))
    out=[]
    for a,b in cols:
        if a<b:
            out.append((a,b,[row[a:b] for row in g]))
    return out

def dihedral_transforms(cells):
    pts=list(cells)
    # normalize around origin later
    trans=[]
    for xform in range(8):
        cur=[]
        for r,c in pts:
            x,y=r,c
            if xform==0: u,v=x,y
            elif xform==1: u,v=x,-y
            elif xform==2: u,v=-x,y
            elif xform==3: u,v=-x,-y
            elif xform==4: u,v=y,x
            elif xform==5: u,v=y,-x
            elif xform==6: u,v=-y,x
            elif xform==7: u,v=-y,-x
            cur.append((u,v))
        minr=min(u for u,v in cur); minc=min(v for u,v in cur)
        trans.append(tuple(sorted((u-minr,v-minc) for u,v in cur)))
    return trans

def norm_dihedral(cells):
    return min(dihedral_transforms(cells))

def hole_count_shape(cells):
    # cells normalized; count 4-connected holes in bounding box complement
    r1,c1,r2,c2=bbox(cells)
    H=r2-r1+1; W=c2-c1+1
    occ={(r-r1,c-c1) for r,c in cells}
    # outside flood on padded box
    H2,W2=H+2,W+2
    seen=set([(0,0)])
    st=[(0,0)]
    dirs=[(-1,0),(1,0),(0,-1),(0,1)]
    while st:
        r,c=st.pop()
        for dr,dc in dirs:
            nr,nc=r+dr,c+dc
            if 0<=nr<H2 and 0<=nc<W2 and (nr,nc) not in seen:
                # map to original coords offset by -1
                orr,occ_c=nr-1,nc-1
                if not (0<=orr<H and 0<=occ_c<W and (orr,occ_c) in occ):
                    seen.add((nr,nc)); st.append((nr,nc))
    holes=0
    for r in range(H):
        for c in range(W):
            pr,pc=r+1,c+1
            if (r,c) in occ or (pr,pc) in seen:
                continue
            holes+=1
            st=[(pr,pc)]
            seen.add((pr,pc))
            while st:
                rr,cc=st.pop()
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<H2 and 0<=nc<W2 and (nr,nc) not in seen:
                        orr,occ_c=nr-1,nc-1
                        if not (0<=orr<H and 0<=occ_c<W and (orr,occ_c) in occ):
                            seen.add((nr,nc)); st.append((nr,nc))
    return holes

def matrix_of_contacts(groups, offsets, bounds):
    exps=[expand_with_stencil(g, offsets, bounds) for g in groups]
    n=len(groups)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=5
            elif exps[i] & exps[j]:
                out[i][j]=8
    return out

def solve_S17_E1(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, PLUS, (h,w)), 8)
    return out

def solve_S17_E2(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, XST, (h,w)), 8)
    return out

def solve_S17_E3(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, SQ1, (h,w)), 8)
    return out

def solve_S17_E4(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    grown=expand_with_stencil(seeds, PLUS, (h,w))
    halo=grown - set(seeds)
    out=blank(h,w,0)
    place(out, halo, 8)
    return out

def solve_S17_E5(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    a=expand_with_stencil(by[2], SQ1, (h,w))
    b=expand_with_stencil(by[3], SQ1, (h,w))
    out=blank(h,w,0)
    place(out, a & b, 8)
    return out

def solve_S17_E6(grid):
    h,w=dims(grid)
    legend=grid[0][0]
    seeds=[(r,c) for r,c,v in nonzero(grid) if (r,c)!=(0,0)]
    offsets=PLUS if legend==1 else XST
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, offsets, (h,w)), 8)
    return out

def solve_S17_E7(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    grown=expand_with_stencil(seeds, PLUS, (h,w))
    out=blank(1,len(grown),8)
    return out

def solve_S17_M1(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    out=blank(h,w,0)
    mapping={2:PLUS,3:XST,4:SQ1}
    for color,seeds in by.items():
        if color in mapping:
            place(out, expand_with_stencil(seeds, mapping[color], (h,w)), color)
    return out

def solve_S17_M2(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    step1=expand_with_stencil(seeds, PLUS, (h,w))
    step2=expand_with_stencil(step1, PLUS, (h,w))
    ring=step2 - step1
    out=blank(h,w,0)
    place(out, ring, 8)
    return out

def solve_S17_M3(grid):
    h,w=dims(grid)
    comps=[comp for comp in components(grid) if comp["color"]!=0]
    best=None
    best_grown=None
    for comp in comps:
        grown=expand_with_stencil(comp["cells"], SQ1, (h,w))
        key=(len(grown), -len(comp["cells"]))  # area first
        if best is None or key>best:
            best=key; best_grown=grown
    return crop_cells(best_grown, 8)

def solve_S17_M4(grid):
    h,w=dims(grid)
    occ=[(r,c) for r,c,v in nonzero(grid)]
    grown=expand_with_stencil(occ, SQ1, (h,w))
    halo=grown - set(occ)
    out=blank(h,w,0)
    place(out, halo, 8)
    return out

def solve_S17_M5(grid):
    h,w=dims(grid)
    target=grid[0][0]
    seeds=[(r,c) for r,c,v in nonzero(grid) if (r,c)!=(0,0) and v==target]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, SQ1, (h,w)), 8)
    return out

def solve_S17_M6(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    a=expand_with_stencil(by[2], PLUS, (h,w))
    b=expand_with_stencil(by[3], PLUS, (h,w))
    out=blank(h,w,0)
    place(out, a & b, 8)
    return out

def solve_S17_M7(grid):
    h,w=dims(grid)
    seeds=[(r,c) for r,c,v in nonzero(grid)]
    candidates=[]
    for s in seeds:
        grown=expand_with_stencil([s], SQ1, (h,w))
        touch=any(r in {0,h-1} or c in {0,w-1} for r,c in grown)
        candidates.append((touch,len(grown),s,grown))
    chosen=max(candidates)  # touch first True>False, then more cells (clipped border maybe smaller? but touch dominates)
    return crop_cells(chosen[3],8)

def solve_S17_H1(grid):
    h,w=dims(grid)
    # legend occupies rows 0:5 cols0:5 ; anchor color 9 indicates center
    legend_cells=[(r,c,v) for r,c,v in nonzero([row[:5] for row in grid[:5]])]
    anchor=[(r,c) for r,c,v in legend_cells if v==9][0]
    offsets=[(r-anchor[0], c-anchor[1]) for r,c,v in legend_cells if v!=9]
    seeds=[(r,c) for r,c,v in nonzero(grid) if not (r<5 and c<5) and v==2]
    out=blank(h,w,0)
    place(out, expand_with_stencil(seeds, offsets, (h,w)), 8)
    return out

def solve_S17_H2(grid):
    # panels separated by col 9s; choose odd panel by plus-grown dihedral signature; output original odd object cropped
    panels=panel_split_vertical(grid, sep=9)
    sigs=[]
    originals=[]
    for a,b,p in panels:
        cells=[(r,c) for r,c,v in nonzero(p)]
        grown=expand_with_stencil(cells, PLUS, dims(p))
        sig=norm_dihedral(grown)
        sigs.append(sig)
        originals.append(cells)
    cnt=Counter(sigs)
    odd_idx=[i for i,s in enumerate(sigs) if cnt[s]==1][0]
    return crop_cells(originals[odd_idx],8)

def solve_S17_H3(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    A=set(by[2]); B=set(by[3])
    # simultaneous growth with plus, find first intersection
    for step in range(10):
        inter=A & B
        if inter:
            out=blank(h,w,0); place(out, inter, 8); return out
        A=expand_with_stencil(A, PLUS, (h,w))
        B=expand_with_stencil(B, PLUS, (h,w))
    raise ValueError("no meet")

def solve_S17_H4(grid):
    h,w=dims(grid)
    comps=[comp for comp in components(grid) if comp["color"]!=0]
    chosen=None
    for comp in comps:
        before=hole_count_shape(comp["cells"])
        grown=expand_with_stencil(comp["cells"], SQ1, (h,w))
        after=hole_count_shape(list(grown))
        if after < before:
            # choose max drop, then smaller area
            key=(before-after, -len(comp["cells"]))
            if chosen is None or key > chosen[0]:
                chosen=(key, comp["cells"])
    assert chosen is not None
    return crop_cells(chosen[1],8)

def solve_S17_H5(grid):
    h,w=dims(grid)
    band=[row[:] for row in grid[:5]]
    panels=panel_split_vertical(band, sep=9)
    stencil_by_color={}
    for a,b,p in panels:
        nz=[(r,c,v) for r,c,v in nonzero(p)]
        anchor=[(r,c) for r,c,v in nz if v==9][0]
        colors=sorted({v for r,c,v in nz if v not in {0,9}})
        assert len(colors)==1
        color=colors[0]
        offsets=[(r-anchor[0], c-anchor[1]) for r,c,v in nz if v==color]
        stencil_by_color[color]=offsets
    out=blank(h,w,0)
    for r,c,v in nonzero(grid):
        if r<5: # library band
            continue
        if v in stencil_by_color:
            place(out, expand_with_stencil([(r,c)], stencil_by_color[v], (h,w)), v)
    return out

def solve_S17_H6(grid):
    h,w=dims(grid)
    mask={(r,c) for r,c,v in nonzero(grid) if v==1}
    comps=[comp for comp in components([[2 if v==2 else 0 for v in row] for row in grid]) if comp["color"]==2]
    best=None
    best_comp=None
    for comp in comps:
        grown=expand_with_stencil(comp["cells"], SQ1, (h,w))
        overlap=len(grown & mask)
        key=(overlap, len(grown), -len(comp["cells"]))
        if best is None or key>best:
            best=key; best_comp=comp["cells"]
    return crop_cells(best_comp,8)

def solve_S17_H7(grid):
    h,w=dims(grid)
    groups=defaultdict(list)
    for r,c,v in nonzero(grid):
        groups[v].append((r,c))
    colors=sorted(groups)
    cell_groups=[groups[c] for c in colors]
    return matrix_of_contacts(cell_groups, SQ1, (h,w))
