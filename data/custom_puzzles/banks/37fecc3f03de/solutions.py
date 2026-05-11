"""Reference solvers for the twenty-fourth 21-task ARC-style puzzle bank.

This batch emphasizes interval completion, anti-diagonal and half-turn symmetry,
square-driven growth, column filtering, marker-based cropping, topology-aware recoloring,
compartment packing, frame filling, width-sorted galleries, docking, scripted transform
galleries, portal pathfinding, hole-key assignment, relation matrices, boolean
composition, ordered checkpoint routing, and wall-geodesic Voronoi fills.
"""

from typing import List, Tuple, Dict, Set
from collections import deque, defaultdict

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

NEW_PRIMITIVES = {
    "one_gap_bridge": "Fill the single 0 exactly between two same-color endpoints in a row or column.",
    "anti_diagonal_orbit": "Add the anti-diagonal reflection of every colored cell while keeping the originals.",
    "square_ring_bloom": "Expand each solid monochrome 2x2 square into the surrounding 4x4 ring of the same color.",
    "bottom_keep": "Keep only the bottommost nonzero cell in each column.",
    "opposite_corner_complete": "Complete rectangles when only one diagonal pair of same-color corners is present.",
    "half_turn_echo": "Add a 180-degree rotational echo of every colored cell.",
    "blocked_crosshair": "Project each seed along its row and column until a wall or the border stops it.",
    "color_key_crop": "Use a color key cell to select which object to crop tightly.",
    "hole_rank_palette": "Recolor each object according to its number of enclosed holes.",
    "compartment_left_pack": "Pack colored cells leftward inside each wall-bounded row compartment while preserving order.",
    "external_seed_fill": "Fill each hollow frame interior using the nearby external seed color.",
    "width_gallery": "Crop objects and lay them out left-to-right sorted by width.",
    "diagonal_segment_connect": "Connect same-color markers by filling an unobstructed diagonal segment.",
    "bbox_center_dock": "Translate an object so its bounding-box center lands on a marker.",
    "script_transform_gallery": "Read a key script and output a gallery of transformed template copies in that order.",
    "portal_shortest_path": "Find the shortest path when stepping onto a portal teleports you to its mate.",
    "hole_key_frame_assign": "Assign objects to frames by matching each object's hole count to a frame key.",
    "left_of_matrix": "Summarize horizontal relations between objects as a binary matrix.",
    "dual_key_boolean": "Transform one shape by a key, then combine two normalized shapes with a keyed boolean op.",
    "ordered_checkpoint_path": "Trace the shortest path that visits numbered checkpoints in ascending order before the goal.",
    "wall_geodesic_voronoi": "Fill each reachable empty cell with the closest seed color by shortest path around walls."
}

def blank(h:int,w:int,val:int=0)->Grid:
    return [[val]*w for _ in range(h)]

def deepcopy_grid(g:Grid)->Grid:
    return [row[:] for row in g]

def dims(g:Grid)->Tuple[int,int]:
    return len(g), len(g[0]) if g else 0

def inb(g:Grid,r:int,c:int)->bool:
    h,w=dims(g)
    return 0<=r<h and 0<=c<w

def bbox_of_cells(cells:List[Tuple[int,int]])->Tuple[int,int,int,int]:
    rs=[r for r,_ in cells]; cs=[c for _,c in cells]
    return min(rs), max(rs), min(cs), max(cs)

def crop_bbox(g:Grid, bbox:Tuple[int,int,int,int])->Grid:
    r0,r1,c0,c1=bbox
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def paste(dst:Grid, src:Grid, top:int, left:int, transparent:int=0)->Grid:
    out=deepcopy_grid(dst)
    h,w=dims(out); sh,sw=dims(src)
    for r in range(sh):
        for c in range(sw):
            rr,cc=top+r,left+c
            if 0<=rr<h and 0<=cc<w and src[r][c]!=transparent:
                out[rr][cc]=src[r][c]
    return out

def rotate90(g:Grid)->Grid:
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g:Grid)->Grid:
    return [row[::-1] for row in g[::-1]]

def rotate270(g:Grid)->Grid:
    return rotate90(rotate180(g))

def flip_h(g:Grid)->Grid:
    return [row[::-1] for row in g]

def flip_v(g:Grid)->Grid:
    return g[::-1]

def transform_by_key(g:Grid, key:int)->Grid:
    if key==1:
        return deepcopy_grid(g)
    if key==2:
        return rotate90(g)
    if key==3:
        return flip_h(g)
    if key==4:
        return rotate180(g)
    if key==5:
        return flip_v(g)
    if key==6:
        return rotate270(g)
    return deepcopy_grid(g)

def find_components(g:Grid, include_zero:bool=False)->List[Dict]:
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            if not include_zero and g[r][c]==0:
                continue
            color=g[r][c]
            q=deque([(r,c)])
            seen[r][c]=True
            cells=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==color:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            bb=bbox_of_cells(cells)
            comps.append({'color':color,'cells':cells,'bbox':bb,'area':len(cells)})
    return comps

def count_holes_in_component(g:Grid, comp:Dict)->int:
    cells=set(comp['cells'])
    r0,r1,c0,c1=comp['bbox']
    # pad bbox by 1 and flood fill zeros outside
    h=(r1-r0+1)+2; w=(c1-c0+1)+2
    arr=[[0]*w for _ in range(h)]
    for r,c in cells:
        arr[r-r0+1][c-c0+1]=1
    seen=[[False]*w for _ in range(h)]
    q=deque([(0,0)]); seen[0][0]=True
    while q:
        rr,cc=q.popleft()
        for dr,dc in DIR4:
            nr,nc=rr+dr,cc+dc
            if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and arr[nr][nc]==0:
                seen[nr][nc]=True; q.append((nr,nc))
    holes=0
    for r in range(h):
        for c in range(w):
            if arr[r][c]==0 and not seen[r][c]:
                holes+=1
                q=deque([(r,c)]); seen[r][c]=True
                while q:
                    rr,cc=q.popleft()
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and arr[nr][nc]==0:
                            seen[nr][nc]=True; q.append((nr,nc))
    return holes

def center_of_bbox(bb:Tuple[int,int,int,int])->Tuple[int,int]:
    r0,r1,c0,c1=bb
    return (r0+r1)//2, (c0+c1)//2

def crop_nonzero(g:Grid)->Grid:
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    return crop_bbox(g,bbox_of_cells(cells))

def frame_bboxes(g:Grid, frame_color:int=5)->List[Tuple[int,int,int,int]]:
    comps=[comp for comp in find_components(g) if comp['color']==frame_color]
    out=[]
    for comp in comps:
        r0,r1,c0,c1=comp['bbox']
        ok=True
        # must be rectangle border only
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                border = r in (r0,r1) or c in (c0,c1)
                if border and g[r][c]!=frame_color:
                    ok=False
                if not border and g[r][c]==frame_color:
                    ok=False
        if ok:
            out.append(comp['bbox'])
    return out

def center_in_rect(src:Grid, dst:Grid, bb:Tuple[int,int,int,int], transparent:int=0)->Grid:
    r0,r1,c0,c1=bb
    sh,sw=dims(src)
    top = r0 + ((r1-r0+1) - sh)//2
    left = c0 + ((c1-c0+1) - sw)//2
    return paste(dst, src, top, left, transparent=transparent)

def pad_to_same(a:Grid,b:Grid)->Tuple[Grid,Grid]:
    ha,wa=dims(a); hb,wb=dims(b)
    h=max(ha,hb); w=max(wa,wb)
    A=blank(h,w); B=blank(h,w)
    A = paste(A,a,(h-ha)//2,(w-wa)//2)
    B = paste(B,b,(h-hb)//2,(w-wb)//2)
    return A,B

def bfs_shortest_path_with_portals(g:Grid, start:Tuple[int,int], goal:Tuple[int,int], wall_colors:Set[int], portal_colors:Set[int], ordered_waypoints:List[Tuple[int,int]]=None):
    # returns path list of cells from start to goal inclusive, visiting ordered_waypoints in order
    ordered_waypoints = ordered_waypoints or []
    portals=defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] in portal_colors:
                portals[g[r][c]].append((r,c))
    def neighbors(cell):
        r,c=cell
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and g[nr][nc] not in wall_colors:
                # stepping onto portal teleports
                if g[nr][nc] in portal_colors and len(portals[g[nr][nc]])==2:
                    a,b=portals[g[nr][nc]]
                    dest=b if (nr,nc)==a else a
                    yield dest
                else:
                    yield (nr,nc)
    segments=[start]+ordered_waypoints+[goal]
    full=[start]
    cur=start
    for target in segments[1:]:
        q=deque([cur]); prev={cur:None}
        while q and target not in prev:
            x=q.popleft()
            for y in neighbors(x):
                if y not in prev:
                    prev[y]=x; q.append(y)
        if target not in prev:
            return None
        path=[]
        x=target
        while x is not None:
            path.append(x); x=prev[x]
        path=path[::-1]
        full.extend(path[1:])
        cur=target
    return full

def geodesic_voronoi_fill(g:Grid, wall_color:int=5)->Grid:
    h,w=dims(g)
    seeds=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] not in (0,wall_color)]
    out=deepcopy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            best=None; bestd=None; tie=False
            for sr,sc,col in seeds:
                q=deque([(sr,sc,0)])
                seen={(sr,sc)}
                found=None
                while q and found is None:
                    rr,cc,d=q.popleft()
                    if (rr,cc)==(r,c):
                        found=d; break
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and (nr,nc) not in seen and g[nr][nc]!=wall_color:
                            seen.add((nr,nc)); q.append((nr,nc,d+1))
                if found is None:
                    continue
                if bestd is None or found<bestd:
                    bestd=found; best=col; tie=False
                elif found==bestd and col!=best:
                    tie=True
            if bestd is not None and not tie:
                out[r][c]=best
    return out

def solve_easy_p01(g:Grid)->Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            # horizontal
            if c-1>=0 and c+1<w and g[r][c-1]!=0 and g[r][c-1]==g[r][c+1]:
                out[r][c]=g[r][c-1]
            # vertical
            if r-1>=0 and r+1<h and g[r-1][c]!=0 and g[r-1][c]==g[r+1][c]:
                out[r][c]=g[r-1][c]
    return out

def solve_easy_p02(g:Grid)->Grid:
    h,w=dims(g)
    assert h==w
    out=deepcopy_grid(g)
    n=h
    for r in range(n):
        for c in range(n):
            if g[r][c]!=0:
                rr,cc=n-1-c,n-1-r
                out[rr][cc]=g[r][c]
    return out

def solve_easy_p03(g:Grid)->Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(h-1):
        for c in range(w-1):
            col=g[r][c]
            if col!=0 and g[r+1][c]==col and g[r][c+1]==col and g[r+1][c+1]==col:
                for rr in range(r-1,r+3):
                    for cc in range(c-1,c+3):
                        if 0<=rr<h and 0<=cc<w:
                            if rr in (r-1,r+2) or cc in (c-1,c+2):
                                out[rr][cc]=col
    return out

def solve_easy_p04(g:Grid)->Grid:
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        for r in range(h-1,-1,-1):
            if g[r][c]!=0:
                out[r][c]=g[r][c]
                break
    return out

def solve_easy_p05(g:Grid)->Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    # search diagonal pairs same color
    for r0 in range(h):
        for c0 in range(w):
            col=g[r0][c0]
            if col==0:
                continue
            for r1 in range(r0+1,h):
                for c1 in range(w):
                    if c1==c0:
                        continue
                    if g[r1][c1]!=col:
                        continue
                    # opposite corners on rectangle: either same orientation works
                    if out[r0][c1]==0 and out[r1][c0]==0:
                        out[r0][c1]=col
                        out[r1][c0]=col
    return out

def solve_easy_p06(g:Grid)->Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[h-1-r][w-1-c]=g[r][c]
    return out

def solve_easy_p07(g:Grid)->Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(h):
        for c in range(w):
            col=g[r][c]
            if col in (0,5):
                continue
            # spread up/down/left/right until wall 5 or border
            for dr,dc in DIR4:
                rr,cc=r+dr,c+dc
                while 0<=rr<h and 0<=cc<w and g[rr][cc]!=5:
                    if g[rr][cc]==0:
                        out[rr][cc]=col
                    rr+=dr; cc+=dc
    return out

def solve_medium_p01(g:Grid)->Grid:
    key=g[0][0]
    comps=[comp for comp in find_components(g) if comp['color']==key and (0,0) not in comp['cells']]
    if not comps:
        return [[0]]
    comp=min(comps, key=lambda comp: comp['bbox'])
    return crop_bbox(g, comp['bbox'])

def solve_medium_p02(g:Grid)->Grid:
    out=blank(*dims(g))
    palette={0:2,1:3,2:4,3:6}
    for comp in find_components(g):
        holes=count_holes_in_component(g, comp)
        col=palette.get(holes,9)
        for r,c in comp['cells']:
            out[r][c]=col
    return out

def solve_medium_p03(g:Grid)->Grid:
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==5:
                out[r][c]=5
                c+=1
                continue
            j=c
            vals=[]
            while j<w and g[r][j]!=5:
                if g[r][j]!=0:
                    vals.append(g[r][j])
                j+=1
            k=c
            for val in vals:
                out[r][k]=val; k+=1
            while k<j:
                out[r][k]=0; k+=1
            c=j
    return out

def solve_medium_p04(g:Grid)->Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for bb in frame_bboxes(g, frame_color=5):
        r0,r1,c0,c1=bb
        mid=(r0+r1)//2
        seed=0
        if c0-1>=0:
            seed=g[mid][c0-1]
        if seed==0 and c1+1<w:
            seed=g[mid][c1+1]
        if seed in (0,5):
            continue
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                out[r][c]=seed
    return out

def solve_medium_p05(g:Grid)->Grid:
    objs=[crop_bbox(g, comp['bbox']) for comp in find_components(g)]
    if not objs:
        return [[0]]
    objs=sorted(objs, key=lambda x: (dims(x)[1], dims(x)[0], x))
    heights=[dims(o)[0] for o in objs]
    widths=[dims(o)[1] for o in objs]
    H=max(heights)
    W=sum(widths)+(len(objs)-1)
    out=blank(H,W)
    c=0
    for obj in objs:
        out=paste(out,obj,0,c)
        c+=dims(obj)[1]+1
    return out

def solve_medium_p06(g:Grid)->Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    positions=defaultdict(list)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                positions[g[r][c]].append((r,c))
    for col,cells in positions.items():
        n=len(cells)
        for i in range(n):
            for j in range(i+1,n):
                r0,c0=cells[i]; r1,c1=cells[j]
                dr=r1-r0; dc=c1-c0
                if abs(dr)==abs(dc) and dr!=0:
                    step_r=1 if dr>0 else -1
                    step_c=1 if dc>0 else -1
                    ok=True
                    rr,cc=r0+step_r,c0+step_c
                    while (rr,cc)!=(r1,c1):
                        if g[rr][cc]!=0:
                            ok=False; break
                        rr+=step_r; cc+=step_c
                    if ok:
                        rr,cc=r0,c0
                        while True:
                            out[rr][cc]=col
                            if (rr,cc)==(r1,c1): break
                            rr+=step_r; cc+=step_c
    return out

def solve_medium_p07(g:Grid)->Grid:
    h,w=dims(g)
    marker=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==8:
                marker=(r,c)
                break
        if marker: break
    comps=[comp for comp in find_components(g) if comp['color']!=8]
    if not marker or not comps:
        return deepcopy_grid(g)
    comp=max(comps, key=lambda comp: comp['area'])
    crop=crop_bbox(g, comp['bbox'])
    ch,cw=dims(crop)
    # center of crop as bbox center; ensure odd dims or floor
    center=(ch//2,cw//2)
    top=marker[0]-center[0]
    left=marker[1]-center[1]
    out=blank(h,w)
    out=paste(out,crop,top,left)
    return out

def solve_hard_p01(g:Grid)->Grid:
    h,w=dims(g)
    keys=[v for v in g[0] if v in (1,2,3,4)]
    comps=[comp for comp in find_components(g) if comp['color'] not in (1,2,3,4)]
    if not comps:
        return [[0]]
    template=crop_bbox(g, max(comps,key=lambda comp: comp['area'])['bbox'])
    variants=[transform_by_key(template,k) for k in keys]
    H=max(dims(v)[0] for v in variants) if variants else 1
    W=sum(dims(v)[1] for v in variants)+max(0,len(variants)-1)
    out=blank(H,W)
    c=0
    for var in variants:
        out=paste(out,var,0,c)
        c+=dims(var)[1]+1
    return out if variants else [[0]]

def solve_hard_p02(g:Grid)->Grid:
    h,w=dims(g)
    start=goal=None
    portals=set()
    for r in range(h):
        for c in range(w):
            if g[r][c]==2: start=(r,c)
            elif g[r][c]==3: goal=(r,c)
            elif g[r][c] in (6,7,9): portals.add(g[r][c])
    if not start or not goal:
        return deepcopy_grid(g)
    path=bfs_shortest_path_with_portals(g,start,goal,{5},portals)
    out=deepcopy_grid(g)
    if path:
        for r,c in path[1:-1]:
            if out[r][c]==0:
                out[r][c]=8
    return out

def solve_hard_p03(g:Grid)->Grid:
    h,w=dims(g)
    frames=frame_bboxes(g, frame_color=5)
    hole_to_obj={}
    temp=deepcopy_grid(g)
    # remove frame borders
    for bb in frames:
        r0,r1,c0,c1=bb
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    temp[r][c]=0
        key_pos=(r0-1,(c0+c1)//2)
        if 0<=key_pos[0]<h and 0<=key_pos[1]<w:
            temp[key_pos[0]][key_pos[1]]=0
    comps=find_components(temp)
    for comp in comps:
        holes=count_holes_in_component(temp, comp)
        if holes not in hole_to_obj or comp['area']>hole_to_obj[holes]['area']:
            hole_to_obj[holes]=comp
    out=blank(h,w)
    for bb in frames:
        r0,r1,c0,c1=bb
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    out[r][c]=5
        key_pos=(r0-1,(c0+c1)//2)
        if 0<=key_pos[0]<h and 0<=key_pos[1]<w:
            key=g[key_pos[0]][key_pos[1]]
            out[key_pos[0]][key_pos[1]]=key
            holes=key-1
            if holes in hole_to_obj:
                crop=crop_bbox(temp, hole_to_obj[holes]['bbox'])
                out=center_in_rect(crop,out,(r0+1,r1-1,c0+1,c1-1))
    return out

def solve_hard_p04(g:Grid)->Grid:
    comps=find_components(g)
    comps=sorted(comps, key=lambda comp: comp['color'])
    n=len(comps)
    out=blank(n,n)
    centers=[center_of_bbox(comp['bbox']) for comp in comps]
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=0
            else:
                out[i][j]=1 if centers[i][1] < centers[j][1] else 0
    return out if comps else [[0]]

def solve_hard_p05(g:Grid)->Grid:
    h,w=dims(g)
    tkey=1; okey=6
    for c,v in enumerate(g[0]):
        if v in (1,2,3,4) and tkey==1:
            tkey=v
        if v in (6,7,8) and okey==6:
            okey=v
    temp=deepcopy_grid(g)
    for c,v in enumerate(g[0]):
        if v in (1,2,3,4,6,7,8):
            temp[0][c]=0
    comps=find_components(temp)
    comps=sorted(comps, key=lambda comp: (comp['bbox'][0], comp['bbox'][2]))
    if len(comps)<2:
        return [[0]]
    A=crop_bbox(temp, comps[0]['bbox'])
    B=crop_bbox(temp, comps[1]['bbox'])
    A=transform_by_key(A,tkey)
    A,B=pad_to_same(A,B)
    hh,ww=dims(A)
    out=blank(hh,ww)
    for r in range(hh):
        for c in range(ww):
            a=A[r][c]!=0; b=B[r][c]!=0
            keep = (a or b) if okey==6 else ((a and b) if okey==7 else (a!=b))
            out[r][c]=8 if keep else 0
    return crop_nonzero(out)

def solve_hard_p06(g:Grid)->Grid:
    h,w=dims(g)
    start=goal=None
    checkpoints=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==2: start=(r,c)
            elif v==3: goal=(r,c)
            elif v in (4,6,7,8,9):
                checkpoints.append((v,(r,c)))
    checkpoints=[cell for _,cell in sorted(checkpoints)]
    if not start or not goal:
        return deepcopy_grid(g)
    path=bfs_shortest_path_with_portals(g,start,goal,{5},set(),ordered_waypoints=checkpoints)
    out=deepcopy_grid(g)
    if path:
        for r,c in path[1:-1]:
            if out[r][c]==0:
                out[r][c]=8
    return out

def solve_hard_p07(g:Grid)->Grid:
    return geodesic_voronoi_fill(g, wall_color=5)

SOLVERS = {
    "easy_p01": solve_easy_p01,
    "easy_p02": solve_easy_p02,
    "easy_p03": solve_easy_p03,
    "easy_p04": solve_easy_p04,
    "easy_p05": solve_easy_p05,
    "easy_p06": solve_easy_p06,
    "easy_p07": solve_easy_p07,
    "medium_p01": solve_medium_p01,
    "medium_p02": solve_medium_p02,
    "medium_p03": solve_medium_p03,
    "medium_p04": solve_medium_p04,
    "medium_p05": solve_medium_p05,
    "medium_p06": solve_medium_p06,
    "medium_p07": solve_medium_p07,
    "hard_p01": solve_hard_p01,
    "hard_p02": solve_hard_p02,
    "hard_p03": solve_hard_p03,
    "hard_p04": solve_hard_p04,
    "hard_p05": solve_hard_p05,
    "hard_p06": solve_hard_p06,
    "hard_p07": solve_hard_p07,
}