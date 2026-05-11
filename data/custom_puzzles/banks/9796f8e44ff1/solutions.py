"""Reference solvers for the seventeenth 21-task ARC-style puzzle bank.

This batch pushes into a different slice of the ARC space: ring completion, marker-driven docking,
diagonal voting, room logic, hull filling, frame summarization, reflected beams, graph outputs,
orbit stamping, visibility unions, object-to-frame assignment, and ordered checkpoint pathfinding.
"""
from typing import List
from collections import deque, defaultdict

Grid = List[List[int]]
DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
SLASH = 1
BACKSLASH = 2
WALL = 5
DIRS = [(-1,0),(0,1),(1,0),(0,-1)]

NEW_PRIMITIVES = {'area_bar_gallery': 'Summarize objects as bottom-aligned bars whose heights equal their areas.',
 'bbox_cross': 'Replace an object by the cross formed by the center row and center column of its '
               'bounding box.',
 'corner_select_transform_insert': 'Select an object, transform it, and insert it into the chosen '
                                   'frame.',
 'diagonal_vote_fill': 'Fill a center cell when its four diagonal neighbors agree.',
 'dilation_adjacency_matrix': 'Build a graph-style adjacency matrix after one-step object '
                              'dilation.',
 'domino_square_expand': 'Expand a two-cell domino into the full 2x2 square on its bounding box.',
 'dual_corner_select_transform': 'One corner selects an object color; the other corner selects a '
                                 'transform.',
 'frame_center_label': 'Reduce each seeded frame to one center label cell.',
 'frame_fit_by_interior': 'Assign each object to the hollow frame whose interior dimensions fit '
                          'it.',
 'main_diagonal_echo': 'Echo every nonzero cell across the grid’s main diagonal.',
 'marker_axis_mirror': 'Mirror the scene across the global vertical or horizontal axis named by a '
                       'marker.',
 'mirror_beam': 'Trace a beam through slash and backslash mirrors until a wall or the boundary.',
 'one_gap_bridge': 'Bridge a one-cell horizontal or vertical gap between matching colors.',
 'orbit_stamp': 'Stamp rotated copies of a base object at anchor markers.',
 'ordered_checkpoint_path': 'Find a shortest path that visits colored checkpoints in order.',
 'pair_hull_fill': 'Fill the bounding hull spanning the two components of a color.',
 'ring_gap_fill': 'Complete a monochrome 3x3 ring that is missing one ring cell.',
 'row_dock_by_marker': 'Use a border marker to dock a horizontal segment flush left or flush '
                       'right.',
 'run_middle_keep': 'Reduce each horizontal run to its middle representative cell.',
 'seeded_room_fill': 'Fill a hollow rectangular room interior from the seed inside it.',
 'visibility_union': 'Combine orthogonal visibility rays from multiple watchers with overlap color '
                     '8.'}

def blank(h,w,v=0):
    return [[v for _ in range(w)] for _ in range(h)]


def copy_grid(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0]) if g else 0


def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop_component(g, cells):
    r0,c0,r1,c1 = bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]], (r0,c0,r1,c1)


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


def comp_same_color(g, connectivity=4):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    dirs=DIR4 if connectivity==4 else DIR8
    comps=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]:
                continue
            seen[r][c]=True
            v=g[r][c]
            if v==0:
                continue
            q=[(r,c)]
            cells=[]
            while q:
                rr,cc=q.pop()
                cells.append((rr,cc))
                for dr,dc in dirs:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({'color':v,'cells':cells})
    return comps


def frame_components(g):
    comps=comp_same_color(g,4)
    frames=[]
    for comp in comps:
        cells=comp['cells']
        color=comp['color']
        r0,c0,r1,c1=bbox(cells)
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if set(cells)==border and r1-r0>=2 and c1-c0>=2:
            frames.append({'color':color,'cells':cells,'bbox':(r0,c0,r1,c1)})
    return frames


def stamp_centered(out, shape, center_r, center_c):
    h,w=dims(shape)
    r0=center_r - h//2
    c0=center_c - w//2
    for r in range(h):
        for c in range(w):
            if shape[r][c]!=0:
                rr,cc=r0+r,c0+c
                if inb(out,rr,cc):
                    out[rr][cc]=shape[r][c]
    return out


def apply_transform_code(shape, code):
    if code==1:
        return copy_grid(shape)
    if code==2:
        return rotate90(shape)
    if code==3:
        return rotate180(shape)
    if code==4:
        return flip_h(shape)
    if code==5:
        return flip_v(shape)
    return copy_grid(shape)


def reflect(dir_idx, mirror):
    # 0 up,1 right,2 down,3 left
    if mirror==SLASH:
        return {0:1,1:0,2:3,3:2}[dir_idx]
    if mirror==BACKSLASH:
        return {0:3,3:0,2:1,1:2}[dir_idx]
    return dir_idx


def dilate_once(cells):
    s=set(cells)
    out=set(s)
    for r,c in list(s):
        for dr,dc in DIR4:
            out.add((r+dr,c+dc))
    return out


def bfs_path_with_checkpoints(g):
    h,w=dims(g)
    points={}
    for r in range(h):
        for c in range(w):
            if g[r][c] in (2,3,4,6):
                points[g[r][c]]=(r,c)
    start=points[2]
    checkpoints=[points[3], points[4], points[6]]
    target_count=0
    start_state=(start[0], start[1], 0)
    q=deque([start_state])
    prev={start_state: None}
    while q:
        r,c,k=q.popleft()
        if k==3 and (r,c)==points[6]:
            end_state=(r,c,k)
            break
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): continue
            if g[nr][nc]==5: continue
            nk=k
            if k<3 and (nr,nc)==checkpoints[k]:
                nk=k+1
            state=(nr,nc,nk)
            if state not in prev:
                prev[state]=(r,c,k)
                q.append(state)
    else:
        return []
    path=[]
    cur=end_state
    while cur is not None:
        path.append((cur[0],cur[1]))
        cur=prev[cur]
    path.reverse()
    return path


def solve_easy_p01(g):
    h,w=dims(g)
    out=copy_grid(g)
    ring=[(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)]
    for r in range(h-2):
        for c in range(w-2):
            vals=[g[r+dr][c+dc] for dr,dc in ring]
            nz=[v for v in vals if v!=0]
            if len(set(nz))==1 and len(nz)==7 and vals.count(0)==1 and g[r+1][c+1]==0:
                miss=vals.index(0)
                dr,dc=ring[miss]
                out[r+dr][c+dc]=nz[0]
    return out


def solve_easy_p02(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        row=g[r]
        if row[0]==1:
            vals=[v for v in row if v not in (0,1,2)]
            for i,v in enumerate(vals):
                out[r][i]=v
        elif row[-1]==2:
            vals=[v for v in row if v not in (0,1,2)]
            start=w-len(vals)
            for i,v in enumerate(vals):
                out[r][start+i]=v
    return out


def solve_easy_p03(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]==0:
                vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
                if vals[0]!=0 and all(v==vals[0] for v in vals):
                    out[r][c]=vals[0]
    return out


def solve_easy_p04(g):
    out=copy_grid(g)
    for comp in comp_same_color(g):
        cells=comp['cells']; color=comp['color']
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=sorted(cells)
        if r1==r2 and abs(c1-c2)==1:
            r=r1; c=min(c1,c2)
            for rr in (r,r+1):
                for cc in (c,c+1):
                    if inb(out,rr,cc):
                        out[rr][cc]=color
        elif c1==c2 and abs(r1-r2)==1:
            r=min(r1,r2); c=c1
            for rr in (r,r+1):
                for cc in (c,c+1):
                    if inb(out,rr,cc):
                        out[rr][cc]=color
    return out


def solve_easy_p05(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                continue
            if 0<c<w-1 and g[r][c-1]!=0 and g[r][c-1]==g[r][c+1]:
                out[r][c]=g[r][c-1]
            if 0<r<h-1 and g[r-1][c]!=0 and g[r-1][c]==g[r+1][c]:
                out[r][c]=g[r-1][c]
    return out


def solve_easy_p06(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1; continue
            color=g[r][c]
            c2=c
            while c2<w and g[r][c2]==color:
                c2+=1
            length=c2-c
            mid=c + length//2
            out[r][mid]=color
            c=c2
    return out


def solve_easy_p07(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[c][r]=g[r][c]
    return out


def solve_medium_p01(g):
    h,w=dims(g)
    sel=g[0][0]
    code=g[0][w-1]
    cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==sel and not (r==0 and c in (0,w-1))]
    if not cells:
        return [[0]]
    obj,_=crop_component(g,cells)
    return apply_transform_code(obj, code)


def solve_medium_p02(g):
    comps=comp_same_color(g)
    comps.sort(key=lambda comp:(-len(comp['cells']), bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color']))
    heights=[len(comp['cells']) for comp in comps]
    H=max(heights) if heights else 1
    W=max(1, 2*len(comps)-1)
    out=blank(H,W)
    col=0
    for comp in comps:
        hgt=len(comp['cells']); color=comp['color']
        for r in range(H-hgt, H):
            out[r][col]=color
        col+=2
    return out


def solve_medium_p03(g):
    out=copy_grid(g)
    for fr in frame_components(g):
        r0,c0,r1,c1=fr['bbox']
        seeds=[g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0, fr['color'])]
        if len(seeds)==1:
            seed=seeds[0]
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=seed
    return out


def solve_medium_p04(g):
    out=copy_grid(g)
    by_color=defaultdict(list)
    for comp in comp_same_color(g):
        by_color[comp['color']].append(comp['cells'])
    for color, comps in by_color.items():
        if len(comps)==2:
            allcells=[cell for comp in comps for cell in comp]
            r0,c0,r1,c1=bbox(allcells)
            for r in range(r0,r1+1):
                for c in range(c0,c1+1):
                    out[r][c]=color
    return out


def solve_medium_p05(g):
    h,w=dims(g)
    marker=g[0][0]
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if (r,c)==(0,0):
                continue
            v=g[r][c]
            if v==0:
                continue
            out[r][c]=v
            if marker==1:
                out[r][w-1-c]=v
            elif marker==2:
                out[h-1-r][c]=v
    return out


def solve_medium_p06(g):
    h,w=dims(g)
    out=blank(h,w)
    for fr in frame_components(g):
        r0,c0,r1,c1=fr['bbox']
        seeds=[g[r][c] for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0, fr['color'])]
        if len(seeds)==1:
            cr=(r0+r1)//2; cc=(c0+c1)//2
            out[cr][cc]=seeds[0]
    return out


def solve_medium_p07(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in comp_same_color(g):
        color=comp['color']
        r0,c0,r1,c1=bbox(comp['cells'])
        cr=(r0+r1)//2
        cc=(c0+c1)//2
        for c in range(c0,c1+1):
            out[cr][c]=color
        for r in range(r0,r1+1):
            out[r][cc]=color
    return out


def solve_hard_p01(g):
    h,w=dims(g)
    out=copy_grid(g)
    sources=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] not in (0,SLASH,BACKSLASH,WALL)]
    if not sources:
        return out
    r,c,color=sources[0]
    if r==0: d=2
    elif r==h-1: d=0
    elif c==0: d=1
    else: d=3
    visited=set()
    while True:
        state=(r,c,d)
        if state in visited:
            break
        visited.add(state)
        dr,dc=DIRS[d]
        nr,nc=r+dr,c+dc
        if not (0<=nr<h and 0<=nc<w):
            break
        cell=g[nr][nc]
        if cell==WALL:
            break
        if cell==0:
            out[nr][nc]=color
            r,c=nr,nc
        elif cell in (SLASH,BACKSLASH):
            d=reflect(d,cell)
            r,c=nr,nc
        else:
            # treat other colored cells as pass-through and recolor? not used
            out[nr][nc]=cell
            r,c=nr,nc
    return out


def solve_hard_p02(g):
    h,w=dims(g)
    sel_color=g[0][0]
    code=g[0][w-1]
    target_frame_color=g[h-1][0]
    # selected object
    obj_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==sel_color and (r,c) not in [(0,0),(0,w-1),(h-1,0)]]
    if not obj_cells:
        return [[0]]
    obj,_=crop_component(g,obj_cells)
    obj=apply_transform_code(obj, code)
    # target frame
    target=None
    for fr in frame_components(g):
        if fr['color']==target_frame_color:
            target=fr
            break
    out=blank(h,w)
    if not target:
        return out
    r0,c0,r1,c1=target['bbox']
    for r,c in target['cells']:
        out[r][c]=target_frame_color
    ih,iw=r1-r0-1,c1-c0-1
    oh,ow=dims(obj)
    sr=r0+1+(ih-oh)//2
    sc=c0+1+(iw-ow)//2
    for r in range(oh):
        for c in range(ow):
            if obj[r][c]!=0:
                out[sr+r][sc+c]=obj[r][c]
    return out


def solve_hard_p03(g):
    comps=comp_same_color(g)
    comps.sort(key=lambda comp:(bbox(comp['cells'])[0], bbox(comp['cells'])[1], comp['color']))
    n=len(comps)
    out=blank(n,n)
    dilated=[dilate_once(comp['cells']) for comp in comps]
    for i,comp in enumerate(comps):
        out[i][i]=comp['color']
    for i in range(n):
        for j in range(i+1,n):
            if dilated[i] & dilated[j]:
                out[i][j]=out[j][i]=8
    return out


def solve_hard_p04(g):
    h,w=dims(g)
    # anchor colors 1,2,3,4. base object is color 6
    base_cells=[(r,c) for r in range(h) for c in range(w) if g[r][c]==6]
    obj,_=crop_component(g,base_cells)
    out=blank(h,w)
    anchors=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in (1,2,3,4)]
    code_to_shape={1:obj,2:rotate90(obj),3:rotate180(obj),4:rotate270(obj)}
    for r,c,code in anchors:
        stamp_centered(out, code_to_shape[code], r, c)
    return out


def solve_hard_p05(g):
    h,w=dims(g)
    out=copy_grid(g)
    seen_map=defaultdict(set)  # cell -> colors
    watchers=[(r,c,g[r][c]) for r in range(h) for c in range(w) if g[r][c] in (2,3,4)]
    for r,c,color in watchers:
        for dr,dc in DIR4:
            rr,cc=r+dr,c+dc
            while 0<=rr<h and 0<=cc<w and g[rr][cc]!=5:
                if g[rr][cc]==0:
                    seen_map[(rr,cc)].add(color)
                rr+=dr; cc+=dc
    for (r,c), colors in seen_map.items():
        if len(colors)==1:
            out[r][c]=next(iter(colors))
        elif len(colors)>=2:
            out[r][c]=8
    return out


def solve_hard_p06(g):
    h,w=dims(g)
    frames=frame_components(g)
    # objects are non-frame components, ignore frames themselves
    frame_cells={(r,c) for fr in frames for r,c in fr['cells']}
    comps=[comp for comp in comp_same_color(g) if not all(cell in frame_cells for cell in comp['cells'])]
    # But this still includes frame cells as comps; filter exact frame sets
    frame_sets=[set(fr['cells']) for fr in frames]
    comps=[comp for comp in comps if set(comp['cells']) not in frame_sets]
    out=blank(h,w)
    used=set()
    # preserve all frames
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=fr['color']
    # match by interior dims, allowing rotation
    for comp in comps:
        shape,_=crop_component(g, comp['cells'])
        sh,sw=dims(shape)
        choice=None
        rotshape=shape
        for idx,fr in enumerate(frames):
            if idx in used:
                continue
            r0,c0,r1,c1=fr['bbox']
            ih,iw=r1-r0-1,c1-c0-1
            if (sh,sw)==(ih,iw):
                choice=(idx,shape); break
            if (sw,sh)==(ih,iw):
                choice=(idx,rotate90(shape)); break
        if choice is None:
            continue
        idx,rotshape=choice
        used.add(idx)
        fr=frames[idx]
        r0,c0,r1,c1=fr['bbox']
        for r in range(len(rotshape)):
            for c in range(len(rotshape[0])):
                if rotshape[r][c]!=0:
                    out[r0+1+r][c0+1+c]=rotshape[r][c]
    return out


def solve_hard_p07(g):
    out=copy_grid(g)
    for r,c in bfs_path_with_checkpoints(g):
        if out[r][c]==0:
            out[r][c]=8
    return out


