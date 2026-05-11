"""Reference helper library and 21 reference solve functions for the sixth custom ARC puzzle bank.

New primitive introduced in this set:
  follow_wire(grid, start, path_colors={1})
It starts from a marker cell, follows the unique non-branching 4-connected path
attached to it, and returns the ordered path cells.
"""

dirs4 = [(-1,0),(1,0),(0,-1),(0,1)]
dirs8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def blank(h,w,v=0): return [[v]*w for _ in range(h)]


def copyg(g): return [row[:] for row in g]


def dims(g): return len(g), len(g[0])


def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w


def components(grid, colors=None, connectivity=4, ignore=None):
    h,w=dims(grid)
    seen=[[False]*w for _ in range(h)]
    dirs=dirs4 if connectivity==4 else dirs8
    ignore=ignore or set()
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]: continue
            seen[r][c]=True
            if (r,c) in ignore: continue
            color=grid[r][c]
            if color==0 or (colors is not None and color not in colors): continue
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if inb(grid,nr,nc) and not seen[nr][nc] and (nr,nc) not in ignore and grid[nr][nc]==color:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({'color':color,'cells':sorted(cells)})
    return comps


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs),min(cs),max(rs),max(cs)


def normalize(cells):
    r1,c1,r2,c2=bbox(cells)
    return sorted((r-r1,c-c1) for r,c in cells)


def reflect_h(norm_cells):
    maxc=max(c for r,c in norm_cells)
    return sorted((r,maxc-c) for r,c in norm_cells)


def rotate(norm_cells,t=1):
    cells=list(norm_cells)
    for _ in range(t%4):
        maxr=max(r for r,c in cells)
        cells=[(c,maxr-r) for r,c in cells]
        r0=min(r for r,c in cells); c0=min(c for r,c in cells)
        cells=sorted((r-r0,c-c0) for r,c in cells)
    return sorted(cells)


def perimeter(grid, comp):
    s=set(comp['cells'])
    p=0
    for r,c in s:
        for dr,dc in dirs4:
            nr,nc=r+dr,c+dc
            if (nr,nc) not in s:
                p+=1
    return p


def follow_wire(grid, start, path_colors={1}, start_colors={2}):
    # start cell is marker; adjacent cell of path color is path start.
    h,w=dims(grid)
    sr,sc=start
    adjs=[(sr+dr,sc+dc) for dr,dc in dirs4 if inb(grid,sr+dr,sc+dc) and grid[sr+dr][sc+dc] in path_colors]
    if len(adjs)!=1:
        # allow endpoint with multiple? just take one deterministically
        if not adjs:
            return []
    cur=adjs[0]
    prev=start
    path=[]
    seen=set([start])
    while True:
        path.append(cur)
        seen.add(cur)
        rr,cc=cur
        nxts=[]
        for dr,dc in dirs4:
            nr,nc=rr+dr,cc+dc
            if not inb(grid,nr,nc): continue
            if (nr,nc)==prev: continue
            if grid[nr][nc] in path_colors:
                nxts.append((nr,nc))
        # remove visited loops
        nxts=[x for x in nxts if x not in seen]
        if len(nxts)==0:
            break
        # non-branching assumption
        prev,cur=cur,nxts[0]
    return path


def turns_in_path(path):
    if len(path)<3: return 0
    turns=0
    dirs=[]
    for (r1,c1),(r2,c2) in zip(path,path[1:]):
        dirs.append((r2-r1,c2-c1))
    for a,b in zip(dirs,dirs[1:]):
        if a!=b:
            turns+=1
    return turns


def shortest_path(grid, start, goal, passable={0}):
    from collections import deque
    q=deque([start])
    prev={start:None}
    while q:
        cur=q.popleft()
        if cur==goal:
            break
        r,c=cur
        for dr,dc in dirs4:
            nr,nc=r+dr,c+dc
            if inb(grid,nr,nc) and (nr,nc) not in prev and (grid[nr][nc] in passable or (nr,nc)==goal):
                prev[(nr,nc)] = cur
                q.append((nr,nc))
    if goal not in prev:
        return []
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=prev[cur]
    return path[::-1]


def fill_room_by_seed(grid, wall_color=8):
    h,w=dims(grid)
    out=copyg(grid)
    seen=set()
    for r in range(h):
        for c in range(w):
            if grid[r][c]==0 and (r,c) not in seen:
                # zero room
                q=[(r,c)]
                seen.add((r,c))
                room=[]
                seeds=set()
                while q:
                    rr,cc=q.pop()
                    room.append((rr,cc))
                    for dr,dc in dirs4:
                        nr,nc=rr+dr,cc+dc
                        if not inb(grid,nr,nc): continue
                        if grid[nr][nc]==0 and (nr,nc) not in seen:
                            seen.add((nr,nc)); q.append((nr,nc))
                        elif grid[nr][nc] not in (0, wall_color):
                            seeds.add(grid[nr][nc])
                if len(seeds)==1:
                    color=next(iter(seeds))
                    for rr,cc in room:
                        out[rr][cc]=color
    return out


def detect_frames(grid):
    # returns list of rectangular hollow frames of nonzero colors
    h,w=dims(grid)
    frames=[]
    for color in set(v for row in grid for v in row if v!=0):
        coords=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==color]
        if not coords: continue
        # components of this color
        for comp in components(grid,{color},4):
            r1,c1,r2,c2=bbox(comp['cells'])
            cells=set(comp['cells'])
            rect=set()
            for r in range(r1,r2+1):
                rect.add((r,c1)); rect.add((r,c2))
            for c in range(c1,c2+1):
                rect.add((r1,c)); rect.add((r2,c))
            if cells==rect:
                frames.append({'color':color,'cells':comp['cells'],'bbox':(r1,c1,r2,c2)})
    return frames


def solve_S6_E1(grid):
    out=copyg(grid)
    starts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    start=starts[0]
    for r,c in follow_wire(grid,start,{1}):
        out[r][c]=3
    return out


def solve_S6_E2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comps=components(grid,None,4)
    comp=max(comps,key=lambda c:len(c['cells']))
    s=set(comp['cells']); col=comp['color']
    for r,c in s:
        if any((r+dr,c+dc) not in s for dr,dc in dirs4):
            out[r][c]=col
    return out


def solve_S6_E3(grid):
    comps=components(grid,None,4)
    comps=sorted(comps,key=lambda c:min(cc for rr,cc in c['cells']))
    a,b=comps[:2]
    out=copyg(grid)
    ca,cb=a['color'],b['color']
    for r,c in a['cells']:
        out[r][c]=cb
    for r,c in b['cells']:
        out[r][c]=ca
    return out


def solve_S6_E4(grid):
    out=copyg(grid)
    cells=[(r,c,v) for r,row in enumerate(grid) for c,v in enumerate(row) if v!=0]
    # assume 3 same-color cells
    color=cells[0][2]
    pts=[(r,c) for r,c,v in cells if v==color]
    rs=sorted(set(r for r,c in pts)); cs=sorted(set(c for r,c in pts))
    if len(rs)==2 and len(cs)==2:
        for r in rs:
            for c in cs:
                if out[r][c]==0:
                    out[r][c]=color
    return out


def solve_S6_E5(grid):
    comps=components(grid,{3},4)
    target=[comp for comp in comps if len(comp['cells'])%2==1][0]
    out=copyg(grid)
    for r,c in target['cells']:
        out[r][c]=1
    return out


def solve_S6_E6(grid):
    start=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2][0]
    n=len(follow_wire(grid,start,{1}))
    return [[6]*n] if n>0 else [[0]]


def solve_S6_E7(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    for r,row in enumerate(grid):
        for c,v in enumerate(row):
            if v==5:
                deg=sum(inb(grid,r+dr,c+dc) and grid[r+dr][c+dc]==5 for dr,dc in dirs4)
                if deg==1:
                    out[r][c]=5
    return out


def solve_S6_M1(grid):
    out=copyg(grid)
    starts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    best=None; best_path=[]
    for st in starts:
        path=follow_wire(grid,st,{1})
        if len(path)>len(best_path):
            best_path=path; best=st
    for r,c in best_path:
        out[r][c]=3
    return out


def solve_S6_M2(grid):
    h,w=dims(grid)
    out=blank(h,w,0)
    comps=components(grid,None,4)
    comps=sorted(comps,key=lambda c:c['color'])[:2]  # assume two objects
    (a,b)=comps[:2]
    r1a,c1a,r2a,c2a=bbox(a['cells']); r1b,c1b,r2b,c2b=bbox(b['cells'])
    rr1=max(r1a,r1b); cc1=max(c1a,c1b); rr2=min(r2a,r2b); cc2=min(c2a,c2b)
    if rr1<=rr2 and cc1<=cc2:
        for r in range(rr1,rr2+1):
            for c in range(cc1,cc2+1):
                out[r][c]=8
    return out


def solve_S6_M3(grid):
    out=copyg(grid)
    frames=detect_frames(grid)
    dots=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==1]
    for r,c in dots:
        enclosing=[]
        for fr in frames:
            r1,c1,r2,c2=fr['bbox']
            if r1<r<r2 and c1<c<c2:
                enclosing.append(fr)
        if enclosing:
            fr=min(enclosing,key=lambda f:(f['bbox'][2]-f['bbox'][0])*(f['bbox'][3]-f['bbox'][1]))
            out[r][c]=fr['color']
    return out


def solve_S6_M4(grid):
    out=copyg(grid)
    frames=detect_frames(grid)
    fr=max(frames,key=lambda f:(f['bbox'][2]-f['bbox'][0])*(f['bbox'][3]-f['bbox'][1]))
    r1,c1,r2,c2=fr['bbox']
    seeds=[(r,c,grid[r][c]) for r in range(r1+1,r2) for c in range(c1+1,c2) if grid[r][c] not in (0,fr['color'])]
    sr,sc,color=seeds[0]
    parity=(sr+sc)%2
    for r in range(r1+1,r2):
        for c in range(c1+1,c2):
            if grid[r][c]==0 and (r+c)%2==parity:
                out[r][c]=color
    return out


def solve_S6_M5(grid):
    comps=components(grid,{6},4)
    norms=[normalize(c['cells']) for c in comps]
    # find pair where one equals reflected other
    pair=[]
    for i in range(len(comps)):
        for j in range(i+1,len(comps)):
            ni=norms[i]; nj=norms[j]
            if sorted(ni)==sorted(reflect_h(nj)) or sorted(nj)==sorted(reflect_h(ni)):
                pair=[i,j]
    h,w=dims(grid); out=blank(h,w,0)
    for idx in pair:
        for r,c in comps[idx]['cells']:
            out[r][c]=2
    return out


def solve_S6_M6(grid):
    comps=components(grid,None,4)
    ranked=sorted(comps,key=lambda c:(-perimeter(grid,c), c['color']))
    return [[c['color'] for c in ranked]]


def solve_S6_M7(grid):
    h,w=dims(grid)
    # anchors are singleton cells whose color also appears in a larger comp.
    comps=components(grid,None,4)
    by_color={}
    for comp in comps:
        by_color.setdefault(comp['color'],[]).append(comp)
    out=blank(h,w,0)
    for color, lst in by_color.items():
        anchors=[c for c in lst if len(c['cells'])==1]
        objs=[c for c in lst if len(c['cells'])>1]
        if anchors and objs:
            ar,ac=anchors[0]['cells'][0]
            obj=max(objs,key=lambda c:len(c['cells']))
            nr0=min(r for r,c in obj['cells']); nc0=min(c for r,c in obj['cells'])
            for r,c in obj['cells']:
                rr=ar+(r-nr0); cc=ac+(c-nc0)
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=color
    return out


def solve_S6_H1(grid):
    return fill_room_by_seed(grid,8)


def solve_S6_H2(grid):
    out=copyg(grid)
    starts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==2]
    best_path=[]; best_turns=-1
    for st in starts:
        path=follow_wire(grid,st,{1})
        turns=turns_in_path(path)
        if turns>best_turns or (turns==best_turns and len(path)>len(best_path)):
            best_turns=turns; best_path=path
    for r,c in best_path:
        out[r][c]=3
    return out


def solve_S6_H3(grid):
    comps=components(grid,None,4)
    # assume exactly two objects
    comps=sorted(comps,key=lambda c:c['color'])[:2]
    n1=set(normalize(comps[0]['cells']))
    n2=set(normalize(comps[1]['cells']))
    cells=sorted(n1.symmetric_difference(n2))
    if not cells:
        return [[0]]
    maxr=max(r for r,c in cells); maxc=max(c for r,c in cells)
    out=blank(maxr+1,maxc+1,0)
    for r,c in cells: out[r][c]=8
    return out


def solve_S6_H4(grid):
    # color 4 template, color 2 marker, color 1 wire, color 7 start marker
    comps=components(grid,{4},4)
    template=max(comps,key=lambda c:len(c['cells']))
    temp_norm=normalize(template['cells'])
    start=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==7][0]
    path=follow_wire(grid,start,{1})
    turns=[]
    for idx in range(1,len(path)-1):
        a=path[idx-1]; b=path[idx]; c=path[idx+1]
        if (b[0]-a[0],b[1]-a[1]) != (c[0]-b[0],c[1]-b[1]):
            turns.append(b)
    h,w=dims(grid)
    out=blank(h,w,0)
    # stamp template with template's top-left aligned at each turn
    for tr,tc in turns:
        for dr,dc in temp_norm:
            rr,cc=tr+dr, tc+dc
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=4
    return out


def solve_S6_H5(grid):
    # outer frame color 8, two seeds nonzero non-wall. fill interior by nearest seed (Manhattan), no ties in examples.
    out=copyg(grid)
    frames=detect_frames(grid)
    fr=max(frames,key=lambda f:(f['bbox'][2]-f['bbox'][0])*(f['bbox'][3]-f['bbox'][1]))
    r1,c1,r2,c2=fr['bbox']
    seeds=[(r,c,grid[r][c]) for r in range(r1+1,r2) for c in range(c1+1,c2) if grid[r][c] not in (0,fr['color'])]
    for r in range(r1+1,r2):
        for c in range(c1+1,c2):
            if grid[r][c]==0:
                dists=sorted(((abs(r-sr)+abs(c-sc), color) for sr,sc,color in seeds))
                if dists[0][0] != dists[1][0]:
                    out[r][c]=dists[0][1]
    return out


def solve_S6_H6(grid):
    comps=components(grid,{6},4)
    # choose majority canonical shape under rotation
    from collections import Counter
    cans=[]
    for comp in comps:
        n=normalize(comp['cells'])
        rots=[tuple(rotate(n,k)) for k in range(4)]
        cans.append(min(rots))
    ctr=Counter(cans)
    target=ctr.most_common(1)[0][0]
    cells=list(target)
    maxr=max(r for r,c in cells); maxc=max(c for r,c in cells)
    out=blank(maxr+1,maxc+1,0)
    for r,c in cells: out[r][c]=2
    return out


def solve_S6_H7(grid):
    # walls 9, markers 3, fill shortest path with 8 through zeros, keep markers/walls
    out=copyg(grid)
    pts=[(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v==3]
    start,goal=pts[0],pts[1]
    path=shortest_path(grid,start,goal,{0})
    for r,c in path[1:-1]:
        if out[r][c]==0:
            out[r][c]=8
    return out

