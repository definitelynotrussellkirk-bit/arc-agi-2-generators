"""Reference solvers for the seventh 21-task ARC-style puzzle bank.

This batch leans into a different slice of the ARC space:
- axis-wise filters and parity constraints
- precedence and competitive painting
- object counting, symmetry, and nearest-control assignment
- extraction to charts and packed galleries
- transform scripts, frame assignment, pathfinding, and shape comparison

Highlighted helper primitives in this batch:
- priority_overlay(proposals, precedence): resolve conflicting paint proposals by an explicit precedence list.
- apply_script(shape, tokens): apply an ordered sequence of discrete transforms encoded by control tokens.
- pack_gallery(shapes, gap, align): pack cropped shapes into a fresh canvas with fixed black gaps.
- center_in_frame(shape, frame_cells): place a cropped shape centered inside a rectangular outline frame.
- normalize_pair(shape_a, shape_b): align two cropped shapes in a common top-left-normalized canvas.
- bfs_path(grid, start, goal, passable): find a shortest orthogonal path through allowed cells.
"""
from typing import List
from collections import Counter, defaultdict, deque

Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]

NEW_PRIMITIVES = {
    "priority_overlay": "Resolve conflicting paint proposals by an explicit precedence order instead of simple last-write-wins.",
    "apply_script": "Apply an ordered sequence of discrete shape transforms encoded by control tokens.",
    "pack_gallery": "Pack cropped shapes into a fresh canvas with fixed black gaps and a chosen vertical alignment.",
    "center_in_frame": "Compute the top-left placement that centers a cropped shape inside a rectangular outline frame.",
    "normalize_pair": "Crop two shapes, align their top-left corners inside a common canvas, and compare them cellwise.",
    "bfs_path": "Find a shortest orthogonal path through allowed cells.",
}

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def copy_grid(g): return [row[:] for row in g]


def dims(g): return len(g), len(g[0])


def inb(g,r,c):
    h,w=dims(g); return 0<=r<h and 0<=c<w


def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop_cells(g,cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells: return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def crop_nonzero(g): return crop_cells(g)


def paste(out, shape, top, left, transparent=True):
    h,w=dims(out); sh,sw=dims(shape)
    for r in range(sh):
        for c in range(sw):
            v=shape[r][c]
            if transparent and v==0: continue
            rr,cc=top+r,left+c
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=v
    return out


def recolor_shape(shape, color):
    return [[color if v!=0 else 0 for v in row] for row in shape]


def cells_of(g, color=None, exclude=None):
    ex=set(exclude or [])
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row)
            if v!=0 and (color is None or v==color) and v not in ex]


def components(g, exclude=None, colors_separate=True):
    ex=set(exclude or [])
    h,w=dims(g)
    seen=set()
    comps=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or v in ex or (r,c) in seen: 
                continue
            q=[(r,c)]
            seen.add((r,c))
            comp=[]
            while q:
                cr,cc=q.pop()
                comp.append((cr,cc))
                for dr,dc in DIR4:
                    nr,nc=cr+dr,cc+dc
                    if inb(g,nr,nc) and (nr,nc) not in seen and g[nr][nc]!=0 and g[nr][nc] not in ex and ((not colors_separate) or g[nr][nc]==v):
                        seen.add((nr,nc)); q.append((nr,nc))
            comps.append({'color':v,'cells':set(comp)})
    return comps


def rotate_cw(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate180(g): return rotate_cw(rotate_cw(g))


def rotate_ccw(g): return rotate_cw(rotate180(g))


def flip_h(g): # mirror left-right
    return [list(reversed(row)) for row in g]


def flip_v(g):
    return list(reversed([row[:] for row in g]))


def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]


def object_shape(comp):
    cells=comp['cells']
    r0,c0,r1,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1)
    for r,c in cells: out[r-r0][c-c0]=comp['color']
    return out,(r0,c0,r1,c1)


def shape_binary(shape): return tuple(tuple(1 if v!=0 else 0 for v in row) for row in shape)


def shape_equal_under_180(shape):
    return shape_binary(shape)==shape_binary(rotate180(shape))


def center_of_bbox(comp):
    r0,c0,r1,c1=bbox(comp['cells'])
    return ((r0+r1)/2.0, (c0+c1)/2.0)


def manhattan(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])


def normalize_binary(shape):
    # crop nonzero and make binary
    cells=[(r,c) for r,row in enumerate(shape) for c,v in enumerate(row) if v!=0]
    if not cells: return ((0,),)
    r0,c0,r1,c1=bbox(cells)
    return tuple(tuple(1 if shape[r][c]!=0 else 0 for c in range(c0,c1+1)) for r in range(r0,r1+1))


def pack_horiz(shapes:List[Grid], gap=1, align='bottom')->Grid:
    hs=[dims(s)[0] for s in shapes]
    ws=[dims(s)[1] for s in shapes]
    H=max(hs) if hs else 1
    W=sum(ws)+gap*(len(shapes)-1 if shapes else 0)
    out=blank(H,W)
    cur=0
    for s in shapes:
        sh,sw=dims(s)
        top=0 if align=='top' else (H-sh if align=='bottom' else (H-sh)//2)
        paste(out,s,top,cur,transparent=True)
        cur += sw + gap
    return out


def priority_overlay(h,w, proposals, precedence):
    # proposals list of (r,c,color)
    rank={color:i for i,color in enumerate(precedence)}
    out=blank(h,w)
    bucket={}
    for r,c,color in proposals:
        if not (0<=r<h and 0<=c<w): 
            continue
        cur=bucket.get((r,c))
        if cur is None or rank[color] > rank[cur]:
            bucket[(r,c)] = color
    for (r,c),color in bucket.items():
        out[r][c]=color
    return out


def apply_transform(shape,key):
    if key==1: return rotate_cw(shape)
    if key==2: return rotate180(shape)
    if key==3: return flip_h(shape)
    if key==4: return transpose(shape)
    return [row[:] for row in shape]


def apply_script(shape, tokens):
    out=[row[:] for row in shape]
    for t in tokens:
        out=apply_transform(out,t)
    return out


def shortest_path(g, start, goal, passable={0}):
    h,w=dims(g)
    q=deque([start])
    prev={start: None}
    allowed=set(passable)|{g[start[0]][start[1]], g[goal[0]][goal[1]]}
    while q:
        r,c=q.popleft()
        if (r,c)==goal: break
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and (nr,nc) not in prev and g[nr][nc] in allowed:
                prev[(nr,nc)] = (r,c)
                q.append((nr,nc))
    if goal not in prev:
        return None
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur); cur=prev[cur]
    return path[::-1]


def pack_gallery(shapes, gap=1, align='center'):
    return pack_horiz(shapes, gap=gap, align=align)


def center_in_frame(shape, frame_cells):
    r0,c0,r1,c1=bbox(frame_cells)
    ih,iw=r1-r0-1,c1-c0-1
    sh,sw=dims(shape)
    top=r0+1 + (ih-sh)//2
    left=c0+1 + (iw-sw)//2
    return top,left


def normalize_pair(shape_a, shape_b):
    a=normalize_binary(shape_a)
    b=normalize_binary(shape_b)
    H=max(len(a),len(b)); W=max(len(a[0]), len(b[0]))
    A=[[1 if r<len(a) and c<len(a[0]) and a[r][c] else 0 for c in range(W)] for r in range(H)]
    B=[[1 if r<len(b) and c<len(b[0]) and b[r][c] else 0 for c in range(W)] for r in range(H)]
    return A,B


def bfs_path(g,start,goal,passable={0}):
    return shortest_path(g,start,goal,passable=passable)


def is_rect_frame(comp):
    cells=comp['cells']
    r0,c0,r1,c1=bbox(cells)
    if r1-r0<2 or c1-c0<2: return False
    border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1)
            if r in (r0,r1) or c in (c0,c1)}
    return cells==border


def solve_g_g01_topmost_per_column(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        for r in range(h):
            if g[r][c]!=0:
                out[r][c]=g[r][c]
                break
    return out


def solve_g_g02_recolor_by_size(g):
    out=blank(*dims(g))
    color_map={1:2,2:4,3:6}
    for comp in components(g):
        sz=len(comp['cells'])
        col=color_map.get(sz,8)
        for r,c in comp['cells']:
            out[r][c]=col
    return out


def solve_g_g03_row_majority_wins(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        nz=[v for v in row if v!=0]
        if not nz:
            continue
        cnt=Counter(nz)
        major=cnt.most_common(1)[0][0]
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=major
    return out


def solve_g_g04_anchor_parity_filter(g):
    h,w=dims(g)
    anchor=None
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                anchor=(r,c)
                break
        if anchor: break
    assert anchor is not None
    p=(anchor[0]+anchor[1])%2
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (r+c)%2==p:
                out[r][c]=g[r][c]
    return out


def solve_g_g05_block_to_main_diagonal(g):
    h,w=dims(g)
    out=blank(h,w)
    used=set()
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r][c+1],g[r+1][c],g[r+1][c+1]]
            if vals[0]!=0 and len(set(vals))==1:
                out[r][c]=vals[0]
                out[r+1][c+1]=vals[0]
                used.update({(r,c),(r,c+1),(r+1,c),(r+1,c+1)})
    # preserve any other nonzero cells not part of a block? probably none, but keep unchanged
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (r,c) not in used:
                out[r][c]=g[r][c]
    return out


def solve_g_g06_shift_object_toward_marker(g):
    h,w=dims(g)
    marker=None
    out=blank(h,w)
    obj_cells=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==9:
                marker=(r,c)
            elif g[r][c]!=0:
                obj_cells.append((r,c,g[r][c]))
    assert marker is not None
    if marker[0]==0: dr,dc=-1,0
    elif marker[0]==h-1: dr,dc=1,0
    elif marker[1]==0: dr,dc=0,-1
    else: dr,dc=0,1
    for r,c,v in obj_cells:
        nr,nc=r+dr,c+dc
        out[nr][nc]=v
    return out


def solve_g_g07_horizontal3_to_vertical3(g):
    h,w=dims(g)
    out=blank(h,w)
    used=set()
    for r in range(h):
        for c in range(w-2):
            v=g[r][c]
            if v!=0 and g[r][c+1]==v and g[r][c+2]==v:
                if 0<r<h-1:
                    out[r-1][c+1]=v
                    out[r][c+1]=v
                    out[r+1][c+1]=v
                    used.update({(r,c),(r,c+1),(r,c+2)})
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 and (r,c) not in used:
                out[r][c]=g[r][c]
    return out


def solve_g_g08_border_rays_precedence(g):
    h,w=dims(g)
    blockers={(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5}
    emitters=[]
    for c in range(w):
        if g[0][c] not in (0,5): emitters.append((0,c,g[0][c],'down'))
        if g[h-1][c] not in (0,5): emitters.append((h-1,c,g[h-1][c],'up'))
    for r in range(1,h-1):
        if g[r][0] not in (0,5): emitters.append((r,0,g[r][0],'right'))
        if g[r][w-1] not in (0,5): emitters.append((r,w-1,g[r][w-1],'left'))
    out=blank(h,w)
    # keep blockers and emitters
    for r,c in blockers: out[r][c]=5
    proposals=[]
    for r,c,color,dirn in emitters:
        out[r][c]=color
        dr,dc={'down':(1,0),'up':(-1,0),'right':(0,1),'left':(0,-1)}[dirn]
        nr,nc=r+dr,c+dc
        while 0<=nr<h and 0<=nc<w and g[nr][nc]!=5:
            proposals.append((nr,nc,color))
            nr+=dr; nc+=dc
    over=priority_overlay(h,w,proposals,precedence=[1,2,3,4,6,7,8,9])
    for r in range(h):
        for c in range(w):
            if over[r][c]!=0 and out[r][c]==0:
                out[r][c]=over[r][c]
    return out


def solve_g_g09_recolor_by_nearest_corner(g):
    h,w=dims(g)
    corners={(0,0):g[0][0], (0,w-1):g[0][w-1], (h-1,0):g[h-1][0], (h-1,w-1):g[h-1][w-1]}
    out=blank(h,w)
    for (r,c),v in corners.items():
        out[r][c]=v
    corner_positions=list(corners.keys())
    for comp in components(g, exclude=[]):
        # exclude corner markers as singleton objects if at corners
        if all((r,c) in corners for r,c in comp['cells']) and len(comp['cells'])==1:
            continue
        ctr=center_of_bbox(comp)
        best=min(corner_positions, key=lambda p: manhattan(ctr,p))
        color=corners[best]
        for r,c in comp['cells']:
            out[r][c]=color
    return out


def solve_g_g10_keep_180_symmetric_object(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        shape,_=object_shape(comp)
        if shape_equal_under_180(shape):
            for r,c in comp['cells']:
                out[r][c]=comp['color']
    return out


def solve_g_g11_bar_chart_sizes(g):
    comps=sorted(components(g), key=lambda comp: (bbox(comp['cells'])[1], bbox(comp['cells'])[0]))
    sizes=[len(comp['cells']) for comp in comps]
    colors=[comp['color'] for comp in comps]
    H=max(sizes) if sizes else 1
    W=max(1, 2*len(comps)-1)
    out=blank(H,W)
    for i,(sz,col) in enumerate(zip(sizes,colors)):
        c=2*i
        for r in range(H-sz,H):
            out[r][c]=col
    return out


def solve_g_g12_transform_by_key(g):
    # one key cell in top row, object elsewhere
    h,w=dims(g)
    key=None
    for c,v in enumerate(g[0]):
        if v in (1,2,3,4):
            key=v; key_pos=(0,c); break
    if key is None:
        for r in range(h):
            for c,v in enumerate(g[r]):
                if v in (1,2,3,4):
                    key=v; key_pos=(r,c); break
            if key is not None: break
    assert key is not None
    temp=copy_grid(g); temp[key_pos[0]][key_pos[1]]=0
    shape=crop_nonzero(temp)
    return apply_transform(shape,key)


def solve_g_g13_checkerfill_bboxes(g):
    h,w=dims(g)
    out=blank(h,w)
    for comp in components(g):
        r0,c0,r1,c1=bbox(comp['cells'])
        col=comp['color']
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if (r-r0 + c-c0)%2==0:
                    out[r][c]=col
    return out


def solve_g_g14_pack_objects_row(g):
    comps=sorted(components(g), key=lambda comp: (bbox(comp['cells'])[1], bbox(comp['cells'])[0]))
    shapes=[object_shape(comp)[0] for comp in comps]
    return pack_gallery(shapes, gap=1, align='center')


def solve_g_g15_assign_objects_to_frames(g):
    h,w=dims(g)
    comps=components(g)
    frames=[comp for comp in comps if is_rect_frame(comp)]
    objs=[comp for comp in comps if not is_rect_frame(comp)]
    frames=sorted(frames, key=lambda comp: ((bbox(comp['cells'])[2]-bbox(comp['cells'])[0]-1)*(bbox(comp['cells'])[3]-bbox(comp['cells'])[1]-1), bbox(comp['cells'])[1]))
    objs=sorted(objs, key=lambda comp: (len(comp['cells']), bbox(comp['cells'])[1]))
    out=blank(h,w)
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=fr['color']
    for obj,fr in zip(objs,frames):
        shape,_=object_shape(obj)
        top,left=center_in_frame(shape, fr['cells'])
        paste(out, shape, top, left, transparent=True)
    return out


def solve_g_g16_scripted_transform(g):
    h,w=dims(g)
    # top row tokens 1-4; object below
    tokens=[v for v in g[0] if v in (1,2,3,4)]
    temp=[row[:] for row in g[1:]]
    shape=crop_nonzero(temp)
    return apply_script(shape, tokens)


def solve_g_g17_precedence_rays_with_legend(g):
    # row0 from col1.. has precedence legend sequence unique colors; row1+ field with border emitters and blockers
    legend=[v for v in g[0] if v!=0]
    field=[row[:] for row in g[1:]]
    h,w=dims(field)
    blockers={(r,c) for r,row in enumerate(field) for c,v in enumerate(row) if v==5}
    emitters=[]
    for c in range(w):
        if field[0][c] not in (0,5): emitters.append((0,c,field[0][c],'down'))
        if field[h-1][c] not in (0,5): emitters.append((h-1,c,field[h-1][c],'up'))
    for r in range(1,h-1):
        if field[r][0] not in (0,5): emitters.append((r,0,field[r][0],'right'))
        if field[r][w-1] not in (0,5): emitters.append((r,w-1,field[r][w-1],'left'))
    out=blank(h,w)
    for r,c in blockers: out[r][c]=5
    proposals=[]
    for r,c,color,dirn in emitters:
        out[r][c]=color
        dr,dc={'down':(1,0),'up':(-1,0),'right':(0,1),'left':(0,-1)}[dirn]
        nr,nc=r+dr,c+dc
        while 0<=nr<h and 0<=nc<w and field[nr][nc]!=5:
            proposals.append((nr,nc,color))
            nr+=dr; nc+=dc
    over=priority_overlay(h,w,proposals,precedence=legend)
    for r in range(h):
        for c in range(w):
            if over[r][c]!=0 and out[r][c]==0:
                out[r][c]=over[r][c]
    return out


def solve_g_g18_shortest_path(g):
    h,w=dims(g)
    pos_by_color=defaultdict(list)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v not in (0,5):
                pos_by_color[v].append((r,c))
    color,pts=min(((col,pts) for col,pts in pos_by_color.items() if len(pts)==2), key=lambda x:x[0])
    path=bfs_path(g, pts[0], pts[1], passable={0,color})
    out=blank(h,w)
    for r,c in path:
        out[r][c]=color
    return out


def solve_g_g19_normalized_xor(g):
    comps=sorted(components(g), key=lambda comp: bbox(comp['cells'])[1])
    assert len(comps)>=2
    s1,_=object_shape(comps[0]); s2,_=object_shape(comps[1])
    A,B=normalize_pair(s1,s2)
    H,W=len(A),len(A[0])
    out=blank(H,W)
    for r in range(H):
        for c in range(W):
            if (A[r][c] and not B[r][c]) or (B[r][c] and not A[r][c]):
                out[r][c]=8
    return out


def solve_g_g20_controlled_gallery(g):
    h,w=dims(g)
    token_positions=[(c,v) for c,v in enumerate(g[h-1]) if v in (1,2,3,4)]
    field=[row[:] for row in g[:-1]]
    comps=components(field)
    assigned=[]
    for comp in sorted(comps, key=lambda comp:bbox(comp['cells'])[1]):
        ctr=center_of_bbox(comp)
        ctoken=min(token_positions, key=lambda cv: abs(ctr[1]-cv[0]))
        shape,_=object_shape(comp)
        assigned.append(apply_transform(shape, ctoken[1]))
    return pack_gallery(assigned, gap=1, align='center')


def solve_g_g21_corner_mosaic(g):
    h,w=dims(g)
    corner_keys={(0,0):g[0][0], (0,w-1):g[0][w-1], (h-1,0):g[h-1][0], (h-1,w-1):g[h-1][w-1]}
    temp=copy_grid(g)
    for r,c in corner_keys:
        temp[r][c]=0
    shape=crop_nonzero(temp)
    tl=apply_transform(shape, corner_keys[(0,0)])
    tr=apply_transform(shape, corner_keys[(0,w-1)])
    bl=apply_transform(shape, corner_keys[(h-1,0)])
    br=apply_transform(shape, corner_keys[(h-1,w-1)])
    top=pack_gallery([tl,tr], gap=1, align='top')
    bot=pack_gallery([bl,br], gap=1, align='top')
    W=max(dims(top)[1],dims(bot)[1])
    top2=blank(dims(top)[0],W); paste(top2, top, 0, 0)
    bot2=blank(dims(bot)[0],W); paste(bot2, bot, 0, 0)
    out=top2 + [ [0]*W ] + bot2
    return out


TASK_FUNCTIONS = {
    "easy_g01": solve_g_g01_topmost_per_column,
    "easy_g02": solve_g_g02_recolor_by_size,
    "easy_g03": solve_g_g03_row_majority_wins,
    "easy_g04": solve_g_g04_anchor_parity_filter,
    "easy_g05": solve_g_g05_block_to_main_diagonal,
    "easy_g06": solve_g_g06_shift_object_toward_marker,
    "easy_g07": solve_g_g07_horizontal3_to_vertical3,
    "medium_g08": solve_g_g08_border_rays_precedence,
    "medium_g09": solve_g_g09_recolor_by_nearest_corner,
    "medium_g10": solve_g_g10_keep_180_symmetric_object,
    "medium_g11": solve_g_g11_bar_chart_sizes,
    "medium_g12": solve_g_g12_transform_by_key,
    "medium_g13": solve_g_g13_checkerfill_bboxes,
    "medium_g14": solve_g_g14_pack_objects_row,
    "hard_g15": solve_g_g15_assign_objects_to_frames,
    "hard_g16": solve_g_g16_scripted_transform,
    "hard_g17": solve_g_g17_precedence_rays_with_legend,
    "hard_g18": solve_g_g18_shortest_path,
    "hard_g19": solve_g_g19_normalized_xor,
    "hard_g20": solve_g_g20_controlled_gallery,
    "hard_g21": solve_g_g21_corner_mosaic,
}


def validate_examples(task_bank):
    for task in task_bank:
        fn = TASK_FUNCTIONS[task["id"]]
        for pair in task["train"] + task["test"]:
            expected = pair["output"]
            got = fn(pair["input"])
            if got != expected:
                raise AssertionError(f"{task['id']} failed validation")
    return True
