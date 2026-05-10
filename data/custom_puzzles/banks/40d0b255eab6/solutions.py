
from __future__ import annotations
import json, inspect, textwrap, zipfile
from pathlib import Path
from typing import List, Tuple, Dict, Callable, Iterable
from collections import deque, Counter, defaultdict

Grid = List[List[int]]

# ----------------------------
# Basic helpers
# ----------------------------

def clone(g: Grid) -> Grid:
    return [row[:] for row in g]

def zeros(h: int, w: int, val: int = 0) -> Grid:
    return [[val for _ in range(w)] for _ in range(h)]

def dims(g: Grid) -> Tuple[int, int]:
    return len(g), len(g[0])

def paste(g: Grid, pat: Grid, top: int, left: int, transparent: int = 0) -> Grid:
    h, w = dims(g)
    ph, pw = dims(pat)
    for r in range(ph):
        for c in range(pw):
            v = pat[r][c]
            if v != transparent:
                rr, cc = top + r, left + c
                assert 0 <= rr < h and 0 <= cc < w, (top, left, ph, pw, h, w)
                g[rr][cc] = v
    return g

def bbox(cells: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    return min(rs), min(cs), max(rs), max(cs)

def crop_bbox(g: Grid, box: Tuple[int, int, int, int]) -> Grid:
    r0, c0, r1, c1 = box
    return [row[c0:c1+1] for row in g[r0:r1+1]]

def crop_nonzero(g: Grid) -> Grid:
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    if not cells:
        return [[0]]
    return crop_bbox(g, bbox(cells))

def add_cells(g: Grid, cells: Iterable[Tuple[int, int]], color: int) -> Grid:
    h, w = dims(g)
    for r, c in cells:
        assert 0 <= r < h and 0 <= c < w, (r, c, h, w)
        g[r][c] = color
    return g

def place_pattern(g: Grid, pat: Grid, top: int, left: int) -> Grid:
    return paste(g, pat, top, left, transparent=0)

def draw_rect(g: Grid, top: int, left: int, h: int, w: int, color: int, border_only: bool = False) -> Grid:
    for r in range(top, top+h):
        for c in range(left, left+w):
            if border_only:
                if r in (top, top+h-1) or c in (left, left+w-1):
                    g[r][c] = color
            else:
                g[r][c] = color
    return g

def components4_any(g: Grid) -> List[List[Tuple[int, int]]]:
    h, w = dims(g)
    seen = set()
    out = []
    for r in range(h):
        for c in range(w):
            if g[r][c] == 0 or (r, c) in seen:
                continue
            q = deque([(r, c)])
            seen.add((r, c))
            comp = []
            while q:
                rr, cc = q.popleft()
                comp.append((rr, cc))
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = rr+dr, cc+dc
                    if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 0 and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        q.append((nr, nc))
            out.append(comp)
    return out

def components4_color(g: Grid, color: int) -> List[List[Tuple[int, int]]]:
    h, w = dims(g)
    seen = set()
    out = []
    for r in range(h):
        for c in range(w):
            if g[r][c] != color or (r, c) in seen:
                continue
            q = deque([(r, c)])
            seen.add((r, c))
            comp = []
            while q:
                rr, cc = q.popleft()
                comp.append((rr, cc))
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = rr+dr, cc+dc
                    if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == color and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        q.append((nr, nc))
            out.append(comp)
    return out

def normalize_offsets(cells: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    cells = list(cells)
    if not cells:
        return []
    r0, c0, _, _ = bbox(cells)
    return sorted((r-r0, c-c0) for r, c in cells)

def offsets_to_grid(offsets: List[Tuple[int, int]], color: int = 1) -> Grid:
    if not offsets:
        return [[0]]
    maxr = max(r for r, c in offsets)
    maxc = max(c for r, c in offsets)
    g = zeros(maxr+1, maxc+1)
    for r, c in offsets:
        g[r][c] = color
    return g

def rotate_grid_cw(g: Grid) -> Grid:
    h, w = dims(g)
    return [[g[h-1-r][c] for r in range(h)] for c in range(w)]

def rotate_grid_ccw(g: Grid) -> Grid:
    h, w = dims(g)
    return [[g[r][w-1-c] for r in range(h)] for c in range(w-1, -1, -1)]

def rotate_grid_180(g: Grid) -> Grid:
    return [row[::-1] for row in g[::-1]]

def flip_horizontal(g: Grid) -> Grid:
    return [row[::-1] for row in g]

def flip_vertical(g: Grid) -> Grid:
    return g[::-1]

def scale_grid(g: Grid, k: int) -> Grid:
    h, w = dims(g)
    out = zeros(h*k, w*k)
    for r in range(h):
        for c in range(w):
            for dr in range(k):
                for dc in range(k):
                    out[r*k+dr][c*k+dc] = g[r][c]
    return out

def is_h_symmetric_offsets(offsets: List[Tuple[int, int]]) -> bool:
    if not offsets:
        return False
    maxr = max(r for r, c in offsets)
    s = set(offsets)
    return all((maxr-r, c) in s for r, c in offsets)

def is_v_symmetric_offsets(offsets: List[Tuple[int, int]]) -> bool:
    if not offsets:
        return False
    maxc = max(c for r, c in offsets)
    s = set(offsets)
    return all((r, maxc-c) in s for r, c in offsets)

def ray_until_block(g: Grid, start: Tuple[int, int], dr: int, dc: int, blockers: set[int], bounds: Tuple[int,int,int,int] | None = None, include_start: bool = False) -> List[Tuple[int, int]]:
    h, w = dims(g)
    r, c = start
    cells = []
    if include_start:
        if bounds is None or (bounds[0] <= r <= bounds[2] and bounds[1] <= c <= bounds[3]):
            cells.append((r, c))
    rr, cc = r + dr, c + dc
    while 0 <= rr < h and 0 <= cc < w:
        if bounds is not None:
            r0, c0, r1, c1 = bounds
            if not (r0 <= rr <= r1 and c0 <= cc <= c1):
                break
        if g[rr][cc] in blockers:
            break
        cells.append((rr, cc))
        rr += dr
        cc += dc
    return cells

def transform_by_key(g: Grid, key: int) -> Grid:
    if key == 1:
        return clone(g)
    if key == 2:
        return rotate_grid_cw(g)
    if key == 3:
        return rotate_grid_180(g)
    if key == 4:
        return flip_horizontal(g)
    raise ValueError(f"unsupported key {key}")

def pack_horiz_top(crops: List[Grid], sep: int = 1) -> Grid:
    if not crops:
        return [[0]]
    heights = [dims(c)[0] for c in crops]
    widths = [dims(c)[1] for c in crops]
    h = max(heights)
    w = sum(widths) + sep * (len(crops)-1)
    out = zeros(h, w)
    x = 0
    for crop in crops:
        paste(out, crop, 0, x)
        x += dims(crop)[1] + sep
    return out

def pack_vert_left(crops: List[Grid], sep: int = 1) -> Grid:
    if not crops:
        return [[0]]
    heights = [dims(c)[0] for c in crops]
    widths = [dims(c)[1] for c in crops]
    h = sum(heights) + sep * (len(crops)-1)
    w = max(widths)
    out = zeros(h, w)
    y = 0
    for crop in crops:
        paste(out, crop, y, 0)
        y += dims(crop)[0] + sep
    return out

def comp_crop(g: Grid, comp: List[Tuple[int, int]]) -> Grid:
    return crop_bbox(g, bbox(comp))

def fill_holes_with_key(crop: Grid, key_color: int) -> Grid:
    h, w = dims(crop)
    seen = set()
    q = deque()
    for r in range(h):
        for c in range(w):
            if r in (0, h-1) or c in (0, w-1):
                if crop[r][c] == 0 and (r, c) not in seen:
                    seen.add((r, c))
                    q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r+dr, c+dc
            if 0 <= nr < h and 0 <= nc < w and crop[nr][nc] == 0 and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc))
    out = clone(crop)
    for r in range(h):
        for c in range(w):
            if crop[r][c] == 0 and (r, c) not in seen:
                out[r][c] = key_color
    return out

def is_rect_border_component(comp: List[Tuple[int,int]]) -> bool:
    offs = normalize_offsets(comp)
    if not offs:
        return False
    maxr = max(r for r,c in offs)
    maxc = max(c for r,c in offs)
    border = set()
    for r in range(maxr+1):
        for c in range(maxc+1):
            if r in (0,maxr) or c in (0,maxc):
                border.add((r,c))
    return set(offs) == border and maxr >= 2 and maxc >= 2

def overlay_counts(crops: List[Grid]) -> Grid:
    if not crops:
        return [[0]]
    h = max(dims(c)[0] for c in crops)
    w = max(dims(c)[1] for c in crops)
    cnt = [[0 for _ in range(w)] for _ in range(h)]
    for crop in crops:
        ch, cw = dims(crop)
        for r in range(ch):
            for c in range(cw):
                if crop[r][c] != 0:
                    cnt[r][c] += 1
    out = zeros(h, w)
    mapping = {1:2, 2:3, 3:4, 4:6}
    for r in range(h):
        for c in range(w):
            if cnt[r][c]:
                out[r][c] = mapping[cnt[r][c]]
    return out

def nonzero_offsets(g: Grid) -> List[Tuple[int,int]]:
    return normalize_offsets((r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v!=0)

def same_shape(g1: Grid, g2: Grid) -> bool:
    return nonzero_offsets(g1) == nonzero_offsets(g2)



# ----------------------------
# Solver functions
# ----------------------------

def solve_easy_29_shoot_rays_to_walls(g: Grid) -> Grid:
    out = clone(g)
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v == 2:
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    for rr, cc in ray_until_block(g, (r, c), dr, dc, blockers={5}, include_start=True):
                        if g[rr][cc] != 5:
                            out[rr][cc] = 8
    return out

def solve_easy_30_crop_nonzero_bbox(g: Grid) -> Grid:
    return crop_nonzero(g)

def solve_easy_31_complete_main_diagonal_symmetry(g: Grid) -> Grid:
    h, w = dims(g)
    assert h == w
    out = clone(g)
    for r in range(h):
        for c in range(w):
            if g[r][c] != 0:
                out[c][r] = g[r][c]
    return out

def solve_easy_32_fill_between_row_endpoints(g: Grid) -> Grid:
    out = clone(g)
    h, w = dims(g)
    for r in range(h):
        nz = [(c, g[r][c]) for c in range(w) if g[r][c] != 0]
        if len(nz) == 2 and nz[0][1] == nz[1][1]:
            c0, col = nz[0]
            c1, _ = nz[1]
            for c in range(min(c0, c1), max(c0, c1)+1):
                out[r][c] = col
    return out

def solve_easy_33_stamp_template_at_marker(g: Grid) -> Grid:
    comps = components4_any([[0 if v == 8 else v for v in row] for row in g])
    template = max(comps, key=len)
    crop = comp_crop(g, template)
    marker = next((r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == 8)
    out = clone(g)
    out[marker[0]][marker[1]] = 0
    paste(out, crop, marker[0], marker[1])
    return out

def solve_easy_34_keep_rarest_color(g: Grid) -> Grid:
    cnt = Counter(v for row in g for v in row if v != 0)
    rare = min(cnt, key=lambda k: (cnt[k], k))
    out = zeros(*dims(g))
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v == rare:
                out[r][c] = v
    return out

def solve_easy_35_hollow_solid_rectangles(g: Grid) -> Grid:
    out = clone(g)
    for comp in components4_color(g, 6):
        r0, c0, r1, c1 = bbox(comp)
        area = (r1-r0+1) * (c1-c0+1)
        if len(comp) == area:
            for r in range(r0+1, r1):
                for c in range(c0+1, c1):
                    out[r][c] = 0
    return out

def solve_medium_29_directional_rays_by_seed_color(g: Grid) -> Grid:
    h, w = dims(g)
    out = zeros(h, w)
    hpaint, vpaint = set(), set()
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v == 5:
                out[r][c] = 5
            elif v == 2:
                hpaint.update(ray_until_block(g, (r, c), 0, 1, blockers={5}, include_start=True))
                hpaint.update(ray_until_block(g, (r, c), 0, -1, blockers={5}))
            elif v == 1:
                vpaint.update(ray_until_block(g, (r, c), 1, 0, blockers={5}, include_start=True))
                vpaint.update(ray_until_block(g, (r, c), -1, 0, blockers={5}))
    for cell in hpaint | vpaint:
        r, c = cell
        if g[r][c] == 5:
            continue
        if cell in hpaint and cell in vpaint:
            out[r][c] = 6
        elif cell in hpaint:
            out[r][c] = 7
        else:
            out[r][c] = 8
    return out

def solve_medium_30_crop_components_and_pack_left_to_right(g: Grid) -> Grid:
    comps = components4_any(g)
    comps.sort(key=lambda comp: (bbox(comp)[1], bbox(comp)[0]))
    crops = [comp_crop(g, comp) for comp in comps]
    return pack_horiz_top(crops, sep=1)

def solve_medium_31_scale_key_adjacent_component(g: Grid) -> Grid:
    marker = next((r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == 8)
    # components excluding marker
    gg = [[0 if v == 8 else v for v in row] for row in g]
    for comp in components4_any(gg):
        s = set(comp)
        for r, c in comp:
            if max(abs(r-marker[0]), abs(c-marker[1])) <= 1:
                crop = comp_crop(g, comp)
                return scale_grid(crop, 2)
    raise AssertionError("no marked component")

def solve_medium_32_fill_frame_intersections(g: Grid) -> Grid:
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    r0, c0, r1, c1 = bbox(cells)
    marked_rows = [r for r in range(r0+1, r1) if g[r][c0] == 2]
    marked_cols = [c for c in range(c0+1, c1) if g[r0][c] == 3]
    out = clone(g)
    for r in marked_rows:
        for c in marked_cols:
            out[r][c] = 7
    return out

def solve_medium_33_extract_bisymmetric_component(g: Grid) -> Grid:
    for comp in components4_any(g):
        offs = normalize_offsets(comp)
        if is_h_symmetric_offsets(offs) and is_v_symmetric_offsets(offs):
            return comp_crop(g, comp)
    raise AssertionError("no bisymmetric component")

def solve_medium_34_component_count_columns(g: Grid) -> Grid:
    colors = sorted({v for row in g for v in row if v != 0})
    counts = []
    for color in colors:
        counts.append(len(components4_color(g, color)))
    h = max(counts)
    w = 2 * len(colors) - 1
    out = zeros(h, w)
    for i, (color, count) in enumerate(zip(colors, counts)):
        col = 2 * i
        for k in range(count):
            out[h-1-k][col] = color
    return out

def solve_medium_35_mirror_component_across_pivot(g: Grid) -> Grid:
    pivot = next((r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == 8)
    gg = [[0 if v == 8 else v for v in row] for row in g]
    comp = max(components4_any(gg), key=len)
    out = zeros(*dims(g))
    out[pivot[0]][pivot[1]] = 8
    pr, pc = pivot
    for r, c in comp:
        v = g[r][c]
        for rr, cc in {(r, c), (r, 2*pc-c), (2*pr-r, c), (2*pr-r, 2*pc-c)}:
            if 0 <= rr < len(out) and 0 <= cc < len(out[0]):
                out[rr][cc] = v
    return out

def solve_hard_29_local_rays_in_chambers(g: Grid) -> Grid:
    out = clone(g)
    frames = [comp for comp in components4_color(g, 5) if is_rect_border_component(comp)]
    for frame in frames:
        r0, c0, r1, c1 = bbox(frame)
        bounds = (r0+1, c0+1, r1-1, c1-1)
        seeds = [(r, c, g[r][c]) for r in range(bounds[0], bounds[2]+1) for c in range(bounds[1], bounds[3]+1) if g[r][c] in (1, 2)]
        for r, c, seed in seeds:
            if seed == 2:
                cells = set(ray_until_block(g, (r, c), 0, 1, blockers={4,5}, bounds=bounds, include_start=True))
                cells |= set(ray_until_block(g, (r, c), 0, -1, blockers={4,5}, bounds=bounds))
            else:
                cells = set(ray_until_block(g, (r, c), 1, 0, blockers={4,5}, bounds=bounds, include_start=True))
                cells |= set(ray_until_block(g, (r, c), -1, 0, blockers={4,5}, bounds=bounds))
            for rr, cc in cells:
                out[rr][cc] = 7
    return out

def solve_hard_30_assemble_transform_panel(g: Grid) -> Grid:
    keys = [v for v in g[-1] if v in (1,2,3,4)]
    gg = clone(g)
    for c, v in enumerate(gg[-1]):
        if v in (1,2,3,4):
            gg[-1][c] = 0
    template = comp_crop(gg, max(components4_any(gg), key=len))
    trans = [transform_by_key(template, k) for k in keys]
    cell_h = max(dims(t)[0] for t in trans)
    cell_w = max(dims(t)[1] for t in trans)
    out = zeros(cell_h*2+1, cell_w*2+1)
    positions = [(0,0),(0,cell_w+1),(cell_h+1,0),(cell_h+1,cell_w+1)]
    for t, (r, c) in zip(trans, positions):
        paste(out, t, r, c)
    return out

def solve_hard_31_boolean_template_combine_by_key(g: Grid) -> Grid:
    key = next(v for row in g for v in row if v in (4,6,8))
    a_cells = [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v == 2]
    b_cells = [(r,c) for r,row in enumerate(g) for c,v in enumerate(row) if v == 3]
    a = offsets_to_grid(normalize_offsets(a_cells), color=1)
    b = offsets_to_grid(normalize_offsets(b_cells), color=1)
    h = max(dims(a)[0], dims(b)[0])
    w = max(dims(a)[1], dims(b)[1])
    aa = zeros(h,w); bb = zeros(h,w)
    paste(aa, a, 0, 0); paste(bb, b, 0, 0)
    out = zeros(h,w)
    for r in range(h):
        for c in range(w):
            av = aa[r][c] != 0
            bv = bb[r][c] != 0
            if key == 4:
                ok = av or bv
            elif key == 6:
                ok = av and bv
            else:
                ok = (av != bv)
            if ok:
                out[r][c] = 7
    return out

def solve_hard_32_shape_match_matrix(g: Grid) -> Grid:
    comps = components4_any(g)
    comps.sort(key=lambda comp: (bbox(comp)[1], bbox(comp)[0]))
    crops = [offsets_to_grid(nonzero_offsets(comp_crop(g, comp)), color=1) for comp in comps]
    n = len(crops)
    out = zeros(n, n)
    for i in range(n):
        for j in range(n):
            if same_shape(crops[i], crops[j]):
                out[i][j] = 8
    return out

def solve_hard_33_local_transform_gallery_sorted_by_width(g: Grid) -> Grid:
    key_positions = [(r, c, v) for r, row in enumerate(g) for c, v in enumerate(row) if v in (1,2,3,4)]
    gg = clone(g)
    for r, c, _ in key_positions:
        gg[r][c] = 0
    comps = components4_any(gg)
    items = []
    for kr, kc, key in key_positions:
        target = None
        for comp in comps:
            r0, c0, r1, c1 = bbox(comp)
            if kr == r0 - 1 and kc == c0:
                target = comp
                break
        if target is None:
            raise AssertionError("no target for key")
        crop = comp_crop(g, target)
        crop = transform_by_key(crop, key)
        items.append(crop)
    items.sort(key=lambda crop: (-dims(crop)[1], -dims(crop)[0]))
    return pack_horiz_top(items, sep=1)

def solve_hard_34_overlay_count_map_from_components(g: Grid) -> Grid:
    crops = [offsets_to_grid(nonzero_offsets(comp_crop(g, comp)), color=1) for comp in components4_any(g)]
    return overlay_counts(crops)

def solve_hard_35_fill_holed_component_with_key_color(g: Grid) -> Grid:
    key = next(v for row in g for v in row if v in (8,9))
    gg = [[0 if v in (8,9) else v for v in row] for row in g]
    for comp in components4_any(gg):
        crop = comp_crop(g, comp)
        filled = fill_holes_with_key(crop, key)
        if filled != crop:
            return filled
    raise AssertionError("no holed component")


SOLVERS = {
    "easy_29_shoot_rays_to_walls": solve_easy_29_shoot_rays_to_walls,
    "easy_30_crop_nonzero_bbox": solve_easy_30_crop_nonzero_bbox,
    "easy_31_complete_main_diagonal_symmetry": solve_easy_31_complete_main_diagonal_symmetry,
    "easy_32_fill_between_row_endpoints": solve_easy_32_fill_between_row_endpoints,
    "easy_33_stamp_template_at_marker": solve_easy_33_stamp_template_at_marker,
    "easy_34_keep_rarest_color": solve_easy_34_keep_rarest_color,
    "easy_35_hollow_solid_rectangles": solve_easy_35_hollow_solid_rectangles,
    "medium_29_directional_rays_by_seed_color": solve_medium_29_directional_rays_by_seed_color,
    "medium_30_crop_components_and_pack_left_to_right": solve_medium_30_crop_components_and_pack_left_to_right,
    "medium_31_scale_key_adjacent_component": solve_medium_31_scale_key_adjacent_component,
    "medium_32_fill_frame_intersections": solve_medium_32_fill_frame_intersections,
    "medium_33_extract_bisymmetric_component": solve_medium_33_extract_bisymmetric_component,
    "medium_34_component_count_columns": solve_medium_34_component_count_columns,
    "medium_35_mirror_component_across_pivot": solve_medium_35_mirror_component_across_pivot,
    "hard_29_local_rays_in_chambers": solve_hard_29_local_rays_in_chambers,
    "hard_30_assemble_transform_panel": solve_hard_30_assemble_transform_panel,
    "hard_31_boolean_template_combine_by_key": solve_hard_31_boolean_template_combine_by_key,
    "hard_32_shape_match_matrix": solve_hard_32_shape_match_matrix,
    "hard_33_local_transform_gallery_sorted_by_width": solve_hard_33_local_transform_gallery_sorted_by_width,
    "hard_34_overlay_count_map_from_components": solve_hard_34_overlay_count_map_from_components,
    "hard_35_fill_holed_component_with_key_color": solve_hard_35_fill_holed_component_with_key_color,
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
    bank_path = Path(__file__).with_name("arc_puzzle_bank_fifth_21.json")
    bank = json.loads(bank_path.read_text())
    verify_bank(bank)
