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
    return min(rs),min(cs),max(rs),max(cs)


def crop_bbox(g, box):
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    if not cells:
        return [[0]]
    rs=[r for r,c in cells]; cs=[c for r,c in cells]
    r0,r1=min(rs),max(rs); c0,c1=min(cs),max(cs)
    return [row[c0:c1+1] for row in g[r0:r1+1]]


def connected_components(g, colors=None):
    colors = None if colors is None else set(colors)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v==0 or seen[r][c] or (colors is not None and v not in colors):
                continue
            seen[r][c]=True
            q=collections.deque([(r,c)])
            cells=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and g[nr][nc]==v and (colors is None or v in colors):
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({"color":v, "cells":cells, "bbox":bbox(cells), "area":len(cells)})
    return comps


def count_holes_binary(g):
    arr=[[1 if v!=0 else 0 for v in row] for row in crop_nonzero(g)]
    h,w=dims(arr)
    seen=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if arr[r][c]==0 and not seen[r][c]:
                seen[r][c]=True
                q=collections.deque([(r,c)])
                touches=False
                while q:
                    rr,cc=q.popleft()
                    if rr in (0,h-1) or cc in (0,w-1):
                        touches=True
                    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and arr[nr][nc]==0 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                if not touches:
                    holes += 1
    return holes


def scale2(g):
    h,w=dims(g)
    out=zeros(h*2,w*2)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            out[2*r][2*c]=out[2*r+1][2*c]=out[2*r][2*c+1]=out[2*r+1][2*c+1]=v
    return out


def rotate_cw(g):
    h,w = dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate_ccw(g):
    h,w = dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w)]


def rotate_180(g):
    return [row[::-1] for row in g[::-1]]


def flip_h(g):
    return [row[::-1] for row in g]


def flip_v(g):
    return g[::-1]


def hstack(grids, gap=1, bg=0):
    if not grids: return [[]]
    h=max(len(g) for g in grids)
    w=sum(len(g[0]) for g in grids)+gap*(len(grids)-1)
    out=zeros(h,w,bg)
    x=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        top=(h-gh)//2
        for r in range(gh):
            for c in range(gw):
                v=g[r][c]
                if v!=bg:
                    out[top+r][x+c]=v
        x+=gw
        if i < len(grids)-1: x+=gap
    return out


def vstack(grids, gap=1, bg=0):
    if not grids: return [[]]
    w=max(len(g[0]) for g in grids)
    h=sum(len(g) for g in grids)+gap*(len(grids)-1)
    out=zeros(h,w,bg)
    y=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        left=(w-gw)//2
        for r in range(gh):
            for c in range(gw):
                v=g[r][c]
                if v!=bg:
                    out[y+r][left+c]=v
        y+=gh
        if i < len(grids)-1: y+=gap
    return out


def draw_rect_border(g,r0,c0,r1,c1,color):
    for c in range(c0,c1+1):
        g[r0][c]=g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=g[r][c1]=color


def fill_rect(g,r0,c0,r1,c1,color):
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            g[r][c]=color


def apply_transform(g, code):
    if code==1: return g
    if code==2: return rotate_cw(g)
    if code==3: return rotate_180(g)
    if code==4: return rotate_ccw(g)
    if code==5: return flip_h(g)
    if code==6: return flip_v(g)
    raise ValueError(code)


def normalize_shape(g):
    return tuple(tuple(1 if v!=0 else 0 for v in row) for row in crop_nonzero(g))


def rotations(g):
    cur=crop_nonzero([[1 if v!=0 else 0 for v in row] for row in g])
    out=[]
    for _ in range(4):
        out.append(tuple(tuple(row) for row in cur))
        cur=rotate_cw(cur)
    return set(out)


def dihedral(g):
    cur=crop_nonzero([[1 if v!=0 else 0 for v in row] for row in g])
    variants=[]
    bases=[cur, flip_h(cur)]
    for base in bases:
        c=base
        for _ in range(4):
            variants.append(tuple(tuple(row) for row in c))
            c=rotate_cw(c)
    return set(variants)



def solve_easy_92_fill_horizontal_intervals(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        pos=collections.defaultdict(list)
        for c,v in enumerate(g[r]):
            if v!=0:
                pos[v].append(c)
        for color, cols in pos.items():
            if len(cols) >= 2:
                for c in range(min(cols), max(cols)+1):
                    out[r][c] = color
    return out


def solve_easy_93_fill_vertical_intervals(g):
    h,w=dims(g)
    out=clone(g)
    for c in range(w):
        pos=collections.defaultdict(list)
        for r in range(h):
            v=g[r][c]
            if v!=0:
                pos[v].append(r)
        for color, rows in pos.items():
            if len(rows) >= 2:
                for r in range(min(rows), max(rows)+1):
                    out[r][c] = color
    return out


def solve_easy_94_mirror_left_panel_to_right(g):
    h,w=dims(g)
    divider=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            divider=c; break
    assert divider is not None
    out=clone(g)
    for r in range(h):
        for c in range(divider):
            if g[r][c] != 0:
                out[r][2*divider - c] = g[r][c]
    return out


def solve_easy_95_draw_rectangle_borders_from_diagonal_corners(g):
    h,w=dims(g)
    out=zeros(h,w)
    pos=collections.defaultdict(list)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)>=2:
            r0=min(r for r,c in cells); r1=max(r for r,c in cells)
            c0=min(c for r,c in cells); c1=max(c for r,c in cells)
            draw_rect_border(out,r0,c0,r1,c1,color)
    return out


def solve_easy_96_keep_centers_of_odd_rectangles(g):
    h,w=dims(g)
    out=zeros(h,w)
    for comp in connected_components(g):
        r0,c0,r1,c1=comp["bbox"]
        rr=(r0+r1)//2
        cc=(c0+c1)//2
        out[rr][cc]=comp["color"]
    return out


def solve_easy_97_mirror_top_panel_to_bottom(g):
    h,w=dims(g)
    divider=None
    for r in range(h):
        if all(v==5 for v in g[r]):
            divider=r; break
    assert divider is not None
    out=clone(g)
    for r in range(divider):
        for c in range(w):
            if g[r][c] != 0:
                out[2*divider-r][c] = g[r][c]
    return out


def solve_easy_98_stamp_pluses_at_markers(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                for dr,dc in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    if 0<=nr<h and 0<=nc<w:
                        out[nr][nc]=v
    return out


def solve_medium_92_crop_component_selected_by_bottom_key(g):
    h,w=dims(g)
    key = next(v for v in g[h-1] if v != 0)
    comps = [comp for comp in connected_components(g[:-1]) if comp["color"] == key]
    comp = comps[0]
    return crop_bbox(g[:-1], comp["bbox"])


def solve_medium_93_rotate_object_by_top_code(g):
    code = next(v for v in g[0] if v != 0)
    obj = crop_nonzero(g[1:])
    return apply_transform(obj, code)


def solve_medium_94_fill_matching_row_column_intersections(g):
    h,w=dims(g)
    out=clone(g)
    # assume outer frame 5 at border, row markers on row1, col markers on col1
    row_colors = {r:g[r][1] for r in range(2,h-1) if g[r][1] not in (0,5)}
    col_colors = {c:g[1][c] for c in range(2,w-1) if g[1][c] not in (0,5)}
    for r,color_r in row_colors.items():
        for c,color_c in col_colors.items():
            if color_r == color_c:
                out[r][c] = color_r
    return out


def solve_medium_95_cast_diagonal_rays_until_wall(g):
    h,w=dims(g)
    out=clone(g)
    # walls are 5, emitters are nonzero !=5
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0 and v!=5:
                for dr,dc in ((1,1),(1,-1),(-1,1),(-1,-1)):
                    nr,nc=r+dr,c+dc
                    while 0<=nr<h and 0<=nc<w and g[nr][nc]==0:
                        out[nr][nc]=v
                        nr += dr; nc += dc
    return out


def solve_medium_96_select_border_touching_object_and_recolor_by_key(g):
    h,w=dims(g)
    # key is singleton color 9? no, any nonzero cell in top-right corner row or bottom row outside objects. We'll define it as first nonzero in row0.
    key = next(v for v in g[0] if v != 0)
    comps = connected_components(g[1:])  # objects below top row
    # adjust bbox not needed, crop shapes from g[1:]
    out = zeros(h-1,w)
    for comp in comps:
        r0,c0,r1,c1=comp["bbox"]
        if r0==0 or c0==0 or r1==h-2 or c1==w-1:
            for r,c in comp["cells"]:
                out[r][c]=key
            break
    return out


def solve_medium_97_sort_cropped_objects_by_width_and_pack_horizontal(g):
    comps = connected_components(g)
    crops = [crop_bbox(g, comp["bbox"]) for comp in comps]
    crops = sorted(crops, key=lambda cg: (len(cg[0]), len(cg), min(v for row in cg for v in row if v!=0)))
    return hstack(crops, gap=1, bg=0)


def solve_medium_98_boolean_xor_of_two_halves(g):
    h,w=dims(g)
    divider=None
    for c in range(w):
        if all(g[r][c]==5 for r in range(h)):
            divider=c; break
    left=[row[:divider] for row in g]
    right=[row[divider+1:] for row in g]
    assert len(left[0]) == len(right[0])
    H,W=dims(left)
    out=zeros(H,W)
    for r in range(H):
        for c in range(W):
            a = left[r][c]!=0
            b = right[r][c]!=0
            if a ^ b:
                out[r][c] = 8
    return out


def solve_hard_92_decode_templates_into_2x2_gallery(g):
    # top 5 rows: 4 panels of width 5 separated by 1
    library={}
    top = g[:5]
    for i in range(4):
        x=i*6
        panel=[row[x:x+5] for row in top]
        cropped=crop_nonzero(panel)
        color=next(v for row in cropped for v in row if v!=0)
        library[color]=cropped
    code_row = g[6]
    pairs=[]
    i=0
    while i+1 < len(code_row):
        if code_row[i]==0:
            break
        pairs.append((code_row[i], code_row[i+1]))
        i+=2
    items=[apply_transform(library[color], code) for color,code in pairs[:4]]
    # arrange 2x2 with gap 1
    row1 = hstack(items[:2], gap=1, bg=0)
    row2 = hstack(items[2:4], gap=1, bg=0)
    return vstack([row1,row2], gap=1, bg=0)


def solve_hard_93_build_dihedral_equivalence_matrix(g):
    # four 5x5 panels side by side gap1
    panels=[]
    for i in range(4):
        x=i*6
        panel=[row[x:x+5] for row in g]
        panels.append(crop_nonzero(panel))
    rot_sets=[rotations(p) for p in panels]
    dih_sets=[dihedral(p) for p in panels]
    n=4
    out=zeros(n,n)
    for i in range(n):
        for j in range(n):
            if i==j:
                out[i][j]=8
            elif normalize_shape(panels[j]) in rot_sets[i]:
                out[i][j]=2
            elif normalize_shape(panels[j]) in dih_sets[i]:
                out[i][j]=6
            else:
                out[i][j]=0
    return out


def solve_hard_94_fill_chambers_by_legend_dot_count(g):
    legend=[v for v in g[0] if v!=0]
    sub=clone(g[2:])
    h,w=dims(sub)
    out=clone(sub)
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if sub[r][c] != 5 and not seen[r][c]:
                seen[r][c]=True
                q=collections.deque([(r,c)])
                cells=[]
                dot_count=0
                while q:
                    rr,cc=q.popleft()
                    cells.append((rr,cc))
                    if sub[rr][cc]==1:
                        dot_count += 1
                    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and sub[nr][nc] != 5 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                color=legend[dot_count-1]
                for rr,cc in cells:
                    out[rr][cc]=color
    full=clone(g)
    for r in range(h):
        full[r+2]=out[r]
    return full


def solve_hard_95_select_holed_object_rotate_and_scale2(g):
    code = next(v for v in g[0] if v!=0)
    comps=connected_components(g[1:])
    selected=None
    base=g[1:]
    for comp in comps:
        crop=crop_bbox(base, comp["bbox"])
        if count_holes_binary(crop)==1:
            selected=crop
            break
    assert selected is not None
    return scale2(apply_transform(selected, code))


def solve_hard_96_build_pairwise_intersection_gallery(g):
    panels=[]
    for i in range(3):
        x=i*6
        panel=[row[x:x+5] for row in g]
        panels.append(panel)
    def inter(a,b):
        h,w=dims(a)
        out=zeros(h,w)
        for r in range(h):
            for c in range(w):
                if a[r][c]!=0 and b[r][c]!=0:
                    out[r][c]=8
        return out
    items=[inter(panels[0], panels[1]), inter(panels[0], panels[2]), inter(panels[1], panels[2])]
    return hstack(items, gap=1, bg=0)


def solve_hard_97_cast_border_rays_and_mark_matching_intersections(g):
    h,w=dims(g)
    out=zeros(h,w)
    # preserve walls and emitters
    for r in range(h):
        for c in range(w):
            if g[r][c]==5 or (r==0 and g[r][c]!=0) or (c==0 and g[r][c]!=0):
                out[r][c]=g[r][c]
    vertical=[ [set() for _ in range(w)] for _ in range(h) ]
    horizontal=[ [set() for _ in range(w)] for _ in range(h) ]
    for c in range(1,w):
        color=g[0][c]
        if color not in (0,5):
            r=1
            while r<h and g[r][c]!=5:
                vertical[r][c].add(color)
                r += 1
    for r in range(1,h):
        color=g[r][0]
        if color not in (0,5):
            c=1
            while c<w and g[r][c]!=5:
                horizontal[r][c].add(color)
                c += 1
    for r in range(1,h):
        for c in range(1,w):
            if g[r][c]==5:
                out[r][c]=5
                continue
            common = vertical[r][c] & horizontal[r][c]
            if common:
                out[r][c]=sorted(common)[0]
    return out


def solve_hard_98_overlay_transformed_templates_to_count_map(g):
    panels=[]
    top=g[:5]
    for i in range(3):
        x=i*6
        panel=[row[x:x+5] for row in top]
        panels.append(panel)
    code_row=g[6]
    codes=[]
    for i in range(3):
        segment=code_row[i*6:i*6+5]
        code=next(v for v in segment if v!=0)
        codes.append(code)
    transformed=[apply_transform(panel, code) for panel,code in zip(panels,codes)]
    h,w=dims(transformed[0])
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            cnt=sum(1 for panel in transformed if panel[r][c]!=0)
            if cnt:
                out[r][c]={1:2,2:4,3:8}[cnt]
    return out


SOLVERS = {
    "solve_easy_92_fill_horizontal_intervals": solve_easy_92_fill_horizontal_intervals,
    "solve_easy_93_fill_vertical_intervals": solve_easy_93_fill_vertical_intervals,
    "solve_easy_94_mirror_left_panel_to_right": solve_easy_94_mirror_left_panel_to_right,
    "solve_easy_95_draw_rectangle_borders_from_diagonal_corners": solve_easy_95_draw_rectangle_borders_from_diagonal_corners,
    "solve_easy_96_keep_centers_of_odd_rectangles": solve_easy_96_keep_centers_of_odd_rectangles,
    "solve_easy_97_mirror_top_panel_to_bottom": solve_easy_97_mirror_top_panel_to_bottom,
    "solve_easy_98_stamp_pluses_at_markers": solve_easy_98_stamp_pluses_at_markers,
    "solve_medium_92_crop_component_selected_by_bottom_key": solve_medium_92_crop_component_selected_by_bottom_key,
    "solve_medium_93_rotate_object_by_top_code": solve_medium_93_rotate_object_by_top_code,
    "solve_medium_94_fill_matching_row_column_intersections": solve_medium_94_fill_matching_row_column_intersections,
    "solve_medium_95_cast_diagonal_rays_until_wall": solve_medium_95_cast_diagonal_rays_until_wall,
    "solve_medium_96_select_border_touching_object_and_recolor_by_key": solve_medium_96_select_border_touching_object_and_recolor_by_key,
    "solve_medium_97_sort_cropped_objects_by_width_and_pack_horizontal": solve_medium_97_sort_cropped_objects_by_width_and_pack_horizontal,
    "solve_medium_98_boolean_xor_of_two_halves": solve_medium_98_boolean_xor_of_two_halves,
    "solve_hard_92_decode_templates_into_2x2_gallery": solve_hard_92_decode_templates_into_2x2_gallery,
    "solve_hard_93_build_dihedral_equivalence_matrix": solve_hard_93_build_dihedral_equivalence_matrix,
    "solve_hard_94_fill_chambers_by_legend_dot_count": solve_hard_94_fill_chambers_by_legend_dot_count,
    "solve_hard_95_select_holed_object_rotate_and_scale2": solve_hard_95_select_holed_object_rotate_and_scale2,
    "solve_hard_96_build_pairwise_intersection_gallery": solve_hard_96_build_pairwise_intersection_gallery,
    "solve_hard_97_cast_border_rays_and_mark_matching_intersections": solve_hard_97_cast_border_rays_and_mark_matching_intersections,
    "solve_hard_98_overlay_transformed_templates_to_count_map": solve_hard_98_overlay_transformed_templates_to_count_map,
}


def verify_against_json(json_path: Path | None = None) -> None:
    if json_path is None:
        json_path = Path(__file__).with_name("arc_puzzle_bank_fourteenth_21.json")
    data = json.loads(json_path.read_text())
    for task in data:
        solver = SOLVERS[task["solver_name"]]
        for section in ("train", "test"):
            for pair in task[section]:
                got = solver(pair["input"])
                if got != pair["output"]:
                    raise AssertionError(f"Mismatch for {task['id']} in {section}")
    print(f"verified {len(data)} tasks against {json_path.name}")


if __name__ == "__main__":
    verify_against_json()
