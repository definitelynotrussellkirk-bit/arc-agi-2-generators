"""Reference helper library and 21 reference solve functions for the eighteenth custom ARC puzzle bank.

New primitive introduced in this set:

  axis_closure(cells, axis='row')

For each occupied row or column, fill every cell between that line's extreme occupied coordinates. This turns sparse endpoints into solid spans, supports row/column gap-bridging, and — when composed across axes or under blockers — builds rectangles, blocked room completions, overlap tests, and relation matrices.

All solve_* functions are deterministic reference programs for the synthetic
ARC-style tasks in set 18.
"""
from typing import List, Tuple
from collections import defaultdict, Counter

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
        if 0 <= r < h and 0 <= c < w:
            g[r][c]=color
    return g

def render_same_size(cells, h,w, color=8):
    g=blank(h,w,0)
    place(g,cells,color)
    return g

def nonzero(g, ignore_colors=None):
    ignore_colors=set(ignore_colors or [])
    return [(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and v not in ignore_colors]

def components(g, colors=None, connectivity=4, ignore_colors=None):
    ignore_colors=set(ignore_colors or [])
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    if connectivity==4:
        dirs=[(-1,0),(1,0),(0,-1),(0,1)]
    else:
        dirs=[(dr,dc) for dr in (-1,0,1) for dc in (-1,0,1) if (dr,dc)!=(0,0)]
    out=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            v=g[r][c]
            if v==0 or v in ignore_colors:
                continue
            if colors is not None and v not in colors:
                continue
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
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_cells(cells, color=8):
    r1,c1,r2,c2=bbox(cells)
    out=blank(r2-r1+1, c2-c1+1, 0)
    for r,c in cells:
        out[r-r1][c-c1]=color
    return out

def norm_cells(cells):
    r1,c1,r2,c2=bbox(cells)
    return tuple(sorted((r-r1,c-c1) for r,c in cells))

def axis_closure(cells, axis='row'):
    cells=set(cells)
    out=set(cells)
    if axis=='row':
        by=defaultdict(list)
        for r,c in cells:
            by[r].append(c)
        for r, cols in by.items():
            for c in range(min(cols), max(cols)+1):
                out.add((r,c))
    else:
        by=defaultdict(list)
        for r,c in cells:
            by[c].append(r)
        for c, rows in by.items():
            for r in range(min(rows), max(rows)+1):
                out.add((r,c))
    return out

def double_closure(cells, first='row', second='col'):
    out=axis_closure(cells, 'row' if first.startswith('r') else 'col')
    out=axis_closure(out, 'row' if second.startswith('r') else 'col')
    return out

def bridge_only(cells, axis='row'):
    cells=set(cells)
    return axis_closure(cells, axis) - cells

def panel_split_vertical(g, sep=9):
    h,w=dims(g)
    out=[]
    start=0
    for c in range(w):
        if all(g[r][c]==sep for r in range(h)):
            if start < c:
                out.append((start,c,[row[start:c] for row in g]))
            start=c+1
    if start < w:
        out.append((start,w,[row[start:w] for row in g]))
    return out

def blocked_axis_closure(cells, axis, bounds, walls):
    h,w=bounds
    walls=set(walls)
    src=set(cells)
    out=set(src)
    if axis=='row':
        for r in range(h):
            blocked=[-1]+sorted(c for rr,c in walls if rr==r)+[w]
            rowcells=sorted(c for rr,c in src if rr==r)
            if not rowcells:
                continue
            for a,b in zip(blocked, blocked[1:]):
                seg=[c for c in rowcells if a < c < b]
                if seg:
                    for c in range(min(seg), max(seg)+1):
                        if (r,c) not in walls:
                            out.add((r,c))
    else:
        for c in range(w):
            blocked=[-1]+sorted(r for r,cc in walls if cc==c)+[h]
            colcells=sorted(r for r,cc in src if cc==c)
            if not colcells:
                continue
            for a,b in zip(blocked, blocked[1:]):
                seg=[r for r in colcells if a < r < b]
                if seg:
                    for r in range(min(seg), max(seg)+1):
                        if (r,c) not in walls:
                            out.add((r,c))
    return out

def count_rows_cols(cells):
    return len({r for r,c in cells}), len({c for r,c in cells})

def solve_S18_E1(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    return render_same_size(axis_closure(cells,'row'), h,w, 8)

def solve_S18_E2(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    return render_same_size(axis_closure(cells,'col'), h,w, 8)

def solve_S18_E3(grid):
    h,w=dims(grid)
    marker=grid[0][0]
    axis='row' if marker==2 else 'col'
    cells=[(r,c) for r,c,v in nonzero(grid) if not (r==0 and c==0)]
    return render_same_size(axis_closure(cells,axis), h,w, 8)

def solve_S18_E4(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    return render_same_size(bridge_only(cells,'row'), h,w, 8)

def solve_S18_E5(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    out=blank(h,w,0)
    place(out, axis_closure(by[2],'row'), 8)
    place(out, axis_closure(by[3],'col'), 6)
    return out

def solve_S18_E6(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    return render_same_size(double_closure(cells,'row','col'), h,w, 8)

def solve_S18_E7(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    by=defaultdict(list)
    for r,c in cells:
        by[r].append(c)
    best=None
    bestlen=-1
    for r, cols in by.items():
        L=max(cols)-min(cols)+1
        if L>bestlen or (L==bestlen and r<best[0] if best is not None else False):
            bestlen=L
            best=(r, min(cols), max(cols))
    out=blank(h,w,0)
    if best:
        r,a,b=best
        for c in range(a,b+1):
            out[r][c]=8
    return out

def solve_S18_M1(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for comp in components(grid):
        closed=axis_closure(comp['cells'],'row')
        place(out, closed, 8)
    return out

def solve_S18_M2(grid):
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    best_color=None
    best_gain=-1
    best_closed=None
    for color,cells in sorted(by.items()):
        closed=axis_closure(cells,'row')
        gain=len(closed)-len(cells)
        if gain>best_gain:
            best_gain=gain; best_color=color; best_closed=closed
    return crop_cells(best_closed, 8)

def solve_S18_M3(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    for color,cells in by.items():
        rs,cs=count_rows_cols(cells)
        axis='row' if cs>=rs else 'col'
        place(out, axis_closure(cells,axis), 8)
    return out

def solve_S18_M4(grid):
    h,w=dims(grid)
    cells=[(r,c) for r,c,v in nonzero(grid)]
    by=defaultdict(list)
    for r,c in cells:
        by[r].append(c)
    out=blank(h,w,0)
    for r, cols in by.items():
        if len(cols)==2:
            for c in range(min(cols), max(cols)+1):
                out[r][c]=8
    return out

def solve_S18_M5(grid):
    h,w=dims(grid)
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    a=axis_closure(by[2],'row')
    b=axis_closure(by[3],'col')
    return render_same_size(a & b, h,w, 8)

def solve_S18_M6(grid):
    panels=panel_split_vertical(grid, 9)
    norms=[]
    closures=[]
    for _,_,p in panels:
        cells=[(r,c) for r,c,v in nonzero(p)]
        closed=double_closure(cells,'row','col')
        closures.append(closed)
        norms.append(norm_cells(closed))
    cnt=Counter(norms)
    idx=next(i for i,n in enumerate(norms) if cnt[n]==1)
    return crop_cells(closures[idx], 8)

def solve_S18_M7(grid):
    h,w=dims(grid)
    walls={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==5}
    seeds=[(r,c) for r,c,v in nonzero(grid, ignore_colors={5})]
    closed=blocked_axis_closure(seeds, 'row', (h,w), walls)
    out=blank(h,w,0)
    place(out, walls, 5)
    place(out, closed, 8)
    return out

def solve_S18_H1(grid):
    # first two rows legend, third row separator 9s, rest scene
    h,w=dims(grid)
    mapping={}
    for c in range(w):
        color=grid[0][c]
        mode=grid[1][c]
        if color!=0 and mode in (1,2,3,4):
            mapping[color]=mode
    out=copyg(grid)
    for r in range(3,h):
        for c in range(w):
            if out[r][c] not in (0,9):
                out[r][c]=0
    by=defaultdict(list)
    for r in range(3,h):
        for c,v in enumerate(grid[r]):
            if v!=0 and v!=9:
                by[v].append((r,c))
    for color,cells in by.items():
        mode=mapping.get(color,1)
        if mode==1:
            transformed=axis_closure(cells,'row')
        elif mode==2:
            transformed=axis_closure(cells,'col')
        elif mode==3:
            transformed=double_closure(cells,'row','col')
        else:
            transformed=bridge_only(cells,'row')
        place(out, transformed, color)
    return out

def solve_S18_H2(grid):
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    objs=[(color, double_closure(cells,'row','col')) for color,cells in sorted(by.items())]
    n=len(objs)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=5
            elif objs[i][1] & objs[j][1]:
                out[i][j]=8
    return out

def solve_S18_H3(grid):
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    best_color=None
    best_closed=None
    best_area=-1
    for color,cells in sorted(by.items()):
        closed=double_closure(cells,'row','col')
        r1,c1,r2,c2=bbox(closed)
        area=(r2-r1+1)*(c2-c1+1)
        if len(closed)==area and area>best_area:
            best_area=area
            best_color=color
            best_closed=closed
    return crop_cells(best_closed, 8)

def solve_S18_H4(grid):
    panels=panel_split_vertical(grid, 9)
    panel_shapes=[dims(p) for _,_,p in panels]
    assert len(set(panel_shapes))==1
    ph,pw=panel_shapes[0]
    counts=Counter()
    for _,_,p in panels:
        cells=[(r,c) for r,c,v in nonzero(p)]
        closed=double_closure(cells,'row','col')
        for cell in closed:
            counts[cell]+=1
    out=blank(ph,pw,0)
    for cell,k in counts.items():
        if k>=2:
            out[cell[0]][cell[1]]=8
    return out

def solve_S18_H5(grid):
    target={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==7}
    by=defaultdict(list)
    for r,c,v in nonzero(grid, ignore_colors={7}):
        by[v].append((r,c))
    best_color=None
    best_closed=None
    best_score=(-1,-10**9,-10**9)
    for color,cells in sorted(by.items()):
        closed=axis_closure(cells,'row')
        overlap=len(closed & target)
        extra=-len(closed - target)
        total=-len(closed)
        score=(overlap, extra, total)
        if score > best_score:
            best_score=score; best_color=color; best_closed=closed
    return crop_cells(best_closed, 8)

def solve_S18_H6(grid):
    h,w=dims(grid)
    walls={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==5}
    seeds=[(r,c) for r,c,v in nonzero(grid, ignore_colors={5})]
    step1=blocked_axis_closure(seeds, 'row', (h,w), walls)
    step2=blocked_axis_closure(step1, 'col', (h,w), walls)
    out=blank(h,w,0)
    place(out, walls, 5)
    place(out, step2, 8)
    return out

def solve_S18_H7(grid):
    by=defaultdict(list)
    for r,c,v in nonzero(grid):
        by[v].append((r,c))
    objs=[(color, norm_cells(double_closure(cells,'row','col'))) for color,cells in sorted(by.items())]
    n=len(objs)
    out=blank(n,n,0)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=5
            elif objs[i][1]==objs[j][1]:
                out[i][j]=8
    return out
