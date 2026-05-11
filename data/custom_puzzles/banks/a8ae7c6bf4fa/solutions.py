"""Reference solvers for the twenty-first 21-task ARC-style puzzle bank.

This batch emphasizes interval completion, local geometric inference, keyed selection,
object symmetry, sorting-and-packing, reflective simulation, containment reasoning,
relation matrices, transform scripts, assignment into frames, and portal pathfinding.
"""

from typing import List
from collections import deque, defaultdict

Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {
    "row_span_fill": "Fill an inclusive row segment between matching same-color endpoints when the interior is empty.",
    "diagonal_mid_fill": "Fill the midpoint between same-color diagonal endpoints that are exactly two steps apart.",
    "four_diag_center": "Fill an empty center cell when all four diagonal neighbors share one nonzero color.",
    "rectangle_fourth_corner": "Infer and complete the missing corner of an axis-aligned monochrome rectangle.",
    "row_majority_filter": "Keep only the most frequent nonzero color in each row.",
    "line_extend_one": "Extend a domino by one cell along its unique open continuation direction.",
    "border_crosshair": "Project top-border markers down columns and left-border markers across rows.",
    "color_key_crop": "Use the top-left color key to select which monochrome object to crop.",
    "bbox_outline_union": "Replace each object by the outline of its tight bounding box.",
    "marker_offset_clone": "Use two marker cells to define a translation vector for cloning an object.",
    "symmetry_signature_recolor": "Recolor objects according to their reflection symmetry signature.",
    "perimeter_gallery": "Crop objects and concatenate them sorted by bounding-box perimeter.",
    "seeded_room_fill": "Flood each enclosed wall room with the room's single seed color.",
    "corner_key_transform": "Apply a transform chosen by the top-left key to the main object and crop the result.",
    "mirror_beam": "Trace an eastward beam through reflective mirrors until it hits a wall or exits the grid.",
    "normalize_boolean": "Normalize two shapes to one origin and apply a keyed Boolean operation.",
    "containment_depth": "Assign each object a color based on how many bounding boxes contain it.",
    "contact_matrix": "Output a relation matrix for orthogonally touching monochrome objects.",
    "script_timeline": "Emit the initial crop and every cumulative transform state in a gallery.",
    "frame_fit_insert": "Insert each loose object into the frame whose interior size exactly matches its crop.",
    "portal_checkpoint_path": "Find a shortest path through a checkpoint using linked portals."
}

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def dims(g):
    return len(g), len(g[0]) if g else 0

def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w

def deepcopy_grid(g):
    return [row[:] for row in g]

def crop_bbox(g,bg=0):
    h,w=dims(g)
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]!=bg]
    if not cells:
        return [[bg]]
    r0=min(r for r,c in cells); r1=max(r for r,c in cells)
    c0=min(c for r,c in cells); c1=max(c for r,c in cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def bbox_of_cells(cells):
    r0=min(r for r,c in cells); r1=max(r for r,c in cells)
    c0=min(c for r,c in cells); c1=max(c for r,c in cells)
    return r0,r1,c0,c1

def rotate90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g):
    return [row[::-1] for row in g[::-1]]

def rotate270(g):
    return rotate90(rotate180(g))

def flip_h(g):
    return [row[::-1] for row in g]

def flip_v(g):
    return g[::-1]

def draw_rect_outline(g,r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color
    return g

def find_components(g, bg=0, color_sensitive=True):
    h,w=dims(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in seen or g[r][c]==bg:
                continue
            color=g[r][c]
            q=deque([(r,c)]); seen.add((r,c)); cells=[]
            while q:
                cr,cc=q.popleft(); cells.append((cr,cc))
                for dr,dc in DIR4:
                    nr,nc=cr+dr,cc+dc
                    if inb(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]!=bg:
                        if (not color_sensitive) or g[nr][nc]==color:
                            seen.add((nr,nc)); q.append((nr,nc))
            comps.append({"color":color,"cells":cells})
    return comps

def crop_component(g, comp):
    cells=comp["cells"]; color=comp["color"]
    r0,r1,c0,c1=bbox_of_cells(cells)
    out=blank(r1-r0+1,c1-c0+1,0)
    for r,c in cells:
        out[r-r0][c-c0]=g[r][c]
    return out

def transform_grid_by_key(g,key):
    # 1 rot90, 2 rot180, 3 rot270, 4 flip_h
    if key==1: return rotate90(g)
    if key==2: return rotate180(g)
    if key==3: return rotate270(g)
    if key==4: return flip_h(g)
    return deepcopy_grid(g)

def object_symmetry_class(crop):
    # returns 'both','h','v','none'
    ch = crop == flip_h(crop)
    cv = crop == flip_v(crop)
    if ch and cv: return 'both'
    if ch: return 'h'
    if cv: return 'v'
    return 'none'

def bbox_perimeter(cells):
    r0,r1,c0,c1=bbox_of_cells(cells)
    h=r1-r0+1; w=c1-c0+1
    return 2*(h+w)

def solve_easy_p01(g: Grid) -> Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(h):
        positions=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                positions[v].append(c)
        for color, cols in positions.items():
            if len(cols)==2:
                c0,c1=cols
                if all(g[r][c]==0 for c in range(c0+1,c1)):
                    for c in range(c0,c1+1):
                        out[r][c]=color
    return out

def solve_easy_p02(g: Grid) -> Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(h):
        for c in range(w):
            color=g[r][c]
            if color==0: 
                continue
            for dr,dc in [(1,1),(1,-1)]:
                r2,c2=r+2*dr,c+2*dc
                rm,cm=r+dr,c+dc
                if inb(g,r2,c2) and g[r2][c2]==color and g[rm][cm]==0:
                    out[rm][cm]=color
    return out

def solve_easy_p03(g: Grid) -> Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            colors=set(v for v in vals if v!=0)
            if len(colors)==1 and len(vals)==4 and all(v==list(colors)[0] for v in vals):
                out[r][c]=list(colors)[0]
    return out

def solve_easy_p04(g: Grid) -> Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    for color in range(1,10):
        pts=[(r,c) for r in range(h) for c in range(w) if g[r][c]==color]
        ptset=set(pts)
        # for every pair of distinct rows and cols, see if exactly 3 corners exist and 1 missing
        rows=sorted(set(r for r,c in pts)); cols=sorted(set(c for r,c in pts))
        for r0 in rows:
            for r1 in rows:
                if r1<=r0: continue
                for c0 in cols:
                    for c1 in cols:
                        if c1<=c0: continue
                        corners=[(r0,c0),(r0,c1),(r1,c0),(r1,c1)]
                        present=[p in ptset for p in corners]
                        if sum(present)==3:
                            missing=corners[present.index(False)]
                            if g[missing[0]][missing[1]]==0:
                                out[missing[0]][missing[1]]=color
    return out

def solve_easy_p05(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w,0)
    for r in range(h):
        counts=defaultdict(int)
        firstpos={}
        for c,v in enumerate(g[r]):
            if v!=0:
                counts[v]+=1
                firstpos.setdefault(v,c)
        if not counts:
            continue
        best=max(counts, key=lambda v:(counts[v], -firstpos[v]))  # most frequent, earliest
        for c,v in enumerate(g[r]):
            if v==best:
                out[r][c]=v
    return out

def solve_easy_p06(g: Grid) -> Grid:
    h,w=dims(g)
    out=deepcopy_grid(g)
    # horizontal dominos
    for r in range(h):
        c=0
        while c<w-1:
            color=g[r][c]
            if color!=0 and g[r][c+1]==color:
                left = c-1
                right = c+2
                left_open = left>=0 and g[r][left]==0
                right_open = right<w and g[r][right]==0
                if left_open ^ right_open:
                    if left_open:
                        out[r][left]=color
                    else:
                        out[r][right]=color
                c += 2
            else:
                c += 1
    # vertical dominos
    for c in range(w):
        r=0
        while r<h-1:
            color=g[r][c]
            if color!=0 and g[r+1][c]==color:
                up = r-1
                down = r+2
                up_open = up>=0 and g[up][c]==0
                down_open = down<h and g[down][c]==0
                if up_open ^ down_open:
                    if up_open:
                        out[up][c]=color
                    else:
                        out[down][c]=color
                r += 2
            else:
                r += 1
    return out

def solve_easy_p07(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w,0)
    # left-column markers paint full row
    for r in range(h):
        color=g[r][0]
        if color!=0:
            for c in range(w):
                out[r][c]=color
    # top-row markers paint full column; these override row paints at intersections
    for c in range(w):
        color=g[0][c]
        if color!=0:
            for r in range(h):
                out[r][c]=color
    return out

def solve_medium_p01(g: Grid) -> Grid:
    key=g[0][0]
    h,w=dims(g)
    comps=find_components(g, bg=0, color_sensitive=True)
    targets=[comp for comp in comps if comp["color"]==key and (0,0) not in comp["cells"]]
    if not targets:
        return [[0]]
    # if multiple components of target color, take largest
    target=max(targets, key=lambda comp: len(comp["cells"]))
    return crop_component(g,target)

def solve_medium_p02(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w,0)
    for comp in find_components(g, bg=0, color_sensitive=True):
        cells=comp["cells"]; color=comp["color"]
        r0,r1,c0,c1=bbox_of_cells(cells)
        draw_rect_outline(out,r0,c0,r1,c1,color)
    return out

def solve_medium_p03(g: Grid) -> Grid:
    h,w=dims(g)
    pts={}
    object_cells=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==1: pts[1]=(r,c)
            elif v==2: pts[2]=(r,c)
    # main object: largest component with color not in {1,2,0}
    comps=[comp for comp in find_components(g,bg=0,color_sensitive=True) if comp["color"] not in (1,2)]
    if not comps or 1 not in pts or 2 not in pts:
        return deepcopy_grid(g)
    obj=max(comps,key=lambda comp: len(comp["cells"]))
    dr=pts[2][0]-pts[1][0]; dc=pts[2][1]-pts[1][1]
    out=blank(h,w,0)
    # keep original
    for r,c in obj["cells"]:
        out[r][c]=obj["color"]
    # translated copy
    for r,c in obj["cells"]:
        nr,nc=r+dr,c+dc
        if inb(g,nr,nc):
            out[nr][nc]=obj["color"]
    return out

def solve_medium_p04(g: Grid) -> Grid:
    mapping={'both':2,'h':3,'v':4,'none':6}
    h,w=dims(g)
    out=blank(h,w,0)
    for comp in find_components(g,bg=0,color_sensitive=True):
        crop=crop_component(g,comp)
        cls=object_symmetry_class([[1 if v!=0 else 0 for v in row] for row in crop])
        newc=mapping[cls]
        for r,c in comp["cells"]:
            out[r][c]=newc
    return out

def solve_medium_p05(g: Grid) -> Grid:
    comps=find_components(g,bg=0,color_sensitive=True)
    # sort by bbox perimeter ascending, then leftmost appearance
    comps_sorted=sorted(comps, key=lambda comp:(bbox_perimeter(comp["cells"]), min(c for r,c in comp["cells"]), min(r for r,c in comp["cells"])))
    crops=[crop_component(g,comp) for comp in comps_sorted]
    H=max(len(c) for c in crops) if crops else 1
    W=sum(len(c[0]) for c in crops) + max(0,len(crops)-1)
    out=blank(H,W,0)
    off=0
    for crop in crops:
        ch,cw=dims(crop)
        for r in range(ch):
            for c in range(cw):
                out[r][off+c]=crop[r][c]
        off += cw + 1
    return out

def solve_medium_p06(g: Grid) -> Grid:
    # walls color 8; each enclosed room has single seed color
    h,w=dims(g)
    out=deepcopy_grid(g)
    seen=set()
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and (r,c) not in seen:
                q=deque([(r,c)]); seen.add((r,c)); cells=[]; seeds=set(); touches_edge=False
                while q:
                    cr,cc=q.popleft(); cells.append((cr,cc))
                    if cr==0 or cc==0 or cr==h-1 or cc==w-1:
                        touches_edge=True
                    for dr,dc in DIR4:
                        nr,nc=cr+dr,cc+dc
                        if not inb(g,nr,nc): continue
                        v=g[nr][nc]
                        if v==0 and (nr,nc) not in seen:
                            seen.add((nr,nc)); q.append((nr,nc))
                        elif v not in (0,8):
                            seeds.add(v)
                if not touches_edge and len(seeds)==1:
                    color=next(iter(seeds))
                    for rr,cc in cells:
                        out[rr][cc]=color
    return out

def solve_medium_p07(g: Grid) -> Grid:
    key=g[0][0]
    comps=[comp for comp in find_components(g,bg=0,color_sensitive=True) if (0,0) not in comp["cells"]]
    if not comps:
        return [[0]]
    # use largest component excluding key
    target=max(comps,key=lambda comp: len(comp["cells"]))
    crop=crop_component(g,target)
    return transform_grid_by_key(crop, key)

def solve_hard_p01(g: Grid) -> Grid:
    # mirror beam: 1 emitter starts east; 2='/' ; 3='\\' ; 8 wall; mark traversed zeros as 7
    h,w=dims(g)
    out=deepcopy_grid(g)
    start=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==1:
                start=(r,c)
    if start is None:
        return out
    dir=(0,1)
    r,c=start
    visited=set()
    # move off emitter
    while True:
        r += dir[0]; c += dir[1]
        if not inb(g,r,c): break
        state=(r,c,dir)
        if state in visited: break
        visited.add(state)
        v=g[r][c]
        if v==8:
            break
        if v==0:
            out[r][c]=7
        elif v==2:  # slash
            dr,dc=dir
            dir=(-dc,-dr)
        elif v==3:  # backslash
            dr,dc=dir
            dir=(dc,dr)
        else:
            # pass through other specials unchanged
            pass
    return out

def solve_hard_p02(g: Grid) -> Grid:
    key=g[0][0]
    comps=[comp for comp in find_components(g,bg=0,color_sensitive=True) if comp["color"] in (4,6)]
    if len(comps)<2:
        return [[0]]
    # one 4-shape and one 6-shape; if multiple, take largest per color
    a=max([c for c in comps if c["color"]==4], key=lambda comp: len(comp["cells"]))
    b=max([c for c in comps if c["color"]==6], key=lambda comp: len(comp["cells"]))
    ca=[[1 if v!=0 else 0 for v in row] for row in crop_component(g,a)]
    cb=[[1 if v!=0 else 0 for v in row] for row in crop_component(g,b)]
    ha,wa=dims(ca); hb,wb=dims(cb)
    H=max(ha,hb); W=max(wa,wb)
    A=blank(H,W,0); B=blank(H,W,0)
    for r in range(ha):
        for c in range(wa):
            A[r][c]=1 if ca[r][c] else 0
    for r in range(hb):
        for c in range(wb):
            B[r][c]=1 if cb[r][c] else 0
    out=blank(H,W,0)
    for r in range(H):
        for c in range(W):
            av=A[r][c]==1; bv=B[r][c]==1
            if key==1:
                keep=av or bv
            elif key==2:
                keep=av and bv
            else:
                keep=(av != bv)
            if keep:
                out[r][c]=8
    return crop_bbox(out,0)

def solve_hard_p03(g: Grid) -> Grid:
    # recolor each monochrome component by nesting depth based on bbox containment
    comps=find_components(g,bg=0,color_sensitive=True)
    boxes=[bbox_of_cells(comp["cells"]) for comp in comps]
    depths=[]
    for i,(r0,r1,c0,c1) in enumerate(boxes):
        depth=1
        for j,(sr0,sr1,sc0,sc1) in enumerate(boxes):
            if i!=j and sr0<=r0 and sr1>=r1 and sc0<=c0 and sc1>=c1:
                if (sr0,sr1,sc0,sc1)!=(r0,r1,c0,c1):
                    depth += 1
        depths.append(depth)
    palette={1:2,2:3,3:4,4:5,5:6}
    h,w=dims(g)
    out=blank(h,w,0)
    for comp,depth in zip(comps,depths):
        color=palette.get(depth,9)
        for r,c in comp["cells"]:
            out[r][c]=color
    return out

def solve_hard_p04(g: Grid) -> Grid:
    comps=find_components(g,bg=0,color_sensitive=True)
    comps=sorted(comps, key=lambda comp:(min(c for r,c in comp["cells"]), min(r for r,c in comp["cells"])))
    n=len(comps)
    out=blank(n,n,0)
    for i in range(n):
        out[i][i]=5
    cellsets=[set(comp["cells"]) for comp in comps]
    for i in range(n):
        for j in range(n):
            if i==j: continue
            touch=False
            for r,c in cellsets[i]:
                for dr,dc in DIR4:
                    if (r+dr,c+dc) in cellsets[j]:
                        touch=True; break
                if touch: break
            if touch:
                out[i][j]=7
    return out

def solve_hard_p05(g: Grid) -> Grid:
    # top row codes until first 0; object is below; gallery initial + cumulative transforms
    h,w=dims(g)
    codes=[]
    for c in range(w):
        if g[0][c]==0: break
        codes.append(g[0][c])
    body=[row[:] for row in g[1:]]
    body_crop=crop_bbox(body,0)
    states=[body_crop]
    cur=body_crop
    for code in codes:
        cur=transform_grid_by_key(cur, code)
        states.append(cur)
    H=max(len(s) for s in states)
    W=sum(len(s[0]) for s in states)+len(states)-1
    out=blank(H,W,0)
    off=0
    for s in states:
        sh,sw=dims(s)
        for r in range(sh):
            for c in range(sw):
                out[r][off+c]=s[r][c]
        off += sw+1
    return out

def solve_hard_p06(g: Grid) -> Grid:
    # match loose objects to hollow frames whose interior dims exactly match object bbox dims
    h,w=dims(g)
    comps=find_components(g,bg=0,color_sensitive=True)
    # frames are components where bbox outline filled and interior mostly zero in original
    frames=[]
    objects=[]
    for comp in comps:
        cells=set(comp["cells"]); color=comp["color"]
        r0,r1,c0,c1=bbox_of_cells(comp["cells"])
        outline={(r0,c) for c in range(c0,c1+1)}|{(r1,c) for c in range(c0,c1+1)}|{(r,c0) for r in range(r0,r1+1)}|{(r,c1) for r in range(r0,r1+1)}
        if cells==outline and r1-r0>=2 and c1-c0>=2:
            frames.append((comp,(r1-r0-1,c1-c0-1)))
        else:
            objects.append((comp,(r1-r0+1,c1-c0+1)))
    out=blank(h,w,0)
    # keep frames
    for comp,_ in frames:
        for r,c in comp["cells"]:
            out[r][c]=comp["color"]
    used=set()
    for fidx,(frame,inner) in enumerate(frames):
        match=None
        for oidx,(obj,shape) in enumerate(objects):
            if oidx in used: continue
            if shape==inner:
                match=oidx; break
        if match is None:
            continue
        used.add(match)
        obj,shape=objects[match]
        crop=crop_component(g,obj)
        r0,r1,c0,c1=bbox_of_cells(frame["cells"])
        for r in range(shape[0]):
            for c in range(shape[1]):
                if crop[r][c]!=0:
                    out[r0+1+r][c0+1+c]=crop[r][c]
    return out

def solve_hard_p07(g: Grid) -> Grid:
    # shortest path from start1 through checkpoint3 to goal2, portals 4 paired. walls 8.
    h,w=dims(g)
    start=goal=check=None
    portals=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==1: start=(r,c)
            elif v==2: goal=(r,c)
            elif v==3: check=(r,c)
            elif v==4: portals.append((r,c))
    portal_map={}
    if len(portals)==2:
        portal_map[portals[0]]=portals[1]
        portal_map[portals[1]]=portals[0]
    def neighbors(state):
        r,c,got=state
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not inb(g,nr,nc): continue
            v=g[nr][nc]
            if v==8: continue
            ngot=got or (v==3)
            if v==4 and (nr,nc) in portal_map:
                tr,tc=portal_map[(nr,nc)]
                yield (tr,tc,ngot)
            else:
                yield (nr,nc,ngot)
    start_state=(start[0],start[1], start==check)
    q=deque([start_state])
    prev={start_state:None}
    end_state=None
    while q:
        st=q.popleft()
        r,c,got=st
        if (r,c)==goal and got:
            end_state=st; break
        for ns in neighbors(st):
            if ns not in prev:
                prev[ns]=st; q.append(ns)
    out=deepcopy_grid(g)
    if end_state is None:
        return out
    st=end_state
    while prev[st] is not None:
        r,c,got=st
        if out[r][c]==0:
            out[r][c]=7
        st=prev[st]
    return out

SOLVERS = {
    'easy_p01': solve_easy_p01,
    'easy_p02': solve_easy_p02,
    'easy_p03': solve_easy_p03,
    'easy_p04': solve_easy_p04,
    'easy_p05': solve_easy_p05,
    'easy_p06': solve_easy_p06,
    'easy_p07': solve_easy_p07,
    'medium_p01': solve_medium_p01,
    'medium_p02': solve_medium_p02,
    'medium_p03': solve_medium_p03,
    'medium_p04': solve_medium_p04,
    'medium_p05': solve_medium_p05,
    'medium_p06': solve_medium_p06,
    'medium_p07': solve_medium_p07,
    'hard_p01': solve_hard_p01,
    'hard_p02': solve_hard_p02,
    'hard_p03': solve_hard_p03,
    'hard_p04': solve_hard_p04,
    'hard_p05': solve_hard_p05,
    'hard_p06': solve_hard_p06,
    'hard_p07': solve_hard_p07,
}