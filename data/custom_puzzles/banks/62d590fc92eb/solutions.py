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


def nonzero_cells(g):
    h,w = dims(g)
    return [(r,c) for r in range(h) for c in range(w) if g[r][c] != 0]


def crop_nonzero(g):
    cells = nonzero_cells(g)
    if not cells:
        return [[0]]
    return crop_bbox(g, bbox(cells))


def connected_components(g, colors=None):
    colors = None if colors is None else set(colors)
    h,w = dims(g)
    seen = [[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0 or seen[r][c] or (colors is not None and v not in colors):
                continue
            seen[r][c]=True
            q=collections.deque([(r,c)])
            cells=[]
            while q:
                rr,cc=q.popleft()
                cells.append((rr,cc))
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc = rr+dr, cc+dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and g[nr][nc] == v and (colors is None or v in colors):
                        seen[nr][nc]=True
                        q.append((nr,nc))
            comps.append({"color": v, "cells": cells, "bbox": bbox(cells), "area": len(cells)})
    return comps


def recolor(g, color):
    return [[color if v != 0 else 0 for v in row] for row in g]


def scale2(g):
    h,w=dims(g)
    out=zeros(h*2,w*2)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            out[2*r][2*c]=out[2*r+1][2*c]=out[2*r][2*c+1]=out[2*r+1][2*c+1]=v
    return out


def rotate_cw(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]


def rotate_ccw(g):
    h,w=dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w)]


def rotate_180(g):
    return [row[::-1] for row in g[::-1]]


def flip_h(g):
    return [row[::-1] for row in g]


def vstack(grids, gap=1, bg=0):
    if not grids:
        return [[]]
    w=max(len(g[0]) for g in grids)
    total=sum(len(g) for g in grids)+gap*(len(grids)-1)
    out=zeros(total,w,bg)
    y=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        for r in range(gh):
            for c in range(gw):
                v=g[r][c]
                if v!=bg:
                    out[y+r][(w-gw)//2+c]=v
        y += gh
        if i != len(grids)-1:
            y += gap
    return out


def hstack(grids, gap=1, bg=0):
    if not grids:
        return [[]]
    h=max(len(g) for g in grids)
    total=sum(len(g[0]) for g in grids)+gap*(len(grids)-1)
    out=zeros(h,total,bg)
    x=0
    for i,g in enumerate(grids):
        gh,gw=dims(g)
        # paste centered vertically
        for r in range(gh):
            for c in range(gw):
                v=g[r][c]
                if v!=bg:
                    out[(h-gh)//2+r][x+c]=v
        x += gw
        if i != len(grids)-1:
            x += gap
    return out


def draw_rect_border(g, r0, c0, r1, c1, color):
    for c in range(c0,c1+1):
        g[r0][c]=color; g[r1][c]=color
    for r in range(r0,r1+1):
        g[r][c0]=color; g[r][c1]=color


def fill_rect(g, r0,c0,r1,c1,color):
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            g[r][c]=color


def is_main_diag_symmetric(g):
    h,w = dims(g)
    if h != w:
        return False
    for r in range(h):
        for c in range(w):
            if (g[r][c]!=0) != (g[c][r]!=0):
                return False
    return True


def is_vertically_symmetric(g):  # left-right mirror
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            if (g[r][c]!=0) != (g[r][w-1-c]!=0):
                return False
    return True


def count_holes_binary(g):
    # g assumed cropped binary or color grid. Count zero components not touching border within bbox of nonzero cells
    b = [[1 if v!=0 else 0 for v in row] for row in crop_nonzero(g)]
    h,w=dims(b)
    seen=[[False]*w for _ in range(h)]
    holes=0
    for r in range(h):
        for c in range(w):
            if b[r][c]==0 and not seen[r][c]:
                seen[r][c]=True
                q=collections.deque([(r,c)])
                cells=[]
                touches=False
                while q:
                    rr,cc=q.popleft()
                    cells.append((rr,cc))
                    if rr in (0,h-1) or cc in (0,w-1):
                        touches=True
                    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and b[nr][nc]==0 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                if not touches:
                    holes += 1
    return holes


def apply_transform(g, code):
    if code==1:
        return g
    if code==2:
        return rotate_cw(g)
    if code==3:
        return rotate_180(g)
    if code==4:
        return rotate_ccw(g)
    if code==5:
        return flip_h(g)
    raise ValueError(code)


def rotations_of_norm(g):
    # binary normalized shapes
    arr=[[1 if v!=0 else 0 for v in row] for row in crop_nonzero(g)]
    rots=[]
    cur=arr
    for _ in range(4):
        rots.append(tuple(tuple(row) for row in cur))
        cur=rotate_cw(cur)
    return set(rots)


def solve_easy_85_outline_filled_rectangles(g):
    out=zeros(*dims(g))
    for comp in connected_components(g):
        r0,c0,r1,c1 = comp["bbox"]
        color=comp["color"]
        draw_rect_border(out, r0,c0,r1,c1,color)
    return out


def solve_easy_86_fill_diagonal_spans_between_matching_endpoints(g):
    out=clone(g)
    pos=collections.defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)!=2:
            continue
        (r1,c1),(r2,c2)=cells
        dr=r2-r1; dc=c2-c1
        if abs(dr)==abs(dc) and dr!=0:
            sr=1 if dr>0 else -1
            sc=1 if dc>0 else -1
            for k in range(abs(dr)+1):
                out[r1+sr*k][c1+sc*k]=color
    return out


def solve_easy_87_compact_each_row_left(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        vals=[v for v in g[r] if v!=0]
        for c,v in enumerate(vals):
            out[r][c]=v
    return out


def solve_easy_88_stamp_hollow_3x3_around_markers(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if dr==0 and dc==0:
                            continue
                        nr,nc=r+dr,c+dc
                        if 0<=nr<h and 0<=nc<w:
                            out[nr][nc]=v
    return out


def solve_easy_89_crop_largest_component(g):
    comps=connected_components(g)
    best=max(comps, key=lambda comp: (comp["area"], -comp["bbox"][0], -comp["bbox"][1]))
    return crop_bbox(g, best["bbox"])


def solve_easy_90_fill_hollow_rectangles(g):
    out=zeros(*dims(g))
    for comp in connected_components(g):
        r0,c0,r1,c1=comp["bbox"]
        color=comp["color"]
        fill_rect(out, r0,c0,r1,c1,color)
    return out


def solve_easy_91_complete_missing_rectangle_corner(g):
    out=clone(g)
    pos=collections.defaultdict(list)
    h,w=dims(g)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            if v!=0:
                pos[v].append((r,c))
    for color,cells in pos.items():
        if len(cells)==3:
            rs=sorted(set(r for r,c in cells))
            cs=sorted(set(c for r,c in cells))
            if len(rs)==2 and len(cs)==2:
                for rr in (rs[0], rs[1]):
                    for cc in (cs[0], cs[1]):
                        out[rr][cc]=color
    return out


def solve_medium_85_scale_keyed_object_2x(g):
    key=g[0][0]
    h,w=dims(g)
    g2=clone(g)
    g2[0][0]=0
    comps=connected_components(g2)
    target=[comp for comp in comps if comp["color"]==key][0]
    cropped=crop_bbox(g2, target["bbox"])
    return scale2(cropped)


def solve_medium_86_recolor_body_via_top_legend(g):
    h,w=dims(g)
    mapping={}
    for c in range(w):
        old=g[0][c]; new=g[1][c]
        if old!=0 and new!=0:
            mapping[old]=new
    body=[row[:] for row in g[2:]]
    out=zeros(len(body), w)
    for r in range(len(body)):
        for c in range(w):
            v=body[r][c]
            out[r][c]=mapping.get(v, 0 if v==0 else v)
    return out


def solve_medium_87_cast_rays_from_emitters_until_wall(g):
    h,w=dims(g)
    out=clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c]==2:
                for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    nr,nc=r+dr,c+dc
                    while 0<=nr<h and 0<=nc<w and g[nr][nc]==0:
                        out[nr][nc]=8
                        nr += dr; nc += dc
    return out


def solve_medium_88_sort_cropped_objects_by_area_and_pack(g):
    comps=connected_components(g)
    crops=[crop_bbox(g, comp["bbox"]) for comp in comps]
    crops=sorted(crops, key=lambda cg: sum(v!=0 for row in cg for v in row))
    return hstack(crops, gap=1, bg=0)


def solve_medium_89_boolean_intersection_of_two_halves(g):
    h,w=dims(g)
    divider=None
    for r,row in enumerate(g):
        if all(v==5 for v in row):
            divider=r
            break
    assert divider is not None
    top=g[:divider]
    bottom=g[divider+1:]
    assert len(top)==len(bottom)
    out=zeros(len(top), w)
    for r in range(len(top)):
        for c in range(w):
            if top[r][c]!=0 and bottom[r][c]!=0:
                out[r][c]=8
    return out


def solve_medium_90_rotate_cropped_object_by_corner_marker(g):
    h,w=dims(g)
    corner_map = {
        (0,0): "id",
        (0,w-1): "cw",
        (h-1,w-1): "180",
        (h-1,0): "ccw",
    }
    marker=None
    for cell,code in corner_map.items():
        r,c=cell
        if g[r][c]==9:
            marker=code
            mr,mc=r,c
            break
    assert marker is not None
    g2=clone(g)
    g2[mr][mc]=0
    obj=crop_nonzero(g2)
    if marker=="id":
        return obj
    if marker=="cw":
        return rotate_cw(obj)
    if marker=="180":
        return rotate_180(obj)
    if marker=="ccw":
        return rotate_ccw(obj)


def solve_medium_91_select_horizontally_symmetric_object_and_recolor(g):
    comps=connected_components(g)
    for comp in comps:
        crop=crop_bbox(g, comp["bbox"])
        if is_vertically_symmetric(crop):
            return recolor(crop, 8)
    return [[0]]


def solve_hard_85_decode_library_shape_transform_and_recolor(g):
    # top 5 rows: 3 library panels width 5 separated by gap 1
    panels=[crop_nonzero([row[i*6:i*6+5] for row in g[:5]]) for i in range(3)]
    colors=[]
    for i in range(3):
        panel=[row[i*6:i*6+5] for row in g[:5]]
        col=next(v for row in panel for v in row if v!=0)
        colors.append(col)
    selector, tcode, outcolor = g[6][0], g[6][1], g[6][2]
    idx=colors.index(selector)
    obj=panels[idx]
    transformed=apply_transform(obj, tcode)
    return recolor(transformed, outcolor)


def solve_hard_86_build_rotation_equivalence_matrix(g):
    panels=[crop_nonzero([row[i*6:i*6+5] for row in g]) for i in range(4)]
    rots=[rotations_of_norm(panel) for panel in panels]
    n=4
    out=zeros(n,n)
    for i in range(n):
        for j in range(n):
            if any(shape in rots[j] for shape in rots[i]):
                out[i][j]=8
    return out


def solve_hard_87_fill_chambers_by_internal_key_parity(g):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]==5:
                out[r][c]=5
    seen=[[False]*w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c]!=5 and not seen[r][c]:
                seen[r][c]=True
                q=collections.deque([(r,c)])
                cells=[]
                keys=0
                while q:
                    rr,cc=q.popleft()
                    cells.append((rr,cc))
                    if g[rr][cc]==2:
                        keys += 1
                    for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                        nr,nc=rr+dr,cc+dc
                        if 0<=nr<h and 0<=nc<w and g[nr][nc]!=5 and not seen[nr][nc]:
                            seen[nr][nc]=True
                            q.append((nr,nc))
                fill=0
                if keys>0:
                    fill=8 if keys%2==1 else 7
                for rr,cc in cells:
                    out[rr][cc]=fill
    return out


def solve_hard_88_select_object_by_holes_and_diag_symmetry_scale2(g):
    comps=connected_components(g)
    for comp in comps:
        crop=crop_bbox(g, comp["bbox"])
        if count_holes_binary(crop) >= 1 and is_main_diag_symmetric([[1 if v!=0 else 0 for v in row] for row in crop]):
            return scale2(recolor(crop, 8))
    return [[0]]


def solve_hard_89_sort_objects_by_holes_then_pack_vertical(g):
    comps=connected_components(g)
    crops=[crop_bbox(g, comp["bbox"]) for comp in comps]
    crops=sorted(crops, key=lambda cg: (count_holes_binary(cg), -sum(v!=0 for row in cg for v in row)))
    return vstack(crops, gap=1, bg=0)


def solve_hard_90_decode_sequence_of_library_shapes(g):
    panels=[crop_nonzero([row[i*6:i*6+5] for row in g[:5]]) for i in range(3)]
    colors=[]
    for i in range(3):
        panel=[row[i*6:i*6+5] for row in g[:5]]
        colors.append(next(v for row in panel for v in row if v!=0))
    code_row=g[6]
    items=[]
    c=0
    while c+1 < len(code_row):
        if code_row[c]==0:
            break
        items.append((code_row[c], code_row[c+1]))
        c += 2
    out_items=[]
    for selector, tcode in items:
        idx=colors.index(selector)
        obj=panels[idx]
        out_items.append(apply_transform(obj, tcode))
    return hstack(out_items, gap=1, bg=0)


def solve_hard_91_overlay_three_shapes_to_count_map(g):
    panels=[ [row[i*6:i*6+5] for row in g] for i in range(3) ]
    h,w=5,5
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            cnt=sum(1 for p in panels if p[r][c]!=0)
            out[r][c]=0 if cnt==0 else {1:2,2:4,3:8}[cnt]
    return out


SOLVERS = {
    "solve_easy_85_outline_filled_rectangles": solve_easy_85_outline_filled_rectangles,
    "solve_easy_86_fill_diagonal_spans_between_matching_endpoints": solve_easy_86_fill_diagonal_spans_between_matching_endpoints,
    "solve_easy_87_compact_each_row_left": solve_easy_87_compact_each_row_left,
    "solve_easy_88_stamp_hollow_3x3_around_markers": solve_easy_88_stamp_hollow_3x3_around_markers,
    "solve_easy_89_crop_largest_component": solve_easy_89_crop_largest_component,
    "solve_easy_90_fill_hollow_rectangles": solve_easy_90_fill_hollow_rectangles,
    "solve_easy_91_complete_missing_rectangle_corner": solve_easy_91_complete_missing_rectangle_corner,
    "solve_medium_85_scale_keyed_object_2x": solve_medium_85_scale_keyed_object_2x,
    "solve_medium_86_recolor_body_via_top_legend": solve_medium_86_recolor_body_via_top_legend,
    "solve_medium_87_cast_rays_from_emitters_until_wall": solve_medium_87_cast_rays_from_emitters_until_wall,
    "solve_medium_88_sort_cropped_objects_by_area_and_pack": solve_medium_88_sort_cropped_objects_by_area_and_pack,
    "solve_medium_89_boolean_intersection_of_two_halves": solve_medium_89_boolean_intersection_of_two_halves,
    "solve_medium_90_rotate_cropped_object_by_corner_marker": solve_medium_90_rotate_cropped_object_by_corner_marker,
    "solve_medium_91_select_horizontally_symmetric_object_and_recolor": solve_medium_91_select_horizontally_symmetric_object_and_recolor,
    "solve_hard_85_decode_library_shape_transform_and_recolor": solve_hard_85_decode_library_shape_transform_and_recolor,
    "solve_hard_86_build_rotation_equivalence_matrix": solve_hard_86_build_rotation_equivalence_matrix,
    "solve_hard_87_fill_chambers_by_internal_key_parity": solve_hard_87_fill_chambers_by_internal_key_parity,
    "solve_hard_88_select_object_by_holes_and_diag_symmetry_scale2": solve_hard_88_select_object_by_holes_and_diag_symmetry_scale2,
    "solve_hard_89_sort_objects_by_holes_then_pack_vertical": solve_hard_89_sort_objects_by_holes_then_pack_vertical,
    "solve_hard_90_decode_sequence_of_library_shapes": solve_hard_90_decode_sequence_of_library_shapes,
    "solve_hard_91_overlay_three_shapes_to_count_map": solve_hard_91_overlay_three_shapes_to_count_map,
}


def verify_against_json(json_path: Path | None = None) -> None:
    if json_path is None:
        json_path = Path(__file__).with_name("arc_puzzle_bank_thirteenth_21.json")
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
