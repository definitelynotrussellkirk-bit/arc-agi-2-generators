from __future__ import annotations
from collections import deque
from pathlib import Path
from typing import List
import json

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
    r0,c0,r1,c1=box
    return [row[c0:c1+1] for row in g[r0:r1+1]]
def crop_nonzero(g):
    cells=[(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0]
    return crop_bbox(g,bbox(cells)) if cells else [[0]]
def stamp(g,obj,top,left,transparent=0):
    H,W=dims(g); h,w=dims(obj)
    for r in range(h):
        for c in range(w):
            v=obj[r][c]
            if v!=transparent:
                rr,cc=top+r,left+c
                if 0<=rr<H and 0<=cc<W:
                    g[rr][cc]=v
    return g
def recolor_nonzero(g,color):
    h,w=dims(g)
    out=zeros(h,w)
    for r in range(h):
        for c in range(w):
            if g[r][c]!=0:
                out[r][c]=color
    return out
def hflip(g):
    return [list(reversed(row)) for row in g]
def vflip(g):
    return [row[:] for row in reversed(g)]
def rot90(g):
    h,w=dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]
def rot180(g): return rot90(rot90(g))
def rot270(g): return rot90(rot180(g))
def scale2(g):
    h,w=dims(g)
    out=zeros(h*2,w*2)
    for r in range(h):
        for c in range(w):
            v=g[r][c]
            out[2*r][2*c]=v
            out[2*r+1][2*c]=v
            out[2*r][2*c+1]=v
            out[2*r+1][2*c+1]=v
    return out
def normalize_binary(g):
    cg=crop_nonzero(g)
    return [[1 if v!=0 else 0 for v in row] for row in cg]
def component_grid(g,cells):
    r0,c0,r1,c1=bbox(cells)
    out=zeros(r1-r0+1,c1-c0+1)
    for r,c in cells:
        out[r-r0][c-c0]=g[r][c]
    return out
def connected_components(g, colors=None, ignore_positions=None):
    colors=None if colors is None else set(colors)
    ignore=set() if ignore_positions is None else set(ignore_positions)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    comps=[]
    for r in range(h):
        for c in range(w):
            if (r,c) in ignore:
                seen[r][c]=True
                continue
            v=g[r][c]
            if seen[r][c] or v==0 or (colors is not None and v not in colors):
                continue
            seen[r][c]=True
            dq=deque([(r,c)]); cells=[]
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and (nr,nc) not in ignore:
                        nv=g[nr][nc]
                        if nv!=0 and (colors is None or nv in colors):
                            seen[nr][nc]=True; dq.append((nr,nc))
            comps.append(cells)
    return comps
def flood_regions_nonwall(g, wall=8, ignore_positions=None, row_start=0):
    ignore=set() if ignore_positions is None else set(ignore_positions)
    h,w=dims(g)
    seen=[[False]*w for _ in range(h)]
    regs=[]
    for r in range(row_start,h):
        for c in range(w):
            if (r,c) in ignore:
                seen[r][c]=True
                continue
            if seen[r][c] or g[r][c]==wall:
                continue
            seen[r][c]=True
            dq=deque([(r,c)]); cells=[]
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if row_start<=nr<h and 0<=nc<w and not seen[nr][nc] and (nr,nc) not in ignore and g[nr][nc]!=wall:
                        seen[nr][nc]=True; dq.append((nr,nc))
            regs.append(cells)
    return regs
def find_holes_in_component(comp_grid):
    # comp_grid with one color ring and zeros holes/bg. returns cells of holes not connected to border.
    h,w=dims(comp_grid)
    seen=[[False]*w for _ in range(h)]
    holes=[]
    for r in range(h):
        for c in range(w):
            if seen[r][c] or comp_grid[r][c]!=0:
                continue
            seen[r][c]=True
            dq=deque([(r,c)]); cells=[]; border=False
            while dq:
                rr,cc=dq.popleft(); cells.append((rr,cc))
                if rr in (0,h-1) or cc in (0,w-1): border=True
                for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr,nc=rr+dr,cc+dc
                    if 0<=nr<h and 0<=nc<w and not seen[nr][nc] and comp_grid[nr][nc]==0:
                        seen[nr][nc]=True; dq.append((nr,nc))
            if not border:
                holes.extend(cells)
    return holes
def apply_transform(g, code):
    # codes 1 id 2 hflip 3 vflip 4 rot90 5 rot180 6 rot270
    if code==1: return clone(g)
    if code==2: return hflip(g)
    if code==3: return vflip(g)
    if code==4: return rot90(g)
    if code==5: return rot180(g)
    if code==6: return rot270(g)
    raise ValueError(code)
def dihedral_variants(bin_g):
    vs=[]
    cur=bin_g
    for _ in range(4):
        vs.append(cur)
        vs.append(hflip(cur))
        cur=rot90(cur)
    uniq=[]
    for v in vs:
        if all(v!=u for u in uniq):
            uniq.append(v)
    return uniq
def centered_stamp_on_canvas(canvas_box, obj, border_val=8):
    # canvas_box is grid of border box (already cropped), border stays.
    out=clone(canvas_box)
    h,w=dims(out)
    # find interior zeros?
    top=(h-len(obj))//2
    left=(w-len(obj[0]))//2
    return stamp(out,obj,top,left,transparent=0)

def solve_easy_141_fill_between_matching_column_markers(g):
    h, w = dims(g)
    out = clone(g)
    for c in range(w):
        nz = [(r, g[r][c]) for r in range(h) if g[r][c] != 0]
        if len(nz) == 2 and nz[0][1] == nz[1][1]:
            r0, color = nz[0]
            r1, _ = nz[1]
            for r in range(min(r0, r1), max(r0, r1) + 1):
                out[r][c] = color
    return out

def solve_easy_142_expand_singletons_to_diagonal_xs(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            color = g[r][c]
            if color == 0:
                continue
            for dr, dc in ((0,0), (-1,-1), (-1,1), (1,-1), (1,1)):
                rr, cc = r + dr, c + dc
                if 0 <= rr < h and 0 <= cc < w:
                    out[rr][cc] = color
    return out

def solve_easy_143_project_top_markers_down_columns(g):
    h, w = dims(g)
    out = zeros(h, w)
    for c in range(w):
        color = g[0][c]
        if color != 0:
            for r in range(h):
                out[r][c] = color
    return out

def solve_easy_144_reduce_solid_3x3_blocks_to_centers(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h - 2):
        for c in range(w - 2):
            color = g[r][c]
            if color == 0:
                continue
            ok = True
            for rr in range(r, r + 3):
                for cc in range(c, c + 3):
                    if g[rr][cc] != color:
                        ok = False
            if ok:
                out[r + 1][c + 1] = color
    return out

def solve_easy_145_mirror_left_half_across_divider(g):
    h, w = dims(g)
    mid = w // 2
    out = clone(g)
    for r in range(h):
        for c in range(mid):
            v = g[r][c]
            if v != 0 and v != 8:
                out[r][w - 1 - c] = v
    return out

def solve_easy_146_outline_rectangles_from_diagonal_corner_pairs(g):
    h, w = dims(g)
    out = zeros(h, w)
    positions = {}
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                positions.setdefault(v, []).append((r, c))
    for color, cells in positions.items():
        if len(cells) != 2:
            continue
        (r0, c0), (r1, c1) = cells
        r0, r1 = sorted((r0, r1))
        c0, c1 = sorted((c0, c1))
        for c in range(c0, c1 + 1):
            out[r0][c] = color
            out[r1][c] = color
        for r in range(r0, r1 + 1):
            out[r][c0] = color
            out[r][c1] = color
    return out

def solve_easy_147_bridge_one_cell_vertical_gaps(g):
    h, w = dims(g)
    out = clone(g)
    for r in range(1, h - 1):
        for c in range(w):
            if g[r][c] == 0 and g[r - 1][c] == g[r + 1][c] and g[r - 1][c] != 0:
                out[r][c] = g[r - 1][c]
    return out

def solve_medium_141_select_legend_object_and_rotate_clockwise(g):
    target_color = g[0][0]
    ignore = {(0, 0)}
    comps = connected_components(g, colors={target_color}, ignore_positions=ignore)
    comp = max(comps, key=len)
    obj = component_grid(g, comp)
    return rot90(obj)

def solve_medium_142_fill_header_selected_intersections(g):
    h, w = dims(g)
    out = clone(g)
    active_rows = [r for r in range(1, h) if g[r][0] == 3]
    active_cols = [c for c in range(1, w) if g[0][c] == 2]
    for r in active_rows:
        for c in active_cols:
            out[r][c] = 5
    return out

def solve_medium_143_apply_downward_gravity_in_walled_columns(g):
    h, w = dims(g)
    out = clone(g)
    for c in range(w):
        start = 0
        while start < h:
            end = start
            while end < h and g[end][c] != 8:
                end += 1
            vals = [g[r][c] for r in range(start, end) if g[r][c] not in (0, 8)]
            for r in range(start, end):
                out[r][c] = 0
            for i, v in enumerate(reversed(vals)):
                out[end - 1 - i][c] = v
            if end < h:
                out[end][c] = 8
            start = end + 1
    return out

def solve_medium_144_crop_the_horizontally_symmetric_object(g):
    comps = connected_components(g)
    for comp in comps:
        obj = component_grid(g, comp)
        bin_obj = [[1 if v != 0 else 0 for v in row] for row in obj]
        if bin_obj == hflip(bin_obj):
            return obj
    return [[0]]

def solve_medium_145_fill_holes_in_ring_components(g):
    out = clone(g)
    comps = connected_components(g)
    for comp in comps:
        obj = component_grid(g, comp)
        holes = find_holes_in_component([[1 if v != 0 else 0 for v in row] for row in obj])
        if not holes:
            continue
        color = next(v for row in obj for v in row if v != 0)
        r0, c0, _, _ = bbox(comp)
        for rr, cc in holes:
            out[r0 + rr][c0 + cc] = color
    return out

def solve_medium_146_decode_transform_and_recolor_from_control_strip(g):
    tcode = g[0][0]
    out_color = g[0][1]
    ignore = {(0, 0), (0, 1)}
    comps = connected_components(g, ignore_positions=ignore)
    comp = max(comps, key=len)
    obj = component_grid(g, comp)
    obj_bin = [[1 if v != 0 else 0 for v in row] for row in obj]
    transformed = apply_transform(obj_bin, tcode)
    return recolor_nonzero(transformed, out_color)

def solve_medium_147_fill_each_walled_chamber_from_its_seed(g):
    h, w = dims(g)
    out = clone(g)
    regions = flood_regions_nonwall(g, wall=8)
    for reg in regions:
        seed_colors = sorted({g[r][c] for r, c in reg if g[r][c] not in (0, 8)})
        if len(seed_colors) != 1:
            continue
        color = seed_colors[0]
        for r, c in reg:
            out[r][c] = color
    return out

def solve_hard_141_decode_dual_code_library_and_center_stamp(g):
    proto_color = g[0][0]
    tcode = g[0][1]
    out_color = g[0][2]
    ignore = {(0, 0), (0, 1), (0, 2)}
    wall_comps = connected_components(g, colors={8}, ignore_positions=ignore)
    frame = max(wall_comps, key=len)
    frame_box = bbox(frame)
    frame_grid = crop_bbox(g, frame_box)
    ignore |= set(frame)
    proto_comps = connected_components(g, colors={proto_color}, ignore_positions=ignore)
    proto = component_grid(g, max(proto_comps, key=len))
    proto_bin = [[1 if v != 0 else 0 for v in row] for row in proto]
    transformed = recolor_nonzero(apply_transform(proto_bin, tcode), out_color)
    return centered_stamp_on_canvas(frame_grid, transformed)

def solve_hard_142_build_dihedral_equivalence_matrix(g):
    comps = connected_components(g)
    comps = sorted(comps, key=lambda comp: bbox(comp)[:2])
    norms = []
    for comp in comps:
        obj = component_grid(g, comp)
        norms.append([[1 if v != 0 else 0 for v in row] for row in obj])
    n = len(norms)
    out = zeros(n, n)
    for i in range(n):
        variants = dihedral_variants(norms[i])
        for j in range(n):
            if any(variants_k == norms[j] for variants_k in variants):
                out[i][j] = 2
    return out

def solve_hard_143_overlay_diagonal_visibility_counts_with_walls(g):
    h, w = dims(g)
    out = zeros(h, w)
    for r in range(h):
        for c in range(w):
            if g[r][c] == 8:
                out[r][c] = 8
    emitters = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 2]
    for r, c in emitters:
        out[r][c] = min(9, (0 if out[r][c] == 8 else out[r][c]) + 1)
        for dr, dc in ((1,1), (1,-1), (-1,1), (-1,-1)):
            rr, cc = r + dr, c + dc
            while 0 <= rr < h and 0 <= cc < w and g[rr][cc] != 8:
                if out[rr][cc] != 8:
                    out[rr][cc] = min(9, out[rr][cc] + 1)
                rr += dr
                cc += dc
    return out

def solve_hard_144_build_transform_recolor_gallery(g):
    h, w = dims(g)
    tcols = [c for c in range(1, w) if g[0][c] != 0]
    rrows = [r for r in range(1, h) if g[r][0] != 0]
    transforms = [g[0][c] for c in tcols]
    colors = [g[r][0] for r in rrows]
    ignore = {(0, c) for c in tcols} | {(r, 0) for r in rrows}
    comps = connected_components(g, ignore_positions=ignore)
    proto = component_grid(g, max(comps, key=len))
    proto_bin = [[1 if v != 0 else 0 for v in row] for row in proto]
    ph, pw = dims(proto_bin)
    out = zeros(len(colors) * ph + (len(colors) - 1), len(transforms) * pw + (len(transforms) - 1))
    for i, color in enumerate(colors):
        for j, tcode in enumerate(transforms):
            tile = recolor_nonzero(apply_transform(proto_bin, tcode), color)
            top = i * (ph + 1)
            left = j * (pw + 1)
            stamp(out, tile, top, left)
    return out

def solve_hard_145_fill_chambers_by_seed_priority_legend(g):
    priority = [v for v in g[0] if v not in (0, 8)]
    rank = {color: i for i, color in enumerate(priority)}
    h, w = dims(g)
    out = clone(g)
    regions = flood_regions_nonwall(g, wall=8, row_start=1)
    for reg in regions:
        colors = sorted({g[r][c] for r, c in reg if g[r][c] not in (0, 8)}, key=lambda v: rank[v])
        if not colors:
            continue
        fill = colors[0]
        for r, c in reg:
            out[r][c] = fill
    return out

def solve_hard_146_select_object_by_border_touch_signature_and_scale2(g):
    required = {v for v in g[0] if v in (1, 2, 3, 4)}
    h, w = dims(g)
    ignore = {(0, c) for c in range(w)}
    comps = connected_components(g, ignore_positions=ignore)
    for comp in comps:
        r0, c0, r1, c1 = bbox(comp)
        sig = set()
        if r0 == 1:
            sig.add(1)
        if c1 == w - 1:
            sig.add(2)
        if r1 == h - 1:
            sig.add(3)
        if c0 == 0:
            sig.add(4)
        if sig == required:
            return scale2(component_grid(g, comp))
    return [[0]]

def solve_hard_147_apply_transform_sequence_and_stamp_at_anchors(g):
    code1, code2 = g[0][0], g[0][1]
    h, w = dims(g)
    ignore = {(0, 0), (0, 1)}
    comps = connected_components(g, colors=None, ignore_positions=ignore)
    proto = None
    anchors = []
    for comp in comps:
        colors = {g[r][c] for r, c in comp}
        if len(colors) == 1 and next(iter(colors)) != 9:
            # one-cell anchors of various colors
            if len(comp) == 1:
                anchors.append(comp[0])
                continue
        if 9 in colors:
            proto = component_grid(g, comp)
    proto_bin = [[1 if v != 0 else 0 for v in row] for row in proto]
    transformed = apply_transform(apply_transform(proto_bin, code1), code2)
    ph, pw = dims(transformed)
    out = zeros(h, w)
    for r, c in anchors:
        color = g[r][c]
        tile = recolor_nonzero(transformed, color)
        top = r - ph // 2
        left = c - pw // 2
        stamp(out, tile, top, left)
    return out

TASK_SOLVERS = {
    "easy_141_fill_between_matching_column_markers": solve_easy_141_fill_between_matching_column_markers,
    "easy_142_expand_singletons_to_diagonal_xs": solve_easy_142_expand_singletons_to_diagonal_xs,
    "easy_143_project_top_markers_down_columns": solve_easy_143_project_top_markers_down_columns,
    "easy_144_reduce_solid_3x3_blocks_to_centers": solve_easy_144_reduce_solid_3x3_blocks_to_centers,
    "easy_145_mirror_left_half_across_divider": solve_easy_145_mirror_left_half_across_divider,
    "easy_146_outline_rectangles_from_diagonal_corner_pairs": solve_easy_146_outline_rectangles_from_diagonal_corner_pairs,
    "easy_147_bridge_one_cell_vertical_gaps": solve_easy_147_bridge_one_cell_vertical_gaps,
    "medium_141_select_legend_object_and_rotate_clockwise": solve_medium_141_select_legend_object_and_rotate_clockwise,
    "medium_142_fill_header_selected_intersections": solve_medium_142_fill_header_selected_intersections,
    "medium_143_apply_downward_gravity_in_walled_columns": solve_medium_143_apply_downward_gravity_in_walled_columns,
    "medium_144_crop_the_horizontally_symmetric_object": solve_medium_144_crop_the_horizontally_symmetric_object,
    "medium_145_fill_holes_in_ring_components": solve_medium_145_fill_holes_in_ring_components,
    "medium_146_decode_transform_and_recolor_from_control_strip": solve_medium_146_decode_transform_and_recolor_from_control_strip,
    "medium_147_fill_each_walled_chamber_from_its_seed": solve_medium_147_fill_each_walled_chamber_from_its_seed,
    "hard_141_decode_dual_code_library_and_center_stamp": solve_hard_141_decode_dual_code_library_and_center_stamp,
    "hard_142_build_dihedral_equivalence_matrix": solve_hard_142_build_dihedral_equivalence_matrix,
    "hard_143_overlay_diagonal_visibility_counts_with_walls": solve_hard_143_overlay_diagonal_visibility_counts_with_walls,
    "hard_144_build_transform_recolor_gallery": solve_hard_144_build_transform_recolor_gallery,
    "hard_145_fill_chambers_by_seed_priority_legend": solve_hard_145_fill_chambers_by_seed_priority_legend,
    "hard_146_select_object_by_border_touch_signature_and_scale2": solve_hard_146_select_object_by_border_touch_signature_and_scale2,
    "hard_147_apply_transform_sequence_and_stamp_at_anchors": solve_hard_147_apply_transform_sequence_and_stamp_at_anchors,
}

def verify_bank(path: str | None = None) -> tuple[int, int]:
    bank_path = Path(path) if path is not None else Path(__file__).with_name("arc_puzzle_bank_twentyfirst_21.json")
    data = json.loads(bank_path.read_text())
    checked = 0
    for task in data:
        solver = TASK_SOLVERS[task["id"]]
        for split in ("train", "test"):
            for pair in task[split]:
                pred = solver(pair["input"])
                assert pred == pair["output"], f"Mismatch for {task['id']} {split}"
                checked += 1
    return len(data), checked

if __name__ == "__main__":
    n_tasks, n_pairs = verify_bank()
    print(f"Verified {n_tasks} tasks / {n_pairs} input-output pairs.")
