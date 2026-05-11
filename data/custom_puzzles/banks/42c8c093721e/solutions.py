from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple, Iterable
from collections import deque, defaultdict

Grid = List[List[int]]

def clone(g: Grid) -> Grid:
    return [row[:] for row in g]

def zeros(h:int, w:int, val:int=0) -> Grid:
    return [[val for _ in range(w)] for _ in range(h)]

def dims(g: Grid) -> Tuple[int,int]:
    return len(g), len(g[0])

def paste(g:Grid, pat:Grid, top:int, left:int, transparent:int=0) -> Grid:
    h,w = dims(g)
    ph,pw = dims(pat)
    for r in range(ph):
        for c in range(pw):
            v = pat[r][c]
            if v != transparent:
                rr,cc = top+r,left+c
                assert 0 <= rr < h and 0 <= cc < w
                g[rr][cc] = v
    return g

def bbox(cells: Iterable[Tuple[int,int]]) -> Tuple[int,int,int,int]:
    cells = list(cells)
    rs = [r for r,c in cells]
    cs = [c for r,c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g:Grid, box:Tuple[int,int,int,int]) -> Grid:
    r0,c0,r1,c1 = box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def normalize_offsets(cells: Iterable[Tuple[int,int]]) -> List[Tuple[int,int]]:
    cells = list(cells)
    if not cells:
        return []
    r0,c0,_,_ = bbox(cells)
    return sorted((r-r0,c-c0) for r,c in cells)

def offsets_to_grid(offsets: Iterable[Tuple[int,int]], color:int=1) -> Grid:
    offsets = list(offsets)
    if not offsets:
        return [[0]]
    rs = [r for r,c in offsets]
    cs = [c for r,c in offsets]
    r0,c0,r1,c1 = min(rs), min(cs), max(rs), max(cs)
    g = zeros(r1-r0+1, c1-c0+1, 0)
    for r,c in offsets:
        g[r-r0][c-c0] = color
    return g

def rotate_grid_cw(g:Grid) -> Grid:
    h,w = dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_grid_180(g:Grid) -> Grid:
    return [row[::-1] for row in g[::-1]]

def rotate_grid_ccw(g:Grid) -> Grid:
    h,w = dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w-1,-1,-1)]

def flip_horizontal(g:Grid) -> Grid:
    return [row[::-1] for row in g]

def flip_vertical(g:Grid) -> Grid:
    return g[::-1]

def scale2(g:Grid) -> Grid:
    out = []
    for row in g:
        big_row = []
        for v in row:
            big_row.extend([v,v])
        out.append(big_row[:])
        out.append(big_row[:])
    return out

def nonzero_cells(g:Grid) -> List[Tuple[int,int]]:
    h,w = dims(g)
    return [(r,c) for r in range(h) for c in range(w) if g[r][c] != 0]

def connected_components(g:Grid, colors:Iterable[int]|None=None) -> List[dict]:
    h,w = dims(g)
    color_set = None if colors is None else set(colors)
    seen = [[False]*w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v == 0 or seen[r][c]:
                continue
            if color_set is not None and v not in color_set:
                continue
            seen[r][c] = True
            q = deque([(r,c)])
            cells = []
            while q:
                rr,cc = q.popleft()
                cells.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc = rr+dr, cc+dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and g[nr][nc] == v:
                        if color_set is None or v in color_set:
                            seen[nr][nc] = True
                            q.append((nr,nc))
            comps.append({"color": v, "cells": cells, "bbox": bbox(cells)})
    return comps

def components_all_nonzero(g:Grid) -> List[dict]:
    h,w = dims(g)
    seen = [[False]*w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            if g[r][c] == 0 or seen[r][c]:
                continue
            seen[r][c] = True
            q = deque([(r,c)])
            cells = []
            colors = set()
            while q:
                rr,cc = q.popleft()
                cells.append((rr,cc))
                colors.add(g[rr][cc])
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc = rr+dr, cc+dc
                    if 0 <= nr < h and 0 <= nc < w and not seen[nr][nc] and g[nr][nc] != 0:
                        seen[nr][nc] = True
                        q.append((nr,nc))
            comps.append({"color_set": colors, "cells": cells, "bbox": bbox(cells)})
    return comps

def inside(box:Tuple[int,int,int,int]) -> Tuple[int,int,int,int]:
    r0,c0,r1,c1 = box
    return r0+1, c0+1, r1-1, c1-1

def frame_boxes_from_color(g:Grid, color:int) -> List[Tuple[int,int,int,int]]:
    boxes = []
    for comp in connected_components(g, colors=[color]):
        r0,c0,r1,c1 = comp["bbox"]
        ok = True
        for c in range(c0, c1+1):
            if g[r0][c] != color or g[r1][c] != color:
                ok = False
        for r in range(r0, r1+1):
            if g[r][c0] != color or g[r][c1] != color:
                ok = False
        if ok and r1-r0 >= 2 and c1-c0 >= 2:
            boxes.append((r0,c0,r1,c1))
    return sorted(boxes)

def unique_nonzero_colors(g:Grid) -> List[int]:
    return sorted({v for row in g for v in row if v != 0})

def component_hole_count(comp_grid:Grid) -> int:
    h,w = dims(comp_grid)
    solid = [[1 if comp_grid[r][c] != 0 else 0 for c in range(w)] for r in range(h)]
    seen = [[False]*w for _ in range(h)]
    holes = 0
    for r in range(h):
        for c in range(w):
            if solid[r][c] == 0 and not seen[r][c]:
                seen[r][c] = True
                q = deque([(r,c)])
                touches = (r == 0 or r == h-1 or c == 0 or c == w-1)
                while q:
                    rr,cc = q.popleft()
                    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                        nr,nc = rr+dr, cc+dc
                        if 0 <= nr < h and 0 <= nc < w and solid[nr][nc] == 0 and not seen[nr][nc]:
                            seen[nr][nc] = True
                            if nr == 0 or nr == h-1 or nc == 0 or nc == w-1:
                                touches = True
                            q.append((nr,nc))
                if not touches:
                    holes += 1
    return holes

def center_of_box(box:Tuple[int,int,int,int]) -> Tuple[int,int]:
    r0,c0,r1,c1 = box
    return (r0+r1)//2, (c0+c1)//2

def tile_2x2(g:Grid) -> Grid:
    h,w = dims(g)
    out = zeros(h*2, w*2, 0)
    paste(out, g, 0, 0)
    paste(out, g, 0, w)
    paste(out, g, h, 0)
    paste(out, g, h, w)
    return out

def solve_easy_43_bridge_row_pairs(g: Grid) -> Grid:
    out = clone(g)
    for r,row in enumerate(g):
        pos = defaultdict(list)
        for c,v in enumerate(row):
            if v != 0:
                pos[v].append(c)
        for color, cols in pos.items():
            if len(cols) >= 2:
                a,b = min(cols), max(cols)
                for c in range(a, b+1):
                    out[r][c] = color
    return out


def solve_easy_44_mirror_across_cyan_axis(g: Grid) -> Grid:
    h,w = dims(g)
    axis = None
    for c in range(w):
        if all(g[r][c] == 8 for r in range(h)):
            axis = c
            break
    assert axis is not None
    out = clone(g)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0 and c != axis:
                mc = 2*axis - c
                if 0 <= mc < w:
                    out[r][mc] = v
    return out


def solve_easy_45_draw_border_from_corners(g: Grid) -> Grid:
    cells = nonzero_cells(g)
    r0,c0,r1,c1 = bbox(cells)
    color = g[cells[0][0]][cells[0][1]]
    out = zeros(len(g), len(g[0]), 0)
    for c in range(c0, c1+1):
        out[r0][c] = color
        out[r1][c] = color
    for r in range(r0, r1+1):
        out[r][c0] = color
        out[r][c1] = color
    return out


def solve_easy_46_crop_frame_contents(g: Grid) -> Grid:
    boxes = frame_boxes_from_color(g, 8)
    assert len(boxes) == 1
    ir0,ic0,ir1,ic1 = inside(boxes[0])
    return [row[ic0:ic1+1] for row in g[ir0:ir1+1]]


def solve_easy_47_keep_most_frequent_color(g: Grid) -> Grid:
    counts = defaultdict(int)
    for row in g:
        for v in row:
            if v != 0:
                counts[v] += 1
    keep = max(counts, key=lambda k: (counts[k], -k))
    out = zeros(len(g), len(g[0]), 0)
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v == keep:
                out[r][c] = v
    return out


def solve_easy_48_component_centers(g: Grid) -> Grid:
    out = zeros(len(g), len(g[0]), 0)
    for comp in connected_components(g):
        rr,cc = center_of_box(comp["bbox"])
        out[rr][cc] = comp["color"]
    return out


def solve_easy_49_palette_row_left_to_right(g: Grid) -> Grid:
    items = []
    for comp in connected_components(g):
        r0,c0,r1,c1 = comp["bbox"]
        items.append((c0, r0, comp["color"]))
    items.sort()
    return [[color for _,_,color in items]]


def solve_medium_43_marked_rowcol_crossings(g: Grid) -> Grid:
    h,w = dims(g)
    rows = [r for r in range(1, h-1) if g[r][0] == 2 and g[r][w-1] == 2]
    cols = [c for c in range(1, w-1) if g[0][c] == 3 and g[h-1][c] == 3]
    out = clone(g)
    for r in rows:
        for c in cols:
            out[r][c] = 8
    return out


def solve_medium_44_stamp_rotated_source_at_markers(g: Grid) -> Grid:
    comps = connected_components(g)
    source = max([comp for comp in comps if comp["color"] not in {1,2,3,4}], key=lambda comp: len(comp["cells"]))
    pat = crop_bbox(g, source["bbox"])
    # binarize the source crop
    pat = [[1 if v == source["color"] else 0 for v in row] for row in pat]
    out = zeros(len(g), len(g[0]), 0)
    rot_map = {1:0, 2:1, 3:2, 4:3}
    for r,row in enumerate(g):
        for c,v in enumerate(row):
            if v in rot_map:
                rg = pat
                for _ in range(rot_map[v]):
                    rg = rotate_grid_cw(rg)
                for rr in range(len(rg)):
                    for cc in range(len(rg[0])):
                        if rg[rr][cc]:
                            out[r+rr][c+cc] = v
    return out


def solve_medium_45_crop_union_of_key_colors(g: Grid) -> Grid:
    key_colors = {v for v in g[0] if v != 0}
    cells = [(r,c) for r in range(1, len(g)) for c,v in enumerate(g[r]) if v in key_colors]
    r0,c0,r1,c1 = bbox(cells)
    out = zeros(r1-r0+1, c1-c0+1, 0)
    for r in range(r0, r1+1):
        for c in range(c0, c1+1):
            if g[r][c] in key_colors:
                out[r-r0][c-c0] = g[r][c]
    return out


def solve_medium_46_scale_smallest_component_x2(g: Grid) -> Grid:
    comp = min(connected_components(g), key=lambda comp: (len(comp["cells"]), comp["bbox"]))
    crop = crop_bbox(g, comp["bbox"])
    return scale2(crop)


def solve_medium_47_pack_nonempty_columns_left(g: Grid) -> Grid:
    h,w = dims(g)
    cols = [c for c in range(w) if any(g[r][c] != 0 for r in range(h))]
    return [[g[r][c] for c in cols] for r in range(h)]


def solve_medium_48_crop_fullest_frame_interior(g: Grid) -> Grid:
    best_box = None
    best_count = -1
    for box in frame_boxes_from_color(g, 1):
        ir0,ic0,ir1,ic1 = inside(box)
        cnt = sum(1 for r in range(ir0, ir1+1) for c in range(ic0, ic1+1) if g[r][c] != 0)
        if cnt > best_count:
            best_count = cnt
            best_box = box
    ir0,ic0,ir1,ic1 = inside(best_box)
    return [row[ic0:ic1+1] for row in g[ir0:ir1+1]]


def solve_medium_49_draw_rectangles_from_opposite_corners(g: Grid) -> Grid:
    h,w = dims(g)
    out = zeros(h, w, 0)
    pos = defaultdict(list)
    for r in range(h):
        for c,v in enumerate(g[r]):
            if v != 0:
                pos[v].append((r,c))
    for color, cells in pos.items():
        if len(cells) == 2:
            (r0,c0),(r1,c1) = cells
            ra,rb = sorted((r0,r1))
            ca,cb = sorted((c0,c1))
            for c in range(ca, cb+1):
                out[ra][c] = color
                out[rb][c] = color
            for r in range(ra, rb+1):
                out[r][ca] = color
                out[r][cb] = color
    return out


def solve_hard_43_local_marked_rowcol_crossings_in_frames(g: Grid) -> Grid:
    out = clone(g)
    for box in frame_boxes_from_color(g, 5):
        r0,c0,r1,c1 = box
        ir0,ic0,ir1,ic1 = inside(box)
        key = None
        if r0-1 >= 0:
            for c in range(c0, c1+1):
                v = g[r0-1][c]
                if v not in (0,5):
                    key = v
                    break
        assert key is not None
        rows = [r for r in range(ir0, ir1+1) if g[r][ic0] == 2 and g[r][ic1] == 2]
        cols = [c for c in range(ic0, ic1+1) if g[ir0][c] == 3 and g[ir1][c] == 3]
        for r in rows:
            for c in cols:
                out[r][c] = key
    return out


def solve_hard_44_template_tiling_from_code_grid(g: Grid) -> Grid:
    boxes = frame_boxes_from_color(g, 1)
    code_to_template = {}
    frame_cells = set()
    for box in boxes:
        for r in range(box[0], box[2]+1):
            for c in range(box[1], box[3]+1):
                frame_cells.add((r,c))
        ir0,ic0,ir1,ic1 = inside(box)
        temp = [row[ic0:ic1+1] for row in g[ir0:ir1+1]]
        colors = {v for row in temp for v in row if v != 0}
        assert len(colors) == 1
        code = next(iter(colors))
        code_to_template[code] = temp
    code_cells = [(r,c) for r in range(len(g)) for c in range(len(g[0])) if g[r][c] != 0 and (r,c) not in frame_cells]
    r0,c0,r1,c1 = bbox(code_cells)
    codes = [row[c0:c1+1] for row in g[r0:r1+1]]
    th,tw = dims(next(iter(code_to_template.values())))
    out = zeros(len(codes)*th, len(codes[0])*tw, 0)
    for rr,row in enumerate(codes):
        for cc,code in enumerate(row):
            paste(out, code_to_template[code], rr*th, cc*tw, transparent=0)
    return out


def solve_hard_45_overlay_selected_components_with_rotation(g: Grid) -> Grid:
    keys = [v for v in g[0] if v != 0]
    a,b = keys[0], keys[1]
    comps = {comp["color"]: comp for comp in connected_components([row[:] for row in g[1:]])}
    ca = comps[a]
    cb = comps[b]
    ga = crop_bbox(g[1:], ca["bbox"])
    gb = crop_bbox(g[1:], cb["bbox"])
    ga = [[a if v == a else 0 for v in row] for row in ga]
    gb = [[b if v == b else 0 for v in row] for row in gb]
    gb = rotate_grid_cw(gb)
    h = max(len(ga), len(gb))
    w = max(len(ga[0]), len(gb[0]))
    out = zeros(h,w,0)
    for r in range(len(ga)):
        for c in range(len(ga[0])):
            if ga[r][c]:
                out[r][c] = a
    for r in range(len(gb)):
        for c in range(len(gb[0])):
            if gb[r][c]:
                if out[r][c] != 0:
                    out[r][c] = 8
                else:
                    out[r][c] = b
    return out


def solve_hard_46_local_symmetry_completion_by_frame_key(g: Grid) -> Grid:
    out = clone(g)
    for box in frame_boxes_from_color(g, 5):
        r0,c0,r1,c1 = box
        ir0,ic0,ir1,ic1 = inside(box)
        key = None
        if r0-1 >= 0:
            for c in range(c0, c1+1):
                v = g[r0-1][c]
                if v in (6,7):
                    key = v
                    break
        assert key is not None
        for r in range(ir0, ir1+1):
            for c in range(ic0, ic1+1):
                v = g[r][c]
                if v != 0:
                    if key == 6:
                        mc = ic0 + ic1 - c
                        out[r][mc] = v
                    else:
                        mr = ir0 + ir1 - r
                        out[mr][c] = v
    return out


def solve_hard_47_tile_component_with_most_holes(g: Grid) -> Grid:
    best = None
    best_holes = -1
    best_cells = -1
    for comp in connected_components(g):
        cg = crop_bbox(g, comp["bbox"])
        holes = component_hole_count([[1 if v == comp["color"] else 0 for v in row] for row in cg])
        score = (holes, len(comp["cells"]))
        if score > (best_holes, best_cells):
            best_holes, best_cells = score
            best = [[comp["color"] if v == comp["color"] else 0 for v in row] for row in cg]
    return tile_2x2(best)


def solve_hard_48_local_rotate_object_to_key_center(g: Grid) -> Grid:
    out = clone(g)
    for box in frame_boxes_from_color(g, 1):
        r0,c0,r1,c1 = box
        ir0,ic0,ir1,ic1 = inside(box)
        key = None
        if r0-1 >= 0:
            for c in range(c0, c1+1):
                v = g[r0-1][c]
                if v in (2,3,4,5):
                    key = v
                    break
        assert key is not None
        # clear the interior
        for r in range(ir0, ir1+1):
            for c in range(ic0, ic1+1):
                out[r][c] = 0
        cells = [(r,c) for r in range(ir0, ir1+1) for c in range(ic0, ic1+1) if g[r][c] != 0]
        box2 = bbox(cells)
        obj = crop_bbox(g, box2)
        colors = {v for row in obj for v in row if v != 0}
        color = next(iter(colors))
        obj = [[color if v == color else 0 for v in row] for row in obj]
        rot_map = {2:0, 3:1, 4:2, 5:3}
        for _ in range(rot_map[key]):
            obj = rotate_grid_cw(obj)
        ph,pw = dims(obj)
        ih,iw = ir1-ir0+1, ic1-ic0+1
        top = ir0 + (ih - ph)//2
        left = ic0 + (iw - pw)//2
        paste(out, obj, top, left, transparent=0)
    return out


def solve_hard_49_rotation_code_mosaic(g: Grid) -> Grid:
    boxes = frame_boxes_from_color(g, 1)
    assert len(boxes) == 1
    box = boxes[0]
    frame_cells = {(r,c) for r in range(box[0], box[2]+1) for c in range(box[1], box[3]+1)}
    ir0,ic0,ir1,ic1 = inside(box)
    src = [row[ic0:ic1+1] for row in g[ir0:ir1+1]]
    colors = {v for row in src for v in row if v != 0}
    color = next(iter(colors))
    src = [[color if v == color else 0 for v in row] for row in src]
    code_cells = [(r,c) for r in range(len(g)) for c in range(len(g[0])) if g[r][c] in (2,3,4,5) and (r,c) not in frame_cells]
    r0,c0,r1,c1 = bbox(code_cells)
    codes = [row[c0:c1+1] for row in g[r0:r1+1]]
    h,w = dims(src)
    out = zeros(len(codes)*h, len(codes[0])*w, 0)
    rot_map = {2:0, 3:1, 4:2, 5:3}
    for rr,row in enumerate(codes):
        for cc,code in enumerate(row):
            pat = src
            for _ in range(rot_map[code]):
                pat = rotate_grid_cw(pat)
            paste(out, pat, rr*h, cc*w, transparent=0)
    return out


SOLVERS = {
    "easy_43_bridge_row_pairs": solve_easy_43_bridge_row_pairs,
    "easy_44_mirror_across_cyan_axis": solve_easy_44_mirror_across_cyan_axis,
    "easy_45_draw_border_from_corners": solve_easy_45_draw_border_from_corners,
    "easy_46_crop_frame_contents": solve_easy_46_crop_frame_contents,
    "easy_47_keep_most_frequent_color": solve_easy_47_keep_most_frequent_color,
    "easy_48_component_centers": solve_easy_48_component_centers,
    "easy_49_palette_row_left_to_right": solve_easy_49_palette_row_left_to_right,
    "medium_43_marked_rowcol_crossings": solve_medium_43_marked_rowcol_crossings,
    "medium_44_stamp_rotated_source_at_markers": solve_medium_44_stamp_rotated_source_at_markers,
    "medium_45_crop_union_of_key_colors": solve_medium_45_crop_union_of_key_colors,
    "medium_46_scale_smallest_component_x2": solve_medium_46_scale_smallest_component_x2,
    "medium_47_pack_nonempty_columns_left": solve_medium_47_pack_nonempty_columns_left,
    "medium_48_crop_fullest_frame_interior": solve_medium_48_crop_fullest_frame_interior,
    "medium_49_draw_rectangles_from_opposite_corners": solve_medium_49_draw_rectangles_from_opposite_corners,
    "hard_43_local_marked_rowcol_crossings_in_frames": solve_hard_43_local_marked_rowcol_crossings_in_frames,
    "hard_44_template_tiling_from_code_grid": solve_hard_44_template_tiling_from_code_grid,
    "hard_45_overlay_selected_components_with_rotation": solve_hard_45_overlay_selected_components_with_rotation,
    "hard_46_local_symmetry_completion_by_frame_key": solve_hard_46_local_symmetry_completion_by_frame_key,
    "hard_47_tile_component_with_most_holes": solve_hard_47_tile_component_with_most_holes,
    "hard_48_local_rotate_object_to_key_center": solve_hard_48_local_rotate_object_to_key_center,
    "hard_49_rotation_code_mosaic": solve_hard_49_rotation_code_mosaic,
}


def verify_bank(bank: List[dict]) -> None:
    for task in bank:
        solver = SOLVERS[task["id"]]
        for split in ("train", "test"):
            for i, example in enumerate(task[split]):
                got = solver(example["input"])
                exp = example["output"]
                if got != exp:
                    raise AssertionError(f'{task["id"]} {split}[{i}] mismatch')
    print(f"verified {len(bank)} tasks")

if __name__ == "__main__":
    bank_path = Path(__file__).with_name("arc_puzzle_bank_seventh_21.json")
    bank = json.loads(bank_path.read_text())
    verify_bank(bank)
