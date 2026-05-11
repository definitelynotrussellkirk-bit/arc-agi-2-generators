"""Reference solvers for the sixth 21-task ARC-style puzzle bank.

This batch leans harder into layout operators, topological descriptors,
object-to-object relations, and keyed transforms than the previous sets.

New helper primitives highlighted in this batch:
- center_pack(seq, span): strip zeros from a 1D sequence, preserve order,
  and place the compact sequence centered in the available span.
- frame_depth(objects, frames): count how many nested rectangular frames
  enclose an object.
- normalize_pair(a, b): align two cropped shapes to the same top-left
  origin inside a common bounding box before combining them.
- contact_degree(objects): compute each object's degree in the graph formed
  by one-step orthogonal dilation overlaps.
"""
from typing import List, Tuple
import collections

Grid = List[List[int]]

DIR4 = [(-1,0),(1,0),(0,-1),(0,1)]
DIR8 = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
KNIGHT = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]

NEW_PRIMITIVES = {
    "center_pack": "Strip zeros from a row or column sequence and reinsert the compact pattern centered in a fixed span.",
    "frame_depth": "Count how many nested rectangular outline frames enclose an object.",
    "normalize_pair": "Align two cropped shapes to the same top-left origin inside a common bounding box before combining them.",
    "contact_degree": "Build a relation graph by one-step orthogonal dilation overlap and return each object's number of neighbors.",
}

def blank(h,w,val=0):
    return [[val]*w for _ in range(h)]

def copy_grid(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def inb(g,r,c):
    h,w = dims(g)
    return 0 <= r < h and 0 <= c < w

def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    r0=min(r for r,c in cells); r1=max(r for r,c in cells)
    c0=min(c for r,c in cells); c1=max(c for r,c in cells)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def bbox_of_cells(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def translate_cells(cells, dr, dc):
    return {(r+dr, c+dc) for r,c in cells}

def paste_cells(h,w,cells,color):
    out=blank(h,w)
    for r,c in cells:
        if 0 <= r < h and 0 <= c < w:
            out[r][c]=color
    return out

def merge_grids(base, over, overwrite_nonzero=True):
    h,w = dims(base)
    out = copy_grid(base)
    for r in range(h):
        for c in range(w):
            if over[r][c]!=0 and (overwrite_nonzero or out[r][c]==0):
                out[r][c]=over[r][c]
    return out

def rotate_cw(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_180(g):
    return [row[::-1] for row in g[::-1]]

def rotate_ccw(g):
    h,w=dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w-1,-1,-1)]

def flip_h(g):
    return [row[::-1] for row in g]

def flip_v(g):
    return g[::-1]

def count_nonzero(g):
    return sum(v!=0 for row in g for v in row)

def colors_present(g):
    seen=[]
    s=set()
    for row in g:
        for v in row:
            if v!=0 and v not in s:
                s.add(v); seen.append(v)
    return seen

def objects4(g, nonzero_only=True):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    objs=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c]: continue
            v=g[r][c]
            if nonzero_only and v==0: 
                seen[r][c]=True
                continue
            # if zero and not nonzero_only, still component
            seen[r][c]=True
            q=[(r,c)]
            cells=[(r,c)]
            while q:
                rr,cc=q.pop()
                for dr,dc in DIR4:
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v:
                        seen[nr][nc]=True
                        q.append((nr,nc))
                        cells.append((nr,nc))
            if not(nonzero_only and v==0):
                objs.append({'color':v,'cells':cells})
    return objs

def manhattan(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def object_bbox(obj):
    return bbox_of_cells(obj['cells'])

def crop_object_grid(g, obj):
    r0,c0,r1,c1=object_bbox(obj)
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def place_grid_at(out, gsmall, top, left, color_map=None):
    h,w=dims(out)
    hs,ws=dims(gsmall)
    for r in range(hs):
        for c in range(ws):
            v=gsmall[r][c]
            if v!=0:
                rr,cc=top+r,left+c
                if 0<=rr<h and 0<=cc<w:
                    out[rr][cc] = color_map.get(v,v) if color_map else v

def neighbors4(g,r,c):
    h,w=dims(g)
    for dr,dc in DIR4:
        nr,nc=r+dr,c+dc
        if 0<=nr<h and 0<=nc<w:
            yield nr,nc

def flood_outside_zeros(g):
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    q=[]
    for r in range(h):
        for c in [0,w-1]:
            if g[r][c]==0 and not seen[r][c]:
                seen[r][c]=True; q.append((r,c))
    for c in range(w):
        for r in [0,h-1]:
            if g[r][c]==0 and not seen[r][c]:
                seen[r][c]=True; q.append((r,c))
    while q:
        rr,cc=q.pop()
        for nr,nc in neighbors4(g,rr,cc):
            if g[nr][nc]==0 and not seen[nr][nc]:
                seen[nr][nc]=True; q.append((nr,nc))
    return seen

def hole_count_for_object(g, obj):
    cells=set(obj['cells'])
    r0,c0,r1,c1=object_bbox(obj)
    sub = [[0]*(c1-c0+1) for _ in range(r1-r0+1)]
    for r,c in cells:
        sub[r-r0][c-c0]=1
    h,w=len(sub),len(sub[0])
    seen=[[False]*w for _ in range(h)]
    q=[]
    for r in range(h):
        for c in [0,w-1]:
            if sub[r][c]==0 and not seen[r][c]:
                seen[r][c]=True; q.append((r,c))
    for c in range(w):
        for r in [0,h-1]:
            if sub[r][c]==0 and not seen[r][c]:
                seen[r][c]=True; q.append((r,c))
    while q:
        rr,cc=q.pop()
        for dr,dc in DIR4:
            nr,nc=rr+dr,cc+dc
            if 0<=nr<h and 0<=nc<w and sub[nr][nc]==0 and not seen[nr][nc]:
                seen[nr][nc]=True; q.append((nr,nc))
    holes=0
    for r in range(h):
        for c in range(w):
            if sub[r][c]==0 and not seen[r][c]:
                holes+=1
                seen[r][c]=True; q=[(r,c)]
                while q:
                    rr,cc=q.pop()
                    for dr,dc in DIR4:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and sub[nr][nc]==0 and not seen[nr][nc]:
                            seen[nr][nc]=True; q.append((nr,nc))
    return holes

def is_frame_object(obj):
    cells=set(obj['cells'])
    r0,c0,r1,c1=object_bbox(obj)
    if r1-r0 < 2 or c1-c0 < 2:
        return False
    border=set()
    for c in range(c0,c1+1):
        border.add((r0,c)); border.add((r1,c))
    for r in range(r0,r1+1):
        border.add((r,c0)); border.add((r,c1))
    return cells == border

def contains_bbox(outer, inner):
    r0,c0,r1,c1 = outer
    a,b,x,y = inner
    return r0 < a and c0 < b and r1 > x and c1 > y

def center_pack(seq, width):
    n=len(seq)
    left=(width-n)//2
    return [0]*left + seq + [0]*(width-left-n)

def first_appearance_palette(g):
    return colors_present(g)

def center_of_bbox(b):
    r0,c0,r1,c1=b
    return ((r0+r1)/2.0,(c0+c1)/2.0)

def dilate_cells(cells, h, w, radius1=True):
    out=set()
    for r,c in cells:
        out.add((r,c))
        for dr,dc in DIR4:
            nr,nc=r+dr,c+dc
            if 0<=nr<h and 0<=nc<w:
                out.add((nr,nc))
    return out

def normalize_object_cells(cells):
    r0,c0,r1,c1=bbox_of_cells(cells)
    return {(r-r0,c-c0) for r,c in cells}, (r1-r0+1, c1-c0+1)

TRANSFORM_MAP = {
    1: lambda g: g,
    2: rotate_cw,
    3: rotate_180,
    4: flip_h,
}

def solve_f_f01_center_pack_rows(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        seq=[v for v in row if v!=0]
        packed=center_pack(seq,w)
        out[r]=packed
    return out

def solve_f_f02_keep_rectangle_corners(g):
    h,w=dims(g)
    out=blank(h,w)
    for obj in objects4(g):
        color=obj['color']
        r0,c0,r1,c1=object_bbox(obj)
        # assume filled rectangle
        for r,c in [(r0,c0),(r0,c1),(r1,c0),(r1,c1)]:
            out[r][c]=color
    return out

def solve_f_f03_knight_halo(g):
    h,w=dims(g)
    out=blank(h,w)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                out[r][c]=v
                for dr,dc in KNIGHT:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out

def solve_f_f04_top_marker_deletes_color(g):
    h,w=dims(g)
    marker_positions=[(0,c) for c,v in enumerate(g[0]) if v!=0]
    assert len(marker_positions)==1
    mr,mc=marker_positions[0]
    color=g[mr][mc]
    out=copy_grid(g)
    for r in range(h):
        for c in range(w):
            if out[r][c]==color and (r,c)!=(mr,mc):
                out[r][c]=0
    return out

def solve_f_f05_keep_diagonal_pairs(g):
    h,w=dims(g)
    out=blank(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0: continue
            keep=False
            for dr,dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and g[nr][nc]==v:
                    keep=True
                    break
            if keep:
                out[r][c]=v
    return out

def solve_f_f06_bottom_pack_columns(g):
    h,w=dims(g)
    out=blank(h,w)
    for c in range(w):
        col=[g[r][c] for r in range(h)]
        vals=[v for v in col if v!=0]
        for i,v in enumerate(vals):
            out[h-len(vals)+i][c]=v
    return out

def solve_f_f07_palette_row(g):
    pal=first_appearance_palette(g)
    return [pal] if pal else [[0]]

def solve_f_m01_recolor_by_holes(g):
    h,w=dims(g)
    out=blank(h,w)
    mapping={0:2,1:8,2:6,3:9}
    for obj in objects4(g):
        holes=hole_count_for_object(g,obj)
        newc=mapping.get(holes,9)
        for r,c in obj['cells']:
            out[r][c]=newc
    return out

def solve_f_m02_corner_marker_selects_nearest_object(g):
    h,w=dims(g)
    corners=[(0,0),(0,w-1),(h-1,0),(h-1,w-1)]
    marker=None
    for r,c in corners:
        if g[r][c]!=0:
            marker=(r,c); break
    assert marker is not None
    marker_set={marker}
    objs=[obj for obj in objects4(g) if marker not in obj['cells']]
    # min distance from marker to any cell
    best=min(objs, key=lambda obj:min(manhattan(marker,cell) for cell in obj['cells']))
    return crop_object_grid(g,best)

def solve_f_m03_symmetry_mosaic(g):
    objs=objects4(g)
    assert len(objs)==1
    objg=crop_object_grid(g,objs[0])
    tl=objg
    tr=flip_h(objg)
    bl=flip_v(objg)
    br=rotate_180(objg)
    h,w=dims(objg)
    out=blank(h*2,w*2)
    place_grid_at(out, tl, 0, 0)
    place_grid_at(out, tr, 0, w)
    place_grid_at(out, bl, h, 0)
    place_grid_at(out, br, h, w)
    return out

def solve_f_m04_object_halos(g):
    h,w=dims(g)
    out=blank(h,w)
    for obj in objects4(g):
        cells=set(obj['cells']); color=obj['color']
        halo=set()
        for r,c in cells:
            for dr,dc in DIR4:
                nr,nc=r+dr,c+dc
                if 0<=nr<h and 0<=nc<w and (nr,nc) not in cells:
                    halo.add((nr,nc))
        for r,c in halo:
            # only fill if background in original to avoid overwriting other objects
            if g[r][c]==0:
                out[r][c]=color
    return out

def solve_f_m05_keep_innermost_frame(g):
    h,w=dims(g)
    frames=[obj for obj in objects4(g) if is_frame_object(obj)]
    depths=[]
    for obj in frames:
        b=object_bbox(obj)
        depth=sum(contains_bbox(object_bbox(other), b) for other in frames if other is not obj)
        depths.append((depth, obj))
    _,best=max(depths, key=lambda t:t[0])
    out=blank(h,w)
    for r,c in best['cells']:
        out[r][c]=best['color']
    return out

def solve_f_m06_stack_objects_by_x(g):
    objs=objects4(g)
    objs=sorted(objs, key=lambda obj:(object_bbox(obj)[1], object_bbox(obj)[0]))
    crops=[crop_object_grid(g,obj) for obj in objs]
    maxw=max(dims(c)[1] for c in crops)
    totalh=sum(dims(c)[0] for c in crops)+max(0,len(crops)-1)
    out=blank(totalh,maxw)
    r0=0
    for i,crop in enumerate(crops):
        place_grid_at(out,crop,r0,0)
        r0 += dims(crop)[0]
        if i != len(crops)-1:
            r0 += 1
    return out

def solve_f_m07_bottom_key_recolors_objects(g):
    h,w=dims(g)
    key=[v for v in g[h-1] if v!=0]
    out=blank(h,w)
    objs=[obj for obj in objects4(g) if all(r != h-1 for r,c in obj['cells'])]
    objs=sorted(objs, key=lambda obj:(object_bbox(obj)[1], object_bbox(obj)[0]))
    for i,obj in enumerate(objs):
        newc=key[i]
        for r,c in obj['cells']:
            out[r][c]=newc
    return out

def solve_f_h01_recolor_by_frame_depth(g):
    h,w=dims(g)
    frames=[obj for obj in objects4(g) if is_frame_object(obj)]
    others=[obj for obj in objects4(g) if not is_frame_object(obj)]
    out=blank(h,w)
    mapping={1:2,2:3,3:8,4:6}
    frame_bboxes=[object_bbox(f) for f in frames]
    for obj in others:
        b=object_bbox(obj)
        center=((b[0]+b[2])/2.0,(b[1]+b[3])/2.0)
        depth=0
        for fb in frame_bboxes:
            r0,c0,r1,c1=fb
            # use bbox center containment
            if r0 < center[0] < r1 and c0 < center[1] < c1:
                depth += 1
        newc=mapping.get(depth,1)
        for r,c in obj['cells']:
            out[r][c]=newc
    return out

def solve_f_h02_move_objects_to_nearest_markers(g):
    h,w=dims(g)
    # markers are singleton cells on empty background and colors 1..9; objects are larger components
    objs=[]
    markers=[]
    for obj in objects4(g):
        if len(obj['cells'])==1:
            markers.append(obj)
        else:
            objs.append(obj)
    assigned={}
    remaining_markers=markers[:]
    # greedy by object size descending to reduce weirdness
    for obj in sorted(objs, key=lambda o:-len(o['cells'])):
        b=object_bbox(obj)
        cr,cc=center_of_bbox(b)
        marker=min(remaining_markers, key=lambda m: manhattan((cr,cc), m['cells'][0]))
        remaining_markers.remove(marker)
        assigned[id(obj)]=marker
    out=blank(h,w)
    for obj in objs:
        marker=assigned[id(obj)]
        mr,mc=marker['cells'][0]
        norm,(hh,ww)=normalize_object_cells(obj['cells'])
        top=mr - hh//2
        left=mc - ww//2
        for r,c in norm:
            rr,cc=top+r,left+c
            if 0<=rr<h and 0<=cc<w:
                out[rr][cc]=marker['color']
    return out

def solve_f_h03_keyrow_transform_strip(g):
    h,w=dims(g)
    keys=[v for v in g[0] if v!=0]
    # unique template object below first row
    sub=g[1:]
    # shift object coords not needed if cropping
    objs=objects4(sub)
    assert len(objs)==1
    template=crop_object_grid(sub,objs[0])
    variants=[TRANSFORM_MAP[k](template) for k in keys]
    heights=[dims(v)[0] for v in variants]
    widths=[dims(v)[1] for v in variants]
    out=blank(max(heights), sum(widths)+max(0,len(variants)-1))
    c0=0
    for i,var in enumerate(variants):
        place_grid_at(out,var,0,c0)
        c0 += dims(var)[1]
        if i != len(variants)-1:
            c0 += 1
    return out

def solve_f_h04_normalized_difference(g):
    objs=sorted(objects4(g), key=lambda o: object_bbox(o)[1])
    assert len(objs)==2
    a,b=objs
    acells, (ah,aw)=normalize_object_cells(a['cells'])
    bcells, (bh,bw)=normalize_object_cells(b['cells'])
    h=max(ah,bh); w=max(aw,bw)
    out=blank(h,w)
    for r,c in acells:
        if (r,c) not in bcells:
            out[r][c]=a['color']
    return out

def solve_f_h05_recolor_by_contact_degree(g):
    h,w=dims(g)
    objs=objects4(g)
    dilations=[]
    for obj in objs:
        dilations.append(dilate_cells(set(obj['cells']), h, w))
    out=blank(h,w)
    mapping={0:2,1:3,2:8,3:6,4:9}
    for i,obj in enumerate(objs):
        degree=0
        for j,other in enumerate(objs):
            if i==j: continue
            if dilations[i] & dilations[j]:
                degree += 1
        newc=mapping.get(degree,9)
        for r,c in obj['cells']:
            out[r][c]=newc
    return out

def solve_f_h06_multi_pair_paths(g):
    h,w=dims(g)
    order = g[0][0]  # 1 horizontal-then-vertical, 2 vertical-then-horizontal
    positions=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and not (r==0 and c==0):
                positions[v].append((r,c))
    out=copy_grid(g)
    for color,cells in positions.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        if order==1:
            # horizontal then vertical
            step=1 if c2>=c1 else -1
            for c in range(c1,c2+step,step):
                out[r1][c]=color
            step=1 if r2>=r1 else -1
            for r in range(r1,r2+step,step):
                out[r][c2]=color
        else:
            step=1 if r2>=r1 else -1
            for r in range(r1,r2+step,step):
                out[r][c1]=color
            step=1 if c2>=c1 else -1
            for c in range(c1,c2+step,step):
                out[r2][c]=color
    return out

def solve_f_h07_interleave_rows_of_two_objects(g):
    objs=sorted(objects4(g), key=lambda o: object_bbox(o)[1])
    assert len(objs)==2
    ga=crop_object_grid(g,objs[0])
    gb=crop_object_grid(g,objs[1])
    ha,wa=dims(ga); hb,wb=dims(gb)
    h=max(ha,hb); w=max(wa,wb)
    pa=blank(h,w); pb=blank(h,w)
    place_grid_at(pa,ga,0,0); place_grid_at(pb,gb,0,0)
    out=blank(h*2,w)
    for r in range(h):
        out[2*r]=pa[r][:]
        out[2*r+1]=pb[r][:]
    return out

SOLVERS = {
    "easy_f01": solve_f_f01_center_pack_rows,
    "easy_f02": solve_f_f02_keep_rectangle_corners,
    "easy_f03": solve_f_f03_knight_halo,
    "easy_f04": solve_f_f04_top_marker_deletes_color,
    "easy_f05": solve_f_f05_keep_diagonal_pairs,
    "easy_f06": solve_f_f06_bottom_pack_columns,
    "easy_f07": solve_f_f07_palette_row,
    "medium_f01": solve_f_m01_recolor_by_holes,
    "medium_f02": solve_f_m02_corner_marker_selects_nearest_object,
    "medium_f03": solve_f_m03_symmetry_mosaic,
    "medium_f04": solve_f_m04_object_halos,
    "medium_f05": solve_f_m05_keep_innermost_frame,
    "medium_f06": solve_f_m06_stack_objects_by_x,
    "medium_f07": solve_f_m07_bottom_key_recolors_objects,
    "hard_f01": solve_f_h01_recolor_by_frame_depth,
    "hard_f02": solve_f_h02_move_objects_to_nearest_markers,
    "hard_f03": solve_f_h03_keyrow_transform_strip,
    "hard_f04": solve_f_h04_normalized_difference,
    "hard_f05": solve_f_h05_recolor_by_contact_degree,
    "hard_f06": solve_f_h06_multi_pair_paths,
    "hard_f07": solve_f_h07_interleave_rows_of_two_objects,
}
