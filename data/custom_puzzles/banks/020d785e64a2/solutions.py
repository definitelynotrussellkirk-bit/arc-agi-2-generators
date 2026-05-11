"""Reference solvers for the eleventh 21-task ARC-style puzzle bank.

This batch leans into:
- axis echoes, row/column projections, and border outer-products
- selection, counting, packing, relative offsets, and aspect reasoning
- matching by dimensions or topology, keyed transforms, and stateful pathfinding
"""
from typing import List, Tuple
from collections import deque

Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]

NEW_PRIMITIVES = {
    "vertical_echo": "Copy every cell to its mirror position across the vertical axis.",
    "crosshair_project": "Project each seed across its full row and full column.",
    "solid_to_frame": "Hollow a solid rectangle so only its border remains.",
    "diagonal_echo": "Copy every cell to its transposed position across the main diagonal.",
    "downcast": "Extend a seed straight downward to the bottom border.",
    "block_main_diagonal": "Reduce each solid 2\u00d72 block to its main diagonal.",
    "border_intersections": "Fill the intersections defined by matching border markers.",
    "corner_select_crop": "Select the object whose color matches the corner key and crop it.",
    "count_rotate": "Rotate an object according to the number of key markers.",
    "pack_by_area": "Crop objects and pack them in increasing order of area.",
    "column_histogram": "Turn each column\u2019s count into a bottom-aligned bar.",
    "offset_transfer": "Copy a motif using its offset from one marker to another.",
    "wall_shadow": "Project occupied cells rightward until a wall stops them.",
    "aspect_recolor": "Recolor objects by whether their bounding boxes are tall, wide, or square.",
    "socket_fit": "Match solid inserts to frames by interior dimensions.",
    "normalized_overlay": "Normalize two objects and color-code only-A, only-B, and overlap.",
    "keyed_path": "Find a shortest path whose state changes after collecting a key.",
    "pack_by_holes": "Crop objects and pack them by increasing hole count.",
    "portal_transfer": "Move a framed pattern into a target frame with a keyed transform.",
    "ordered_centroid_polyline": "Connect component centers in key order using L-shaped segments.",
    "topology_socket": "Match objects to frames by topological class (hole count)."
}

def blank(h,w,v=0):
    return [[v for _ in range(w)] for __ in range(h)]

def dims(g):
    return len(g), len(g[0]) if g else 0

def copy_grid(g):
    return [row[:] for row in g]

def bbox_cells(cells):
    rs=[r for r,c in cells]
    cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, cells=None, pad=0):
    if cells is None:
        cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0,c0,r1,c1=bbox_cells(cells)
    r0=max(0,r0-pad); c0=max(0,c0-pad); r1=min(len(g)-1,r1+pad); c1=min(len(g[0])-1,c1+pad)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def normalize_coords(cells):
    if not cells: return []
    r0,c0,r1,c1=bbox_cells(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def rotate90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate180(g):
    return [row[::-1] for row in g[::-1]]

def rotate270(g):
    h,w=dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w-1,-1,-1)]

def reflect_h(g):  # horizontal mirror left-right
    return [row[::-1] for row in g]

def reflect_v(g):  # vertical mirror top-bottom
    return g[::-1]

def find_components(g, colors=None, conn4=True):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    dirs=DIR4 if conn4 else [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or seen[r][c]: 
                continue
            if colors is not None and v not in colors:
                continue
            color=v
            q=deque([(r,c)])
            seen[r][c]=True
            cells=[]
            while q:
                x,y=q.popleft()
                cells.append((x,y))
                for dx,dy in dirs:
                    nx,ny=x+dx,y+dy
                    if 0<=nx<h and 0<=ny<w and not seen[nx][ny] and g[nx][ny]==color:
                        seen[nx][ny]=True
                        q.append((nx,ny))
            comps.append({'color':color,'cells':cells})
    return comps

def component_bbox(comp):
    return bbox_cells(comp['cells'])

def component_crop(g, comp):
    return crop_bbox(g, comp['cells'])

def bottom_align_pack(crops, gap=1):
    h=max(len(g) for g in crops)
    w=sum(len(g[0]) for g in crops)+gap*(len(crops)-1)
    out=blank(h,w)
    c0=0
    for g in crops:
        gh,gw=dims(g)
        r0=h-gh
        for r in range(gh):
            for c in range(gw):
                if g[r][c]:
                    out[r0+r][c0+c]=g[r][c]
        c0 += gw+gap
    return out

def count_holes(cells):
    if not cells: return 0
    norm=normalize_coords(cells)
    rs=[r for r,c in norm]; cs=[c for r,c in norm]
    h=max(rs)+1; w=max(cs)+1
    occ=set(norm)
    seen=set()
    holes=0
    for r in range(-1,h+1):
        for c in range(-1,w+1):
            if (r,c) in occ or (r,c) in seen:
                continue
            q=deque([(r,c)]); seen.add((r,c)); comp=[]
            touches_out=False
            while q:
                x,y=q.popleft()
                comp.append((x,y))
                if x in (-1,h) or y in (-1,w):
                    touches_out=True
                for dx,dy in DIR4:
                    nx,ny=x+dx,y+dy
                    if -1<=nx<=h and -1<=ny<=w and (nx,ny) not in occ and (nx,ny) not in seen:
                        seen.add((nx,ny)); q.append((nx,ny))
            if not touches_out:
                holes += 1
    return holes

def select_corner_marker(g: Grid):
    h,w=dims(g)
    corners=[(0,0),(0,w-1),(h-1,0),(h-1,w-1)]
    markers=[(r,c,g[r][c]) for r,c in corners if g[r][c]!=0]
    return markers[0] if markers else None

def remove_corner_markers(g: Grid):
    h,w=dims(g)
    out=copy_grid(g)
    for r,c in [(0,0),(0,w-1),(h-1,0),(h-1,w-1)]:
        out[r][c]=0
    return out

def frame_boxes(g, frame_colors=None):
    # detect hollow rectangular frames by color and bbox
    comps=find_components(g)
    frames=[]
    for comp in comps:
        color=comp['color']
        if frame_colors is not None and color not in frame_colors:
            continue
        r0,c0,r1,c1=component_bbox(comp)
        cells=set(comp['cells'])
        # verify rectangle border
        border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
        if cells==border:
            frames.append({'color':color,'bbox':(r0,c0,r1,c1),'cells':comp['cells']})
    return frames

def shortest_path_with_state(g: Grid) -> List[Tuple[int,int]]:
    h,w=dims(g)
    start=next((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2)
    goal=next((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3)
    keys={(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==4}
    doors={(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==5}
    walls={(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==8}
    start_state=(start[0],start[1],False)
    q=deque([start_state])
    prev={start_state: None}
    while q:
        r,c,has_key=q.popleft()
        if (r,c)==goal:
            st=(r,c,has_key)
            path=[]
            while st is not None:
                path.append((st[0],st[1]))
                st=prev[st]
            return path[::-1]
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if not (0<=nr<h and 0<=nc<w): continue
            if (nr,nc) in walls: continue
            new_has=has_key or ((nr,nc) in keys)
            if (nr,nc) in doors and not new_has:
                continue
            st=(nr,nc,new_has)
            if st not in prev:
                prev[st]=(r,c,has_key)
                q.append(st)
    return []

def transform_by_key(obj: Grid, key: int) -> Grid:
    if key==1:
        return reflect_h(obj)
    if key==2:
        return reflect_v(obj)
    if key==3:
        return rotate180(obj)
    return obj

def solve_k01_vertical_echo(g: Grid) -> Grid:
    h,w=dims(g)
    out=copy_grid(g)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0:
                out[r][w-1-c]=v
    return out

def solve_k02_crosshair_project(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    seeds=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    for r,c,v in seeds:
        for cc in range(w):
            out[r][cc]=v
        for rr in range(h):
            out[rr][c]=v
    return out

def solve_k03_solid_to_frame(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    comps=find_components(g)
    for comp in comps:
        r0,c0,r1,c1=component_bbox(comp)
        color=comp['color']
        for r in range(r0,r1+1):
            for c in range(c0,c1+1):
                if r in (r0,r1) or c in (c0,c1):
                    out[r][c]=color
    return out

def solve_k04_diagonal_echo(g: Grid) -> Grid:
    h,w=dims(g); assert h==w
    out=copy_grid(g)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0:
                out[c][r]=v
    return out

def solve_k05_downcast(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v!=0:
                for rr in range(r,h):
                    out[rr][c]=v
    return out

def solve_k06_block_main_diagonal(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    used=[[False]*w for _ in range(h)]
    for r in range(h-1):
        for c in range(w-1):
            vals=[g[r][c],g[r+1][c],g[r][c+1],g[r+1][c+1]]
            nz={v for v in vals if v!=0}
            if len(nz)==1 and all(v!=0 for v in vals):
                color=vals[0]
                out[r][c]=color
                out[r+1][c+1]=color
    return out

def solve_k07_border_intersections(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    top={}
    left={}
    for c,v in enumerate(g[0]):
        if v!=0:
            top.setdefault(v, []).append(c)
    for r in range(h):
        v=g[r][0]
        if v!=0:
            left.setdefault(v, []).append(r)
    for color in sorted(set(top)&set(left)):
        for r in left[color]:
            for c in top[color]:
                out[r][c]=color
    return out

def solve_k08_corner_select_crop(g: Grid) -> Grid:
    h,w=dims(g)
    marker=select_corner_marker(g)
    color=marker[2]
    gg=remove_corner_markers(g)
    cells=[(r,c) for r,row in enumerate(gg) for c,v in enumerate(row) if v==color]
    return crop_bbox(gg, cells)

def solve_k09_count_rotate(g: Grid) -> Grid:
    h,w=dims(g)
    gg=copy_grid(g)
    # markers are key color 9 in top row
    count=sum(1 for c in range(w) if gg[0][c]==9)
    for c in range(w):
        if gg[0][c]==9:
            gg[0][c]=0
    cells=[(r,c) for r,row in enumerate(gg) for c,v in enumerate(row) if v!=0]
    obj=crop_bbox(gg, cells)
    if count==1:
        return rotate90(obj)
    elif count==2:
        return rotate180(obj)
    else:
        return rotate270(obj)

def solve_k10_pack_by_area(g: Grid) -> Grid:
    comps=find_components(g)
    crops=[]
    for comp in comps:
        crops.append((len(comp['cells']), crop_bbox(g, comp['cells'])))
    crops.sort(key=lambda x:(x[0], len(x[1]), len(x[1][0]), min(v for row in x[1] for v in row if v!=0)))
    return bottom_align_pack([c for _,c in crops], gap=1)

def solve_k11_column_histogram(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        cells=[g[r][c] for r in range(h) if g[r][c]!=0]
        if not cells:
            continue
        # choose the first nonzero color (generator ensures same color per col)
        color=cells[0]
        k=len(cells)
        for rr in range(h-k,h):
            out[rr][c]=color
    return out

def solve_k12_offset_transfer(g: Grid) -> Grid:
    h,w=dims(g)
    # source marker color 1, target marker color 2, motif any other colors
    src = next((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==1)
    tgt = next((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2)
    gg=copy_grid(g)
    gg[src[0]][src[1]]=0
    gg[tgt[0]][tgt[1]]=0
    # all remaining nonzero cells are motif
    motif=[(r,c,gg[r][c]) for r,row in enumerate(gg) for c,v in enumerate(row) if v!=0]
    # motif is near source: compute relative positions to source
    rel=[(r-src[0], c-src[1], v) for r,c,v in motif]
    out=blank(h,w)
    for dr,dc,v in rel:
        rr,cc=tgt[0]+dr, tgt[1]+dc
        if 0<=rr<h and 0<=cc<w:
            out[rr][cc]=v
    return crop_bbox(out)

def solve_k13_wall_shadow(g: Grid) -> Grid:
    h,w=dims(g)
    # wall color is 5, vertical line
    wall_col=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            wall_col=c
            break
    out=copy_grid(g)
    if wall_col is None:
        return out
    for r in range(h):
        for c in range(wall_col):
            v=g[r][c]
            if v!=0 and v!=5:
                for cc in range(c+1, wall_col):
                    if out[r][cc]==0:
                        out[r][cc]=v
    return out

def solve_k14_aspect_recolor(g: Grid) -> Grid:
    out=blank(*dims(g))
    comps=find_components(g)
    for comp in comps:
        r0,c0,r1,c1=component_bbox(comp)
        h=r1-r0+1; w=c1-c0+1
        if h>w:
            color=2
        elif w>h:
            color=3
        else:
            color=4
        for r,c in comp['cells']:
            out[r][c]=color
    return out

def solve_k15_socket_fit(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    frames=frame_boxes(g, frame_colors={8})
    # keep frames
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=8
    # inserts are solid rectangles of non-8 colors not inside frames
    comps=find_components(g)
    inserts=[]
    frame_cellset=set((r,c) for fr in frames for r,c in fr['cells'])
    for comp in comps:
        if comp['color']==8:
            continue
        # skip marker or tiny? no, all are inserts
        r0,c0,r1,c1=component_bbox(comp)
        cells=set(comp['cells'])
        full={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1)}
        if cells==full:  # solid rectangle
            inserts.append({'color':comp['color'],'size':(r1-r0+1,c1-c0+1),'cells':comp['cells']})
    # match by frame interior size
    frame_by_size={(fr['bbox'][2]-fr['bbox'][0]-1, fr['bbox'][3]-fr['bbox'][1]-1): fr for fr in frames}
    for ins in inserts:
        if ins['size'] in frame_by_size:
            fr=frame_by_size[ins['size']]
            r0,c0,r1,c1=fr['bbox']
            ih,iw=ins['size']
            # fill interior with solid insert color
            for r in range(r0+1,r1):
                for c in range(c0+1,c1):
                    out[r][c]=ins['color']
    return out

def solve_k16_normalized_overlay(g: Grid) -> Grid:
    # two objects: colors 2 and 3, output normalized overlay: 2 only A, 3 only B, 8 overlap
    cellsA=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==2]
    cellsB=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==3]
    A=set(normalize_coords(cellsA))
    B=set(normalize_coords(cellsB))
    allc=A|B
    h=max([r for r,c in allc], default=0)+1
    w=max([c for r,c in allc], default=0)+1
    out=blank(h,w)
    for r,c in allc:
        if (r,c) in A and (r,c) in B:
            out[r][c]=8
        elif (r,c) in A:
            out[r][c]=2
        else:
            out[r][c]=3
    return out

def solve_k17_keyed_path(g: Grid) -> Grid:
    out=copy_grid(g)
    path=shortest_path_with_state(g)
    for r,c in path:
        if out[r][c] not in (2,3,4,5,8):
            out[r][c]=7
    return out

def solve_k18_pack_by_holes(g: Grid) -> Grid:
    comps=find_components(g)
    items=[]
    for comp in comps:
        crop=component_crop(g, comp)
        holes=count_holes(comp['cells'])
        items.append((holes, crop, comp['color']))
    items.sort(key=lambda x:(x[0], len(x[1]), len(x[1][0]), x[2]))
    return bottom_align_pack([crop for holes,crop,color in items], gap=1)

def solve_k19_portal_transfer(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    # frames: color 6 or 7, same size; one contains pattern, one empty
    frames=frame_boxes(g, frame_colors={6,7})
    for fr in frames:
        for r,c in fr['cells']:
            out[r][c]=fr['color']
    # key marker color 1/2/3 anywhere outside frames
    key = next((v for r,row in enumerate(g) for c,v in enumerate(row) if v in (1,2,3)), 0)
    # find source frame interior with nonzero cells and target empty interior
    src=None; tgt=None
    src_obj=None
    for fr in frames:
        r0,c0,r1,c1=fr['bbox']
        interior=[(r,c,g[r][c]) for r in range(r0+1,r1) for c in range(c0+1,c1) if g[r][c] not in (0,fr['color'])]
        if interior:
            src=fr
            # interior crop exact size
            src_obj=[[g[r][c] if g[r][c]!=fr['color'] else 0 for c in range(c0+1,c1)] for r in range(r0+1,r1)]
            src_obj=[[0 if v in (6,7) else v for v in row] for row in src_obj]
        else:
            tgt=fr
    transformed=transform_by_key(src_obj, key)
    # place centered/fit in target interior (same size assumed)
    r0,c0,r1,c1=tgt['bbox']
    for r in range(r1-r0-1):
        for c in range(c1-c0-1):
            v=transformed[r][c]
            if v:
                out[r0+1+r][c0+1+c]=v
    return out

def solve_k20_ordered_centroid_polyline(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    comps=find_components(g)
    # order by color ascending
    pts=[]
    for comp in comps:
        cells=comp['cells']
        rs=[r for r,c in cells]; cs=[c for r,c in cells]
        # guaranteed odd-dimension bars or markers -> integer centroid at bbox center
        r0,c0,r1,c1=component_bbox(comp)
        cr=(r0+r1)//2; cc=(c0+c1)//2
        pts.append((comp['color'], cr, cc))
        # maybe keep original centroid marker? we'll use path only
    pts.sort()
    for i in range(len(pts)-1):
        color, r1,c1=pts[i]
        _, r2,c2=pts[i+1]
        # L-path: horizontal then vertical
        step = 1 if c2>=c1 else -1
        for c in range(c1, c2+step, step):
            out[r1][c]=color
        step = 1 if r2>=r1 else -1
        for r in range(r1, r2+step, step):
            out[r][c2]=color
    # endpoints keep their own colors
    for color,r,c in pts:
        out[r][c]=color
    return out

def solve_k21_topology_socket(g: Grid) -> Grid:
    h,w=dims(g)
    out=blank(h,w)
    # frames with border colors 1,2,3 correspond to hole counts 0,1,2
    frames=frame_boxes(g, frame_colors={1,2,3})
    frame_by_holes={}
    for fr in frames:
        frame_by_holes[fr['color']-1]=fr  # color 1->0 holes, 2->1, 3->2
        for r,c in fr['cells']:
            out[r][c]=fr['color']
    # other objects placed centered in matching frame
    comps=find_components(g)
    frame_cells={(r,c) for fr in frames for r,c in fr['cells']}
    for comp in comps:
        if comp['color'] in {1,2,3}:
            # frame or maybe object same colors? generator avoids
            r0,c0,r1,c1=component_bbox(comp)
            border={(r,c) for r in range(r0,r1+1) for c in range(c0,c1+1) if r in (r0,r1) or c in (c0,c1)}
            if set(comp['cells'])==border:
                continue
        holes=count_holes(comp['cells'])
        if holes not in frame_by_holes:
            continue
        crop=component_crop(g, comp)
        fr=frame_by_holes[holes]
        r0,c0,r1,c1=fr['bbox']
        ih,iw=r1-r0-1, c1-c0-1
        gh,gw=dims(crop)
        off_r=(ih-gh)//2
        off_c=(iw-gw)//2
        for r in range(gh):
            for c in range(gw):
                v=crop[r][c]
                if v:
                    out[r0+1+off_r+r][c0+1+off_c+c]=v
    return out

