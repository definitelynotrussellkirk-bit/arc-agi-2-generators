"""Reference solvers for the ninth 21-task ARC-style puzzle bank.

This batch leans into:
- run and segment logic
- marker-driven projection and keyed selection
- blocker-aware gravity and frame placement
- shortest paths, rigid pivot motion, and parity flood fills
- dihedral matching and keyed Boolean shape composition
"""
from typing import List
from collections import deque, Counter

Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {
    "run_endpoints": "Reduce each horizontal run to its first and last cell.",
    "column_paint_from_header": "Treat top-row markers as seeds that paint full columns.",
    "complete_monochrome_block": "Complete a 2x2 monochrome block when one corner is missing.",
    "bridge_if_clear": "Connect two matching endpoints only when the segment between them is empty.",
    "diagonal_consensus_fill": "Fill a center cell when its four diagonal neighbors agree.",
    "global_color_parity": "Filter colors by whether their total frequency is even or odd.",
    "half_mirror": "Mirror one half of the grid into the other half.",
    "corner_color_select": "Use a corner key color to choose which object to crop.",
    "color_area_rank": "Rank connected objects by area and map those ranks to new colors.",
    "corner_rectangle_fill": "Fill a rectangle once all four same-color corners are present.",
    "gravity_segments": "Apply gravity independently inside blocker-separated segments.",
    "frame_center": "Center a cropped object inside a frame interior.",
    "axis_mirror": "Reflect content across an explicit mirror axis.",
    "hole_fill": "Detect enclosed black holes and fill them with the surrounding object color.",
    "match_by_bbox_size": "Pair objects and containers by exact bounding-box size.",
    "frame_insert": "Move an insert object into its matching hollow frame.",
    "apply_script": "Map marker colors to geometric transforms.",
    "pack_gallery": "Pack several cropped shapes into one gallery with gaps.",
    "bfs_path": "Use breadth-first search to recover one shortest path through free cells.",
    "orbit_about_pivot": "Rotate an object rigidly around a designated pivot cell.",
    "parity_flood": "Color cells according to shortest-path or Manhattan-distance parity from a seed.",
    "match_under_dihedral": "Compare shapes up to rotation and reflection.",
    "dihedral_select": "Select the object whose normalized shape matches a template under dihedral symmetry.",
    "keyed_boolean": "Choose union, intersection, or xor from a key marker.",
    "shape_boolean": "Combine two aligned binary shapes with a Boolean set operation."
}


def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]



def copy_grid(g):
    return [row[:] for row in g]



def dims(g):
    return len(g), len(g[0])



def inb(g,r,c):
    h,w=dims(g)
    return 0<=r<h and 0<=c<w



def bbox(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs),min(cs),max(rs),max(cs)



def crop_cells(g,cells=None):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]



def crop_nonzero(g):
    return crop_cells(g)



def paste(out, shape, top, left, transparent=True):
    h,w=dims(out); sh,sw=dims(shape)
    for r in range(sh):
        for c in range(sw):
            v=shape[r][c]
            if transparent and v==0:
                continue
            rr,cc=top+r,left+c
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=v
    return out



def rotate90(shape):
    sh,sw=dims(shape)
    return [[shape[sh-1-r][c] for r in range(sh)] for c in range(sw)]



def rotate180(shape):
    return [row[::-1] for row in shape[::-1]]



def rotate270(shape):
    sh,sw=dims(shape)
    return [[shape[r][sw-1-c] for r in range(sh)] for c in range(sw)]



def hflip(shape):
    return [row[::-1] for row in shape]



def normalize_binary(shape):
    cells=[(r,c) for r,row in enumerate(shape) for c,v in enumerate(row) if v!=0]
    if not cells:
        return ((0,),)
    r0,c0,r1,c1=bbox(cells)
    sub=[row[c0:c1+1] for row in shape[r0:r1+1]]
    return tuple(tuple(1 if v!=0 else 0 for v in row) for row in sub)



def components_same_color(g):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or seen[r][c]:
                continue
            color=g[r][c]
            stack=[(r,c)]
            seen[r][c]=True
            cells=[]
            while stack:
                rr,cc=stack.pop()
                cells.append((rr,cc))
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if inb(g,nr,nc) and not seen[nr][nc] and g[nr][nc]==color:
                        seen[nr][nc]=True
                        stack.append((nr,nc))
            comps.append({"cells":cells,"color":color})
    return comps



def hole_mask(g, target_color=None):
    # return enclosed zero cells within overall nonzero walls or specific target color walls
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    from collections import deque
    q=deque()
    allow=lambda r,c: g[r][c]==0
    for r in range(h):
        for c in [0,w-1]:
            if allow(r,c) and not seen[r][c]:
                seen[r][c]=True;q.append((r,c))
    for c in range(w):
        for r in [0,h-1]:
            if allow(r,c) and not seen[r][c]:
                seen[r][c]=True;q.append((r,c))
    while q:
        r,c=q.popleft()
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if inb(g,nr,nc) and allow(nr,nc) and not seen[nr][nc]:
                seen[nr][nc]=True;q.append((nr,nc))
    holes=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 and not seen[r][c]:
                holes.append((r,c))
    return holes



def subgrid(g, r0,c0,r1,c1):
    return [row[c0:c1+1] for row in g[r0:r1+1]]



def find_color_cells(g, color):
    return [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==color]



def component_shape_from_cells(g,cells):
    r0,c0,r1,c1=bbox(cells)
    out=blank(r1-r0+1,c1-c0+1,0)
    for r,c in cells:
        out[r-r0][c-c0]=g[r][c]
    return out,(r0,c0)



def bbox_dims(cells):
    r0,c0,r1,c1=bbox(cells)
    return (r1-r0+1,c1-c0+1)



def center_position(frame_bbox, shape_dims):
    r0,c0,r1,c1=frame_bbox
    fh,fw=(r1-r0+1,c1-c0+1)
    sh,sw=shape_dims
    top=r0+(fh-sh)//2
    left=c0+(fw-sw)//2
    return top,left



def norm_variants(shape):
    vars=[]
    cur=shape
    for _ in range(4):
        vars.append(normalize_binary(cur))
        vars.append(normalize_binary(hflip(cur)))
        cur=rotate90(cur)
    # unique preserving order
    out=[]
    seen=set()
    for v in vars:
        if v not in seen:
            seen.add(v); out.append(v)
    return out



def shortest_path_with_walls(g, start, goal, walls={5}):
    h,w=dims(g)
    q=deque([start])
    prev={start:None}
    while q:
        cur=q.popleft()
        if cur==goal:
            break
        r,c=cur
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not inb(g,nr,nc):
                continue
            if (nr,nc) in prev:
                continue
            if (nr,nc)!=goal and g[nr][nc] in walls:
                continue
            # allow travel through zeros and endpoints only
            if (nr,nc)!=goal and g[nr][nc]!=0:
                continue
            prev[(nr,nc)]=cur
            q.append((nr,nc))
    if goal not in prev:
        return None
    path=[]
    cur=goal
    while cur is not None:
        path.append(cur)
        cur=prev[cur]
    return path[::-1]



def solve_i01_run_endpoints(g):
    h,w=dims(g)
    out=blank(h,w,0)
    for r in range(h):
        c=0
        while c<w:
            if g[r][c]==0:
                c+=1; continue
            color=g[r][c]
            j=c
            while j+1<w and g[r][j+1]==color:
                j+=1
            out[r][c]=color
            out[r][j]=color
            c=j+1
    return out



def solve_i02_top_row_columns(g):
    h,w=dims(g)
    out=blank(h,w,0)
    for c,v in enumerate(g[0]):
        if v!=0:
            for r in range(h):
                out[r][c]=v
    return out



def solve_i03_complete_l_to_square(g):
    out=copy_grid(g)
    h,w=dims(g)
    changes=[]
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r+1][c],g[r][c+1],g[r+1][c+1]]
            nz=[v for v in vals if v!=0]
            if len(nz)==3 and len(set(nz))==1:
                color=nz[0]
                positions=[(r,c),(r+1,c),(r,c+1),(r+1,c+1)]
                for (rr,cc),v in zip(positions,vals):
                    if v==0:
                        changes.append((rr,cc,color))
    for r,c,color in changes:
        out[r][c]=color
    return out



def solve_i04_vertical_bridge_clear(g):
    h,w=dims(g)
    out=copy_grid(g)
    colors=sorted({v for row in g for v in row if v!=0})
    for c in range(w):
        for color in colors:
            rows=[r for r in range(h) if g[r][c]==color]
            if len(rows)==2:
                r0,r1=rows
                if all(g[r][c]==0 for r in range(r0+1,r1)):
                    for r in range(r0,r1+1):
                        out[r][c]=color
    return out



def solve_i05_x_center_fill(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            if g[r][c]!=0:
                continue
            vals=[g[r-1][c-1],g[r-1][c+1],g[r+1][c-1],g[r+1][c+1]]
            if vals[0]!=0 and len(set(vals))==1:
                out[r][c]=vals[0]
    return out



def solve_i06_keep_even_frequency(g):
    from collections import Counter
    cnt=Counter(v for row in g for v in row if v!=0)
    keep={color for color,n in cnt.items() if n%2==0}
    return [[v if v in keep else 0 for v in row] for row in g]



def solve_i07_mirror_upper_to_lower(g):
    h,w=dims(g)
    assert h%2==0
    half=h//2
    out=copy_grid(g)
    for r in range(half,h):
        src=half-1-(r-half)
        out[r]=g[src][:]
    return out



def solve_i08_crop_corner_named_color(g):
    target=g[0][0]
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==target and not (r==0 and c==0)]
    return crop_cells(g,cells)



def solve_i09_recolor_by_area_rank(g):
    comps=components_same_color(g)
    # assume 3 objects distinct sizes
    ordered=sorted(comps,key=lambda comp:(len(comp["cells"]), bbox(comp["cells"])[0], bbox(comp["cells"])[1]))
    palette=[2,3,4,6,7,8,9]
    mapping={}
    for idx,comp in enumerate(ordered):
        mapping[id(comp)] = palette[idx]
    out=blank(*dims(g),0)
    for idx,comp in enumerate(ordered):
        color=palette[idx]
        for r,c in comp["cells"]:
            out[r][c]=color
    return out



def solve_i10_fill_corner_rectangles(g):
    out=copy_grid(g)
    colors=sorted({v for row in g for v in row if v!=0})
    for color in colors:
        cells=find_color_cells(g,color)
        cellset=set(cells)
        rows=sorted(set(r for r,c in cells))
        cols=sorted(set(c for r,c in cells))
        # fill all rectangles whose four corners exist
        done=set()
        for r0 in rows:
            for r1 in rows:
                if r1<=r0: continue
                for c0 in cols:
                    for c1 in cols:
                        if c1<=c0: continue
                        corners={(r0,c0),(r0,c1),(r1,c0),(r1,c1)}
                        if corners.issubset(cellset):
                            for r in range(r0,r1+1):
                                for c in range(c0,c1+1):
                                    out[r][c]=color
        # if color has only one rectangle corners this is fine
    return out



def solve_i11_gravity_with_blockers(g):
    h,w=dims(g)
    out=blank(h,w,0)
    # copy blockers first
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                out[r][c]=5
    for c in range(w):
        segments=[]
        start=0
        for r in range(h+1):
            if r==h or g[r][c]==5:
                segments.append((start,r-1))
                start=r+1
        for a,b in segments:
            if a>b: continue
            vals=[g[r][c] for r in range(a,b+1) if g[r][c] not in (0,5)]
            rr=b
            for v in reversed(vals):
                out[rr][c]=v
                rr-=1
    return out



def solve_i12_center_object_in_frame(g):
    comps=components_same_color(g)
    # identify frame component as one whose cropped shape has border only
    frame=None; obj=None
    for comp in comps:
        cells=comp["cells"]; color=comp["color"]
        r0,c0,r1,c1=bbox(cells)
        shape=component_shape_from_cells(g,cells)[0]
        sh,sw=dims(shape)
        full_border=set()
        for c in range(sw):
            full_border.add((0,c)); full_border.add((sh-1,c))
        for r in range(sh):
            full_border.add((r,0)); full_border.add((r,sw-1))
        shape_cells={(r,c) for r,row in enumerate(shape) for c,v in enumerate(row) if v!=0}
        if shape_cells==full_border and sh>=3 and sw>=3:
            frame=comp
        else:
            obj=comp
    out=blank(*dims(g),0)
    # keep frame
    for r,c in frame["cells"]:
        out[r][c]=frame["color"]
    shape,_=component_shape_from_cells(g,obj["cells"])
    fr0,fc0,fr1,fc1=bbox(frame["cells"])
    interior_bbox=(fr0+1,fc0+1,fr1-1,fc1-1)
    sh,sw=dims(shape)
    top,left=center_position(interior_bbox,(sh,sw))
    paste(out,shape,top,left,transparent=True)
    return out



def solve_i13_mirror_across_gray_axis(g):
    h,w=dims(g)
    axis_cols=[c for c in range(w) if all(g[r][c]==5 for r in range(h))]
    assert len(axis_cols)==1
    a=axis_cols[0]
    out=blank(h,w,0)
    for r in range(h):
        out[r][a]=5
    for r in range(h):
        for c in range(a):
            v=g[r][c]
            if v!=0 and v!=5:
                out[r][c]=v
                mc=2*a-c
                if 0<=mc<w:
                    out[r][mc]=v
    return out



def solve_i14_fill_holes(g):
    h,w=dims(g)
    out=copy_grid(g)
    # fill holes per color component bounding box
    for comp in components_same_color(g):
        color=comp["color"]
        r0,c0,r1,c1=bbox(comp["cells"])
        sub=blank(r1-r0+1,c1-c0+1,0)
        for r,c in comp["cells"]:
            sub[r-r0][c-c0]=color
        holes=hole_mask(sub)
        for rr,cc in holes:
            out[r0+rr][c0+cc]=color
    return out



def solve_i15_match_frames_and_inserts_by_size(g):
    comps=components_same_color(g)
    frames=[]
    inserts=[]
    for comp in comps:
        shape,_=component_shape_from_cells(g,comp["cells"])
        sh,sw=dims(shape)
        full_border=set()
        for c in range(sw):
            full_border.add((0,c)); full_border.add((sh-1,c))
        for r in range(sh):
            full_border.add((r,0)); full_border.add((r,sw-1))
        shape_cells={(r,c) for r,row in enumerate(shape) for c,v in enumerate(row) if v!=0}
        if sh>=3 and sw>=3 and shape_cells==full_border:
            frames.append(comp)
        else:
            inserts.append(comp)
    out=blank(*dims(g),0)
    # draw frames
    for fr in frames:
        for r,c in fr["cells"]:
            out[r][c]=fr["color"]
    # match insert bbox dims to frame interior dims
    used=set()
    for ins in inserts:
        sh,sw=bbox_dims(ins["cells"])
        matched=None
        for idx,fr in enumerate(frames):
            fr0,fc0,fr1,fc1=bbox(fr["cells"])
            ih,iw=(fr1-fr0-1, fc1-fc0-1)  # interior dims?
            ih=fr1-fr0-1
            iw=fc1-fc0-1
            if (ih,iw)==(sh,sw) and idx not in used:
                matched=idx
                break
        if matched is None:
            raise ValueError("no matching frame")
        used.add(matched)
        fr=frames[matched]
        shape,_=component_shape_from_cells(g,ins["cells"])
        fr0,fc0,fr1,fc1=bbox(fr["cells"])
        top,left=fr0+1,fc0+1
        paste(out,shape,top,left,transparent=True)
    return out



def solve_i16_template_gallery_by_marker_script(g):
    h,w=dims(g)
    markers=[v for v in g[h-1] if v!=0]
    template=[row[:] for row in g[:-1]]
    template=crop_nonzero(template)
    trans_map={
        1: lambda x:x,
        2: rotate90,
        3: rotate180,
        4: hflip,
    }
    shapes=[trans_map[m](template) for m in markers]
    heights=[len(s) for s in shapes]; widths=[len(s[0]) for s in shapes]
    H=max(heights); W=sum(widths)+max(0,len(shapes)-1)
    out=blank(H,W,0)
    cur=0
    for s in shapes:
        paste(out,s,(H-len(s))//2,cur,transparent=True)
        cur+=len(s[0])+1
    return out



def solve_i17_shortest_path_fill(g):
    colors=[v for row in g for v in row if v not in (0,5)]
    # pair color occurring exactly twice
    from collections import Counter
    cnt=Counter(colors)
    color=[k for k,v in cnt.items() if v==2][0]
    cells=find_color_cells(g,color)
    start,goal=cells[0],cells[1]
    path=shortest_path_with_walls(g,start,goal,{5})
    out=copy_grid(g)
    for r,c in path:
        out[r][c]=color
    return out



def solve_i18_rotate_object_around_pivot_by_key(g):
    key=g[0][0]
    rotations={1:0,2:1,3:2,4:3}[key]
    # pivot color 9, object all other nonzero except key
    piv=find_color_cells(g,9)[0]
    pr,pc=piv
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0 and not (r==0 and c==0) and v!=9]
    color_cells=[(r,c,g[r][c]) for r,c in cells]
    def rot_point(r,c,k):
        dr,dc=r-pr,c-pc
        for _ in range(k):
            dr,dc=dc,-dr  # clockwise? let's verify: (0,1)->(1,0) good
        return pr+dr, pc+dc
    out=blank(*dims(g),0)
    out[0][0]=key
    out[pr][pc]=9
    for r,c,v in color_cells:
        nr,nc=rot_point(r,c,rotations)
        out[nr][nc]=v
    return out



def solve_i19_parity_fill_inside_frame(g):
    # one frame color A and one seed color B inside
    h,w=dims(g)
    colors=sorted({v for row in g for v in row if v!=0})
    # identify seed as singleton not on border of bbox perhaps
    comps=components_same_color(g)
    frame=None; seed=None
    for comp in comps:
        cells=comp["cells"]; color=comp["color"]
        shape,_=component_shape_from_cells(g,cells)
        sh,sw=dims(shape)
        full_border=set()
        for c in range(sw):
            full_border.add((0,c)); full_border.add((sh-1,c))
        for r in range(sh):
            full_border.add((r,0)); full_border.add((r,sw-1))
        shape_cells={(r,c) for r,row in enumerate(shape) for c,v in enumerate(row) if v!=0}
        if len(cells)>1 and sh>=3 and sw>=3 and shape_cells==full_border:
            frame=comp
        elif len(cells)==1:
            seed=(cells[0],color)
    out=copy_grid(g)
    fr0,fc0,fr1,fc1=bbox(frame["cells"])
    seed_pos,seed_color=seed
    frame_color=frame["color"]
    # fill interior zeros reachable inside bbox without crossing border frame
    for r in range(fr0+1,fr1):
        for c in range(fc0+1,fc1):
            if g[r][c]==0:
                dist=abs(r-seed_pos[0])+abs(c-seed_pos[1])
                out[r][c]=seed_color if dist%2==0 else frame_color
    return out



def solve_i20_select_dihedral_match(g):
    comps=components_same_color(g)
    template=[comp for comp in comps if comp["color"]==1][0]
    target_variants=norm_variants(component_shape_from_cells(g,template["cells"])[0])
    # find matching candidate (not color1)
    best=None
    for comp in comps:
        if comp["color"]==1:
            continue
        shape,_=component_shape_from_cells(g,comp["cells"])
        if normalize_binary(shape) in target_variants:
            best=comp
            break
    if best is None:
        raise ValueError("no dihedral match")
    shape,_=component_shape_from_cells(g,best["cells"])
    return [[8 if v!=0 else 0 for v in row] for row in shape]



def solve_i21_boolean_by_key(g):
    key=g[0][0]
    comps=components_same_color(g)
    objects=[comp for comp in comps if not (len(comp["cells"])==1 and comp["cells"][0]==(0,0))]
    assert len(objects)==2
    shapes=[component_shape_from_cells(g,comp["cells"])[0] for comp in objects]
    # align by top-left of cropped bboxes into common canvas
    hs=[len(s) for s in shapes]; ws=[len(s[0]) for s in shapes]
    H=max(hs); W=max(ws)
    mats=[]
    for s in shapes:
        h,w=dims(s)
        m=blank(H,W,0)
        paste(m,s,0,0,transparent=True)
        mats.append(m)
    a,b=mats
    out=blank(H,W,0)
    for r in range(H):
        for c in range(W):
            av=a[r][c]!=0; bv=b[r][c]!=0
            keep=False
            if key==1: keep=av or bv
            elif key==2: keep=av and bv
            elif key==3: keep=(av!=bv)
            else: keep=False
            if keep: out[r][c]=8
    return crop_nonzero(out)


