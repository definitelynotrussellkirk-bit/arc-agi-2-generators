"""Reference helper library and 21 reference solve functions for the seventh custom ARC puzzle bank.

New primitive introduced in this set:
  slide_component(grid, cells, step, blockers=None)
It repeatedly translates a connected shape one step at a time until the next
step would leave the grid or hit a blocker.
"""

from typing import Iterable, Tuple, List

Grid = List[List[int]]

dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]

dir_from_marker = {1:(0,-1), 2:(0,1), 3:(-1,0), 4:(1,0)}


def blank(h,w,v=0):
    return [[v]*w for _ in range(h)]


def copyg(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def inb(g,r,c):
    h,w = dims(g)
    return 0 <= r < h and 0 <= c < w


def components(grid, colors=None, connectivity=4, include_zero=False):
    h,w = dims(grid)
    seen = [[False]*w for _ in range(h)]
    dirs = dirs4 if connectivity == 4 else dirs8
    comps = []
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c] = True
            color = grid[r][c]
            if (color == 0 and not include_zero) or (colors is not None and color not in colors):
                continue
            q = [(r,c)]
            cells = []
            while q:
                rr,cc = q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc = rr+dr, cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and grid[nr][nc] == color:
                        seen[nr][nc] = True
                        q.append((nr,nc))
            comps.append({'color': color, 'cells': sorted(cells)})
    return comps


def nonzero_components(grid, connectivity=4):
    h,w=dims(grid)
    seen = [[False]*w for _ in range(h)]
    dirs = dirs4 if connectivity == 4 else dirs8
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c]==0:
                continue
            seen[r][c]=True
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and grid[nr][nc]!=0:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({'cells': sorted(cells)})
    return comps


def bbox(cells):
    rs = [r for r,c in cells]
    cs = [c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def normalize(cells):
    r1,c1,r2,c2 = bbox(cells)
    return sorted((r-r1, c-c1) for r,c in cells)


def slide_component(grid:Grid, cells:Iterable[Tuple[int,int]], step:Tuple[int,int], blockers=None):
    """Move a connected shape stepwise until the next move would leave the grid or hit a blocker."""
    h,w=dims(grid)
    cells = set(cells)
    if blockers is None:
        blockers={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0 and (r,c) not in cells}
    else:
        blockers=set(blockers) - cells
    dr,dc=step
    cur=set(cells)
    while True:
        nxt={(r+dr,c+dc) for r,c in cur}
        if any(not (0<=r<h and 0<=c<w) for r,c in nxt):
            break
        if any((r,c) in blockers for r,c in nxt):
            break
        cur=nxt
    return sorted(cur)


def area(comp):
    return len(comp['cells'])


def comp_height(comp):
    r1,c1,r2,c2=bbox(comp['cells'])
    return r2-r1+1


def extract_component_from_cell(grid, cell, ignore_colors={0,8,1,2,3,4}):
    r,c=cell
    color=grid[r][c]
    assert color not in ignore_colors
    seen={cell}
    q=[cell]
    cells=[]
    while q:
        rr,cc=q.pop()
        cells.append((rr,cc))
        for dr,dc in dirs4:
            nr,nc=rr+dr,cc+dc
            if inb(grid,nr,nc) and (nr,nc) not in seen and grid[nr][nc]==color:
                seen.add((nr,nc)); q.append((nr,nc))
    return {'color':color,'cells':sorted(cells)}


def gravity_slide_all(grid, step, immobile_colors={8}, remove_marker_pos=None, dynamic_colors=None):
    # move all nonzero components except immobile colors and optional marker positions as rigid bodies
    h,w=dims(grid)
    out=copyg(grid)
    if remove_marker_pos:
        for r,c in remove_marker_pos:
            out[r][c]=0
    # repeat until stable
    changed=True
    while changed:
        changed=False
        # collect movable components on current grid
        comps=[]
        seen=[[False]*w for _ in range(h)]
        for r in range(h):
            for c in range(w):
                if seen[r][c] or out[r][c]==0 or out[r][c] in immobile_colors or (remove_marker_pos and (r,c) in remove_marker_pos):
                    continue
                color=out[r][c]
                if dynamic_colors is not None and color not in dynamic_colors:
                    continue
                seen[r][c]=True
                q=[(r,c)]
                cells=[]
                while q:
                    rr,cc=q.pop()
                    cells.append((rr,cc))
                    for dr,dc in dirs4:
                        nr,nc=rr+dr,cc+dc
                        if inb(out,nr,nc) and not seen[nr][nc] and out[nr][nc]==color:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                comps.append({'color':color,'cells':sorted(cells)})
        dr,dc=step
        # order opposite of motion so leading components settle first
        if step==(1,0):
            comps=sorted(comps,key=lambda comp:max(r for r,c in comp['cells']), reverse=True)
        elif step==(-1,0):
            comps=sorted(comps,key=lambda comp:min(r for r,c in comp['cells']))
        elif step==(0,1):
            comps=sorted(comps,key=lambda comp:max(c for r,c in comp['cells']), reverse=True)
        else:
            comps=sorted(comps,key=lambda comp:min(c for r,c in comp['cells']))
        for comp in comps:
            cells=set(comp['cells'])
            blockers={(r,c) for r,row in enumerate(out) for c,v in enumerate(row) if v!=0 and (r,c) not in cells and v not in ()}
            slid=slide_component(out, cells, step, blockers)
            if set(slid) != cells:
                changed=True
                # move comp in out
                for r,c in cells:
                    out[r][c]=0
                for r,c in slid:
                    out[r][c]=comp['color']
        # loop until none moved
    return out


def solve_S7_E1(grid):
    out=copyg(grid)
    reds=[comp for comp in components(grid,{2},4)]
    assert len(reds)==1
    comp=reds[0]
    for r,c in comp['cells']:
        out[r][c]=0
    blockers={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0 and v!=2}
    slid=slide_component(grid, comp['cells'], (0,1), blockers)
    for r,c in slid:
        out[r][c]=2
    return out


def solve_S7_E2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for c in range(w):
        cnt=sum(grid[r][c]==1 for r in range(h))
        for r in range(h-cnt,h):
            out[r][c]=1
    return out


def solve_S7_E3(grid):
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==4]
    assert len(pts)==2
    (r1,c1),(r2,c2)=pts
    ra,rb=sorted([r1,r2]); ca,cb=sorted([c1,c2])
    return [row[ca+1:cb] for row in grid[ra+1:rb]]


def solve_S7_E4(grid):
    comps=components(grid,{6},4)
    assert len(comps)==1
    r1,c1,r2,c2=bbox(comps[0]['cells'])
    out=blank(*dims(grid),0)
    for r in range(r1,r2+1):
        for c in range(c1,c2+1):
            out[r][c]=6
    return out


def solve_S7_E5(grid):
    comps=[comp for comp in components(grid,{3},4)]
    assert len(comps)==1
    norm=normalize(comps[0]['cells'])
    h,w=dims(grid)
    out=blank(h,w,0)
    for r,c in norm:
        out[r][c]=3
    return out


def solve_S7_E6(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for c in range(w):
        for r in range(h):
            if grid[r][c]==4:
                out[r][c]=4
                break
    return out


def solve_S7_E7(grid):
    cnt=len(components(grid,{1},4))
    return [[1]*cnt]


def solve_S7_M1(grid):
    out=copyg(grid)
    frames=components(grid,{8},4)
    assert len(frames)==1
    fr=frames[0]
    fr_bbox=bbox(fr['cells'])
    objs=components(grid,{2},4)
    assert len(objs)==1
    comp=objs[0]
    ob=bbox(comp['cells'])
    # infer direction from relative position
    if ob[3] < fr_bbox[1]:
        step=(0,1)
    elif ob[1] > fr_bbox[3]:
        step=(0,-1)
    elif ob[2] < fr_bbox[0]:
        step=(1,0)
    else:
        step=(-1,0)
    for r,c in comp['cells']:
        out[r][c]=0
    blockers={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0 and v!=2}
    slid=slide_component(grid, comp['cells'], step, blockers)
    for r,c in slid:
        out[r][c]=2
    return out


def solve_S7_M2(grid):
    return gravity_slide_all(grid, (1,0), immobile_colors={8})


def solve_S7_M3(grid):
    comps=components(grid,None,4)
    ranked=sorted(comps,key=lambda comp:(-comp_height(comp), bbox(comp['cells'])[1], comp['color']))
    return [[comp['color'] for comp in ranked]]


def solve_S7_M4(grid):
    src=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==1][0]
    tgt=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    comps=components(grid,{3},4)
    assert len(comps)==1
    dr=tgt[0]-src[0]; dc=tgt[1]-src[1]
    out=blank(*dims(grid),0)
    for r,c in comps[0]['cells']:
        nr,nc=r+dr,c+dc
        if inb(out,nr,nc):
            out[nr][nc]=2
    return out


def solve_S7_M5(grid):
    comps=components(grid,None,4)
    # movable are colors not 8
    movable=[comp for comp in comps if comp['color']!=8]
    best=None; best_dist=-1; best_key=None
    for comp in movable:
        blockers={(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0 and (r,c) not in comp['cells']}
        slid=slide_component(grid, comp['cells'], (0,1), blockers)
        dist=bbox(slid)[1]-bbox(comp['cells'])[1]
        key=(-dist, bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color'])
        # want max dist, then topmost, then leftmost, then color
        if dist>best_dist or (dist==best_dist and (bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color']) < best_key):
            best_dist=dist
            best=({'color':comp['color'], 'cells':slid})
            best_key=(bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color'])
    out=blank(*dims(grid),0)
    for r,c in best['cells']:
        out[r][c]=best['color']
    return out


def solve_S7_M6(grid):
    h,w=dims(grid)
    out=blank(h,1,0)
    for r in range(h):
        counts={}
        firstpos={}
        for c,v in enumerate(grid[r]):
            if v==0:
                continue
            counts[v]=counts.get(v,0)+1
            firstpos.setdefault(v,c)
        if not counts:
            out[r][0]=0
        else:
            best=max(counts, key=lambda v:(counts[v], -firstpos[v]))
            out[r][0]=best
    return out


def solve_S7_M7(grid):
    h,w=dims(grid)
    out=copyg(grid)
    for r in range(h):
        for c in range(w):
            if grid[r][c]!=0:
                continue
            neigh={grid[r+dr][c+dc] for dr,dc in dirs4 if inb(grid,r+dr,c+dc) and grid[r+dr][c+dc]!=0}
            if len(neigh)==1:
                out[r][c]=next(iter(neigh))
    return out


def solve_S7_H1(grid):
    h,w=dims(grid)
    out=copyg(grid)
    markers=sorted([(r,c,out[r][c]) for r in range(h) for c in range(w) if out[r][c] in dir_from_marker], key=lambda t:(t[0],t[1]))
    # remove markers first
    for r,c,v in markers:
        out[r][c]=0
    for mr,mc,mv in markers:
        # find adjacent component in current out
        adjs=[(mr+dr,mc+dc) for dr,dc in dirs4 if inb(out,mr+dr,mc+dc) and out[mr+dr][mc+dc] not in {0,8}]
        if len(adjs)!=1:
            # if multiple, pick deterministic first
            if not adjs:
                continue
            adjs=sorted(adjs)
        comp=extract_component_from_cell(out, adjs[0], ignore_colors={0,8})
        for r,c in comp['cells']:
            out[r][c]=0
        blockers={(r,c) for r,row in enumerate(out) for c,v in enumerate(row) if v!=0}
        slid=slide_component(out, comp['cells'], dir_from_marker[mv], blockers)
        for r,c in slid:
            out[r][c]=comp['color']
    return out


def solve_S7_H2(grid):
    marker=grid[0][0]
    step=dir_from_marker[marker]
    out=gravity_slide_all(grid, step, immobile_colors={8}, remove_marker_pos={(0,0)})
    return out


def solve_S7_H3(grid):
    comps=nonzero_components(grid,4)
    assert len(comps)==2
    # each comp has one connector color 2 and nonzero other cells
    comps2=[]
    for comp in comps:
        cells=comp['cells']
        conn=[(r,c) for r,c in cells if grid[r][c]==2]
        assert len(conn)==1
        conn=conn[0]
        comps2.append({'cells':cells,'conn':conn})
    # choose first by connector reading order
    comps2=sorted(comps2,key=lambda x:x['conn'])
    a,b=comps2
    dr=a['conn'][0]-b['conn'][0]
    dc=a['conn'][1]-b['conn'][1]
    out=blank(*dims(grid),0)
    for r,c in a['cells']:
        out[r][c]=6
    for r,c in b['cells']:
        out[r+dr][c+dc]=6
    return out


def solve_S7_H4(grid):
    comps=components(grid,None,4)
    walls=[comp for comp in comps if comp['color']==8]
    objs=[comp for comp in comps if comp['color']!=8]
    assert len(objs)==2
    objs=sorted(objs,key=lambda comp:bbox(comp['cells'])[1])
    left,right=objs
    h,w=dims(grid)
    wallcells={(r,c) for comp in walls for r,c in comp['cells']}
    # move simultaneously toward center until next step invalid (overlap or wall/out)
    left_cells=set(left['cells']); right_cells=set(right['cells'])
    while True:
        left_n={(r,c+1) for r,c in left_cells}
        right_n={(r,c-1) for r,c in right_cells}
        if any(c<0 or c>=w or r<0 or r>=h for r,c in left_n|right_n):
            break
        if left_n & wallcells or right_n & wallcells:
            break
        if left_n & right_n:
            break
        if left_n & right_cells or right_n & left_cells:
            break
        left_cells, right_cells = left_n, right_n
    out=blank(h,w,0)
    # preserve walls? maybe yes to show corridor; but output only moved shapes? decide maybe preserve walls too
    for r,c in wallcells:
        out[r][c]=8
    for r,c in left_cells|right_cells:
        out[r][c]=7
    return out


def solve_S7_H5(grid):
    comps=components(grid,{3},4)
    norms=[normalize(comp['cells']) for comp in comps]
    counts={}
    for norm in norms:
        for cell in norm:
            counts[cell]=counts.get(cell,0)+1
    keep=[cell for cell,cnt in counts.items() if cnt>=2]
    if not keep:
        return [[0]]
    r1,c1,r2,c2=bbox(keep)
    h=r2-r1+1; w=c2-c1+1
    out=blank(h,w,0)
    for r,c in keep:
        out[r-r1][c-c1]=3
    return out


def solve_S7_H6(grid):
    comps=components(grid,None,4)
    comps=sorted(comps,key=lambda comp:(-area(comp), comp['color']))
    norms=[]
    maxh=0
    totalw=0
    for comp in comps:
        norm=normalize(comp['cells'])
        norms.append((comp['color'], norm))
        ch=max(r for r,c in norm)+1
        cw=max(c for r,c in norm)+1
        maxh=max(maxh,ch)
        totalw += cw
    totalw += max(0, len(norms)-1)
    out=blank(maxh,totalw,0)
    curc=0
    for color,norm in norms:
        ch=max(r for r,c in norm)+1
        cw=max(c for r,c in norm)+1
        for r,c in norm:
            out[r][curc+c]=color
        curc += cw + 1
    return out


def solve_S7_H7(grid):
    h,w=dims(grid)
    # detect 8 frames with exactly one colored label inside
    frames=components(grid,{8},4)
    bays=[]
    label_positions=set()
    for fr in frames:
        r1,c1,r2,c2=bbox(fr['cells'])
        # verify hollow rectangle maybe optional
        interior=[(r,c,grid[r][c]) for r in range(r1+1,r2) for c in range(c1+1,c2) if grid[r][c] not in (0,8)]
        if len(interior)==1:
            r,c,color = interior[0]
            bays.append({'color':color,'bbox':(r1,c1,r2,c2),'label':(r,c)})
            label_positions.add((r,c))
    # extract shapes excluding frames and labels
    seen=[[False]*w for _ in range(h)]
    shapes=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or grid[r][c]==0 or grid[r][c]==8 or (r,c) in label_positions:
                continue
            color=grid[r][c]
            seen[r][c]=True
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs4:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and grid[nr][nc]==color and (nr,nc) not in label_positions:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            shapes.append({'color':color,'cells':sorted(cells)})
    out=blank(h,w,0)
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=8
    for shape in shapes:
        color=shape['color']
        bay=[b for b in bays if b['color']==color]
        if not bay:
            continue
        bay=bay[0]
        norm=normalize(shape['cells'])
        ir=bay['bbox'][0]+1
        ic=bay['bbox'][1]+1
        for r,c in norm:
            out[ir+r][ic+c]=color
    return out

