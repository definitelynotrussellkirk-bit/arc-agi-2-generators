"""Reference helper library and 21 reference solve functions for the nineteenth custom ARC puzzle bank.

New primitive introduced in this set:

  extract_panels(grid, divider_color=9, axis='col')

Split a grid into a linear sequence of subgrids separated by full divider rows or columns. This turns multi-panel ARC layouts into explicit panel objects that can be selected, compared, voted over, used as examples in a tiny transformation library, or converted into symbolic outputs like strips and relation matrices.

All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 19.
"""
from typing import List, Tuple
from collections import Counter

Grid = List[List[int]]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]


def dims(g):
    return len(g), len(g[0])


def copyg(g):
    return [row[:] for row in g]


def place(g, cells, color):
    h,w=dims(g)
    for r,c in cells:
        if 0<=r<h and 0<=c<w:
            g[r][c]=color
    return g


def render_same_size(cells,h,w,color=8):
    g=blank(h,w,0)
    place(g,cells,color)
    return g


def extract_panels(grid, divider_color=9, axis='col', keep_empty=False):
    h,w=dims(grid)
    out=[]
    if axis.startswith('c'):
        start=0
        c=0
        while c<w:
            if all(grid[r][c]==divider_color for r in range(h)):
                if keep_empty or start<c:
                    out.append([row[start:c] for row in grid])
                while c<w and all(grid[r][c]==divider_color for r in range(h)):
                    c+=1
                start=c
            else:
                c+=1
        if keep_empty or start<w:
            out.append([row[start:w] for row in grid])
    else:
        start=0
        r=0
        while r<h:
            if all(v==divider_color for v in grid[r]):
                if keep_empty or start<r:
                    out.append([row[:] for row in grid[start:r]])
                while r<h and all(v==divider_color for v in grid[r]):
                    r+=1
                start=r
            else:
                r+=1
        if keep_empty or start<h:
            out.append([row[:] for row in grid[start:h]])
    return out


def panel_occ(panel):
    return {(r,c) for r,row in enumerate(panel) for c,v in enumerate(row) if v!=0 and v!=9}


def panel_color(panel):
    cols=[v for row in panel for v in row if v!=0 and v!=9]
    return cols[0] if cols else 0


def recolor_panel(panel,color=8):
    h,w=dims(panel)
    return render_same_size(panel_occ(panel), h,w, color)


def union_cells(*panels):
    out=set()
    for p in panels:
        out |= panel_occ(p)
    return out


def inter_cells(a,b):
    return panel_occ(a) & panel_occ(b)


def xor_cells(a,b):
    return panel_occ(a) ^ panel_occ(b)


def minus_cells(a,b):
    return panel_occ(a) - panel_occ(b)


def rotate90_cells(cells):
    # rotate within bbox around top-left normalized
    if not cells:
        return []
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    h=max(rs)-min(rs)+1; w=max(cs)-min(cs)+1
    norm=[(r-min(rs), c-min(cs)) for r,c in cells]
    rot=[(c, h-1-r) for r,c in norm]
    minr=min(r for r,c in rot); minc=min(c for r,c in rot)
    return [(r-minr,c-minc) for r,c in rot]


def rotate_times(cells, k):
    out=list(cells)
    for _ in range(k%4):
        out=rotate90_cells(out)
    return out


def reflect_h_cells(cells):
    if not cells:
        return []
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    h=max(rs)-min(rs)+1; w=max(cs)-min(cs)+1
    norm=[(r-min(rs), c-min(cs)) for r,c in cells]
    ref=[(r, w-1-c) for r,c in norm]
    minr=min(r for r,c in ref); minc=min(c for r,c in ref)
    return [(r-minr,c-minc) for r,c in ref]


def normalize(cells):
    if not cells:
        return tuple()
    minr=min(r for r,c in cells); minc=min(c for r,c in cells)
    return tuple(sorted((r-minr,c-minc) for r,c in cells))


def dihedral_variants(cells):
    base=list(cells)
    outs=set()
    cur=base
    for k in range(4):
        rot=rotate_times(base,k)
        outs.add(normalize(rot))
        outs.add(normalize(reflect_h_cells(rot)))
    return outs


def majority_cells(panels, k):
    h,w=dims(panels[0])
    cnt=Counter()
    for p in panels:
        for cell in panel_occ(p):
            cnt[cell]+=1
    return {cell for cell,n in cnt.items() if n>=k}


def op_from_header(header):
    cells=panel_occ(header)
    if (0,0) in cells:
        return 'union'
    if (0,dims(header)[1]-1) in cells:
        return 'inter'
    if (dims(header)[0]-1,0) in cells:
        return 'xor'
    return 'minus'


def stamp_template(template_panel, markers_panel, marker_color=3):
    template=panel_occ(template_panel)
    # anchor template by its bbox top-left
    rs=[r for r,c in template]; cs=[c for r,c in template]
    minr,minc=min(rs),min(cs)
    offsets=[(r-minr,c-minc) for r,c in template]
    h,w=dims(markers_panel)
    out=set()
    for r,row in enumerate(markers_panel):
        for c,v in enumerate(row):
            if v==marker_color:
                for dr,dc in offsets:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out.add((nr,nc))
    return render_same_size(out,h,w,8)


def identify_transform(a,b):
    target=normalize(panel_occ(b))
    ops=[('rot0',0),('rot1',1),('rot2',2),('rot3',3)]
    for name,k in ops:
        if normalize(rotate_times(list(panel_occ(a)),k))==target:
            return name
    if normalize(reflect_h_cells(list(panel_occ(a))))==target:
        return 'flip'
    # fallback exact
    return 'rot0'


def solve_S19_E1(grid):
    a,b=extract_panels(grid, axis='col')
    h,w=dims(a)
    return render_same_size(union_cells(a,b), h,w, 8)


def solve_S19_E2(grid):
    a,b=extract_panels(grid, axis='col')
    h,w=dims(a)
    return render_same_size(inter_cells(a,b), h,w, 8)


def solve_S19_E3(grid):
    pans=extract_panels(grid, axis='col')
    best=max(pans, key=lambda p: (len(panel_occ(p)), -pans.index(p)))
    return recolor_panel(best, 8)


def solve_S19_E4(grid):
    header,p1,p2,p3=extract_panels(grid, axis='row')
    n=sum(1 for row in header for v in row if v!=0)
    chosen=[p1,p2,p3][n-1]
    return recolor_panel(chosen,8)


def solve_S19_E5(grid):
    p1,p2,p3=extract_panels(grid, axis='col')
    occs=[panel_occ(p1), panel_occ(p2), panel_occ(p3)]
    # choose repeated exact occupancy
    if occs[0]==occs[1] or occs[0]==occs[2]:
        return recolor_panel(p1,8)
    return recolor_panel(p2,8)


def solve_S19_E6(grid):
    pans=extract_panels(grid, axis='col')
    h,w=dims(pans[0])
    return render_same_size(majority_cells(pans,2), h,w, 8)


def solve_S19_E7(grid):
    key,*cands=extract_panels(grid, axis='col')
    k=panel_color(key)
    for p in cands:
        if panel_color(p)==k:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)


def solve_S19_M1(grid):
    a,b=extract_panels(grid, axis='col')
    h,w=dims(a)
    return render_same_size(xor_cells(a,b), h,w, 8)


def solve_S19_M2(grid):
    src,*cands=extract_panels(grid, axis='col')
    ns=normalize(panel_occ(src))
    for p in cands:
        if normalize(panel_occ(p))==ns:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)


def solve_S19_M3(grid):
    src,*cands=extract_panels(grid, axis='col')
    ns=normalize(panel_occ(src))
    out=[[8 if normalize(panel_occ(p))==ns else 0 for p in cands]]
    return out


def solve_S19_M4(grid):
    header,a,b=extract_panels(grid, axis='row')
    h,w=dims(a)
    op=op_from_header(header)
    if op=='union':
        cells=union_cells(a,b)
    elif op=='inter':
        cells=inter_cells(a,b)
    elif op=='xor':
        cells=xor_cells(a,b)
    else:
        cells=minus_cells(a,b)
    return render_same_size(cells, h,w, 8)


def solve_S19_M5(grid):
    src,*cands=extract_panels(grid, axis='col')
    src_occ=panel_occ(src)
    variants={normalize(rotate_times(list(src_occ),k)) for k in range(4)}
    for p in cands:
        if normalize(panel_occ(p)) in variants:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)


def solve_S19_M6(grid):
    template, markers=extract_panels(grid, axis='row')
    return stamp_template(template, markers, 3)


def solve_S19_M7(grid):
    pans=extract_panels(grid, axis='col')
    ordered=sorted(pans, key=lambda p:(len(panel_occ(p)), pans.index(p)))
    # assemble 2x2 mosaic
    ph,pw=dims(ordered[0])
    out=blank(ph*2, pw*2, 0)
    positions=[(0,0),(0,pw),(ph,0),(ph,pw)]
    for p,(r0,c0) in zip(ordered,positions):
        for r,c in panel_occ(p):
            out[r0+r][c0+c]=8
    return out


def solve_S19_H1(grid):
    pans=extract_panels(grid, axis='col')
    n=len(pans)
    out=blank(n,n,0)
    for i,a in enumerate(pans):
        va=dihedral_variants(panel_occ(a))
        for j,b in enumerate(pans):
            if normalize(panel_occ(b)) in va:
                out[i][j]=8
    return out


def solve_S19_H2(grid):
    pans=extract_panels(grid, axis='col')
    a,b,c,*cands=pans
    tf=identify_transform(a,b)
    if tf=='flip':
        target=normalize(reflect_h_cells(list(panel_occ(c))))
    else:
        target=normalize(rotate_times(list(panel_occ(c)), int(tf[-1])))
    for p in cands:
        if normalize(panel_occ(p))==target:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)


def solve_S19_H3(grid):
    src,target,*cands=extract_panels(grid, axis='col')
    target_occ=panel_occ(target)
    src_occ=panel_occ(src)
    for p in cands:
        if src_occ | panel_occ(p) == target_occ:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)


def solve_S19_H4(grid):
    src,target,*cands=extract_panels(grid, axis='col')
    target_occ=panel_occ(target)
    src_occ=panel_occ(src)
    for p in cands:
        if src_occ ^ panel_occ(p) == target_occ:
            return recolor_panel(p,8)
    return blank(*dims(cands[0]),0)


def solve_S19_H5(grid):
    pans=extract_panels(grid, axis='col')
    # alternating key,value ..., query last
    query=pans[-1]
    pairs=list(zip(pans[0:-1:2], pans[1:-1:2]))
    qn=normalize(panel_occ(query))
    qd=dihedral_variants(panel_occ(query))
    for key,val in pairs:
        if normalize(panel_occ(key)) in qd:
            return recolor_panel(val,8)
    return blank(*dims(pairs[0][1]),0)


def solve_S19_H6(grid):
    header,p1,p2,p3=extract_panels(grid, axis='row')
    codes=[header[0][i] for i in range(3)]
    pans=[p1,p2,p3]
    transformed=[]
    for p,code in zip(pans,codes):
        k={1:0,2:1,3:2,4:3}.get(code,0)
        transformed.append(render_same_size(set(rotate_times(list(panel_occ(p)),k)), *dims(p), 8))
    h,w=dims(p1)
    return render_same_size(majority_cells(transformed,2), h,w, 8)


def solve_S19_H7(grid):
    pans=extract_panels(grid, axis='col')
    src,target,*cands=pans
    src_occ=panel_occ(src); target_occ=panel_occ(target)
    out=[[0]*len(cands)]
    for i in range(len(cands)):
        for j in range(i+1,len(cands)):
            if src_occ | panel_occ(cands[i]) | panel_occ(cands[j]) == target_occ:
                out[0][i]=8
                out[0][j]=8
                return out
    return out

