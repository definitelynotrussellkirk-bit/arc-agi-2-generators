from collections import Counter, defaultdict, deque

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

def copy_grid(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0]) if g else 0


def zeros(h, w):
    return [[0]*w for _ in range(h)]


def nonzero_cells(g):
    return [(r,c,g[r][c]) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]


def bbox_of_cells(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)


def crop_bbox(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox_of_cells(cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def components4(g, color_sensitive=True):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if g[r][c]==0 or seen[r][c]:
                continue
            col=g[r][c]
            q=deque([(r,c)]); seen[r][c]=True; cells=[]
            while q:
                x,y=q.popleft(); cells.append((x,y))
                for dx,dy in DIR4:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and not seen[nx][ny] and g[nx][ny]!=0 and ((not color_sensitive) or g[nx][ny]==col):
                        seen[nx][ny]=True; q.append((nx,ny))
            comps.append({"color":col,"cells":cells})
    return comps


def crop_from_cells(g, cells):
    r0,c0,r1,c1=bbox_of_cells(cells)
    sub=[[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in cells:
        sub[r-r0][c-c0]=g[r][c]
    return sub, (r0,c0,r1,c1)


def find_rect_frames(g):
    # detect rectangular frames of single color thickness 1 with zero interior or mixed interior
    h,w=dims(g)
    frames=[]
    pos_by_color=defaultdict(list)
    for r,c,v in nonzero_cells(g):
        pos_by_color[v].append((r,c))
    # brute-force rectangles from same color cells? we'll just detect bboxes of components of frame color.
    for comp in components4(g, color_sensitive=True):
        cells=comp["cells"]; color=comp["color"]
        r0,c0,r1,c1=bbox_of_cells(cells)
        # check border cells of bbox are all color and interior doesn't have this color maybe
        ok=True
        border=set()
        for c in range(c0,c1+1):
            border.add((r0,c)); border.add((r1,c))
        for r in range(r0,r1+1):
            border.add((r,c0)); border.add((r,c1))
        if not all((r,c) in cells for r,c in border):
            ok=False
        if ok and r1-r0>=2 and c1-c0>=2:
            frames.append({"color":color, "bbox":(r0,c0,r1,c1), "cells":cells})
    return frames


def normalize_object_to_origin(g, comp):
    sub,_=crop_from_cells(g, comp["cells"])
    return sub


def scale_grid_nearest(sub, k):
    sh,sw=dims(sub)
    out=zeros(sh*k, sw*k)
    for r in range(sh):
        for c in range(sw):
            v=sub[r][c]
            for rr in range(k):
                for cc in range(k):
                    out[r*k+rr][c*k+cc]=v
    return out


def solve_e1_hollow_square_fill(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(1,h-1):
        for c in range(1,w-1):
            color=g[r-1][c-1]
            if color!=0:
                coords=[(r-1,c-1),(r-1,c),(r-1,c+1),(r,c-1),(r,c+1),(r+1,c-1),(r+1,c),(r+1,c+1)]
                if all(g[x][y]==color for x,y in coords) and g[r][c]==0:
                    out[r][c]=color
    return out


def solve_e2_seed_column(g):
    h,w=dims(g)
    out=zeros(h,w)
    for c in range(w):
        # any nonzero in column paints whole column using first nonzero's color
        col=0
        for r in range(h):
            if g[r][c]!=0:
                col=g[r][c]; break
        if col!=0:
            for r in range(h):
                out[r][c]=col
    return out


def solve_e3_crop_bbox(g):
    return crop_bbox(g)


def solve_e4_mirror_left_half(g):
    h,w=dims(g); assert w%2==0
    out=copy_grid(g)
    half=w//2
    for r in range(h):
        for c in range(half):
            out[r][w-1-c]=g[r][c]
    return out


def solve_e5_diagonal_dr(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r,c,v in nonzero_cells(g):
        x,y=r,c
        while 0<=x<h and 0<=y<w:
            out[x][y]=v
            x+=1; y+=1
    return out


def solve_e6_isolated_to_8(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r,c,v in nonzero_cells(g):
        if all(not (0<=r+dr<h and 0<=c+dc<w and g[r+dr][c+dc]!=0) for dr,dc in DIR4):
            out[r][c]=8
    return out


def solve_e7_domino_to_2x2(g):
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h-1):
        for c in range(w-1):
            v=g[r][c]
            if v!=0 and g[r][c+1]==v:
                out[r+1][c]=v
                out[r+1][c+1]=v
    return out


def solve_m1_keep_largest_recolor(g):
    h,w=dims(g)
    comps=components4(g, color_sensitive=True)
    if not comps:
        return zeros(h,w)
    best=max(comps, key=lambda comp: len(comp["cells"]))
    out=zeros(h,w)
    for r,c in best["cells"]:
        out[r][c]=8
    return out


def solve_m2_marker_rectangle_border(g):
    h,w=dims(g)
    positions=defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                positions[v].append((r,c))
    out=zeros(h,w)
    for color,cells in positions.items():
        if len(cells)!=2:
            # just copy cells if not exactly two? but our examples will use pairs only
            for r,c in cells:
                out[r][c]=color
            continue
        (r1,c1),(r2,c2)=cells
        ra,rb=sorted([r1,r2]); ca,cb=sorted([c1,c2])
        for c in range(ca,cb+1):
            out[ra][c]=color
            out[rb][c]=color
        for r in range(ra,rb+1):
            out[r][ca]=color
            out[r][cb]=color
    return out


def solve_m3_scale2(g):
    h,w=dims(g)
    out=zeros(h*2,w*2)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            out[2*r][2*c]=v
            out[2*r][2*c+1]=v
            out[2*r+1][2*c]=v
            out[2*r+1][2*c+1]=v
    return out


def solve_m4_center_object(g):
    h,w=dims(g)
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return zeros(h,w)
    rs=[r for r,c,v in cells]; cs=[c for r,c,v in cells]
    r0,c0,r1,c1=min(rs),min(cs),max(rs),max(cs)
    obj_h,obj_w=r1-r0+1,c1-c0+1
    new_r=(h-obj_h)//2
    new_c=(w-obj_w)//2
    out=zeros(h,w)
    for r,c,v in cells:
        out[new_r + (r-r0)][new_c + (c-c0)] = v
    return out


def solve_m5_color_rank_recolor(g):
    counts=Counter(v for row in g for v in row if v!=0)
    order=[color for color,_ in sorted(counts.items(), key=lambda kv:(-kv[1], kv[0]))]
    mapping={color:i+1 for i,color in enumerate(order)}
    return [[mapping.get(v,0) for v in row] for row in g]


def solve_m6_fill_bbox_each_object(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in components4(g, color_sensitive=True):
        color=comp["color"]
        r0,c0,r1,c1=bbox_of_cells(comp["cells"])
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                out[r][c]=color
    return out


def solve_m7_fill_holes(g):
    h,w=dims(g)
    out=copy_grid(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0 or seen[r][c]:
                continue
            q=deque([(r,c)]); seen[r][c]=True; region=[]; touches=False; neigh_colors=set()
            while q:
                x,y=q.popleft(); region.append((x,y))
                if x==0 or y==0 or x==h-1 or y==w-1:
                    touches=True
                for dx,dy in DIR4:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w:
                        if g[nx][ny]==0 and not seen[nx][ny]:
                            seen[nx][ny]=True; q.append((nx,ny))
                        elif g[nx][ny]!=0:
                            neigh_colors.add(g[nx][ny])
            if not touches and len(neigh_colors)==1:
                color=next(iter(neigh_colors))
                for x,y in region:
                    out[x][y]=color
    return out


def solve_h1_pack_objects_sorted(g):
    comps=components4(g, color_sensitive=True)
    if not comps:
        return [[0]]
    # crop each object to bbox
    items=[]
    for comp in comps:
        sub,_=crop_from_cells(g, comp["cells"])
        h,w=dims(sub)
        items.append((len(comp["cells"]), h, w, comp["color"], sub))
    # sort by area desc, then top-left of original via min coords
    def key(item):
        area,h,w,color,sub=item
        return (-area, -h, -w, color)
    items=sorted(items, key=key)
    out_h=max(dims(sub)[0] for _,_,_,_,sub in items)
    out_w=sum(dims(sub)[1] for _,_,_,_,sub in items) + (len(items)-1)
    out=zeros(out_h,out_w)
    cur=0
    for _,_,_,_,sub in items:
        sh,sw=dims(sub)
        for r in range(sh):
            for c in range(sw):
                out[r][cur+c]=sub[r][c]
        cur += sw + 1
    return out


def solve_h2_frame_fill_from_seed(g):
    out=copy_grid(g)
    frames=find_rect_frames(g)
    for fr in frames:
        color=fr["color"]; r0,c0,r1,c1=fr["bbox"]
        # find nonzero seed cells strictly inside that are not frame color
        seeds=[]
        for r in range(r0+1,r1):
            for c in range(c0+1,c1):
                if g[r][c]!=0 and g[r][c]!=color:
                    seeds.append(g[r][c])
        if len(set(seeds))==1 and seeds:
            fill=seeds[0]
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=fill
    return out


def solve_h3_stamp_template_at_anchors(g):
    h,w=dims(g)
    comps=components4(g, color_sensitive=True)
    # template = unique component with size >1; anchors = singleton components
    templates=[comp for comp in comps if len(comp["cells"])>1]
    singles=[comp for comp in comps if len(comp["cells"])==1]
    assert len(templates)==1
    template=templates[0]
    temp_sub,_=crop_from_cells(g, template["cells"])
    # anchor color from singleton comps, assume all same color
    anchor_color=singles[0]["color"] if singles else template["color"]
    out=zeros(h,w)
    # use anchor cell as top-left placement
    for comp in singles:
        (ar,ac)=comp["cells"][0]
        for r,row in enumerate(temp_sub):
            for c,v in enumerate(row):
                if v!=0 and 0<=ar+r<h and 0<=ac+c<w:
                    out[ar+r][ac+c]=anchor_color
    return out


def solve_h4_move_object_toward_marker(g):
    h,w=dims(g)
    comps=components4(g, color_sensitive=True)
    singles=[comp for comp in comps if len(comp["cells"])==1]
    objects=[comp for comp in comps if len(comp["cells"])>1]
    assert len(singles)==1 and len(objects)==1
    marker=singles[0]["cells"][0]
    obj=objects[0]
    r0,c0,r1,c1=bbox_of_cells(obj["cells"])
    mr,mc=marker
    # determine if marker is left/right/up/down of bbox with no overlap in that axis
    dr=dc=0
    if mc > c1:
        dc = (mc - 1) - c1
    elif mc < c0:
        dc = (mc + 1) - c0
    elif mr > r1:
        dr = (mr - 1) - r1
    elif mr < r0:
        dr = (mr + 1) - r0
    else:
        # marker aligned inside bbox projection; choose minimal move away? not used
        pass
    out=zeros(h,w)
    # keep marker
    out[mr][mc]=g[mr][mc]
    color=obj["color"]
    for r,c in obj["cells"]:
        nr,nc=r+dr,c+dc
        out[nr][nc]=color
    return out


def solve_h5_enclosed_recolor_keep_frames(g):
    h,w=dims(g)
    out=zeros(h,w)
    frames=find_rect_frames(g)
    # keep frames
    for fr in frames:
        for r,c in fr["cells"]:
            out[r][c]=fr["color"]
    # recolor enclosed objects
    comps=components4(g, color_sensitive=True)
    frame_cell_sets=[set(fr["cells"]) for fr in frames]
    for comp in comps:
        cells=set(comp["cells"])
        # skip frames themselves
        if any(cells==fset for fset in frame_cell_sets):
            continue
        # find containing frame whose bbox strictly contains comp bbox
        cr0,cc0,cr1,cc1=bbox_of_cells(comp["cells"])
        containing=[]
        for fr in frames:
            r0,c0,r1,c1=fr["bbox"]
            if r0 < cr0 and c0 < cc0 and cr1 < r1 and cc1 < c1:
                containing.append(fr)
        if containing:
            # choose smallest containing frame by area
            fr=min(containing, key=lambda fr:(fr["bbox"][2]-fr["bbox"][0])*(fr["bbox"][3]-fr["bbox"][1]))
            for r,c in comp["cells"]:
                out[r][c]=fr["color"]
    return out


def solve_h6_overlay_normalized(g):
    comps=components4(g, color_sensitive=True)
    assert len(comps)==2
    comp_a, comp_b = comps
    sub_a=normalize_object_to_origin(g, comp_a)
    sub_b=normalize_object_to_origin(g, comp_b)
    ha,wa=dims(sub_a); hb,wb=dims(sub_b)
    out=zeros(max(ha,hb), max(wa,wb))
    color_a=comp_a["color"]; color_b=comp_b["color"]
    for r in range(len(out)):
        for c in range(len(out[0])):
            va = sub_a[r][c] if r<ha and c<wa else 0
            vb = sub_b[r][c] if r<hb and c<wb else 0
            if va!=0 and vb!=0:
                out[r][c]=8
            elif va!=0:
                out[r][c]=color_a
            elif vb!=0:
                out[r][c]=color_b
    return out


def solve_h7_scale_template_by_marker_count(g):
    comps=components4(g, color_sensitive=True)
    templates=[comp for comp in comps if len(comp["cells"])>1]
    markers=[comp for comp in comps if len(comp["cells"])==1]
    assert len(templates)==1
    k=len(markers)
    sub,_=crop_from_cells(g, templates[0]["cells"])
    return scale_grid_nearest(sub, k)

