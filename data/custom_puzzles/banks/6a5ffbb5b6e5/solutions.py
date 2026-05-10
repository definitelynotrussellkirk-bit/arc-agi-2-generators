"""Reference helper library and 21 reference solve functions for the second custom ARC puzzle bank."""

from collections import Counter, defaultdict

dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

dirs8 = dirs4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

def components(grid, include_colors=None, connectivity=4):
    h,w=len(grid),len(grid[0])
    seen=[[False]*w for _ in range(h)]
    dirs=dirs4 if connectivity==4 else dirs8
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]: continue
            color=grid[r][c]
            if color==0 or (include_colors is not None and color not in include_colors):
                seen[r][c]=True
                continue
            seen[r][c]=True
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and grid[nr][nc]==color:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({'color':color,'cells':cells})
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs),min(cs),max(rs),max(cs)

def normalize(cells):
    r1,c1,_,_=bbox(cells)
    return sorted((r-r1,c-c1) for r,c in cells)

def copyg(g): return [row[:] for row in g]

def manhattan_to_comp(marker, comp):
    mr,mc=marker
    return min(abs(mr-r)+abs(mc-c) for r,c in comp['cells'])

def is_rectangle_outline_cells(cells):
    r1,c1,r2,c2=bbox(cells)
    if r2-r1<2 or c2-c1<2:
        return False
    expected=set()
    for c in range(c1,c2+1):
        expected.add((r1,c)); expected.add((r2,c))
    for r in range(r1,r2+1):
        expected.add((r,c1)); expected.add((r,c2))
    return set(cells)==expected

def rotate_norm(norm_cells, k):
    # k 0,1,2,3 90 clockwise each
    cells=list(norm_cells)
    for _ in range(k):
        max_r=max(r for r,c in cells)
        cells=[(c,max_r-r) for r,c in cells]
        # renormalize
        minr=min(r for r,c in cells); minc=min(c for r,c in cells)
        cells=[(r-minr,c-minc) for r,c in cells]
    return sorted(cells)

def find_zero_separator_rowcol(grid):
    h,w=len(grid),len(grid[0])
    zero_rows=[r for r in range(h) if all(v==0 for v in grid[r])]
    zero_cols=[c for c in range(w) if all(grid[r][c]==0 for r in range(h))]
    # choose middle-ish
    sr=min(zero_rows, key=lambda r: abs(r-h//2))
    sc=min(zero_cols, key=lambda c: abs(c-w//2))
    return sr, sc

def solve_b2e1(grid):
    out=copyg(grid)
    for comp in components(grid, {1}, 4):
        if normalize(comp['cells'])==[(0,0),(1,0),(2,0)]:
            for r,c in comp['cells']:
                out[r][c]=2
    return out

def solve_b2e2(grid):
    out=copyg(grid)
    comps=components(grid,{3},4)
    smallest=min(comps,key=lambda comp: len(comp['cells']))
    for r,c in smallest['cells']:
        out[r][c]=6
    return out

def solve_b2e3(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        cols=[c for c in range(w) if grid[r][c]==7]
        if len(cols)==2 and all(grid[r][c]==0 for c in range(cols[0]+1, cols[1])):
            for c in range(cols[0],cols[1]+1):
                out[r][c]=7
    return out

def solve_b2e4(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            if grid[r][c]==2 and r+1<h and c+1<w and grid[r+1][c+1]==0:
                out[r+1][c+1]=4
    return out

def solve_b2e5(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for r in range(h-1):
        for c in range(w-1):
            cells=[(r,c),(r+1,c),(r,c+1),(r+1,c+1)]
            vals=[grid[rr][cc] for rr,cc in cells]
            if vals.count(8)==3 and vals.count(0)==1:
                rr,cc=cells[vals.index(0)]
                out[rr][cc]=8
    return out

def solve_b2e6(grid):
    out=copyg(grid)
    for comp in components(grid,{4},4):
        if len(comp['cells'])==3:
            r1,c1,r2,c2=bbox(comp['cells'])
            if r2-r1==1 and c2-c1==1: # 2x2 bbox => L triomino
                for r,c in comp['cells']:
                    out[r][c]=3
    return out

def solve_b2e7(grid):
    out=[[0]*len(grid[0]) for _ in grid]
    for comp in components(grid,{6},4):
        if normalize(comp['cells'])==[(0,0),(0,1),(1,0),(1,1)]:
            for r,c in comp['cells']:
                out[r][c]=6
    return out

def solve_b2m1(grid):
    out=copyg(grid)
    marker=None
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==6:
                marker=(r,c)
    comps=components(grid,{1},4)
    target=min(comps,key=lambda comp: manhattan_to_comp(marker, comp))
    for r,c in target['cells']:
        out[r][c]=7
    return out

def solve_b2m2(grid):
    out=copyg(grid)
    for comp in components(grid,{5},4):
        if not is_rectangle_outline_cells(comp['cells']):
            continue
        r1,c1,r2,c2=bbox(comp['cells'])
        inner_colors=set()
        dot_color=None
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                if grid[r][c] not in (0,5):
                    inner_colors.add(grid[r][c])
        if len(inner_colors)!=1:
            continue
        dot_color=next(iter(inner_colors))
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                out[r][c]=dot_color
    return out

def solve_b2m3(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    for comp in components(grid,{2},4):
        r1,c1,r2,c2=bbox(comp['cells'])
        for c in range(c1,c2+1):
            out[r1][c]=2; out[r2][c]=2
        for r in range(r1,r2+1):
            out[r][c1]=2; out[r][c2]=2
    return out

def solve_b2m4(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    cols=[c for c in range(1,w) if grid[0][c]==1]
    rows=[r for r in range(1,h) if grid[r][0]==2]
    for r in rows:
        for c in cols:
            out[r][c]=4
    return out

def solve_b2m5(grid):
    out=copyg(grid)
    for comp in components(grid,{3},4):
        if is_rectangle_outline_cells(comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=7
    return out

def solve_b2m6(grid):
    out=copyg(grid)
    reds=components(grid,{2},4)
    template=max(reds,key=lambda comp: len(comp['cells']))
    tmpl=normalize(template['cells'])
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==1:
                for dr,dc in tmpl:
                    rr,cc=r+dr,c+dc
                    out[rr][cc]=1
    return out

def solve_b2m7(grid):
    out=copyg(grid)
    positions=defaultdict(list)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v!=0:
                positions[v].append((r,c))
    # only colors with exactly two singleton cells (as entire color count 2)
    for color,cells in positions.items():
        if len(cells)==2:
            (r1,c1),(r2,c2)=cells
            for r in range(min(r1,r2),max(r1,r2)+1):
                for c in range(min(c1,c2),max(c1,c2)+1):
                    out[r][c]=color
    return out

def solve_b2h1(grid):
    h,w=len(grid),len(grid[0])
    sr,sc=find_zero_separator_rowcol(grid)
    quads=[
        ((0,0),(sr,sc)),
        ((0,sc+1),(sr,w)),
        ((sr+1,0),(h,sc)),
        ((sr+1,sc+1),(h,w)),
    ]
    shapes=[]
    empty_idx=None
    color=None
    for i,((r0,c0),(r1,c1)) in enumerate(quads):
        cells=[]
        cols=set()
        for r in range(r0,r1):
            for c in range(c0,c1):
                if grid[r][c]!=0:
                    cells.append((r-r0,c-c0))
                    cols.add(grid[r][c])
        if cells:
            shapes.append((i,sorted(cells), next(iter(cols))))
        else:
            empty_idx=i
    # choose common shape from first non-empty (assumed same)
    shape=shapes[0][1]
    color=shapes[0][2]
    out=copyg(grid)
    (r0,c0),(r1,c1)=quads[empty_idx]
    for dr,dc in shape:
        out[r0+dr][c0+dc]=color
    return out

def solve_b2h2(grid):
    out=copyg(grid)
    k=sum(1 for v in grid[0] if v==1)
    comps=[comp for comp in components(grid,{3},4) if all(r>0 for r,c in comp['cells'])]
    comps_sorted=sorted(comps,key=lambda comp: (-len(comp['cells']), min(comp['cells'])))
    target=comps_sorted[k-1]
    for r,c in target['cells']:
        out[r][c]=2
    return out

def solve_b2h3(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    # keep marker
    corners={(0,0):0,(0,w-1):1,(h-1,w-1):2,(h-1,0):3}
    k=None
    for (r,c),rot in corners.items():
        if grid[r][c]==8:
            k=rot
            out[r][c]=8
            break
    comp=max(components(grid,{2},4), key=lambda comp: len(comp['cells']))
    r1,c1,r2,c2=bbox(comp['cells'])
    rot_cells=rotate_norm(normalize(comp['cells']), k)
    for dr,dc in rot_cells:
        out[r1+dr][c1+dc]=2
    return out

def solve_b2h4(grid):
    out=copyg(grid)
    template=max(components(grid,{5},4), key=lambda comp: len(comp['cells']))
    tmpl=normalize(template['cells'])
    color_to_rot={1:0,2:1,3:2,4:3}
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v in color_to_rot:
                rot_cells=rotate_norm(tmpl, color_to_rot[v])
                for dr,dc in rot_cells:
                    rr,cc=r+dr,c+dc
                    out[rr][cc]=v
    return out

def solve_b2h5(grid):
    out=copyg(grid)
    nonzero=[v for v in grid[0] if v!=0]
    # pair consecutive nonzeros
    pairs=list(zip(nonzero[::2], nonzero[1::2]))
    mapping={}
    for a,b in pairs:
        mapping[a]=b
    for r in range(1,len(grid)):
        for c in range(len(grid[0])):
            v=grid[r][c]
            if v in mapping:
                out[r][c]=mapping[v]
    return out

def solve_b2h6(grid):
    h,w=len(grid),len(grid[0])
    out=copyg(grid)
    top=grid[0]
    left=[grid[r][0] for r in range(h)]
    for r in range(1,h):
        for c in range(1,w):
            out[r][c]=top[c] if top[c]==left[r] else 0
    return out

def solve_b2h7(grid):
    out=copyg(grid)
    comps=components(grid,{3},4)
    shape_counts=Counter(tuple(normalize(comp['cells'])) for comp in comps)
    target=None
    for comp in comps:
        sh=tuple(normalize(comp['cells']))
        if shape_counts[sh]==1:
            target=comp
            break
    r1,c1,r2,c2=bbox(target['cells'])
    # draw border outside bbox one cell away
    for c in range(c1-1,c2+2):
        out[r1-1][c]=4
        out[r2+1][c]=4
    for r in range(r1-1,r2+2):
        out[r][c1-1]=4
        out[r][c2+1]=4
    return out

SOLVERS = {

    "S2_E1": solve_b2e1,
    "S2_E2": solve_b2e2,
    "S2_E3": solve_b2e3,
    "S2_E4": solve_b2e4,
    "S2_E5": solve_b2e5,
    "S2_E6": solve_b2e6,
    "S2_E7": solve_b2e7,
    "S2_M1": solve_b2m1,
    "S2_M2": solve_b2m2,
    "S2_M3": solve_b2m3,
    "S2_M4": solve_b2m4,
    "S2_M5": solve_b2m5,
    "S2_M6": solve_b2m6,
    "S2_M7": solve_b2m7,
    "S2_H1": solve_b2h1,
    "S2_H2": solve_b2h2,
    "S2_H3": solve_b2h3,
    "S2_H4": solve_b2h4,
    "S2_H5": solve_b2h5,
    "S2_H6": solve_b2h6,
    "S2_H7": solve_b2h7,
}
