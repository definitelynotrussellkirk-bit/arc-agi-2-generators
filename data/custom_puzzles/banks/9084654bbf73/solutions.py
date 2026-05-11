"""Reference helper library and 21 reference solve functions for the eighth custom ARC puzzle bank.

New primitive introduced in this set:
  line_runs(grid, axis="row", colors=None, nonzero=True)
It returns contiguous same-color segments along rows or columns,
including their start/end positions, lengths, and cells.
"""
from typing import List

Grid = List[List[int]]

dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,v=0): return [[v]*w for _ in range(h)]


def copyg(g): return [row[:] for row in g]


def dims(g): return len(g), len(g[0])


def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w


def components(grid, colors=None, connectivity=4, include_zero=False, ignore=None):
    if ignore is None: ignore=set()
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    dirs = dirs4 if connectivity==4 else [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            if (r,c) in ignore:
                continue
            v=grid[r][c]
            if v==0 and not include_zero: 
                continue
            if colors is not None and v not in colors:
                continue
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and (nr,nc) not in ignore and grid[nr][nc]==v:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            out.append({'color':v,'cells':sorted(cells)})
    return out


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop_bbox(grid,cells):
    r1,c1,r2,c2=bbox(cells)
    return [row[c1:c2+1] for row in grid[r1:r2+1]]


def line_runs(grid:Grid, axis:str="row", colors=None, nonzero=True):
    """Return contiguous same-color runs along rows or columns.
    Each run: dict(axis_index,start,end,length,color,cells).
    """
    h,w=dims(grid)
    runs=[]
    if axis=="row":
        for r in range(h):
            c=0
            while c<w:
                v=grid[r][c]
                if (nonzero and v==0) or (colors is not None and v not in colors):
                    c+=1; continue
                c2=c
                while c2+1<w and grid[r][c2+1]==v:
                    c2+=1
                runs.append({'axis':'row','line':r,'start':c,'end':c2,'length':c2-c+1,'color':v,
                             'cells':[(r,cc) for cc in range(c,c2+1)]})
                c=c2+1
    elif axis=="col":
        for c in range(w):
            r=0
            while r<h:
                v=grid[r][c]
                if (nonzero and v==0) or (colors is not None and v not in colors):
                    r+=1; continue
                r2=r
                while r2+1<h and grid[r2+1][c]==v:
                    r2+=1
                runs.append({'axis':'col','line':c,'start':r,'end':r2,'length':r2-r+1,'color':v,
                             'cells':[(rr,c) for rr in range(r,r2+1)]})
                r=r2+1
    else:
        raise ValueError
    return runs


def smallest_period(seq):
    n=len(seq)
    for p in range(1,n+1):
        if n%p==0:
            ok=True
            for i,x in enumerate(seq):
                if x!=seq[i%p]:
                    ok=False; break
            if ok: return seq[:p]
    return seq


def repeat_to_length(pattern,length):
    if not pattern: return [0]*length
    return [pattern[i%len(pattern)] for i in range(length)]


def tile2d(tile,h,w):
    th,tw=dims(tile)
    return [[tile[r%th][c%tw] for c in range(w)] for r in range(h)]


def row_signature(cells):
    # normalized row signature: tuple of sorted column positions per row after normalization
    r1,c1,r2,c2=bbox(cells)
    rows=[]
    for r in range(r1,r2+1):
        cols=sorted(c-c1 for rr,c in cells if rr==r)
        rows.append(tuple(cols))
    return tuple(rows)


def infer_tile_from_periodic_hole(grid):
    # assume full grid is tiled by a small tile and one rectangular zero hole.
    h,w=dims(grid)
    # search tile sizes 1..4 maybe 5
    hole=[(r,c) for r in range(h) for c,v in enumerate(grid[r]) if v==0]
    if not hole:
        return [[grid[0][0]]]
    # We assume zero only appears in hole and not elsewhere in pattern.
    # Find smallest tile dimensions consistent with all nonzero cells.
    for th in range(1,min(5,h)+1):
        for tw in range(1,min(5,w)+1):
            ok=True
            vals={}
            for r in range(h):
                for c in range(w):
                    v=grid[r][c]
                    if v==0: 
                        continue
                    key=(r%th,c%tw)
                    if key in vals and vals[key]!=v:
                        ok=False; break
                    vals[key]=v
                if not ok: break
            if ok:
                tile=[[vals[(r,c)] for c in range(tw)] for r in range(th)]
                return tile
    raise AssertionError("no tile found")


def solve_S8_E1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        runs=[run for run in line_runs([grid[r]], axis="row") if run['color']!=0]  # but line index 0
        if not runs: 
            continue
        # leftmost unique longest
        best=max(runs,key=lambda run:(run['length'],-run['start']))
        for _,c in best['cells']:
            out[r][c]=best['color']
    return out


def solve_S8_E2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for run in line_runs(grid,'row'):
        if run['color']==0: continue
        assert run['length']%2==1
        mid=(run['start']+run['end'])//2
        out[run['line']][mid]=run['color']
    return out


def solve_S8_E3(grid):
    h,w=dims(grid)
    # find full vertical bar color 8
    bar_cols=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))]
    assert len(bar_cols)==1
    b=bar_cols[0]
    out=copyg(grid)
    for r in range(h):
        for c in range(b):
            v=grid[r][c]
            if v!=0:
                mc=2*b-c
                if 0<=mc<w and grid[r][mc]==0:
                    out[r][mc]=v
    return out


def solve_S8_E4(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    body_w=w-1
    for r in range(h):
        k=grid[r][0]
        body=grid[r][1:]
        shift=k%body_w
        out[r][0]=k
        out[r][1:]=body[-shift:]+body[:-shift] if shift else body[:]
    return out


def solve_S8_E5(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for run in line_runs(grid,'row'):
        if run['color']==0: continue
        for i,(r,c) in enumerate(run['cells']):
            if i%2==0:
                out[r][c]=run['color']
    return out


def solve_S8_E6(grid):
    h,w=dims(grid)
    bar_cols=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))]
    assert len(bar_cols)==1
    b=bar_cols[0]
    out=blank(h,w,0)
    for r in range(h):
        for c in range(b):
            mc=2*b-c
            if 0<=mc<w:
                if grid[r][c]!=0 and grid[r][mc]!=0:
                    out[r][mc]=2
    return out


def solve_S8_E7(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        row=grid[r]
        # seed prefix: initial contiguous nonzero block
        c=0
        while c<w and row[c]!=0:
            c+=1
        seed=row[:c]
        out[r]=repeat_to_length(seed,w)
    return out


def solve_S8_M1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        runs=[run for run in line_runs([grid[r]], 'row') if run['color']!=0]
        runs=sorted(runs,key=lambda run:(-run['length'], run['start']))
        c=0
        for idx,run in enumerate(runs):
            for _ in range(run['length']):
                if c<w:
                    out[r][c]=run['color']; c+=1
            if idx!=len(runs)-1 and c<w:
                c+=1  # one zero separator
        # rest zeros
    return out


def solve_S8_M2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    hruns={}
    for run in line_runs(grid,'row'):
        if run['color']==0: continue
        if run['length']>=3:
            for cell in run['cells']:
                hruns[cell]=run['color']
    vruns=set()
    for run in line_runs(grid,'col'):
        if run['color']==0: continue
        if run['length']>=3:
            for cell in run['cells']:
                vruns.add(cell)
    for cell,color in hruns.items():
        if cell in vruns:
            r,c=cell
            out[r][c]=8
    return out


def solve_S8_M3(grid):
    h,w=dims(grid)
    bar_cols=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))]
    assert len(bar_cols)==1
    b=bar_cols[0]
    out=blank(h,w,0)
    for r in range(h):
        for c in range(b):
            mc=2*b-c
            if 0<=mc<w:
                left = grid[r][c]!=0
                right = grid[r][mc]!=0
                if left ^ right:
                    out[r][mc]=7
    return out


def solve_S8_M4(grid):
    h,w=dims(grid)
    # legend colors in top row, contiguous nonzero cells ignoring zeros
    legend=[v for v in grid[0] if v!=0]
    body=[row[:] for row in grid[1:]]
    out=copyg(grid)
    # find components of color 1 in body coordinates
    comps=[]
    sub=body
    for comp in components(sub,{1},4):
        comps.append(comp)
    comps=sorted(comps,key=lambda comp:min(c for r,c in comp['cells']))
    assert len(comps)<=len(legend)
    for comp,color in zip(comps, legend):
        for r,c in comp['cells']:
            out[r+1][c]=color
    return out


def solve_S8_M5(grid):
    h,w=dims(grid)
    # seed row is top row's contiguous nonzero prefix
    c=0
    while c<w and grid[0][c]!=0:
        c+=1
    seed=grid[0][:c]
    out=copyg(grid)
    # find rectangle of 8s in rows >=1
    cells=[(r,c) for r in range(1,h) for c,v in enumerate(grid[r]) if v==8]
    r1,c1,r2,c2=bbox(cells)
    for r in range(r1,r2+1):
        out[r][c1:c2+1]=repeat_to_length(seed,c2-c1+1)
    return out


def solve_S8_M6(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for c in range(w):
        r=0
        while r<h and grid[r][c]!=0:
            r+=1
        seed=[grid[i][c] for i in range(r)]
        col=repeat_to_length(seed,h)
        for rr in range(h):
            out[rr][c]=col[rr]
    return out


def solve_S8_M7(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r in range(h):
        row=grid[r]
        k=0
        while k<w and row[k]!=0:
            k+=1
        prefix=row[:k]
        period=smallest_period(prefix)
        out[r]=repeat_to_length(period,w)
    return out


def solve_S8_H1(grid):
    h,w=dims(grid)
    axis_cells=[(r,c) for r in range(h) for c,v in enumerate(grid[r]) if v==8]
    cols=sorted(set(c for r,c in axis_cells))
    rows=sorted(set(r for r,c in axis_cells))
    out=copyg(grid)
    if len(cols)==1:  # vertical axis
        b=cols[0]
        for r in range(h):
            for c,v in enumerate(grid[r]):
                if v!=0 and v!=8:
                    mc=2*b-c
                    if 0<=mc<w and out[r][mc]==0:
                        out[r][mc]=v
    elif len(rows)==1:  # horizontal axis
        b=rows[0]
        for r in range(h):
            for c,v in enumerate(grid[r]):
                if v!=0 and v!=8:
                    mr=2*b-r
                    if 0<=mr<h and out[mr][c]==0:
                        out[mr][c]=v
    else:
        raise AssertionError("axis markers not on one line")
    return out


def solve_S8_H2(grid):
    h,w=dims(grid)
    tile=infer_tile_from_periodic_hole(grid)
    full=tile2d(tile,h,w)
    out=copyg(grid)
    for r in range(h):
        for c in range(w):
            if out[r][c]==0:
                out[r][c]=full[r][c]
    return out


def solve_S8_H3(grid):
    h,w=dims(grid)
    row_lengths=[grid[r][0] for r in range(1,h)]
    col_heights=grid[0][1:]
    # output interior only, color 3
    out=blank(h-1,w-1,0)
    for r,L in enumerate(row_lengths):
        for c in range(min(L,w-1)):
            out[r][c]=3
    # assume headers are consistent; could validate col heights
    return out


def solve_S8_H4(grid):
    # query object color 8. Candidate objects other colors. Output bbox crop of matching candidate.
    comps=components(grid, None,4)
    query=[comp for comp in comps if comp['color']==8]
    assert len(query)==1
    qs=row_signature(query[0]['cells'])
    cands=[comp for comp in comps if comp['color'] not in (0,8)]
    matches=[comp for comp in cands if row_signature(comp['cells'])==qs]
    assert len(matches)==1
    return crop_bbox(grid, matches[0]['cells'])


def solve_S8_H5(grid):
    h,w=dims(grid)
    bar_cols=[c for c in range(w) if all(grid[r][c]==8 for r in range(h))]
    assert len(bar_cols)==1
    b=bar_cols[0]
    out=blank(h,w,0)
    for r in range(h):
        for c in range(b):
            mc=2*b-c
            if 0<=mc<w:
                lv=grid[r][c]
                rv=grid[r][mc]
                if lv!=0 and lv==rv:
                    out[r][mc]=lv
    return out


def solve_S8_H6(grid):
    h,w=dims(grid)
    canon=grid[0][:]
    out=blank(h,w,0)
    out[0]=canon[:]
    for r in range(1,h):
        row=grid[r]
        # find cyclic shift that matches canon
        found=None
        for s in range(w):
            shifted=row[s:]+row[:s]
            if shifted==canon:
                found=shifted; break
        assert found is not None
        out[r]=found
    return out


def solve_S8_H7(grid):
    h,w=dims(grid)
    # detect seed block at top-left: maximal rectangle of nonzero cells from (0,0)
    th=0
    while th<h and all(grid[th][c]!=0 for c in range(0,1)): # at least first col nonzero
        th+=1
        if th<h and grid[th][0]==0:
            break
    # Actually seed occupies contiguous nonzero rows and cols from origin until zero encountered in row0/col0
    tw=0
    while tw<w and grid[0][tw]!=0:
        tw+=1
    th=0
    while th<h and grid[th][0]!=0:
        th+=1
    tile=[row[:tw] for row in grid[:th]]
    # find mask of 8s, use bbox top-left as origin
    cells=[(r,c) for r in range(h) for c,v in enumerate(grid[r]) if v==8]
    r1,c1,r2,c2=bbox(cells)
    out=copyg(grid)
    for r,c in cells:
        out[r][c]=tile[(r-r1)%th][(c-c1)%tw]
    return out


SOLVERS = {
    "S8_E1": solve_S8_E1,
    "S8_E2": solve_S8_E2,
    "S8_E3": solve_S8_E3,
    "S8_E4": solve_S8_E4,
    "S8_E5": solve_S8_E5,
    "S8_E6": solve_S8_E6,
    "S8_E7": solve_S8_E7,
    "S8_M1": solve_S8_M1,
    "S8_M2": solve_S8_M2,
    "S8_M3": solve_S8_M3,
    "S8_M4": solve_S8_M4,
    "S8_M5": solve_S8_M5,
    "S8_M6": solve_S8_M6,
    "S8_M7": solve_S8_M7,
    "S8_H1": solve_S8_H1,
    "S8_H2": solve_S8_H2,
    "S8_H3": solve_S8_H3,
    "S8_H4": solve_S8_H4,
    "S8_H5": solve_S8_H5,
    "S8_H6": solve_S8_H6,
    "S8_H7": solve_S8_H7,
}
