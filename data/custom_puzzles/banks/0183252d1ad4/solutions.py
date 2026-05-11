"""Reference helper library and 21 reference solve functions for the fourth custom ARC puzzle bank."""



from collections import defaultdict



dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

dirs8 = dirs4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

square2 = [(0,0),(0,1),(1,0),(1,1)]

diag2_shapes = {((0,0),(1,1)), ((0,1),(1,0))}

T_shapes = {
    ((0, 0), (0, 1), (0, 2), (1, 1)),
    ((0, 0), (1, 0), (1, 1), (2, 0)),
    ((0, 1), (1, 0), (1, 1), (1, 2)),
    ((0, 1), (1, 0), (1, 1), (2, 1)),
}



def components(grid, include_colors=None, connectivity=4):
    h,w=len(grid),len(grid[0])
    seen=[[False]*w for _ in range(h)]
    dirs=dirs4 if connectivity==4 else dirs8
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
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
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and grid[nr][nc]==color:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({'color':color,'cells':sorted(cells)})
    return comps

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def normalize(cells):
    r0,c0,_,_=bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def center_bbox(cells):
    r1,c1,r2,c2=bbox(cells)
    return ((r1+r2)/2, (c1+c2)/2)

def copyg(g): return [row[:] for row in g]

def fill_between_vertical_markers(grid, color):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for c in range(w):
        rows=[r for r in range(h) if grid[r][c]==color]
        if len(rows)>=2:
            # pair consecutive? fill between every pair? We'll use top-bottom if exactly 2
            if len(rows)==2:
                r1,r2=rows
                for r in range(r1,r2+1):
                    out[r][c]=color
    return out

def ring3_centers(grid, color_ring=5, color_fill=8):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for r in range(h-2):
        for c in range(w-2):
            cells=[grid[r+i][c+j] for i in range(3) for j in range(3)]
            ring_positions={(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)}
            if all(grid[r+i][c+j]==color_ring for i,j in ring_positions) and grid[r+1][c+1]==0:
                out[r+1][c+1]=color_fill
    return out

def rotate_norm_cells(cells, times=1):
    shape=normalize(cells)
    for _ in range(times%4):
        # rotate within bbox
        maxr=max(r for r,c in shape); maxc=max(c for r,c in shape)
        h=maxr+1; w=maxc+1
        shape=sorted((c, h-1-r) for r,c in shape)
        # renormalize
        r0=min(r for r,c in shape); c0=min(c for r,c in shape)
        shape=sorted((r-r0,c-c0) for r,c in shape)
    return shape

def is_rect_outline(cells):
    r1,c1,r2,c2=bbox(cells)
    expected=set()
    for c in range(c1,c2+1):
        expected.add((r1,c)); expected.add((r2,c))
    for r in range(r1,r2+1):
        expected.add((r,c1)); expected.add((r,c2))
    return set(cells)==expected and r2-r1>=2 and c2-c1>=2

def count_holes_component(grid, comp):
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
            region=[]
            touch=False
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
                holes+=1
    return holes

def is_solid_rectangle(cells):
    r1,c1,r2,c2=bbox(cells)
    return set(cells)=={(r,c) for r in range(r1,r2+1) for c in range(c1,c2+1)}



def solve_s4e1(grid):
    out=copyg(grid)
    for comp in components(grid,{1},4):
        if normalize(comp['cells'])==sorted(square2):
            for r,c in comp['cells']:
                out[r][c]=2
    return out

def solve_s4e2(grid):
    out=copyg(grid)
    comps=components(grid,{2},4)
    target=max(comps,key=lambda comp:(bbox(comp['cells'])[2], bbox(comp['cells'])[0], bbox(comp['cells'])[1]))
    for r,c in target['cells']:
        out[r][c]=3
    return out

def solve_s4e3(grid):
    return fill_between_vertical_markers(grid,7)

def solve_s4e4(grid):
    return ring3_centers(grid,5,8)

def solve_s4e5(grid):
    out=copyg(grid)
    for comp in components(grid,{3},4):
        if tuple(normalize(comp['cells'])) in T_shapes:
            for r,c in comp['cells']:
                out[r][c]=6
    return out

def solve_s4e6(grid):
    out=copyg(grid)
    for comp in components(grid,{1},4):
        if any(c==0 for r,c in comp['cells']):
            for r,c in comp['cells']:
                out[r][c]=4
    return out

def solve_s4e7(grid):
    out=copyg(grid)
    for comp in components(grid,{2},8):
        if len(comp['cells'])==2 and tuple(normalize(comp['cells'])) in diag2_shapes:
            for r,c in comp['cells']:
                out[r][c]=8
    return out

def solve_s4m1(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    gc=((h-1)/2,(w-1)/2)
    def dist(comp):
        cr,cc=center_bbox(comp['cells'])
        return abs(cr-gc[0])+abs(cc-gc[1])
    comps=components(grid,{3},4)
    target=min(comps,key=lambda comp:(dist(comp), bbox(comp['cells'])[0], bbox(comp['cells'])[1]))
    for r,c in target['cells']:
        out[r][c]=7
    return out

def solve_s4m2(grid):
    out=copyg(grid)
    comps=components(grid,None,4)
    # group vertical bars by color and row span
    bars=[]
    for comp in comps:
        r1,c1,r2,c2=bbox(comp['cells'])
        if c1==c2 and len(comp['cells'])==r2-r1+1 and len(comp['cells'])>=2:
            bars.append((comp['color'], r1,r2,c1))
    grouped=defaultdict(list)
    for color,r1,r2,c in bars:
        grouped[(color,r1,r2)].append(c)
    for (color,r1,r2), cols in grouped.items():
        cols=sorted(cols)
        if len(cols)>=2:
            # pair consecutive
            for i in range(0,len(cols),2):
                if i+1 < len(cols):
                    c1,c2=cols[i],cols[i+1]
                    for r in range(r1,r2+1):
                        for c in range(c1,c2+1):
                            out[r][c]=color
    return out

def solve_s4m3(grid):
    out=copyg(grid)
    n=len(grid)
    for r in range(n):
        for c in range(n):
            if grid[r][c]!=0:
                out[c][r]=grid[r][c]
    return out

def solve_s4m4(grid):
    out=copyg(grid)
    count=sum(v==5 for row in grid for v in row)
    comps=components(grid,{1},4)
    target=min([comp for comp in comps if len(comp['cells'])==count], key=lambda comp:bbox(comp['cells']))
    for r,c in target['cells']:
        out[r][c]=2
    return out

def solve_s4m5(grid):
    out=copyg(grid)
    for comp in components(grid,{4},4):
        cells=comp['cells']
        r1,c1,r2,c2=bbox(cells)
        h,w=r2-r1+1,c2-c1+1
        if h%2==1 and w%2==1 and is_solid_rectangle(cells):
            for r,c in cells:
                out[r][c]=0
            mr=(r1+r2)//2
            mc=(c1+c2)//2
            for c in range(c1,c2+1):
                out[mr][c]=4
            for r in range(r1,r2+1):
                out[r][mc]=4
    return out

def solve_s4m6(grid):
    out=copyg(grid)
    pos_by_color=defaultdict(list)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                pos_by_color[grid[r][c]].append((r,c))
    for color, cells in pos_by_color.items():
        if len(cells)==4:
            rs=sorted(set(r for r,c in cells)); cs=sorted(set(c for r,c in cells))
            if len(rs)==2 and len(cs)==2 and set(cells)=={(rs[0],cs[0]),(rs[0],cs[1]),(rs[1],cs[0]),(rs[1],cs[1])}:
                r1,r2=rs; c1,c2=cs
                for c in range(c1,c2+1):
                    out[r1][c]=color; out[r2][c]=color
                for r in range(r1,r2+1):
                    out[r][c1]=color; out[r][c2]=color
    return out

def solve_s4m7(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for comp in components(grid,{3},4):
        cells=set(comp['cells'])
        if len(cells)!=4 or tuple(normalize(comp['cells'])) not in T_shapes:
            continue
        # find center degree 3
        center=None
        for r,c in cells:
            n=sum((r+dr,c+dc) in cells for dr,dc in dirs4)
            if n==3:
                center=(r,c)
                break
        if center is None: 
            continue
        r,c=center
        for dr,dc in dirs4:
            nr,nc=r+dr,c+dc
            if (nr,nc) not in cells:
                out[nr][nc]=3
    return out

def solve_s4h1(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    assert h==w and h%2==0
    midr=h//2
    midc=w//2
    # source upper-left quadrant
    for r in range(midr):
        for c in range(midc):
            val=grid[r][c]
            if val!=0:
                out[r][c]=val
                out[r][w-1-c]=val
                out[h-1-r][c]=val
                out[h-1-r][w-1-c]=val
    return out

def solve_s4h2(grid):
    out=copyg(grid)
    # template: first component of color 2 not inside frame color 5
    comps2=components(grid,{2},4)
    # choose component with smallest bbox top-left
    template=min(comps2,key=lambda comp:(bbox(comp['cells'])[0],bbox(comp['cells'])[1]))
    template_shape=normalize(template['cells'])
    # erase any markers? We'll overwrite interiors only
    frames=[comp for comp in components(grid,{5},4) if is_rect_outline(comp['cells'])]
    for frame in frames:
        r1,c1,r2,c2=bbox(frame['cells'])
        # find marker color 8 inside bbox
        marker=None
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                if grid[r][c]==8:
                    marker=(r,c)
        if marker is None:
            continue
        mr,mc=marker
        # mapping corner to rotation
        corners={(r1+1,c1+1):0,(r1+1,c2-1):1,(r2-1,c2-1):2,(r2-1,c1+1):3}
        # marker expected exactly at one interior corner
        rot=corners[marker]
        shape=rotate_norm_cells(template_shape, rot)
        # clear marker interior
        out[mr][mc]=0
        # stamp in interior anchored at top-left interior
        for dr,dc in shape:
            rr,cc=r1+1+dr,c1+1+dc
            out[rr][cc]=2
    return out

def solve_s4h3(grid):
    out=copyg(grid)
    marker_count=sum(v==6 for row in grid for v in row)
    # target among green components
    targets=[]
    for comp in components(grid,{3},4):
        holes=count_holes_component(grid,comp)
        if holes==marker_count:
            targets.append(comp)
    # choose top-left if multiple
    if targets:
        target=min(targets,key=lambda comp:bbox(comp['cells']))
        for r,c in target['cells']:
            out[r][c]=7
    return out

def solve_s4h4(grid):
    # fixed layout 11x11: top header 3 blocks rows 0:2 at cols [3:5,6:8,9:11]
    # left header 3 blocks cols 0:2 at rows [3:5,6:8,9:11]
    out=copyg(grid)
    row_starts=[3,6,9]
    col_starts=[3,6,9]
    top_counts=[]
    left_counts=[]
    for cs in col_starts:
        cnt=sum(grid[r][c]!=0 for r in range(0,2) for c in range(cs,cs+2))
        top_counts.append(cnt)
    for rs in row_starts:
        cnt=sum(grid[r][c]!=0 for r in range(rs,rs+2) for c in range(0,2))
        left_counts.append(cnt)
    for i,rs in enumerate(row_starts):
        for j,cs in enumerate(col_starts):
            if top_counts[j]>left_counts[i]:
                color=4
            elif top_counts[j]<left_counts[i]:
                color=3
            else:
                color=8
            for r in range(rs,rs+2):
                for c in range(cs,cs+2):
                    out[r][c]=color
    return out

def solve_s4h5(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    # pivot is 9
    pivots=[(r,c) for r in range(h) for c in range(w) if grid[r][c]==9]
    assert len(pivots)==1
    pr,pc=pivots[0]
    # choose non-pivot cells of color 2? Could support all nonzero except 9 and maybe keep others?
    cells=[(r,c,grid[r][c]) for r in range(h) for c in range(w) if grid[r][c]!=0 and grid[r][c]!=9]
    for r,c,color in cells:
        dr,dc=r-pr,c-pc
        rots=[(dr,dc),(dc,-dr),(-dr,-dc),(-dc,dr)]
        for rr,cc in rots:
            out[pr+rr][pc+cc]=color
    return out

def solve_s4h6(grid):
    out=copyg(grid)
    # template: neutral color 1 component with smallest bbox
    template=min(components(grid,{1},4), key=lambda comp:bbox(comp['cells']))
    shape=normalize(template['cells'])
    frames=[comp for comp in components(grid,{5},4) if is_rect_outline(comp['cells'])]
    for frame in frames:
        r1,c1,r2,c2=bbox(frame['cells'])
        # find any nonzero interior marker not 5
        marker=None
        for r in range(r1+1,r2):
            for c in range(c1+1,c2):
                if grid[r][c] not in (0,5):
                    marker=(r,c,grid[r][c])
        if marker is None:
            continue
        mr,mc,color=marker
        out[mr][mc]=0
        for dr,dc in shape:
            out[r1+1+dr][c1+1+dc]=color
    return out

def solve_s4h7(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    zero_cols=[c for c in range(w) if all(grid[r][c]==0 for r in range(h)) and any(any(v!=0 for v in row[:c]) for row in grid) and any(any(v!=0 for v in row[c+1:]) for row in grid)]
    sep=min(zero_cols, key=lambda c: abs(c-w/2))
    comps_left=[comp for comp in components(grid,{1},4) if bbox(comp['cells'])[3] < sep]
    mapping={}
    for comp in comps_left:
        r1,c1,r2,c2=bbox(comp['cells'])
        sample=None
        for r in range(max(0,r1-1), min(h,r2+2)):
            for c in range(c2+1,sep):
                if grid[r][c] not in (0,1):
                    sample=grid[r][c]
        mapping[tuple(normalize(comp['cells']))]=sample
    for comp in components(grid,{1},4):
        if bbox(comp['cells'])[1] > sep:
            color=mapping.get(tuple(normalize(comp['cells'])),1)
            for r,c in comp['cells']:
                out[r][c]=color
    return out



SOLVERS = {

    'S4_E1': solve_s4e1,

    'S4_E2': solve_s4e2,

    'S4_E3': solve_s4e3,

    'S4_E4': solve_s4e4,

    'S4_E5': solve_s4e5,

    'S4_E6': solve_s4e6,

    'S4_E7': solve_s4e7,

    'S4_M1': solve_s4m1,

    'S4_M2': solve_s4m2,

    'S4_M3': solve_s4m3,

    'S4_M4': solve_s4m4,

    'S4_M5': solve_s4m5,

    'S4_M6': solve_s4m6,

    'S4_M7': solve_s4m7,

    'S4_H1': solve_s4h1,

    'S4_H2': solve_s4h2,

    'S4_H3': solve_s4h3,

    'S4_H4': solve_s4h4,

    'S4_H5': solve_s4h5,

    'S4_H6': solve_s4h6,

    'S4_H7': solve_s4h7,

}
