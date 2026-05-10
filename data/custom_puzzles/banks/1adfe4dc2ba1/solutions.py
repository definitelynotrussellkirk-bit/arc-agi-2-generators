"""Reference solvers for the thirteenth 21-task ARC-style puzzle bank.

This batch leans into:
- run structure, diagonal completion, row signatures, border-directed rays, and degree filters
- frame reasoning, instruction markers, sorted galleries, rank-based recoloring, and container logic
- dihedral shape matching, transform scripts, ordered pathfinding, visibility graphs, Boolean shape algebra,
  transformed frame stamping, and two-key compositional control
"""
from typing import List, Tuple
from collections import deque, defaultdict

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {
    "horizontal_run_starts": "Reduce each horizontal run to its first cell.",
    "diagonal_midpoint_bridge": "Fill the zero midpoint when a 3\u00d73 diagonal has matching endpoints.",
    "row_population_pack": "Rewrite each row as a left-packed bar whose length is that row\u2019s nonzero count.",
    "nearest_border_ray": "Extend a seed straight toward its uniquely nearest border.",
    "minority_to_majority": "Replace the globally rarer nonzero color with the dominant one.",
    "halo_without_center": "Expand a seed to its orthogonal neighbors but clear the center.",
    "degree1_filter": "Keep only cells with exactly one same-color orthogonal neighbor.",
    "scan_rect_frames": "Detect rectangular frames by scanning for constant-color borders, even when interiors contain objects.",
    "fill_largest_frame": "Fill the interior of the largest detected frame.",
    "corner_instruction_transform": "Use the marker corner position to choose a rigid transform.",
    "gallery_sort_by_height": "Crop objects and pack them left-to-right ordered by height.",
    "area_rank_recolor": "Assign colors by sorted component area.",
    "nearest_marker_recolor": "Recolor each object using the nearest label marker by column.",
    "keep_matching_container_contents": "Preserve only contents whose color matches the enclosing frame.",
    "repeat_template_by_count": "Count markers and emit that many copies of a template.",
    "dihedral_match_select": "Find the candidate matching a target up to rotation or reflection.",
    "transform_timeline": "Apply a script of transforms and keep every intermediate state.",
    "ordered_waypoint_path": "Route one path through waypoints in increasing order.",
    "visibility_degree": "Build a visibility graph and recolor by graph degree.",
    "keyed_boolean_shape": "Use a key to choose union, intersection, or xor of normalized shapes.",
    "transformed_frame_stamp": "Transform a template per marker and stamp it inside a frame.",
    "rank_select_then_transform": "Select an object by area rank, then transform it via a second key."
}

def blank(h,w,v=0): return [[v]*w for _ in range(h)]

def dims(g): return len(g), len(g[0]) if g else 0

def copy_grid(g): return [row[:] for row in g]

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g,cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def place_cells(g, cells, color, r0=0, c0=0):
    h,w=dims(g)
    for r,c in cells:
        rr=r0+r; cc=c0+c
        if 0<=rr<h and 0<=cc<w:
            g[rr][cc]=color

def paste(g, sub, r0, c0):
    h,w=dims(g)
    for r,row in enumerate(sub):
        for c,v in enumerate(row):
            if v!=0:
                rr=r0+r; cc=c0+c
                if 0<=rr<h and 0<=cc<w:
                    g[rr][cc]=v

def find_components(g, ignore_colors=None):
    h,w=dims(g)
    ignore=set(ignore_colors or [])
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or g[r][c]==0 or g[r][c] in ignore: 
                continue
            col=g[r][c]
            q=[(r,c)]
            seen[r][c]=True
            cells=[]
            while q:
                x,y=q.pop()
                cells.append((x,y))
                for dx,dy in DIR4:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and not seen[nx][ny] and g[nx][ny]==col:
                        seen[nx][ny]=True
                        q.append((nx,ny))
            comps.append({'color':col,'cells':cells,'bbox':bbox(cells),'area':len(cells)})
    return comps

def grid_from_cells(cells,color=1):
    if not cells: return [[0]]
    r0,c0,r1,c1=bbox(cells)
    h,w=r1-r0+1,c1-c0+1
    g=blank(h,w)
    for r,c in cells:
        g[r-r0][c-c0]=color
    return g

def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    return crop_bbox(g,cells)

def rotate90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g): return rotate90(rotate90(g))

def flip_h(g): # mirror left-right
    return [list(reversed(row)) for row in g]

def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]

def dihedral_grids(g):
    gs=[]
    base=g
    for k in range(4):
        rg=base
        for _ in range(k):
            rg=rotate90(rg)
        gs.append(crop_nonzero(rg))
    fg=flip_h(base)
    for k in range(4):
        rg=fg
        for _ in range(k):
            rg=rotate90(rg)
        gs.append(crop_nonzero(rg))
    # dedupe by tuple
    out=[]
    seen=set()
    for x in gs:
        t=tuple(tuple(row) for row in x)
        if t not in seen:
            seen.add(t); out.append(x)
    return out

def same_shape_under_dihedral(g1,g2):
    t2=tuple(tuple(1 if v else 0 for v in row) for row in crop_nonzero(g2))
    base=[[1 if v else 0 for v in row] for row in crop_nonzero(g1)]
    for x in dihedral_grids(base):
        tx=tuple(tuple(1 if v else 0 for v in row) for row in x)
        if tx==t2:
            return True
    return False

def recolor_grid(g,color):
    return [[color if v!=0 else 0 for v in row] for row in g]

def object_grid_from_comp(g, comp):
    return crop_bbox(g, comp['cells'])

def fill_frame_interior(g, frame):
    out=copy_grid(g)
    r0,c0,r1,c1=frame['bbox']
    col=frame['color']
    for r in range(r0+1,r1):
        for c in range(c0+1,c1):
            out[r][c]=col
    return out

def center_of_bbox(comp):
    r0,c0,r1,c1=comp['bbox']
    return ((r0+r1)/2.0, (c0+c1)/2.0)

def apply_transform_code(grid, code):
    # code can be 1 rot90, 2 rot180, 3 flip_h, 4 transpose, 5 identity, 6 flip_v? maybe adjust later
    if code==1:
        return crop_nonzero(rotate90(grid))
    if code==2:
        return crop_nonzero(rotate180(grid))
    if code==3:
        return crop_nonzero(flip_h(grid))
    if code==4:
        return crop_nonzero(transpose(grid))
    if code==5:
        return crop_nonzero(grid)
    if code==6:
        return crop_nonzero(flip_v(grid))
    if code==7:
        return crop_nonzero(rotate270(grid))
    return crop_nonzero(grid)

def bfs_path(g, start, goal, passable=None):
    h,w=dims(g)
    if passable is None:
        def passable(r,c):
            return g[r][c] != 1  # default walls=1
    dq=deque([start])
    prev={start:None}
    while dq:
        cur=dq.popleft()
        if cur==goal: break
        for dx,dy in DIR4:
            nx,ny=cur[0]+dx, cur[1]+dy
            if 0<=nx<h and 0<=ny<w and (nx,ny) not in prev and passable(nx,ny):
                prev[(nx,ny)]=cur
                dq.append((nx,ny))
    if goal not in prev:
        return None
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur); cur=prev[cur]
    return list(reversed(path))

def visibility_edges(g):
    comps=find_components(g)
    idgrid=[[-1]*dims(g)[1] for _ in range(dims(g)[0])]
    for i,comp in enumerate(comps):
        for r,c in comp['cells']:
            idgrid[r][c]=i
    edges=set()
    h,w=dims(g)
    for r in range(h):
        prev=None
        c=0
        while c<w:
            if idgrid[r][c]!=-1:
                cur=idgrid[r][c]
                # skip same component run contiguous horizontally
                cc=c
                while cc+1<w and idgrid[r][cc+1]==cur: cc+=1
                if prev is not None and prev!=cur:
                    # ensure cells between previous object's rightmost encounter and here were zeros? scanning contiguous nonzero/zeros already
                    edges.add(tuple(sorted((prev,cur))))
                prev=cur
                c=cc+1
            elif g[r][c]==0:
                c+=1
            else:
                c+=1
    # This is wrong because adjacency across row with other object; need only separated by zeros, scanning works because prev persists across zeros.
    for c in range(w):
        prev=None
        r=0
        while r<h:
            if idgrid[r][c]!=-1:
                cur=idgrid[r][c]
                rr=r
                while rr+1<h and idgrid[rr+1][c]==cur: rr+=1
                if prev is not None and prev!=cur:
                    edges.add(tuple(sorted((prev,cur))))
                prev=cur
                r=rr+1
            elif g[r][c]==0:
                r+=1
            else:
                r+=1
    return comps, edges

def center_paste_in_box(out, sub, box, color_override=None):
    r0,c0,r1,c1=box
    ih,iw=r1-r0+1,c1-c0+1
    sh,sw=dims(sub)
    sr=r0+(ih-sh)//2
    sc=c0+(iw-sw)//2
    for r,row in enumerate(sub):
        for c,v in enumerate(row):
            if v!=0:
                out[sr+r][sc+c] = color_override if color_override is not None else v

def count_colors(g):
    d=defaultdict(int)
    for row in g:
        for v in row:
            if v!=0: d[v]+=1
    return d

def scan_rect_frames(g):
    h,w=dims(g)
    found={}
    for r0 in range(h-2):
        for c0 in range(w-2):
            col=g[r0][c0]
            if col==0: continue
            for r1 in range(r0+2,h):
                if g[r1][c0]!=col: 
                    continue
                for c1 in range(c0+2,w):
                    if g[r0][c1]!=col or g[r1][c1]!=col:
                        continue
                    ok=True
                    for c in range(c0,c1+1):
                        if g[r0][c]!=col or g[r1][c]!=col:
                            ok=False; break
                    if not ok: 
                        continue
                    for r in range(r0,r1+1):
                        if g[r][c0]!=col or g[r][c1]!=col:
                            ok=False; break
                    if ok:
                        found[(r0,c0,r1,c1,col)]={'color':col,'bbox':(r0,c0,r1,c1),'interior_area':(r1-r0-1)*(c1-c0-1)}
    # filter non-maximal same-color frames? We can keep all; but examples may have only intended ones.
    return list(found.values())

def solve_easy_m01(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (c==0 or g[r][c-1]!=g[r][c]):
                out[r][c]=g[r][c]
    return out

def solve_easy_m02(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0: continue
            colors=[]
            if 0<=r-1<h and 0<=c-1<w and 0<=r+1<h and 0<=c+1<w:
                a,b=g[r-1][c-1],g[r+1][c+1]
                if a!=0 and a==b: colors.append(a)
            if 0<=r-1<h and 0<=c+1<w and 0<=r+1<h and 0<=c-1<w:
                a,b=g[r-1][c+1],g[r+1][c-1]
                if a!=0 and a==b: colors.append(a)
            if colors:
                # assume either one or all same in valid examples
                out[r][c]=colors[0]
    return out

def solve_easy_m03(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        vals=[v for v in row if v!=0]
        if not vals: continue
        # assume one color per row
        color=vals[0]
        n=len(vals)
        for c in range(min(n,w)):
            out[r][c]=color
    return out

def solve_easy_m04(g):
    h,w=dims(g)
    out=copy_grid(g)
    seeds=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c]!=0]
    for r,c,v in seeds:
        ds=[r,h-1-r,c,w-1-c]
        m=min(ds)
        # assume unique
        idx=ds.index(m)
        if idx==0:
            for rr in range(0,r+1): out[rr][c]=v
        elif idx==1:
            for rr in range(r,h): out[rr][c]=v
        elif idx==2:
            for cc in range(0,c+1): out[r][cc]=v
        else:
            for cc in range(c,w): out[r][cc]=v
    return out

def solve_easy_m05(g):
    counts=count_colors(g)
    if len(counts)<2:
        return copy_grid(g)
    dominant=max(counts.items(), key=lambda kv:(kv[1],-kv[0]))[0]
    rare=min(counts.items(), key=lambda kv:(kv[1],kv[0]))[0]
    out=copy_grid(g)
    for r,row in enumerate(out):
        for c,v in enumerate(row):
            if v==rare:
                out[r][c]=dominant
    return out

def solve_easy_m06(g):
    h,w=dims(g)
    out=blank(h,w)
    seeds=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c]!=0]
    for r,c,v in seeds:
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out[nr][nc]=v
    return out

def solve_easy_m07(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            deg=sum(1 for dr,dc in DIR4 if 0<=r+dr<h and 0<=c+dc<w and g[r+dr][c+dc]==v)
            if deg==1:
                out[r][c]=v
    return out

def solve_medium_m01(g):
    frames=scan_rect_frames(g)
    if not frames:
        return copy_grid(g)
    best=max(frames, key=lambda fr:(fr['interior_area'], fr['bbox'][2]-fr['bbox'][0], fr['bbox'][3]-fr['bbox'][1]))
    return fill_frame_interior(g,best)

def solve_medium_m02(g):
    h,w=dims(g)
    # marker color 9 in one corner
    corners=[(0,0),(0,w-1),(h-1,0),(h-1,w-1)]
    marker=None
    for pos in corners:
        if g[pos[0]][pos[1]]==9:
            marker=pos; break
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]!=0 and g[r][c]!=9]
    obj=crop_bbox(g,cells)
    if marker==(0,0):
        out=obj
    elif marker==(0,w-1):
        out=crop_nonzero(rotate90(obj))
    elif marker==(h-1,0):
        out=crop_nonzero(flip_h(obj))
    else:
        out=crop_nonzero(rotate180(obj))
    return out

def solve_medium_m03(g):
    comps=find_components(g)
    crops=[object_grid_from_comp(g,comp) for comp in comps]
    crops=sorted(crops, key=lambda sub:(len(sub), len(sub[0]), tuple(tuple(row) for row in sub)))
    H=max(len(sub) for sub in crops)
    W=sum(len(sub[0]) for sub in crops)+max(0,len(crops)-1)
    out=blank(H,W)
    c0=0
    for i,sub in enumerate(crops):
        paste(out,sub,0,c0)
        c0+=len(sub[0])+1
    return out

def solve_medium_m04(g):
    comps=find_components(g)
    comps_sorted=sorted(comps, key=lambda comp:(comp['area'], comp['bbox']))
    out=blank(*dims(g))
    for rank,comp in enumerate(comps_sorted, start=1):
        color=rank  # 1,2,3
        for r,c in comp['cells']:
            out[r][c]=color
    return out

def solve_medium_m05(g):
    h,w=dims(g)
    markers=[(c,g[0][c]) for c in range(w) if g[0][c]!=0]
    comps=find_components(g, ignore_colors={v for c,v in markers})
    out=copy_grid(g)
    marker_cols_colors=markers
    marker_colors=set(v for c,v in markers)
    # wipe objects first? recolor over existing objects
    for comp in comps:
        _, cx = center_of_bbox(comp)
        mc, col = min(marker_cols_colors, key=lambda item:(abs(item[0]-cx), item[0]))
        for r,c in comp['cells']:
            out[r][c]=col
    return out

def solve_medium_m06(g):
    out=copy_grid(g)
    frames=scan_rect_frames(g)
    for fr in frames:
        r0,c0,r1,c1=fr['bbox']
        inner=[]
        inner_colors=set()
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if out[r][c]!=0:
                    inner.append((r,c))
                    inner_colors.add(out[r][c])
        if inner and (len(inner_colors)!=1 or next(iter(inner_colors)) != fr['color']):
            for r,c in inner:
                out[r][c]=0
    return out

def solve_medium_m07(g):
    h,w=dims(g)
    marker_count=sum(1 for r in range(h) for c in range(w) if g[r][c]==9)
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]!=0 and g[r][c]!=9]
    template=crop_bbox(g,cells)
    th,tw=dims(template)
    H=th
    W=marker_count*tw + max(0, marker_count-1)
    out=blank(H,W)
    c0=0
    for i in range(marker_count):
        paste(out,template,0,c0)
        c0+=tw+1
    return out

def solve_hard_m01(g):
    h,w=dims(g)
    # target color 2
    target_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==2]
    target=crop_bbox(g,target_cells)
    comps=find_components(g, ignore_colors={2})
    # candidate components among others
    for comp in comps:
        cand=object_grid_from_comp(g,comp)
        if same_shape_under_dihedral(target, recolor_grid(cand,1)):
            return cand
    return [[0]]

def solve_hard_m02(g):
    h,w=dims(g)
    scripts=[v for v in g[0] if v!=0]
    # template = all nonzero below row0
    cells=[(r,c) for r in range(1,h) for c in range(w) if g[r][c]!=0]
    cur=crop_bbox(g,cells)
    states=[]
    for code in scripts:
        cur=apply_transform_code(cur, code)
        states.append(cur)
    H=max(len(sub) for sub in states)
    W=sum(len(sub[0]) for sub in states)+max(0,len(states)-1)
    out=blank(H,W)
    c0=0
    for sub in states:
        paste(out, sub, 0, c0)
        c0 += len(sub[0])+1
    return out

def solve_hard_m03(g):
    h,w=dims(g)
    pos={}
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v in {2,3,4,5,6,7}:
                pos[v]=(r,c)
    order=[2]+[k for k in sorted(pos) if k not in {2,3}] + [3]
    # ensure waypoints only 4+
    mids=[k for k in sorted(pos) if k not in {2,3}]
    order=[2]+mids+[3]
    out=copy_grid(g)
    for a,b in zip(order, order[1:]):
        path=bfs_path(g, pos[a], pos[b], passable=lambda r,c: g[r][c] != 1)
        if path is None:
            continue
        for r,c in path[1:-1]:
            if out[r][c]==0:
                out[r][c]=8
    return out

def solve_hard_m04(g):
    comps, edges = visibility_edges(g)
    deg=defaultdict(int)
    for a,b in edges:
        deg[a]+=1; deg[b]+=1
    out=blank(*dims(g))
    for i,comp in enumerate(comps):
        color=deg[i]+1
        for r,c in comp['cells']:
            out[r][c]=color
    return out

def solve_hard_m05(g):
    h,w=dims(g)
    key=g[0][0]
    comps=find_components(g, ignore_colors={key})
    # assume exactly two components besides key
    subs=[object_grid_from_comp(g,comp) for comp in comps]
    # choose two largest maybe
    subs=sorted(subs, key=lambda sub:(-sum(v!=0 for row in sub for v in row), len(sub), len(sub[0])))
    a,b=subs[:2]
    a_occ={(r,c) for r,row in enumerate(a) for c,v in enumerate(row) if v!=0}
    b_occ={(r,c) for r,row in enumerate(b) for c,v in enumerate(row) if v!=0}
    H=max(len(a),len(b)); W=max(len(a[0]),len(b[0]))
    if key==1: # union
        occ={(r,c) for r in range(H) for c in range(W) if (r,c) in a_occ or (r,c) in b_occ}
    elif key==2: # intersection
        occ={(r,c) for r in range(H) for c in range(W) if (r,c) in a_occ and (r,c) in b_occ}
    else: # xor
        occ={(r,c) for r in range(H) for c in range(W) if ((r,c) in a_occ) ^ ((r,c) in b_occ)}
    if not occ:
        return [[0]]
    rr=[r for r,c in occ]; cc=[c for r,c in occ]
    r0,c0,r1,c1=min(rr),min(cc),max(rr),max(cc)
    out=blank(r1-r0+1, c1-c0+1)
    for r,c in occ:
        out[r-r0][c-c0]=8
    return out

def solve_hard_m06(g):
    h,w=dims(g)
    frames=scan_rect_frames(g)
    # template color 7 cells not in any frame border or frame interior? We want one template outside frames.
    frame_boxes=[fr['bbox'] for fr in frames]
    def in_any_frame(r,c):
        for r0,c0,r1,c1 in frame_boxes:
            if r0<=r<=r1 and c0<=c<=c1:
                return True
        return False
    template_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==7 and not in_any_frame(r,c)]
    template=crop_bbox(g, template_cells)
    out=copy_grid(g)
    for r,c in template_cells:
        out[r][c]=0
    for fr in frames:
        r0,c0,r1,c1=fr['bbox']
        code=None; marker_pos=None
        for pos in [(r0-1,c0),(r0,c0-1),(r0-1,c1),(r1,c0-1)]:
            r,c=pos
            if 0<=r<h and 0<=c<w and g[r][c] in {1,2,3,4}:
                code=g[r][c]; marker_pos=pos; break
        if code is None: code=4
        sub=apply_transform_code(template, {1:1,2:2,3:3,4:5}[code])
        if marker_pos is not None:
            out[marker_pos[0]][marker_pos[1]]=0
        center_paste_in_box(out, recolor_grid(sub, code), (r0+1,c0+1,r1-1,c1-1), color_override=code)
    return out

def solve_hard_m07(g):
    h,w=dims(g)
    rank_key=g[0][0]  # 1 smallest,2 middle,3 largest
    tf_key=g[0][w-1]  # 4 id,5 rot90,6 flip_h,7 rot180
    ignore={rank_key, tf_key}
    comps=find_components(g, ignore_colors=ignore)
    comps_sorted=sorted(comps, key=lambda comp:(comp['area'], comp['bbox']))
    selected=comps_sorted[rank_key-1]
    sub=object_grid_from_comp(g, selected)
    if tf_key==4:
        out=sub
    elif tf_key==5:
        out=crop_nonzero(rotate90(sub))
    elif tf_key==6:
        out=crop_nonzero(flip_h(sub))
    else:
        out=crop_nonzero(rotate180(sub))
    return out

SOLVER_MAP = {
    'easy_m01': solve_easy_m01,
    'easy_m02': solve_easy_m02,
    'easy_m03': solve_easy_m03,
    'easy_m04': solve_easy_m04,
    'easy_m05': solve_easy_m05,
    'easy_m06': solve_easy_m06,
    'easy_m07': solve_easy_m07,
    'medium_m01': solve_medium_m01,
    'medium_m02': solve_medium_m02,
    'medium_m03': solve_medium_m03,
    'medium_m04': solve_medium_m04,
    'medium_m05': solve_medium_m05,
    'medium_m06': solve_medium_m06,
    'medium_m07': solve_medium_m07,
    'hard_m01': solve_hard_m01,
    'hard_m02': solve_hard_m02,
    'hard_m03': solve_hard_m03,
    'hard_m04': solve_hard_m04,
    'hard_m05': solve_hard_m05,
    'hard_m06': solve_hard_m06,
    'hard_m07': solve_hard_m07,
}

def validate_bank(tasks):
    """Return a list of validation log lines for the stored task bank."""
    lines = []
    checked = 0
    for task in tasks:
        fn = SOLVER_MAP[task["id"]]
        for split in ("train", "test"):
            for idx, ex in enumerate(task[split], start=1):
                got = fn(ex["input"])
                ok = got == ex["output"]
                checked += 1
                lines.append(f"{task['id']} {split}#{idx}: {'OK' if ok else 'FAIL'}")
                if not ok:
                    lines.append("expected:")
                    lines.extend(" ".join(map(str, row)) for row in ex["output"])
                    lines.append("got:")
                    lines.extend(" ".join(map(str, row)) for row in got)
    lines.append(f"checked_pairs={checked}")
    return lines
