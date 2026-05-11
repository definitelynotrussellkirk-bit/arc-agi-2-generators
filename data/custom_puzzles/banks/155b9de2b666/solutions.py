"""Reference solvers for the twentieth 21-task ARC-style puzzle bank.

This batch emphasizes anti-diagonal symmetry, local completion, beams, object orientation,
bounding abstractions, keyed extraction, room flooding, scaling, keyed insertion,
portal pathfinding, topological matching, Boolean composition, ordered waypoint routing,
scripted galleries, and dihedral stamping.
"""



from typing import List, Dict, Tuple

from collections import deque, defaultdict





Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

DIR8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]





NEW_PRIMITIVES = {
    "column_span_fill": "Fill an inclusive column segment between matching same-color endpoints when the interior is empty.",
    "anti_diagonal_union": "Copy every nonzero cell across the anti-diagonal and keep the originals.",
    "seed_plus": "Expand each isolated seed into a radius-1 plus of the same color.",
    "missing_corner_fill2": "Complete a 2x2 block that has three cells of one nonzero color and one empty corner.",
    "inward_border_beam": "Fire a straight beam inward from each border seed until a wall or the grid edge.",
    "domino_square_grow": "Expand a same-color domino into a filled 2x2 square in the only open orthogonal direction.",
    "aligned_midpoint_fill": "Fill the midpoint between aligned same-color endpoints separated by one empty cell.",
    "orientation_recolor": "Recolor each connected object by whether its bounding box is horizontal, vertical, or square.",
    "bbox_outline": "Replace each object by the outline of its tight axis-aligned bounding box.",
    "corner_key_extract": "Use the top-left color key to select one object color and crop that object.",
    "axis_key_reflect": "Use a marker key to choose horizontal versus vertical reflection of the cropped object.",
    "room_fill": "Flood each wall-enclosed room with the room's single seed color.",
    "size_sorted_strip": "Extract object crops and concatenate them in ascending area order.",
    "marker_count_scale": "Scale an object by the number of marker cells in a control row.",
    "keyed_frame_insert": "Select an object by color key, transform it by a second key, and center it inside a frame.",
    "key_door_portal_bfs": "Run shortest-path search with inventory state, locked doors, and paired teleport portals.",
    "holecount_frame_assign": "Match template objects to frames by topological hole count and recolor them to the frame.",
    "boolean_transform_compose": "Transform one normalized shape, align it with another, and apply a keyed Boolean operation.",
    "ordered_waypoint_path": "Find a shortest path that visits checkpoints in increasing order before reaching the goal.",
    "scripted_gallery": "Apply a sequence of transforms cumulatively and emit the intermediate states as a gallery.",
    "dihedral_anchor_stamp": "Stamp transformed copies of a template at anchor positions using dihedral transform keys."
}



def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]


def deepcopy_grid(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0]) if g else 0


def inb(g,r,c):
    h,w=dims(g); return 0<=r<h and 0<=c<w


def place_cells(g, cells, color):
    for r,c in cells:
        if inb(g,r,c):
            g[r][c]=color
    return g


def draw_rect_outline(g, r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color
    return g


def draw_rect_fill(g, r0,c0,r1,c1,color):
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            g[r][c]=color
    return g


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


def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]


def components(g,bg=0,diag=False):
    h,w=dims(g); dirs=DIR8 if diag else DIR4
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=bg and not seen[r][c]:
                color=g[r][c]
                q=[(r,c)]; seen[r][c]=True; cells=[]
                while q:
                    rr,cc=q.pop()
                    cells.append((rr,cc))
                    for dr,dc in dirs:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==color:
                            seen[nr][nc]=True; q.append((nr,nc))
                r0,r1,c0,c1=bbox_of_cells(cells)
                crop=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
                for rr,cc in cells:
                    crop[rr-r0][cc-c0]=color
                comps.append({"color":color,"cells":cells,"bbox":(r0,r1,c0,c1),"crop":crop,"area":len(cells),"height":r1-r0+1,"width":c1-c0+1})
    return comps


def connected_regions(g, passable):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    regs=[]
    for r in range(h):
        for c in range(w):
            if passable(r,c) and not seen[r][c]:
                q=deque([(r,c)]); seen[r][c]=True; cells=[]
                while q:
                    rr,cc=q.popleft(); cells.append((rr,cc))
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and passable(nr,nc):
                            seen[nr][nc]=True; q.append((nr,nc))
                regs.append(cells)
    return regs


def hole_count_for_component(comp_crop):
    # comp_crop values nonzero/0
    h,w=dims(comp_crop)
    # pad with zero border and count zero regions not touching outside
    H,W=h+2,w+2
    pad=blank(H,W,0)
    for r in range(h):
        for c in range(w):
            pad[r+1][c+1]=1 if comp_crop[r][c]!=0 else 0
    seen=[[False]*W for _ in range(H)]
    holes=0
    for r in range(H):
        for c in range(W):
            if pad[r][c]==0 and not seen[r][c]:
                q=deque([(r,c)]); seen[r][c]=True; cells=[]; touches=False
                while q:
                    rr,cc=q.popleft(); cells.append((rr,cc))
                    if rr in (0,H-1) or cc in (0,W-1): touches=True
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<H and 0<=nc<W and pad[nr][nc]==0 and not seen[nr][nc]:
                            seen[nr][nc]=True; q.append((nr,nc))
                if not touches:
                    holes+=1
    return holes


def scale_up(g,k):
    h,w=dims(g)
    out=blank(h*k,w*k,0)
    for r in range(h):
        for c in range(w):
            for rr in range(r*k,(r+1)*k):
                for cc in range(c*k,(c+1)*k):
                    out[rr][cc]=g[r][c]
    return out


def paste(g, obj, top, left, transparent=0):
    h,w=dims(g); oh,ow=dims(obj)
    out=deepcopy_grid(g)
    for r in range(oh):
        for c in range(ow):
            if obj[r][c]!=transparent:
                rr,cc=top+r,left+c
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc]=obj[r][c]
    return out


def center_paste_into_bbox(base, obj, bbox):
    r0,r1,c0,c1=bbox
    H=r1-r0+1; W=c1-c0+1
    oh,ow=dims(obj)
    top=r0+(H-oh)//2; left=c0+(W-ow)//2
    return paste(base,obj,top,left,transparent=0)


def normalize_binary_crop(crop):
    return [[1 if v!=0 else 0 for v in row] for row in crop_bbox(crop,0)]


def transform_by_code(g, code):
    if code==1:  # rot90 in h01
        return rotate90(g)
    if code==2:
        return rotate180(g)
    if code==3:
        return flip_h(g)
    if code==4:
        return g
    return g


def is_rectangle_frame(comp, color):
    r0,r1,c0,c1=comp["bbox"]
    hh=r1-r0+1; ww=c1-c0+1
    if hh<3 or ww<3:
        return False
    # every cell on bbox border in crop equals color and interior zeros
    crop=comp["crop"]
    ch,cw=dims(crop)
    # comp crop only has component cells, zeros elsewhere
    for r in range(ch):
        for c in range(cw):
            border = r in (0,ch-1) or c in (0,cw-1)
            if border:
                if crop[r][c]!=color: return False
            else:
                if crop[r][c]!=0: return False
    return True


def transform_second_shape(shape, code):
    if code==6:
        return shape
    if code==7:
        return flip_h(shape)
    if code==8:
        return rotate90(shape)
    return shape


def bfs_path(g, start, goal):
    h,w=dims(g)
    dq=deque([start])
    parent={start:None}
    while dq:
        r,c=dq.popleft()
        if (r,c)==goal: break
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w and g[nr][nc]!=8 and (nr,nc) not in parent:
                parent[(nr,nc)]=(r,c)
                dq.append((nr,nc))
    assert goal in parent
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur); cur=parent[cur]
    return path[::-1]


def apply_script_step(obj, code):
    if code==1:
        return obj
    if code==2:
        return rotate90(obj)
    if code==3:
        return flip_h(obj)
    if code==4:
        return rotate180(obj)
    return obj


def dihedral_transform_template(tpl, code):
    if code==1: return tpl
    if code==2: return rotate90(tpl)
    if code==3: return rotate180(tpl)
    if code==4: return rotate270(tpl)
    if code==5: return flip_h(tpl)
    return tpl


def solve_easy_p01(g:Grid)->Grid:  # column span fill
    h,w=dims(g)
    out=deepcopy_grid(g)
    for c in range(w):
        # group occurrences by color
        pos=defaultdict(list)
        for r in range(h):
            if g[r][c]!=0:
                pos[g[r][c]].append(r)
        for color, rows in pos.items():
            if len(rows)==2:
                r0,r1=rows
                if all(g[r][c]==0 for r in range(r0+1,r1)):
                    for r in range(r0,r1+1):
                        out[r][c]=color
    return out


def solve_easy_p02(g:Grid)->Grid:  # anti-diagonal union
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


def solve_easy_p03(g:Grid)->Grid:  # seed plus
    h,w=dims(g)
    out=blank(h,w,0)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                color=g[r][c]
                for dr,dc in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=color
    return out


def solve_easy_p04(g:Grid)->Grid:  # missing corner fill in 2x2 from original snapshot
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r+1][c],g[r][c+1],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1 and vals.count(0)==1:
                color=nz[0]
                idx=vals.index(0)
                if idx==0: out[r][c]=color
                elif idx==1: out[r+1][c]=color
                elif idx==2: out[r][c+1]=color
                else: out[r+1][c+1]=color
    return out


def solve_easy_p05(g:Grid)->Grid:  # inward border beam until wall 8 or edge
    h,w=dims(g)
    out=deepcopy_grid(g)
    seeds=[]
    for c in range(w):
        if g[0][c] not in (0,8): seeds.append((0,c,1,0,g[0][c]))
        if g[h-1][c] not in (0,8): seeds.append((h-1,c,-1,0,g[h-1][c]))
    for r in range(1,h-1):
        if g[r][0] not in (0,8): seeds.append((r,0,0,1,g[r][0]))
        if g[r][w-1] not in (0,8): seeds.append((r,w-1,0,-1,g[r][w-1]))
    for r,c,dr,dc,color in seeds:
        rr,cc=r+dr,c+dc
        while 0<=rr<h and 0<=cc<w and g[rr][cc]!=8:
            if out[rr][cc]==0:
                out[rr][cc]=color
            rr+=dr; cc+=dc
    return out


def solve_easy_p06(g:Grid)->Grid:  # domino to square
    h,w=dims(g)
    out=deepcopy_grid(g)
    # horizontal dominoes
    for r in range(h-1):
        for c in range(w-1):
            color=g[r][c]
            if color!=0 and g[r][c+1]==color and (c==0 or g[r][c-1]!=color) and (c+2>=w or g[r][c+2]!=color):
                # only if below cells empty and original not already 2x2
                if g[r+1][c]==0 and g[r+1][c+1]==0:
                    out[r+1][c]=color; out[r+1][c+1]=color
    # vertical dominoes
    for r in range(h-1):
        for c in range(w-1):
            color=g[r][c]
            if color!=0 and g[r+1][c]==color and (r==0 or g[r-1][c]!=color) and (r+2>=h or g[r+2][c]!=color):
                if g[r][c+1]==0 and g[r+1][c+1]==0:
                    out[r][c+1]=color; out[r+1][c+1]=color
    return out


def solve_easy_p07(g:Grid)->Grid:  # aligned midpoint fill distance 2
    h,w=dims(g)
    out=deepcopy_grid(g)
    for r in range(h):
        for c in range(w-2):
            color=g[r][c]
            if color!=0 and g[r][c+1]==0 and g[r][c+2]==color:
                out[r][c+1]=color
    for r in range(h-2):
        for c in range(w):
            color=g[r][c]
            if color!=0 and g[r+1][c]==0 and g[r+2][c]==color:
                out[r+1][c]=color
    return out


def solve_medium_p01(g:Grid)->Grid:  # orientation recolor
    h,w=dims(g)
    out=blank(h,w,0)
    for comp in components(g,0,diag=False):
        r0,r1,c0,c1=comp["bbox"]
        hh=r1-r0+1; ww=c1-c0+1
        if ww>hh: color=2
        elif hh>ww: color=3
        else: color=4
        for r,c in comp["cells"]:
            out[r][c]=color
    return out


def solve_medium_p02(g:Grid)->Grid:  # bbox outline same color
    h,w=dims(g)
    out=blank(h,w,0)
    for comp in components(g,0,diag=False):
        r0,r1,c0,c1=comp["bbox"]
        draw_rect_outline(out,r0,c0,r1,c1,comp["color"])
    return out


def solve_medium_p03(g:Grid)->Grid:  # corner key extract by color top-left
    key=g[0][0]
    h,w=dims(g)
    temp=deepcopy_grid(g)
    temp[0][0]=0
    # collect all cells of key color except marker
    cells=[(r,c) for r in range(h) for c in range(w) if temp[r][c]==key]
    if not cells:
        return [[0]]
    r0,r1,c0,c1=bbox_of_cells(cells)
    return [row[c0:c1+1] for row in temp[r0:r1+1]]


def solve_medium_p04(g:Grid)->Grid:  # axis key reflect, key at 0,0 (1 flip_h, 2 flip_v)
    key=g[0][0]
    temp=deepcopy_grid(g); temp[0][0]=0
    obj=crop_bbox(temp,0)
    if key==1:
        return flip_h(obj)
    elif key==2:
        return flip_v(obj)
    else:
        return obj


def solve_medium_p05(g:Grid)->Grid:  # room fill from doors, walls 8
    h,w=dims(g)
    out=deepcopy_grid(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=8 and not seen[r][c]:
                q=deque([(r,c)]); seen[r][c]=True; cells=[]; seeds=set()
                while q:
                    rr,cc=q.popleft(); cells.append((rr,cc))
                    if g[rr][cc] not in (0,8):
                        seeds.add(g[rr][cc])
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and g[nr][nc]!=8 and not seen[nr][nc]:
                            seen[nr][nc]=True; q.append((nr,nc))
                if len(seeds)==1:
                    color=next(iter(seeds))
                    for rr,cc in cells:
                        if g[rr][cc]==0:
                            out[rr][cc]=color
    return out


def solve_medium_p06(g:Grid)->Grid:  # size sorted strip top aligned, separator 0 col
    comps=components(g,0,diag=False)
    comps=sorted(comps, key=lambda c:(c["area"], c["height"], c["width"], c["color"]))
    crops=[]
    for comp in comps:
        r0,r1,c0,c1=comp["bbox"]
        crop=[row[c0:c1+1] for row in g[r0:r1+1]]
        crops.append(crop)
    H=max(len(c) for c in crops) if crops else 1
    W=sum(len(c[0]) for c in crops)+max(0,len(crops)-1)
    out=blank(H,W,0)
    cur=0
    for i,crop in enumerate(crops):
        ch,cw=dims(crop)
        for r in range(ch):
            for c in range(cw):
                out[r][cur+c]=crop[r][c]
        cur+=cw
        if i+1<len(crops):
            cur+=1
    return out


def solve_medium_p07(g:Grid)->Grid:  # marker count scale
    # count markers color 1 in top row
    k=sum(1 for v in g[0] if v==1)
    temp=deepcopy_grid(g)
    for c,v in enumerate(temp[0]):
        if v==1: temp[0][c]=0
    obj=crop_bbox(temp,0)
    return scale_up(obj,k)


def solve_hard_p01(g:Grid)->Grid:  # keyed frame insert
    h,w=dims(g)
    select_color=g[0][0]
    tcode=g[0][w-1]
    temp=deepcopy_grid(g)
    temp[0][0]=0; temp[0][w-1]=0
    # selected object crop
    cells=[(r,c) for r in range(h) for c in range(w) if temp[r][c]==select_color]
    if not cells:
        return blank(h,w,0)
    r0,r1,c0,c1=bbox_of_cells(cells)
    obj=[row[c0:c1+1] for row in temp[r0:r1+1]]
    obj=transform_by_code(obj,tcode)
    # frame bbox from all 8s
    fcells=[(r,c) for r in range(h) for c in range(w) if temp[r][c]==8]
    fr0,fr1,fc0,fc1=bbox_of_cells(fcells)
    out=blank(h,w,0)
    draw_rect_outline(out,fr0,fc0,fr1,fc1,8)
    out=center_paste_into_bbox(out,obj,(fr0+1,fr1-1,fc0+1,fc1-1))
    return out


def solve_hard_p02(g:Grid)->Grid:  # key-door-portal bfs
    h,w=dims(g)
    start=goal=key=None
    portals=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==2: start=(r,c)
            elif g[r][c]==3: goal=(r,c)
            elif g[r][c]==4: key=(r,c)
            elif g[r][c]==6: portals.append((r,c))
    portal_map={}
    if len(portals)==2:
        portal_map[portals[0]]=portals[1]
        portal_map[portals[1]]=portals[0]
    dq=deque([(start[0],start[1],False)])
    parent={(start[0],start[1],False): None}
    end_state=None
    while dq:
        r,c,has_key=dq.popleft()
        if (r,c)==goal:
            end_state=(r,c,has_key); break
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): continue
            cell=g[nr][nc]
            if cell==8: continue
            nkey=has_key or cell==4
            if cell==5 and not nkey:  # door requires key
                continue
            tr,tc=nr,nc
            if (nr,nc) in portal_map:
                tr,tc=portal_map[(nr,nc)]
                # landing cell keeps nkey as is
            st=(tr,tc,nkey)
            if st not in parent:
                parent[st]=(r,c,has_key)
                dq.append(st)
    assert end_state is not None
    path=[]
    cur=end_state
    while cur is not None:
        path.append(cur)
        cur=parent[cur]
    path=path[::-1]
    out=deepcopy_grid(g)
    specials={2,3,4,5,6,8}
    for r,c,has_key in path:
        if g[r][c]==0:
            out[r][c]=7
    return out


def solve_hard_p03(g:Grid)->Grid:  # holecount frame assign
    h,w=dims(g)
    comps=components(g,0,diag=False)
    frames=[]
    objs=[]
    for comp in comps:
        if comp["color"] in (2,3) and is_rectangle_frame(comp, comp["color"]):
            frames.append(comp)
        else:
            objs.append(comp)
    # map holecount to binary crop of object
    hole_to_obj={}
    for comp in objs:
        crop=[row[:] for row in comp["crop"]]
        holes=hole_count_for_component(crop)
        hole_to_obj[holes]=[[1 if v!=0 else 0 for v in row] for row in crop]
    out=blank(h,w,0)
    for frame in frames:
        color=frame["color"]
        r0,r1,c0,c1=frame["bbox"]
        draw_rect_outline(out,r0,c0,r1,c1,color)
        target_hole = 0 if color==2 else 1
        objmask=hole_to_obj[target_hole]
        obj=[[color if v else 0 for v in row] for row in objmask]
        out=center_paste_into_bbox(out,obj,(r0+1,r1-1,c0+1,c1-1))
    return out


def solve_hard_p04(g:Grid)->Grid:  # boolean with transform key
    h,w=dims(g)
    op=g[0][0]
    tcode=g[0][w-1]
    temp=deepcopy_grid(g); temp[0][0]=0; temp[0][w-1]=0
    cells4=[(r,c) for r in range(h) for c in range(w) if temp[r][c]==4]
    cells5=[(r,c) for r in range(h) for c in range(w) if temp[r][c]==5]
    def crop_cells(cells,color):
        r0,r1,c0,c1=bbox_of_cells(cells)
        arr=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
        for r,c in cells:
            arr[r-r0][c-c0]=1
        return arr
    a=crop_cells(cells4,4)
    b=crop_cells(cells5,5)
    b=transform_second_shape(b,tcode)
    H=max(len(a),len(b)); W=max(len(a[0]),len(b[0]))
    A=blank(H,W,0); B=blank(H,W,0)
    for r in range(len(a)):
        for c in range(len(a[0])):
            A[r][c]=a[r][c]
    for r in range(len(b)):
        for c in range(len(b[0])):
            B[r][c]=b[r][c]
    R=blank(H,W,0)
    for r in range(H):
        for c in range(W):
            va, vb = A[r][c], B[r][c]
            if op==1:
                vv = va or vb
            elif op==2:
                vv = va and vb
            else:
                vv = (va+vb)==1
            R[r][c]=9 if vv else 0
    return crop_bbox(R,0)


def solve_hard_p05(g:Grid)->Grid:  # ordered waypoint path 2->4->5->3 if present
    h,w=dims(g)
    pos={}
    for r in range(h):
        for c in range(w):
            if g[r][c] in (2,3,4,5,6,7):
                pos[g[r][c]]=(r,c)
    order=[2]
    for k in sorted(k for k in pos if k not in (2,3) and 4<=k<=7):
        order.append(k)
    order.append(3)
    out=deepcopy_grid(g)
    for a,b in zip(order, order[1:]):
        path=bfs_path(g,pos[a],pos[b])
        for r,c in path:
            if g[r][c]==0:
                out[r][c]=7
    return out


def solve_hard_p06(g:Grid)->Grid:  # scripted gallery cumulative
    script=[v for v in g[0] if v in (1,2,3,4)]
    temp=deepcopy_grid(g)
    for c,v in enumerate(temp[0]):
        if v in (1,2,3,4): temp[0][c]=0
    obj=crop_bbox(temp,0)
    states=[]
    cur=obj
    for code in script:
        cur=apply_script_step(cur,code)
        states.append(cur)
    H=max(len(s) for s in states) if states else 1
    W=sum(len(s[0]) for s in states)+max(0,len(states)-1)
    out=blank(H,W,0)
    x=0
    for i,s in enumerate(states):
        sh,sw=dims(s)
        for r in range(sh):
            for c in range(sw):
                out[r][x+c]=s[r][c]
        x+=sw
        if i+1<len(states): x+=1
    return out


def solve_hard_p07(g:Grid)->Grid:  # dihedral anchor stamp
    h,w=dims(g)
    # template uses colors >=6, anchors are 1..5
    temp=deepcopy_grid(g)
    anchors=[]
    for r in range(h):
        for c in range(w):
            if 1<=g[r][c]<=5:
                anchors.append((r,c,g[r][c]))
                temp[r][c]=0
    tpl=crop_bbox(temp,0)
    out=blank(h,w,0)
    for r,c,code in anchors:
        stamp=dihedral_transform_template(tpl,code)
        sh,sw=dims(stamp)
        for rr in range(sh):
            for cc in range(sw):
                if stamp[rr][cc]!=0:
                    tr,tc=r+rr,c+cc
                    if 0<=tr<h and 0<=tc<w:
                        out[tr][tc]=stamp[rr][cc]
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
    'hard_p07': solve_hard_p07
}
