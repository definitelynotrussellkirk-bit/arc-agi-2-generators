"""Reference helper library and 21 reference solve functions for the third custom ARC puzzle bank."""

from collections import defaultdict

dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

dirs8 = dirs4 + [(-1,-1),(-1,1),(1,-1),(1,1)]

def components(grid, include_colors=None, connectivity=4):
    h,w=len(grid),len(grid[0])
    seen=[[False]*w for _ in range(h)]
    dirs=dirs4 if connectivity==4 else dirs8
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
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

def border_distance(comp,h,w):
    r1,c1,r2,c2=bbox(comp['cells'])
    return min(r1,c1,h-1-r2,w-1-c2)

def choose_separator_row(grid):
    h=len(grid)
    candidates=[r for r in range(h) if all(v==0 for v in grid[r]) and any(any(x!=0 for x in row) for row in grid[:r]) and any(any(x!=0 for x in row) for row in grid[r+1:])]
    if not candidates:
        raise ValueError("no separator row")
    return min(candidates, key=lambda r: abs(r-h//2))

def choose_separator_col(grid):
    h,w=len(grid),len(grid[0])
    candidates=[c for c in range(w) if all(grid[r][c]==0 for r in range(h)) and any(any(row[:c]) for row in grid) and any(any(row[c+1:]) for row in grid)]
    if not candidates:
        raise ValueError("no separator col")
    return min(candidates, key=lambda c: abs(c-w//2))

def count_holes_in_component(grid, comp):
    # count 4-connected zero components fully enclosed in bbox and not touching bbox edge
    cells=set(comp['cells'])
    color=comp['color']
    r1,c1,r2,c2=bbox(comp['cells'])
    seen=set()
    holes=0
    for r in range(r1,r2+1):
        for c in range(c1,c2+1):
            if (r,c) in cells or (r,c) in seen:
                continue
            if grid[r][c]!=0:
                seen.add((r,c))
                continue
            # flood zero region within bbox
            q=[(r,c)]
            seen.add((r,c))
            region=[]
            touches=False
            while q:
                rr,cc=q.pop()
                region.append((rr,cc))
                if rr in (r1,r2) or cc in (c1,c2):
                    touches=True
                for dr,dc in dirs4:
                    nr,nc=rr+dr,cc+dc
                    if r1<=nr<=r2 and c1<=nc<=c2 and (nr,nc) not in seen and (nr,nc) not in cells and grid[nr][nc]==0:
                        seen.add((nr,nc))
                        q.append((nr,nc))
            if not touches:
                holes+=1
    return holes

def solve_s3e1(grid):
    out=copyg(grid)
    for comp in components(grid,{1},4):
        if len(comp['cells'])==1:
            r,c=comp['cells'][0]
            out[r][c]=2
    return out

def solve_s3e2(grid):
    out=copyg(grid)
    comps=components(grid,{4},4)
    target=min(comps,key=lambda comp:(bbox(comp['cells'])[1],bbox(comp['cells'])[0]))
    for r,c in target['cells']:
        out[r][c]=3
    return out

def solve_s3e3(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for c in range(w):
        rows=[r for r in range(h) if grid[r][c]==6]
        if len(rows)==2 and all(grid[r][c]==0 for r in range(rows[0]+1, rows[1])):
            for r in range(rows[0], rows[1]+1):
                out[r][c]=6
    return out

def solve_s3e4(grid):
    out=copyg(grid)
    for comp in components(grid,{2},4):
        if normalize(comp['cells'])==[(0,0),(0,1),(0,2)]:
            r1,c1,_,_=bbox(comp['cells'])
            out[r1][c1+1]=1
    return out

def solve_s3e5(grid):
    out=copyg(grid)
    for comp in components(grid,{5},4):
        if normalize(comp['cells'])==[(0,0),(0,1)]:
            for r,c in comp['cells']:
                out[r][c]=8
    return out

def solve_s3e6(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    for r in range(h):
        for c in range(w):
            if grid[r][c]==9:
                rr,cc=r+1,c-1
                if 0<=rr<h and 0<=cc<w and out[rr][cc]==0:
                    out[rr][cc]=5
    return out

def solve_s3e7(grid):
    out=copyg(grid)
    comps=components(grid,None,4)
    by_color=defaultdict(list)
    for comp in comps:
        by_color[comp['color']].append(comp)
    target_color=min([color for color,lst in by_color.items() if len(lst)==1])
    for comp in by_color[target_color]:
        for r,c in comp['cells']:
            out[r][c]=4
    return out

def solve_s3m1(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    pivot=next((r,c) for r in range(h) for c in range(w) if grid[r][c]==5)
    pr,pc=pivot
    for r in range(h):
        for c in range(w):
            v=grid[r][c]
            if v not in (0,5):
                rr,cc=2*pr-r, 2*pc-c
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=v
    return out

def solve_s3m2(grid):
    out=copyg(grid)
    comps=components(grid,None,4)
    frames=[comp for comp in comps if comp['color']!=2 and is_rectangle_outline_cells(comp['cells'])]
    dots=[comp for comp in comps if comp['color']==2 and len(comp['cells'])==1]
    for frame in frames:
        r1,c1,r2,c2=bbox(frame['cells'])
        for dot in dots:
            dr,dc=dot['cells'][0]
            if r1<dr<r2 and c1<dc<c2:
                color=frame['color']
                for c in range(c1+1,c2):
                    out[dr][c]=color
                for r in range(r1+1,r2):
                    out[r][dc]=color
    return out

def solve_s3m3(grid):
    out=copyg(grid)
    comps=components(grid,{1},4)
    h,w=len(grid),len(grid[0])
    target=max(comps,key=lambda comp:(border_distance(comp,h,w), -bbox(comp['cells'])[0], -bbox(comp['cells'])[1]))
    for r,c in target['cells']:
        out[r][c]=7
    return out

def solve_s3m4(grid):
    out=copyg(grid)
    h,w=len(grid),len(grid[0])
    marked=[c for c in range(w) if grid[0][c]==2]
    for r in range(1,h):
        for c in marked:
            if grid[r][c]==1:
                out[r][c]=3
    return out

def solve_s3m5(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    for comp in components(grid,None,4):
        if comp['color']==0: 
            continue
        r1,c1,r2,c2=bbox(comp['cells'])
        # assume odd dimensions
        cr,cc=(r1+r2)//2,(c1+c2)//2
        out[cr][cc]=comp['color']
    return out

def solve_s3m6(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    for comp in components(grid,None,4):
        if comp['color']==0: continue
        r1,c1,r2,c2=bbox(comp['cells'])
        for rr,cc in [(r1,c1),(r1,c2),(r2,c1),(r2,c2)]:
            out[rr][cc]=comp['color']
    return out

def solve_s3m7(grid):
    h,w=len(grid),len(grid[0])
    out=[[0]*w for _ in range(h)]
    pivot=next((r,c) for r in range(h) for c in range(w) if grid[r][c]==6)
    pr,pc=pivot
    out[pr][pc]=6
    for comp in components(grid,None,4):
        if comp['color'] in (0,6): continue
        for r,c in comp['cells']:
            dr,dc=r-pr,c-pc
            rr,cc=pr+dc, pc-dr
            out[rr][cc]=comp['color']
    return out

def solve_s3h1(grid):
    h,w=len(grid),len(grid[0])
    sep=choose_separator_row(grid)
    legend=components([row[:] for row in grid[:sep]], None, 4)
    mapping={}
    for comp in legend:
        mapping[tuple(normalize(comp['cells']))]=comp['color']
    out=copyg(grid)
    for comp in components([row[:] for row in grid[sep+1:]], {5}, 4):
        shape=tuple(normalize(comp['cells']))
        color=mapping[shape]
        for r,c in comp['cells']:
            out[sep+1+r][c]=color
    return out

def solve_s3h2(grid):
    out=copyg(grid)
    k=sum(1 for v in grid[0] if v==1)
    for c in range(len(grid[0])):
        if out[0][c]==1:
            out[0][c]=0
    candidates=[comp for comp in components(grid,{3},4) if all(r>0 for r,c in comp['cells'])]
    target=next(comp for comp in candidates if count_holes_in_component(grid, comp)==k)
    for r,c in target['cells']:
        out[r][c]=2
    return out

def solve_s3h3(grid):
    # template color 3, anchors 1 and 2. output overlap of template stamped at anchor positions, color 8
    h,w=len(grid),len(grid[0])
    template=max(components(grid,{3},4), key=lambda comp: len(comp['cells']))
    shape=normalize(template['cells'])
    anchors={}
    for r in range(h):
        for c in range(w):
            if grid[r][c] in (1,2):
                anchors[grid[r][c]]=(r,c)
    stamps=[]
    for marker in (1,2):
        r0,c0=anchors[marker]
        stamps.append(set((r0+dr,c0+dc) for dr,dc in shape))
    overlap=stamps[0] & stamps[1]
    out=[[0]*w for _ in range(h)]
    for r,c in overlap:
        if 0<=r<h and 0<=c<w:
            out[r][c]=8
    return out

def solve_s3h4(grid):
    # frame defines vertical symmetry axis; mirror nonzero non-frame cells from whichever side exists
    out=copyg(grid)
    frame=max([comp for comp in components(grid,None,4) if is_rectangle_outline_cells(comp['cells'])], key=lambda comp: len(comp['cells']))
    r1,c1,r2,c2=bbox(frame['cells'])
    axis=(c1+c2)//2
    for r in range(r1+1,r2):
        for c in range(c1+1,c2+1):
            v=grid[r][c]
            if v!=0 and v!=frame['color']:
                mc=2*axis-c
                if c1<mc<c2:
                    out[r][mc]=v
    return out

def solve_s3h5(grid):
    out=copyg(grid)
    frames=[comp for comp in components(grid,None,4) if is_rectangle_outline_cells(comp['cells'])]
    dots=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==1]
    for r,c in dots:
        enclosing=[]
        for frame in frames:
            r1,c1,r2,c2=bbox(frame['cells'])
            if r1<r<r2 and c1<c<c2:
                area=(r2-r1+1)*(c2-c1+1)
                enclosing.append((area,frame['color']))
        if enclosing:
            color=min(enclosing)[1]
            out[r][c]=color
    return out

def solve_s3h6(grid):
    h,w=len(grid),len(grid[0])
    sep=choose_separator_col(grid)
    k=sum(1 for r in range(h) for c in range(sep) if grid[r][c]==1)
    right=[[grid[r][c] for c in range(sep+1,w)] for r in range(h)]
    target=None
    for comp in components(right,{3},4):
        if len(comp['cells'])==k:
            target=comp; break
    out=copyg(grid)
    r1,c1,r2,c2=bbox(target['cells'])
    c1+=sep+1; c2+=sep+1
    for c in range(c1,c2+1):
        out[r1][c]=8; out[r2][c]=8
    for r in range(r1,r2+1):
        out[r][c1]=8; out[r][c2]=8
    return out

def solve_s3h7(grid):
    # top legend row contains groups of 2's,4's,6's? Actually groups of 1 markers? Use contiguous markers of colors as legend? 
    # Let's define top row has groups of color markers where group length encodes size and color itself is output color.
    # bottom gray objects of sizes matching lengths; recolor by matching size.
    h,w=len(grid),len(grid[0])
    # parse top row contiguous groups nonzero
    top=grid[0]
    mapping={}
    c=0
    while c<w:
        if top[c]==0:
            c+=1; continue
        color=top[c]
        start=c
        while c<w and top[c]==color:
            c+=1
        length=c-start
        mapping[length]=color
    out=copyg(grid)
    for comp in components(grid[1:],{5},4):
        size=len(comp['cells'])
        color=mapping[size]
        for r,c in comp['cells']:
            out[1+r][c]=color
    return out

SOLVERS = {

    "S3_E1": solve_s3e1,
    "S3_E2": solve_s3e2,
    "S3_E3": solve_s3e3,
    "S3_E4": solve_s3e4,
    "S3_E5": solve_s3e5,
    "S3_E6": solve_s3e6,
    "S3_E7": solve_s3e7,
    "S3_M1": solve_s3m1,
    "S3_M2": solve_s3m2,
    "S3_M3": solve_s3m3,
    "S3_M4": solve_s3m4,
    "S3_M5": solve_s3m5,
    "S3_M6": solve_s3m6,
    "S3_M7": solve_s3m7,
    "S3_H1": solve_s3h1,
    "S3_H2": solve_s3h2,
    "S3_H3": solve_s3h3,
    "S3_H4": solve_s3h4,
    "S3_H5": solve_s3h5,
    "S3_H6": solve_s3h6,
    "S3_H7": solve_s3h7,
}
