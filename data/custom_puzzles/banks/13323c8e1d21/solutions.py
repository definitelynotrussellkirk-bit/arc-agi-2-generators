"""Reference helper library and 21 reference solve functions for the fifth custom ARC puzzle bank.

New primitive introduced in this set:
  raycast_until(grid, start, step, blockers=None, include_blocker=False)
It walks from start+step in a straight line until the first blocker or the edge,
and returns the traversed cells.
"""

from typing import List, Tuple, Dict, Any, Set

Grid = List[List[int]]

dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]

def copyg(g): return [row[:] for row in g]

def dims(g): return len(g), len(g[0])

def inb(g,r,c): 
    h,w=dims(g)
    return 0 <= r < h and 0 <= c < w

def components(grid: Grid, include_colors: Set[int]|None=None, connectivity=4, ignore_cells:Set[Tuple[int,int]]|None=None):
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    dirs = dirs4 if connectivity==4 else dirs8
    ignore_cells = ignore_cells or set()
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            if (r,c) in ignore_cells:
                continue
            color=grid[r][c]
            if color==0 or (include_colors is not None and color not in include_colors):
                continue
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and (nr,nc) not in ignore_cells and grid[nr][nc]==color:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({'color':color,'cells':sorted(cells)})
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(grid, cells):
    r1,c1,r2,c2 = bbox(cells)
    return [row[c1:c2+1] for row in grid[r1:r2+1]]

def normalize_cells(cells):
    r1,c1,r2,c2 = bbox(cells)
    return sorted((r-r1,c-c1) for r,c in cells)

def rotate_norm_cells(norm_cells, times=1):
    cells = list(norm_cells)
    for _ in range(times%4):
        maxr=max(r for r,c in cells)
        maxc=max(c for r,c in cells)
        h=maxr+1
        cells=[(c, h-1-r) for r,c in cells]
        # renormalize
        r0=min(r for r,c in cells); c0=min(c for r,c in cells)
        cells=sorted((r-r0,c-c0) for r,c in cells)
    return sorted(cells)

def canonical_rot(norm_cells):
    rots=[tuple(rotate_norm_cells(norm_cells, k)) for k in range(4)]
    return min(rots)

def count_holes(grid, comp):
    cells=set(comp['cells'])
    r1,c1,r2,c2=bbox(comp['cells'])
    seen=set()
    holes=0
    for r in range(r1,r2+1):
        for c in range(c1,c2+1):
            if (r,c) in cells or (r,c) in seen or grid[r][c]!=0:
                seen.add((r,c))
                continue
            q=[(r,c)]
            seen.add((r,c))
            touch=False
            region=[]
            while q:
                rr,cc=q.pop()
                region.append((rr,cc))
                if rr in (r1,r2) or cc in (c1,c2):
                    touch=True
                for dr,dc in dirs4:
                    nr,nc=rr+dr,cc+dc
                    if r1<=nr<=r2 and c1<=nc<=c2 and (nr,nc) not in seen and (nr,nc) not in cells and grid[nr][nc]==0:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            if not touch:
                holes += 1
    return holes

def raycast_until(grid: Grid, start: Tuple[int,int], step: Tuple[int,int], blockers: Set[int]|None=None, include_blocker=False):
    """Walk from start+step until boundary or blocker. Return traversed cells, excluding start.
    If include_blocker=True, include the first blocker cell."""
    blockers = set() if blockers is None else set(blockers)
    h,w=dims(grid)
    r,c=start
    dr,dc=step
    out=[]
    r+=dr; c+=dc
    while 0<=r<h and 0<=c<w:
        if grid[r][c] in blockers:
            if include_blocker:
                out.append((r,c))
            break
        out.append((r,c))
        r+=dr; c+=dc
    return out


# --- Solver functions ---

def solve_S5_E1(grid):
    target = grid[0][0]
    comps = components(grid, {target}, 4, ignore_cells={(0,0)})
    # choose largest or only
    comp = max(comps, key=lambda c: len(c['cells']))
    return crop_bbox(grid, comp['cells'])

def solve_S5_E2(grid):
    n = sum(cell==1 for row in grid for cell in row)
    return [[2]*n] if n>0 else [[0]]

def solve_S5_E3(grid):
    r = next(i for i,row in enumerate(grid) if row[0]==6)
    return [grid[r][1:]]

def solve_S5_E4(grid):
    out = copyg(grid)
    for r,row in enumerate(grid):
        for c,val in enumerate(row):
            if val==4:
                for rr,cc in raycast_until(grid,(r,c),(0,1),blockers={9}):
                    if out[rr][cc]==0:
                        out[rr][cc]=8
    return out

def solve_S5_E5(grid):
    comps = components(grid, {2}, 4)
    h,w=dims(grid)
    def touches_border(comp):
        return any(r in (0,h-1) or c in (0,w-1) for r,c in comp['cells'])
    comp = next(comp for comp in comps if touches_border(comp))
    return crop_bbox(grid, comp['cells'])

def solve_S5_E6(grid):
    out = copyg(grid)
    h,w=dims(grid)
    for r in range(h):
        cols=[c for c in range(w) if grid[r][c]==1]
        if len(cols)==2:
            a,b=cols
            for c in range(a,b+1):
                out[r][c]=1
    return out

def solve_S5_E7(grid):
    n = sum(cell==3 for row in grid for cell in row)
    return [[7]*n for _ in range(n)] if n>0 else [[0]]

def solve_S5_M1(grid):
    h,w=dims(grid)
    mh,mw=h//2,w//2
    out=[[0,0],[0,0]]
    quads=[(0,mh,0,mw),(0,mh,mw,w),(mh,h,0,mw),(mh,h,mw,w)]
    for idx,(r1,r2,c1,c2) in enumerate(quads):
        colors={grid[r][c] for r in range(r1,r2) for c in range(c1,c2) if grid[r][c]!=0}
        val=next(iter(colors)) if colors else 0
        out[idx//2][idx%2]=val
    return out

def solve_S5_M2(grid):
    h,w=dims(grid)
    vert=set()
    horiz=set()
    for c,val in enumerate(grid[0]):
        if val==2:
            vert.update(raycast_until(grid,(0,c),(1,0),blockers={5}))
    for r in range(h):
        if grid[r][0]==1:
            horiz.update(raycast_until(grid,(r,0),(0,1),blockers={5}))
    inter=vert & horiz
    out=blank(h,w)
    for r,c in inter:
        out[r][c]=6
    return out

def solve_S5_M3(grid):
    cols=[c for c,v in enumerate(grid[0]) if v==4]
    body=grid[1:]
    return [[row[c] for c in cols] for row in body]

def solve_S5_M4(grid):
    comps=components(grid, None, 4)
    comps_sorted=sorted(comps, key=lambda comp:(len(comp['cells']), comp['color']))
    return [[comp['color'] for comp in comps_sorted]]

def solve_S5_M5(grid):
    k=sum(v==1 for v in grid[0])
    body=grid[1:]
    # components in body with absolute coords offset by 1 row
    comps=components(grid, {7}, 4)
    # ignore top row markers if any 7? none
    selected=None
    for comp in comps:
        if count_holes(grid, comp)==k:
            selected=comp
            break
    return crop_bbox(grid, selected['cells'])

def solve_S5_M6(grid):
    comps=components(grid, {3}, 4)
    template = max(comps, key=lambda c: len(c['cells']))
    norm = normalize_cells(template['cells'])
    out=blank(*dims(grid))
    h,w=dims(grid)
    # anchors color4
    for r in range(h):
        for c in range(w):
            if grid[r][c]==4:
                for dr,dc in norm:
                    rr,cc=r+dr,c+dc
                    if 0<=rr<h and 0<=cc<w:
                        out[rr][cc]=8
    return out

def solve_S5_M7(grid):
    rows=[row[:] for row in grid if any(v!=0 for v in row)]
    return rows if rows else [[0]*len(grid[0])]

def solve_S5_H1(grid):
    h,w=dims(grid)
    counts=[[0]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if grid[r][c]==4:
                for step in dirs4:
                    for rr,cc in raycast_until(grid,(r,c),step,blockers={5}):
                        counts[rr][cc]+=1
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if counts[r][c]>=2:
                out[r][c]=2
    return out

def solve_S5_H2(grid):
    src=grid[0]
    tgt=grid[1]
    mp={}
    for a,b in zip(src,tgt):
        if a!=0:
            mp[a]=b
    body=grid[2:]
    return [[mp.get(v,v) if v!=0 else 0 for v in row] for row in body]

def solve_S5_H3(grid):
    # colors 1,2,4,5 => rotations 0,1,2,3 quarter turns
    rot_map={1:0,2:1,4:2,5:3}
    template=max(components(grid,{3},4), key=lambda c: len(c['cells']))
    base=normalize_cells(template['cells'])
    out=blank(*dims(grid))
    h,w=dims(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c] in rot_map:
                shape=rotate_norm_cells(base, rot_map[grid[r][c]])
                for dr,dc in shape:
                    rr,cc=r+dr,c+dc
                    if 0<=rr<h and 0<=cc<w:
                        out[rr][cc]=8
    return out

def solve_S5_H4(grid):
    comps=components(grid,{1},4)
    canons=[canonical_rot(normalize_cells(comp['cells'])) for comp in comps]
    from collections import Counter
    cnt=Counter(canons)
    target=next(c for c,n in cnt.items() if n>=2)
    # output canonical shape in color 8
    maxr=max(r for r,c in target); maxc=max(c for r,c in target)
    out=blank(maxr+1,maxc+1)
    for r,c in target:
        out[r][c]=8
    return out

def solve_S5_H5(grid):
    h,w=dims(grid)
    positions={}
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                positions.setdefault(v, []).append((r,c))
    out=blank(h,w)
    for color,cells in positions.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if r1==r2:
            a,b=sorted([c1,c2])
            clear=all(grid[r1][c]==0 or c in (a,b) for c in range(a,b+1))
            if clear:
                for c in range(a,b+1):
                    out[r1][c]=color
        elif c1==c2:
            a,b=sorted([r1,r2])
            clear=all(grid[r][c1]==0 or r in (a,b) for r in range(a,b+1))
            if clear:
                for r in range(a,b+1):
                    out[r][c1]=color
    return out

def solve_S5_H6(grid):
    colors=[1,2,3]
    counts=[sum(v==color for row in grid for v in row) for color in colors]
    w=max(counts) if counts else 1
    out=blank(len(colors), w)
    for i,color in enumerate(colors):
        for c in range(counts[i]):
            out[i][c]=color
    return out

def solve_S5_H7(grid):
    sel_cols=[c for c,v in enumerate(grid[0]) if v==4 and c>0]
    sel_rows=[r for r in range(1,len(grid)) if grid[r][0]==5]
    return [[grid[r][c] for c in sel_cols] for r in sel_rows]


SOLVERS = {
    'S5_E1': solve_S5_E1,
    'S5_E2': solve_S5_E2,
    'S5_E3': solve_S5_E3,
    'S5_E4': solve_S5_E4,
    'S5_E5': solve_S5_E5,
    'S5_E6': solve_S5_E6,
    'S5_E7': solve_S5_E7,
    'S5_M1': solve_S5_M1,
    'S5_M2': solve_S5_M2,
    'S5_M3': solve_S5_M3,
    'S5_M4': solve_S5_M4,
    'S5_M5': solve_S5_M5,
    'S5_M6': solve_S5_M6,
    'S5_M7': solve_S5_M7,
    'S5_H1': solve_S5_H1,
    'S5_H2': solve_S5_H2,
    'S5_H3': solve_S5_H3,
    'S5_H4': solve_S5_H4,
    'S5_H5': solve_S5_H5,
    'S5_H6': solve_S5_H6,
    'S5_H7': solve_S5_H7,
}

if __name__ == '__main__':
    print(f'loaded {len(SOLVERS)} solvers')
