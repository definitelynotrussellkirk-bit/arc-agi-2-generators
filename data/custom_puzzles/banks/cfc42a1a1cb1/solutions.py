from __future__ import annotations
import json
from pathlib import Path
from typing import List
import collections

Grid = List[List[int]]

def zeros(h,w,val=0):
    return [[val for _ in range(w)] for _ in range(h)]

def clone(g):
    return [row[:] for row in g]

def dims(g):
    return len(g), len(g[0])

def bbox(cells):
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g, box):
    r0,c0,r1,c1 = box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    return crop_bbox(g, bbox(cells))

def stamp(g,obj,top,left,transparent=0):
    h,w=dims(g)
    oh,ow=dims(obj)
    for r in range(oh):
        for c in range(ow):
            v=obj[r][c]
            if v!=transparent:
                rr,cc=top+r,left+c
                if 0 <= rr < h and 0 <= cc < w:
                    g[rr][cc]=v
    return g

def countmap_stamp(counts,obj,top,left,transparent=0):
    h,w=dims(counts)
    oh,ow=dims(obj)
    for r in range(oh):
        for c in range(ow):
            v=obj[r][c]
            if v!=transparent:
                rr,cc=top+r,left+c
                if 0 <= rr < h and 0 <= cc < w:
                    counts[rr][cc]+=1
    return counts

def hflip(g):
    return [list(reversed(row)) for row in g]

def vflip(g):
    return list(reversed([row[:] for row in g]))

def rot90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rot180(g):
    return rot90(rot90(g))

def rot270(g):
    return rot90(rot180(g))

def transpose(g):
    h,w=dims(g)
    return [[g[r][c] for r in range(h)] for c in range(w)]

def scale2(g):
    out=[]
    for row in g:
        expanded=[]
        for v in row:
            expanded.extend([v,v])
        out.append(expanded[:])
        out.append(expanded[:])
    return out

def normalize_shape(g):
    cg=crop_nonzero(g)
    return [[1 if v!=0 else 0 for v in row] for row in cg]

def recolor_mask(mask,color):
    return [[color if v else 0 for v in row] for row in mask]

def connected_components(g, ignore_positions=None, colors=None):
    if ignore_positions is None:
        ignore_positions=set()
    else:
        ignore_positions=set(ignore_positions)
    colors = None if colors is None else set(colors)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in ignore_positions:
                seen[r][c]=True
                continue
            v=g[r][c]
            if v==0 or seen[r][c] or (colors is not None and v not in colors):
                continue
            seen[r][c]=True
            dq=collections.deque([(r,c)])
            cells=[]
            while dq:
                rr,cc=dq.popleft()
                cells.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and (nr,nc) not in ignore_positions and g[nr][nc]==v and (colors is None or v in colors):
                        seen[nr][nc]=True
                        dq.append((nr,nc))
            comps.append({"color":v, "cells":cells, "bbox":bbox(cells), "area":len(cells)})
    return comps

def find_holes_binary(mask):
    h,w=dims(mask)
    seen=[[False]*w for _ in range(h)]
    holes=[]
    for r in range(h):
        for c in range(w):
            if mask[r][c]!=0 or seen[r][c]:
                continue
            dq=collections.deque([(r,c)])
            seen[r][c]=True
            cells=[]
            touches=False
            while dq:
                rr,cc=dq.popleft()
                cells.append((rr,cc))
                if rr in (0,h-1) or cc in (0,w-1):
                    touches=True
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0 <= nr < h and 0 <= nc < w and mask[nr][nc]==0 and not seen[nr][nc]:
                        seen[nr][nc]=True
                        dq.append((nr,nc))
            if not touches:
                holes.append(cells)
    return holes

def count_holes_binary(g):
    arr=[[1 if v!=0 else 0 for v in row] for row in crop_nonzero(g)]
    return len(find_holes_binary(arr))

def fill_holes_same_color(obj):
    color=max(v for row in obj for v in row)
    mask=[[1 if v!=0 else 0 for v in row] for row in obj]
    holes=find_holes_binary(mask)
    out=clone(obj)
    for hole in holes:
        for r,c in hole:
            out[r][c]=color
    return out

def object_crop_from_component(g, comp):
    return crop_bbox(g, comp["bbox"])

def sort_components_reading(comps):
    return sorted(comps, key=lambda comp:(comp["bbox"][0], comp["bbox"][1]))

def sort_components_by_area_desc(comps):
    return sorted(comps, key=lambda comp:(-comp["area"], comp["bbox"][0], comp["bbox"][1]))

def apply_transform_code(obj, code):
    if code==1: return clone(obj)
    if code==2: return rot90(obj)
    if code==3: return rot180(obj)
    if code==4: return rot270(obj)
    if code==5: return hflip(obj)
    if code==6: return vflip(obj)
    if code==7: return transpose(obj)
    raise ValueError(code)

def same_under_rotation(a,b):
    aa=normalize_shape(a)
    bb=normalize_shape(b)
    cur=aa
    for _ in range(4):
        if cur==bb:
            return True
        cur=rot90(cur)
    return False


def solve_easy_99_fill_main_diagonal_spans(g):
    h,w=dims(g)
    out=clone(g)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[(v, r-c)].append((r,c))
    for (color, diag), cells in groups.items():
        if len(cells) >= 2:
            rows=sorted(r for r,c in cells)
            r0,r1=rows[0], rows[-1]
            for r in range(r0, r1+1):
                c=r-diag
                if 0 <= c < w:
                    out[r][c]=color
    return out

def solve_easy_100_fill_antidiagonal_spans(g):
    h,w=dims(g)
    out=clone(g)
    groups=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                groups[(v, r+c)].append((r,c))
    for (color, diag), cells in groups.items():
        if len(cells) >= 2:
            rows=sorted(r for r,c in cells)
            r0,r1=rows[0], rows[-1]
            s=diag
            for r in range(r0, r1+1):
                c=s-r
                if 0 <= c < w:
                    out[r][c]=color
    return out

def solve_easy_101_stamp_hollow_3x3_rings(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(1,h-1):
        for c in range(1,w-1):
            color=g[r][c]
            if color!=0:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if not (dr==0 and dc==0):
                            out[r+dr][c+dc]=color
    return out

def solve_easy_102_stamp_x_shapes_at_markers(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(1,h-1):
        for c in range(1,w-1):
            color=g[r][c]
            if color!=0:
                for dr,dc in ((0,0),(-1,-1),(-1,1),(1,-1),(1,1)):
                    out[r+dr][c+dc]=color
    return out

def solve_easy_103_fill_rectangles_from_opposite_corners(g):
    out=clone(g)
    pos=collections.defaultdict(list)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v!=0:
                pos[v].append((r,c))
    for color, cells in pos.items():
        if len(cells) >= 2:
            r0=min(r for r,c in cells)
            r1=max(r for r,c in cells)
            c0=min(c for r,c in cells)
            c1=max(c for r,c in cells)
            for r in range(r0,r1+1):
                for c in range(c0,c1+1):
                    out[r][c]=color
    return out

def solve_easy_104_read_singleton_colors_left_to_right(g):
    cells=[(r,c,v) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    cells.sort(key=lambda t:(t[1], t[0]))
    return [[v for r,c,v in cells]]

def solve_easy_105_crop_the_unique_object(g):
    return crop_nonzero(g)

def solve_medium_99_transform_object_by_corner_code(g):
    code=g[0][0]
    h,w=dims(g)
    work=clone(g)
    work[0][0]=0
    obj=crop_nonzero(work)
    return apply_transform_code(obj, code)

def solve_medium_100_select_object_by_key_and_scale2(g):
    h,w=dims(g)
    key=g[h-1][0]
    work=clone(g)
    work[h-1][0]=0
    comps=connected_components(work, colors={key})
    comp=max(comps, key=lambda comp:(comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    obj=object_crop_from_component(work, comp)
    return scale2(obj)

def solve_medium_101_stamp_prototype_at_all_anchors(g):
    h,w=dims(g)
    out=zeros(h,w)
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    comps=connected_components(g, colors=set(range(1,9)))
    proto=max(comps, key=lambda comp: comp["area"])
    proto_obj=object_crop_from_component(g, proto)
    stamp(out, proto_obj, proto["bbox"][0], proto["bbox"][1])
    for r,c in anchors:
        stamp(out, proto_obj, r, c)
    return out

def solve_medium_102_frame_each_object_with_key_color(g):
    h,w=dims(g)
    key=g[0][w-1]
    out=clone(g)
    comps=connected_components(g, ignore_positions={(0,w-1)})
    for comp in comps:
        r0,c0,r1,c1=comp["bbox"]
        for c in range(c0,c1+1):
            out[r0][c]=key
            out[r1][c]=key
        for r in range(r0,r1+1):
            out[r][c0]=key
            out[r][c1]=key
    out[0][w-1]=key
    return out

def solve_medium_103_pack_objects_by_area_descending(g):
    comps=sort_components_by_area_desc(connected_components(g))
    crops=[object_crop_from_component(g, comp) for comp in comps]
    width=max(len(crop[0]) for crop in crops)
    height=sum(len(crop) for crop in crops) + (len(crops)-1)
    out=zeros(height, width)
    rr=0
    for i,crop in enumerate(crops):
        for r,row in enumerate(crop):
            for c,v in enumerate(row):
                out[rr+r][c]=v
        rr += len(crop)
        if i != len(crops)-1:
            rr += 1
    return out

def solve_medium_104_read_frame_majorities_into_row(g):
    h,w=dims(g)
    frames=[]
    for r in range(h-4):
        for c in range(w-4):
            # detect 5x5 frame of 8s
            ok=True
            for k in range(5):
                if g[r][c+k]!=8 or g[r+4][c+k]!=8 or g[r+k][c]!=8 or g[r+k][c+4]!=8:
                    ok=False
                    break
            if ok:
                frames.append((r,c))
    # remove duplicates from overlapping scans
    uniq=[]
    seen=set()
    for rc in frames:
        if rc not in seen:
            uniq.append(rc); seen.add(rc)
    uniq.sort(key=lambda t:(t[1], t[0]))
    out=[]
    for r,c in uniq:
        counts=collections.Counter()
        for rr in range(r+1,r+4):
            for cc in range(c+1,c+4):
                v=g[rr][cc]
                if v!=0:
                    counts[v]+=1
        best=max(counts.items(), key=lambda kv:(kv[1], -kv[0]))[0]
        out.append(best)
    return [out]

def solve_medium_105_fill_the_hole_of_the_holed_object(g):
    comps=connected_components(g)
    holed=[]
    for comp in comps:
        crop=object_crop_from_component(g, comp)
        holes=count_holes_binary(crop)
        if holes>0:
            holed.append((holes, comp, crop))
    holes, comp, crop = max(holed, key=lambda t:(t[0], t[1]["area"]))
    return fill_holes_same_color(crop)

def solve_hard_99_decode_template_transform_gallery(g):
    templates = {
        1: [row[0:4] for row in g[0:4]],
        2: [row[5:9] for row in g[0:4]],
        3: [row[10:14] for row in g[0:4]],
    }
    tid = [row[0:2] for row in g[6:8]]
    tcode = [row[3:5] for row in g[6:8]]
    cell_h=4; cell_w=4
    out=zeros(cell_h*2+1, cell_w*2+1)
    for gr in range(2):
        for gc in range(2):
            template=clone(templates[tid[gr][gc]])
            transformed=apply_transform_code(template, tcode[gr][gc])
            top=gr*(cell_h+1)
            left=gc*(cell_w+1)
            stamp(out, transformed, top, left)
    return out

def solve_hard_100_build_rotation_equivalence_matrix(g):
    comps=sort_components_reading(connected_components(g))
    objs=[object_crop_from_component(g, comp) for comp in comps]
    n=len(objs)
    out=zeros(n,n)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=1
            elif same_under_rotation(objs[i], objs[j]):
                out[i][j]=2
            else:
                out[i][j]=0
    return out

def solve_hard_101_fill_chambers_by_dot_count_legend(g):
    h,w=dims(g)
    legend={c:v for c,v in enumerate(g[0]) if v!=0}
    out=clone(g)
    seen=[[False]*w for _ in range(h)]
    for r in range(1,h):
        for c in range(w):
            if g[r][c]==0 and not seen[r][c]:
                dq=collections.deque([(r,c)])
                seen[r][c]=True
                cells=[]
                while dq:
                    rr,cc=dq.popleft()
                    cells.append((rr,cc))
                    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr,nc=rr+dr,cc+dc
                        if 1 <= nr < h and 0 <= nc < w and g[nr][nc]==0 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            dq.append((nr,nc))
                cellset=set(cells)
                dots=[]
                r0=min(rr for rr,cc in cells); r1=max(rr for rr,cc in cells)
                c0=min(cc for rr,cc in cells); c1=max(cc for rr,cc in cells)
                for rr in range(max(1,r0-1), min(h-1,r1+1)+1):
                    for cc in range(max(0,c0-1), min(w-1,c1+1)+1):
                        if g[rr][cc]==1:
                            for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                                if (rr+dr,cc+dc) in cellset:
                                    dots.append((rr,cc))
                                    break
                n=len(dots)
                if n in legend:
                    color=legend[n]
                    for rr,cc in cells + dots:
                        out[rr][cc]=color
    return out

def solve_hard_102_select_symmetric_object_rotate_and_scale2(g):
    h,w=dims(g)
    code=g[h-1][w-1]
    work=clone(g)
    work[h-1][w-1]=0
    comps=connected_components(work)
    candidates=[]
    for comp in comps:
        crop=object_crop_from_component(work, comp)
        if crop == hflip(crop) and crop == vflip(crop):
            candidates.append((comp["area"], comp, crop))
    _, comp, crop = max(candidates, key=lambda t:t[0])
    transformed=apply_transform_code(crop, {1:2, 2:3, 3:4}[code])
    return scale2(transformed)

def solve_hard_103_overlay_anchor_stamps_into_count_map(g):
    h,w=dims(g)
    anchors=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v==9]
    comps=connected_components(g, colors=set(range(1,9)))
    proto=max(comps, key=lambda comp: comp["area"])
    proto_obj=normalize_shape(object_crop_from_component(g, proto))
    counts=zeros(h,w)
    for r,c in anchors:
        countmap_stamp(counts, proto_obj, r, c, transparent=0)
    return counts

def solve_hard_104_build_shape_color_cross_product_gallery(g):
    colors=[v for v in g[0] if v!=0]
    shapes=[
        [row[0:3] for row in g[2:5]],
        [row[4:7] for row in g[2:5]],
        [row[8:11] for row in g[2:5]],
    ]
    masks=[normalize_shape(shape) for shape in shapes]
    cell=3
    out=zeros(cell*3+2, cell*3+2)
    for i,mask in enumerate(masks):
        for j,color in enumerate(colors):
            tile=recolor_mask(mask, color)
            stamp(out, tile, i*(cell+1), j*(cell+1))
    return out

def solve_hard_105_select_by_key_and_apply_transform_sequence(g):
    h,w=dims(g)
    seq=[v for v in g[0] if v!=0]
    key=g[h-1][0]
    work=clone(g)
    work[0]=[0]*w
    work[h-1][0]=0
    comps=connected_components(work, colors={key})
    comp=max(comps, key=lambda comp: comp["area"])
    obj=object_crop_from_component(work, comp)
    for code in seq:
        obj=apply_transform_code(obj, {1:2, 2:5, 3:7, 4:6}[code])
    return obj


SOLVERS = {
    "solve_easy_99_fill_main_diagonal_spans": solve_easy_99_fill_main_diagonal_spans,
    "solve_easy_100_fill_antidiagonal_spans": solve_easy_100_fill_antidiagonal_spans,
    "solve_easy_101_stamp_hollow_3x3_rings": solve_easy_101_stamp_hollow_3x3_rings,
    "solve_easy_102_stamp_x_shapes_at_markers": solve_easy_102_stamp_x_shapes_at_markers,
    "solve_easy_103_fill_rectangles_from_opposite_corners": solve_easy_103_fill_rectangles_from_opposite_corners,
    "solve_easy_104_read_singleton_colors_left_to_right": solve_easy_104_read_singleton_colors_left_to_right,
    "solve_easy_105_crop_the_unique_object": solve_easy_105_crop_the_unique_object,
    "solve_medium_99_transform_object_by_corner_code": solve_medium_99_transform_object_by_corner_code,
    "solve_medium_100_select_object_by_key_and_scale2": solve_medium_100_select_object_by_key_and_scale2,
    "solve_medium_101_stamp_prototype_at_all_anchors": solve_medium_101_stamp_prototype_at_all_anchors,
    "solve_medium_102_frame_each_object_with_key_color": solve_medium_102_frame_each_object_with_key_color,
    "solve_medium_103_pack_objects_by_area_descending": solve_medium_103_pack_objects_by_area_descending,
    "solve_medium_104_read_frame_majorities_into_row": solve_medium_104_read_frame_majorities_into_row,
    "solve_medium_105_fill_the_hole_of_the_holed_object": solve_medium_105_fill_the_hole_of_the_holed_object,
    "solve_hard_99_decode_template_transform_gallery": solve_hard_99_decode_template_transform_gallery,
    "solve_hard_100_build_rotation_equivalence_matrix": solve_hard_100_build_rotation_equivalence_matrix,
    "solve_hard_101_fill_chambers_by_dot_count_legend": solve_hard_101_fill_chambers_by_dot_count_legend,
    "solve_hard_102_select_symmetric_object_rotate_and_scale2": solve_hard_102_select_symmetric_object_rotate_and_scale2,
    "solve_hard_103_overlay_anchor_stamps_into_count_map": solve_hard_103_overlay_anchor_stamps_into_count_map,
    "solve_hard_104_build_shape_color_cross_product_gallery": solve_hard_104_build_shape_color_cross_product_gallery,
    "solve_hard_105_select_by_key_and_apply_transform_sequence": solve_hard_105_select_by_key_and_apply_transform_sequence,
}

def verify_against_bank(json_path: str | Path | None = None):
    if json_path is None:
        json_path = Path(__file__).with_name("arc_puzzle_bank_fifteenth_21.json")
    data = json.loads(Path(json_path).read_text())
    mismatches=[]
    for task in data:
        fn=SOLVERS[task["solver_name"]]
        for split in ("train","test"):
            for i,pair in enumerate(task[split]):
                got=fn(pair["input"])
                if got != pair["output"]:
                    mismatches.append((task["id"], split, i))
    return mismatches

if __name__ == "__main__":
    mismatches = verify_against_bank()
    if mismatches:
        print("MISMATCHES:", mismatches)
        raise SystemExit(1)
    print("All tasks verified against the stored bank.")
