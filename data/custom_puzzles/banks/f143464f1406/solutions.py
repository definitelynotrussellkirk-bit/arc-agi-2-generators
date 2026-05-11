
"""Reference solvers for the fourth 21-task ARC-style puzzle bank."""


def blank(h, w, val=0):
    return [[val for _ in range(w)] for _ in range(h)]


def copy_grid(g):
    return [row[:] for row in g]


def dims(g):
    return len(g), len(g[0])


def paste(g, shape, top, left):
    H, W = dims(g)
    h, w = dims(shape)
    for r in range(h):
        for c in range(w):
            v = shape[r][c]
            if v != 0:
                rr, cc = top + r, left + c
                assert 0 <= rr < H and 0 <= cc < W, (rr, cc, H, W)
                g[rr][cc] = v
    return g


def crop_nonzero(g):
    cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0]
    if not cells:
        return [[0]]
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    r0, r1 = min(rs), max(rs)
    c0, c1 = min(cs), max(cs)
    return [row[c0:c1 + 1] for row in g[r0:r1 + 1]]


def rotate_cw(g):
    h, w = dims(g)
    return [[g[h - 1 - r][c] for r in range(h)] for c in range(w)]


def rotate_times(g, k):
    out = g
    for _ in range(k % 4):
        out = rotate_cw(out)
    return out


def flip_h(g):
    return [row[::-1] for row in g]


def flip_v(g):
    return g[::-1]


def bbox_cells(cells):
    rs = [r for r, c in cells]
    cs = [c for r, c in cells]
    return min(rs), max(rs), min(cs), max(cs)


def components(g):
    h, w = dims(g)
    vis = [[False] * w for _ in range(h)]
    comps = []
    for r in range(h):
        for c in range(w):
            if vis[r][c] or g[r][c] == 0:
                continue
            color = g[r][c]
            stack = [(r, c)]
            vis[r][c] = True
            cells = []
            while stack:
                x, y = stack.pop()
                cells.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < h and 0 <= ny < w and not vis[nx][ny] and g[nx][ny] == color:
                        vis[nx][ny] = True
                        stack.append((nx, ny))
            comps.append({"color": color, "cells": cells})
    return comps


def component_grid(comp):
    r0, r1, c0, c1 = bbox_cells(comp["cells"])
    out = blank(r1 - r0 + 1, c1 - c0 + 1)
    for r, c in comp["cells"]:
        out[r - r0][c - c0] = comp["color"]
    return out


def frame(color, h, w):
    g = blank(h, w)
    for r in range(h):
        g[r][0] = color
        g[r][w - 1] = color
    for c in range(w):
        g[0][c] = color
        g[h - 1][c] = color
    return g


def recolor(shape, color):
    return [[color if v != 0 else 0 for v in row] for row in shape]


def is_frame(comp):
    cells = set(comp["cells"])
    r0, r1, c0, c1 = bbox_cells(comp["cells"])
    if r1 - r0 + 1 < 3 or c1 - c0 + 1 < 3:
        return False
    border = {
        (r, c)
        for r in range(r0, r1 + 1)
        for c in range(c0, c1 + 1)
        if r in (r0, r1) or c in (c0, c1)
    }
    return cells == border


def solve_d_e1_keep_leftmost_per_row(g):
    h, w = dims(g)
    out = blank(h, w)
    for r, row in enumerate(g):
        for c, v in enumerate(row):
            if v != 0:
                out[r][c] = v
                break
    return out


def solve_d_e2_paint_up_from_seed(g):
    h, w = dims(g)
    out = blank(h, w)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                for rr in range(r + 1):
                    out[rr][c] = v
    return out


def solve_d_e3_diag_domino_to_2x2(g):
    h, w = dims(g)
    out = copy_grid(g)
    for r in range(h - 1):
        for c in range(w - 1):
            a, b, c1, d = g[r][c], g[r][c + 1], g[r + 1][c], g[r + 1][c + 1]
            if a != 0 and d == a and b == 0 and c1 == 0:
                out[r][c + 1] = a
                out[r + 1][c] = a
            if b != 0 and c1 == b and a == 0 and d == 0:
                out[r][c] = b
                out[r + 1][c + 1] = b
    return out


def solve_d_e4_seed_to_x(g):
    h, w = dims(g)
    out = blank(h, w)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                for dr, dc in [(0, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < h and 0 <= cc < w:
                        out[rr][cc] = v
    return out


def solve_d_e5_diag_down_left(g):
    h, w = dims(g)
    out = blank(h, w)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v != 0:
                rr, cc = r, c
                while rr < h and cc >= 0:
                    out[rr][cc] = v
                    rr += 1
                    cc -= 1
    return out


def solve_d_e6_mirror_right_half(g):
    h, w = dims(g)
    assert w % 2 == 0
    out = copy_grid(g)
    for r in range(h):
        for c in range(w // 2):
            out[r][c] = g[r][w - 1 - c]
    return out


def solve_d_e7_rotate_cw(g):
    return rotate_cw(g)


def solve_d_m1_move_object_to_corner_by_marker(g):
    h, w = dims(g)
    marker = None
    obj = blank(h, w)
    for r in range(h):
        for c in range(w):
            v = g[r][c]
            if v in (1, 2, 3, 4):
                marker = v
            elif v != 0:
                obj[r][c] = v
    assert marker is not None
    shape = crop_nonzero(obj)
    out = blank(h, w)
    sh, sw = dims(shape)
    if marker == 1:
        top, left = 0, 0
    elif marker == 2:
        top, left = 0, w - sw
    elif marker == 3:
        top, left = h - sh, 0
    else:
        top, left = h - sh, w - sw
    paste(out, shape, top, left)
    return out


def solve_d_m2_keep_odd_area(g):
    h, w = dims(g)
    out = blank(h, w)
    for comp in components(g):
        if len(comp["cells"]) % 2 == 1:
            for r, c in comp["cells"]:
                out[r][c] = comp["color"]
    return out


def solve_d_m3_recolor_border_touch(g):
    h, w = dims(g)
    out = blank(h, w)
    for comp in components(g):
        touch = any(r in (0, h - 1) or c in (0, w - 1) for r, c in comp["cells"])
        color = 2 if touch else 8
        for r, c in comp["cells"]:
            out[r][c] = color
    return out


def solve_d_m4_stack_object_and_vmirror(g):
    shape = crop_nonzero(g)
    return shape + flip_v(shape)


def solve_d_m5_columns_to_hbar(g):
    h, w = dims(g)
    counts = []
    colors = []
    for c in range(w):
        vals = [g[r][c] for r in range(h) if g[r][c] != 0]
        counts.append(len(vals))
        colors.append(vals[0] if vals else 0)
    width = max(counts) if counts else 1
    out = blank(w, width)
    for r in range(w):
        count = counts[r]
        color = colors[r]
        for c in range(count):
            out[r][c] = color
    return out


def solve_d_m6_center_selected_color_object(g):
    h, w = dims(g)
    comps = components(g)
    marker_comp = None
    target_color = None
    for comp in comps:
        if len(comp["cells"]) == 1:
            color = comp["color"]
            if sum(1 for c in comps if c["color"] == color) > 1:
                marker_comp = comp
                target_color = color
                break
    assert marker_comp is not None
    target_cells = []
    for comp in comps:
        if comp is marker_comp:
            continue
        if comp["color"] == target_color:
            target_cells.extend(comp["cells"])
    r0, r1, c0, c1 = bbox_cells(target_cells)
    shape = blank(r1 - r0 + 1, c1 - c0 + 1)
    for r, c in target_cells:
        shape[r - r0][c - c0] = target_color
    out = blank(h, w)
    sh, sw = dims(shape)
    top = (h - sh) // 2
    left = (w - sw) // 2
    paste(out, shape, top, left)
    return out


def solve_d_m7_fill_box_per_color(g):
    h, w = dims(g)
    out = blank(h, w)
    colors = sorted({v for row in g for v in row if v != 0})
    for color in colors:
        cells = [(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v == color]
        if not cells:
            continue
        r0, r1, c0, c1 = bbox_cells(cells)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                out[r][c] = color
    return out


def solve_d_h1_quadrant_mosaic_by_area(g):
    comps = components(g)
    assert len(comps) == 4
    items = []
    for comp in comps:
        shape = component_grid(comp)
        items.append((len(comp["cells"]), shape))
    items.sort(key=lambda x: (-x[0], dims(x[1])[0] * 100 + dims(x[1])[1]))
    shapes = [it[1] for it in items]
    h0 = max(dims(shapes[0])[0], dims(shapes[1])[0])
    h1 = max(dims(shapes[2])[0], dims(shapes[3])[0])
    w0 = max(dims(shapes[0])[1], dims(shapes[2])[1])
    w1 = max(dims(shapes[1])[1], dims(shapes[3])[1])
    out = blank(h0 + 1 + h1, w0 + 1 + w1)
    paste(out, shapes[0], 0, 0)
    paste(out, shapes[1], 0, w0 + 1)
    paste(out, shapes[2], h0 + 1, 0)
    paste(out, shapes[3], h0 + 1, w0 + 1)
    return out


def solve_d_h2_rotate_enclosed_by_frame_color(g):
    h, w = dims(g)
    out = blank(h, w)
    comps = components(g)
    frames = [comp for comp in comps if is_frame(comp) and comp["color"] in (1, 2, 3, 4)]
    for frame_comp in frames:
        color = frame_comp["color"]
        r0, r1, c0, c1 = bbox_cells(frame_comp["cells"])
        for r, c in frame_comp["cells"]:
            out[r][c] = color
        interior = blank(r1 - r0 - 1, c1 - c0 - 1)
        for r in range(r0 + 1, r1):
            for c in range(c0 + 1, c1):
                if g[r][c] != 0:
                    interior[r - (r0 + 1)][c - (c0 + 1)] = g[r][c]
        inner_shape = crop_nonzero(interior)
        rot = rotate_times(inner_shape, color - 1)
        ih, iw = dims(interior)
        sh, sw = dims(rot)
        top = r0 + 1 + (ih - sh) // 2
        left = c0 + 1 + (iw - sw) // 2
        paste(out, rot, top, left)
    return out


def solve_d_h3_recolor_stamp_template(g):
    h, w = dims(g)
    comps = components(g)
    comps_sorted = sorted(comps, key=lambda comp: len(comp["cells"]), reverse=True)
    template_comp = None
    for comp in comps_sorted:
        if len(comp["cells"]) > 1:
            template_comp = comp
            break
    assert template_comp is not None
    template_shape = [[1 if v != 0 else 0 for v in row] for row in component_grid(template_comp)]
    template_cells = set(template_comp["cells"])
    markers = []
    for comp in comps:
        if len(comp["cells"]) == 1 and comp["cells"][0] not in template_cells:
            r, c = comp["cells"][0]
            markers.append((r, c, comp["color"]))
    out = blank(h, w)
    for r, c, color in markers:
        shp = recolor(template_shape, color)
        paste(out, shp, r, c)
    return out


def solve_d_h4_xor_two_normalized_objects(g):
    comps = components(g)
    assert len(comps) == 2
    def key(comp):
        r0, r1, c0, c1 = bbox_cells(comp["cells"])
        return (r0, c0, comp["color"])
    comps = sorted(comps, key=key)
    A, B = comps
    ga = component_grid(A)
    gb = component_grid(B)
    ha, wa = dims(ga)
    hb, wb = dims(gb)
    H = max(ha, hb)
    W = max(wa, wb)
    out = blank(H, W)
    for r in range(H):
        for c in range(W):
            va = ga[r][c] if r < ha and c < wa else 0
            vb = gb[r][c] if r < hb and c < wb else 0
            if (va != 0) ^ (vb != 0):
                out[r][c] = A["color"] if va != 0 else B["color"]
    return out


def solve_d_h5_key_row_orders_gallery(g):
    h, w = dims(g)
    key = [v for v in g[0] if v != 0]
    body = [row[:] for row in g[1:]]
    comps = components(body)
    by_color = {}
    for comp in comps:
        by_color.setdefault(comp["color"], []).append(comp)
    shapes = []
    for color in key:
        comp = max(by_color[color], key=lambda c: len(c["cells"]))
        shapes.append(component_grid(comp))
    H = max(dims(s)[0] for s in shapes)
    W = sum(dims(s)[1] for s in shapes) + (len(shapes) - 1)
    out = blank(H, W)
    col = 0
    for s in shapes:
        paste(out, s, 0, col)
        col += dims(s)[1] + 1
    return out


def solve_d_h6_alternating_copies_by_marker_count(g):
    comps = components(g)
    template = max(comps, key=lambda c: len(c["cells"]))
    shape = component_grid(template)
    n = sum(1 for comp in comps if len(comp["cells"]) == 1 and comp is not template)
    assert n >= 1
    variants = [shape if i % 2 == 0 else flip_h(shape) for i in range(n)]
    H = max(dims(v)[0] for v in variants)
    W = sum(dims(v)[1] for v in variants) + (n - 1)
    out = blank(H, W)
    col = 0
    for v in variants:
        paste(out, v, 0, col)
        col += dims(v)[1] + 1
    return out


def solve_d_h7_gallery_of_frame_interiors_sorted_by_frame_color(g):
    comps = components(g)
    frames = [comp for comp in comps if is_frame(comp)]
    frames = sorted(frames, key=lambda comp: comp["color"])
    shapes = []
    for fr in frames:
        r0, r1, c0, c1 = bbox_cells(fr["cells"])
        interior = blank(r1 - r0 - 1, c1 - c0 - 1)
        for r in range(r0 + 1, r1):
            for c in range(c0 + 1, c1):
                if g[r][c] != 0 and g[r][c] != fr["color"]:
                    interior[r - (r0 + 1)][c - (c0 + 1)] = g[r][c]
        shapes.append(crop_nonzero(interior))
    H = max(dims(s)[0] for s in shapes)
    W = sum(dims(s)[1] for s in shapes) + len(shapes) - 1
    out = blank(H, W)
    col = 0
    for s in shapes:
        paste(out, s, 0, col)
        col += dims(s)[1] + 1
    return out
