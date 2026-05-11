"""Reference solvers for the tenth 21-task ARC-style puzzle bank.

This batch leans into:
- run rewrites and local vote rules
- profile extraction and legend-driven recoloring
- symmetry classification and marker docking
- waypoint routing, majority overlays, and keyed transform galleries
"""
from typing import List
from collections import deque, defaultdict

Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {
    'diamond_bloom': 'Expand a singleton seed into its full Manhattan-distance-2 diamond.',
    'run_median': 'Collapse each odd horizontal run to its middle cell.',
    'zebra_bridge': 'Fill every other cell between matched row endpoints.',
    'plus_vote_fill': 'Fill a center cell when all four orthogonal neighbors agree.',
    'run_grow': 'Extend each horizontal run by one cell at both ends.',
    'run_dash': 'Keep every other cell of each horizontal run.',
    'row_flush_right': 'Slide each row’s nonzero cells to the right edge, preserving order.',
    'perimeter_rank': 'Rank connected objects by perimeter and map the ranks to output colors.',
    'bbox_frame': 'Replace an object by the rectangular frame of its tight bounding box.',
    'row_profile': 'Convert a cropped object into a row-count histogram.',
    'symmetry_class': 'Classify objects by vertical and horizontal mirror symmetry.',
    'stack_by_height': 'Crop objects and stack them from tallest to shortest.',
    'marker_dock': 'Dock each colored object under its matching marker column.',
    'palette_legend': 'Read adjacent old→new color pairs from a legend row.',
    'waypoint_path': 'Route a shortest orthogonal path that must pass through a waypoint.',
    'threeway_majority': 'Keep cells occupied by at least two of three normalized shapes.',
    'frame_rotate_insert': 'Rotate an external insert object according to a key and place it into its matching frame.',
    'anchor_polyline': 'Connect ordered object anchors with orthogonal polylines.',
    'dual_key_transform': 'One key selects an object and the other key selects a transform.',
    'transform_timeline': 'Apply a script of transforms and emit every intermediate stage.',
    'symmetry_table': 'Pack objects into a 2×2 gallery based on symmetry class.',
}

def blank(h,w,v=0): return [[v for _ in range(w)] for _ in range(h)]


def copy_grid(g): return [row[:] for row in g]


def dims(g): return len(g), len(g[0]) if g else 0


def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells: return [[0]]
    r0=min(r for r,c in cells); r1=max(r for r,c in cells)
    c0=min(c for r,c in cells); c1=max(c for r,c in cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def bbox_of_cells(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def rotate90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate180(g): return rotate90(rotate90(g))


def rotate270(g): return rotate90(rotate180(g))


def hmirror(g): return [list(reversed(row)) for row in g]


def vmirror(g): return list(reversed([row[:] for row in g]))


def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]


def paste(dst, src, top, left, transparent=True):
    h,w=dims(src)
    H,W=dims(dst)
    for r in range(h):
        for c in range(w):
            if 0<=top+r<H and 0<=left+c<W and (not transparent or src[r][c]!=0):
                dst[top+r][left+c]=src[r][c]
    return dst


def connected_components(g):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and not seen[r][c]:
                color=g[r][c]
                q=deque([(r,c)]); seen[r][c]=True; cells=[]
                while q:
                    rr,cc=q.popleft(); cells.append((rr,cc))
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==color:
                            seen[nr][nc]=True; q.append((nr,nc))
                comps.append({'color':color,'cells':cells})
    return comps


def shape_mask(g):
    return [[1 if v!=0 else 0 for v in row] for row in g]


def crop_component(g, comp):
    r0,c0,r1,c1=bbox_of_cells(comp['cells'])
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def perimeter_of_comp(g, comp):
    s=set(comp['cells']); p=0
    for r,c in comp['cells']:
        for dr,dc in DIR4:
            if (r+dr,c+dc) not in s: p+=1
    return p


def v_sym(mask):
    return mask == hmirror(mask)


def h_sym(mask):
    return mask == vmirror(mask)


def normalize_shapes(shapes):
    # shapes list of cropped grids, output on common canvas
    hs=[len(s) for s in shapes]; ws=[len(s[0]) for s in shapes]
    H=max(hs); W=max(ws)
    mats=[]
    for s in shapes:
        h,w=dims(s)
        m=blank(H,W,0)
        paste(m,s,0,0,transparent=True)
        mats.append(m)
    return mats


def shortest_path_with_waypoint(g, start_color, waypoint_color, goal_color, wall=5):
    # start/waypoint/goal singletons
    pos={}
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in (start_color, waypoint_color, goal_color):
                pos[v]=(r,c)
    def bfs(src, dst):
        H,W=dims(g)
        q=deque([src]); prev={src:None}
        while q:
            cur=q.popleft()
            if cur==dst: break
            for dr,dc in DIR4:
                nr,nc=cur[0]+dr, cur[1]+dc
                if 0<=nr<H and 0<=nc<W and (nr,nc) not in prev:
                    if g[nr][nc] not in (wall,) or (nr,nc)==dst:
                        prev[(nr,nc)]=cur; q.append((nr,nc))
        if dst not in prev: return None
        path=[]; cur=dst
        while cur is not None:
            path.append(cur); cur=prev[cur]
        return list(reversed(path))
    p1=bfs(pos[start_color], pos[waypoint_color]); p2=bfs(pos[waypoint_color], pos[goal_color])
    assert p1 and p2
    return p1[:-1]+p2


def is_frame_component(g, comp):
    color=comp['color']
    r0,c0,r1,c1=bbox_of_cells(comp['cells'])
    cells=set(comp['cells'])
    # all border positions occupied
    border=[]
    for c in range(c0,c1+1):
        border.append((r0,c)); border.append((r1,c))
    for r in range(r0,r1+1):
        border.append((r,c0)); border.append((r,c1))
    border=set(border)
    return cells==border and r1-r0>=2 and c1-c0>=2


def apply_key_transform(shape, key):
    if key==1: return shape
    if key==2: return rotate90(shape)
    if key==3: return hmirror(shape)
    if key==4: return transpose(shape)
    if key==5: return rotate180(shape)
    return shape


def solve_j01_diamond_bloom(g: Grid) -> Grid:
    H,W=dims(g)
    out=blank(H,W,0)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                for rr in range(H):
                    for cc in range(W):
                        if abs(rr-r)+abs(cc-c)<=2:
                            out[rr][cc]=v
    return out


def solve_j02_run_median(g: Grid) -> Grid:
    H,W=dims(g); out=blank(H,W,0)
    for r in range(H):
        c=0
        while c<W:
            if g[r][c]==0:
                c+=1; continue
            color=g[r][c]; s=c
            while c<W and g[r][c]==color: c+=1
            e=c-1; L=e-s+1
            mid=s+L//2
            out[r][mid]=color
    return out


def solve_j03_zebra_bridge(g: Grid) -> Grid:
    H,W=dims(g); out=copy_grid(g)
    for r in range(H):
        positions=defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0: positions[v].append(c)
        for color, cols in positions.items():
            if len(cols)==2:
                a,b=cols
                if all(g[r][c]==0 for c in range(a+1,b)):
                    for k,c in enumerate(range(a+1,b), start=1):
                        if k%2==1:
                            out[r][c]=color
    return out


def solve_j04_plus_vote_fill(g: Grid) -> Grid:
    H,W=dims(g); out=copy_grid(g)
    for r in range(1,H-1):
        for c in range(1,W-1):
            if g[r][c]==0:
                vals=[g[r-1][c], g[r+1][c], g[r][c-1], g[r][c+1]]
                if vals[0]!=0 and vals.count(vals[0])==4:
                    out[r][c]=vals[0]
    return out


def solve_j05_run_grow(g: Grid) -> Grid:
    H,W=dims(g); out=copy_grid(g)
    for r in range(H):
        c=0
        while c<W:
            if g[r][c]==0:
                c+=1; continue
            color=g[r][c]; s=c
            while c<W and g[r][c]==color: c+=1
            e=c-1
            if s-1>=0 and g[r][s-1]==0: out[r][s-1]=color
            if e+1<W and g[r][e+1]==0: out[r][e+1]=color
    return out


def solve_j06_run_dash(g: Grid) -> Grid:
    H,W=dims(g); out=blank(H,W,0)
    for r in range(H):
        c=0
        while c<W:
            if g[r][c]==0:
                c+=1; continue
            color=g[r][c]; s=c
            while c<W and g[r][c]==color: c+=1
            for idx,cc in enumerate(range(s,c)):
                if idx%2==0:
                    out[r][cc]=color
    return out


def solve_j07_row_flush_right(g: Grid) -> Grid:
    H,W=dims(g); out=blank(H,W,0)
    for r in range(H):
        vals=[v for v in g[r] if v!=0]
        start=W-len(vals)
        for i,v in enumerate(vals):
            out[r][start+i]=v
    return out


def solve_j08_perimeter_rank(g: Grid) -> Grid:
    comps=connected_components(g)
    perims=sorted({perimeter_of_comp(g, comp) for comp in comps}, reverse=True)
    color_map={}
    palette=[2,3,4,6,8,9,1,5,7]
    for i,p in enumerate(perims):
        color_map[p]=palette[i]
    out=blank(*dims(g),0)
    for comp in comps:
        newc=color_map[perimeter_of_comp(g, comp)]
        for r,c in comp['cells']:
            out[r][c]=newc
    return out


def solve_j09_bbox_frame(g: Grid) -> Grid:
    H,W=dims(g); out=blank(H,W,0)
    for comp in connected_components(g):
        r0,c0,r1,c1=bbox_of_cells(comp['cells'])
        color=comp['color']
        for c in range(c0,c1+1):
            out[r0][c]=color; out[r1][c]=color
        for r in range(r0,r1+1):
            out[r][c0]=color; out[r][c1]=color
    return out


def solve_j10_row_profile(g: Grid) -> Grid:
    comp=max(connected_components(g), key=lambda comp: len(comp['cells']))
    cropped=crop_component(g, comp)
    mask=shape_mask(cropped)
    counts=[sum(row) for row in mask]
    color=comp['color']
    W=max(counts)
    out=blank(len(counts), W, 0)
    for r,cnt in enumerate(counts):
        for c in range(cnt):
            out[r][c]=color
    return out


def solve_j11_symmetry_class(g: Grid) -> Grid:
    H,W=dims(g); out=blank(H,W,0)
    for comp in connected_components(g):
        mask=shape_mask(crop_component(g, comp))
        vs=v_sym(mask); hs=h_sym(mask)
        if vs and hs: newc=8
        elif vs: newc=2
        elif hs: newc=3
        else: newc=4
        for r,c in comp['cells']: out[r][c]=newc
    return out


def solve_j12_stack_by_height(g: Grid) -> Grid:
    comps=connected_components(g)
    items=[]
    for comp in comps:
        crop=crop_component(g, comp)
        items.append((len(crop), comp['color'], crop))
    items.sort(key=lambda t:(-t[0], t[1]))
    width=max(len(crop[0]) for _,_,crop in items)
    height=sum(len(crop) for _,_,crop in items)+(len(items)-1)
    out=blank(height,width,0)
    r=0
    for _,_,crop in items:
        paste(out, crop, r, 0, transparent=True)
        r += len(crop)+1
    return out


def solve_j13_marker_dock(g: Grid) -> Grid:
    H,W=dims(g)
    markers={}
    for c,v in enumerate(g[0]):
        if v!=0: markers[v]=c
    comps=connected_components(g[1:])  # components in body, row offset to fix
    real=[]
    for comp in comps:
        cells=[(r+1,c) for r,c in comp['cells']]
        real.append({'color': comp['color'], 'cells': cells})
    # assume one object per marker color
    crops={}
    for comp in real:
        crop=crop_component(g, comp)
        crops[comp['color']]=crop
    max_h=max(len(c) for c in crops.values()) if crops else 1
    out_h=max_h
    out=blank(out_h,W,0)
    for color,col in markers.items():
        crop=crops[color]
        h,w=dims(crop)
        top=out_h-h
        left=col
        paste(out, crop, top, left, transparent=True)
    return out


def solve_j14_palette_legend(g: Grid) -> Grid:
    top=g[0]
    mapping={}
    c=0
    while c+1<len(top):
        if top[c]!=0 and top[c+1]!=0:
            mapping[top[c]]=top[c+1]
            c+=2
        else:
            c+=1
    body=[row[:] for row in g[1:]]
    for r,row in enumerate(body):
        for c,v in enumerate(row):
            if v in mapping:
                body[r][c]=mapping[v]
    return body


def solve_j15_waypoint_path(g: Grid) -> Grid:
    path=shortest_path_with_waypoint(g, 2, 3, 4, wall=5)
    out=copy_grid(g)
    for r,c in path:
        out[r][c]=8
    return out


def solve_j16_threeway_majority(g: Grid) -> Grid:
    comps=connected_components(g)
    shapes=[crop_component(g, comp) for comp in comps]
    mats=normalize_shapes(shapes)
    H,W=dims(mats[0])
    out=blank(H,W,0)
    for r in range(H):
        for c in range(W):
            cnt=sum(1 for m in mats if m[r][c]!=0)
            if cnt>=2: out[r][c]=8
    return crop_nonzero(out)


def solve_j17_frame_rotate_insert(g: Grid) -> Grid:
    H,W=dims(g)
    comps=connected_components(g)
    frames=[comp for comp in comps if is_frame_component(g, comp)]
    objects=[comp for comp in comps if not is_frame_component(g, comp) and len(comp['cells'])>1]
    out=blank(H,W,0)
    # copy frames first
    for fr in frames:
        for r,c in fr['cells']: out[r][c]=fr['color']
    # markers singletons
    singles=[comp for comp in comps if len(comp['cells'])==1 and comp['color'] in (1,2,3,4)]
    for fr in frames:
        r0,c0,r1,c1=bbox_of_cells(fr['cells'])
        color=fr['color']
        key=1
        for s in singles:
            (sr,sc)=s['cells'][0]
            if r0<sr<r1 and c0<sc<c1:
                key=s['color']
        obj=[o for o in objects if o['color']==color][0]
        crop=crop_component(g, obj)
        if key==1: tr=crop
        elif key==2: tr=rotate90(crop)
        elif key==3: tr=rotate180(crop)
        elif key==4: tr=rotate270(crop)
        else: tr=crop
        paste(out, tr, r0+1, c0+1, transparent=True)
    return out


def solve_j18_anchor_polyline(g: Grid) -> Grid:
    out=copy_grid(g)
    comps=sorted(connected_components(g), key=lambda comp: min(c for r,c in comp['cells']))
    anchors=[]
    for comp in comps:
        r0,c0,r1,c1=bbox_of_cells(comp['cells'])
        anchors.append((r0,c0))
    for (r1,c1),(r2,c2) in zip(anchors, anchors[1:]):
        step=1 if c2>=c1 else -1
        for c in range(c1, c2+step, step):
            out[r1][c]=8
        step=1 if r2>=r1 else -1
        for r in range(r1, r2+step, step):
            out[r][c2]=8
    return out


def solve_j19_dual_key_transform(g: Grid) -> Grid:
    # top row has [select_color, transform_key]
    sel=g[0][0]
    key=g[0][-1]
    comps=[comp for comp in connected_components(g[1:])]
    chosen=None
    for comp in comps:
        if comp['color']==sel:
            cells=[(r+1,c) for r,c in comp['cells']]
            chosen={'color':comp['color'],'cells':cells}
    assert chosen is not None
    crop=crop_component(g, chosen)
    return crop_nonzero(apply_key_transform(crop, key))


def solve_j20_transform_timeline(g: Grid) -> Grid:
    keys=[v for v in g[0] if v!=0]
    body=[row[:] for row in g[1:]]
    comp=max(connected_components(body), key=lambda comp: len(comp['cells']))
    # rebuild chosen in body coordinates
    crop=crop_component(body, comp)
    stages=[crop_nonzero(crop)]
    cur=stages[0]
    for k in keys:
        cur=crop_nonzero(apply_key_transform(cur, k))
        stages.append(cur)
    height=max(len(s) for s in stages)
    width=sum(len(s[0]) for s in stages)+(len(stages)-1)
    out=blank(height,width,0)
    c=0
    for s in stages:
        paste(out, s, 0, c, transparent=True)
        c += len(s[0])+1
    return out


def solve_j21_symmetry_table(g: Grid) -> Grid:
    comps=connected_components(g)
    classes={}
    for comp in comps:
        crop=crop_component(g, comp)
        mask=shape_mask(crop)
        vs=v_sym(mask); hs=h_sym(mask)
        if vs and hs: cls='both'
        elif vs: cls='vertical'
        elif hs: cls='horizontal'
        else: cls='neither'
        classes[cls]=crop
    order=[classes['both'], classes['vertical'], classes['horizontal'], classes['neither']]
    hs=[len(x) for x in order]; ws=[len(x[0]) for x in order]
    top_h=max(hs[0],hs[1]); bot_h=max(hs[2],hs[3]); left_w=max(ws[0],ws[2]); right_w=max(ws[1],ws[3])
    H=top_h+1+bot_h; W=left_w+1+right_w
    out=blank(H,W,0)
    paste(out, order[0], 0, 0, transparent=True)
    paste(out, order[1], 0, left_w+1, transparent=True)
    paste(out, order[2], top_h+1, 0, transparent=True)
    paste(out, order[3], top_h+1, left_w+1, transparent=True)
    return out


TASK_SOLVERS = {
    'easy_j01': solve_j01_diamond_bloom,
    'easy_j02': solve_j02_run_median,
    'easy_j03': solve_j03_zebra_bridge,
    'easy_j04': solve_j04_plus_vote_fill,
    'easy_j05': solve_j05_run_grow,
    'easy_j06': solve_j06_run_dash,
    'easy_j07': solve_j07_row_flush_right,
    'medium_j08': solve_j08_perimeter_rank,
    'medium_j09': solve_j09_bbox_frame,
    'medium_j10': solve_j10_row_profile,
    'medium_j11': solve_j11_symmetry_class,
    'medium_j12': solve_j12_stack_by_height,
    'medium_j13': solve_j13_marker_dock,
    'medium_j14': solve_j14_palette_legend,
    'hard_j15': solve_j15_waypoint_path,
    'hard_j16': solve_j16_threeway_majority,
    'hard_j17': solve_j17_frame_rotate_insert,
    'hard_j18': solve_j18_anchor_polyline,
    'hard_j19': solve_j19_dual_key_transform,
    'hard_j20': solve_j20_transform_timeline,
    'hard_j21': solve_j21_symmetry_table,
}
