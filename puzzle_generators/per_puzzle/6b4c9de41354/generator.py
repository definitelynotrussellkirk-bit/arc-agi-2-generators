"""Generator for puzzle 49dcbdbc.

Rule: 4-connected components in bg=0; if any cell touches grid border
→ recolor to 2, else → 8. (Same family as 705dfdee/eb3fb5b2.)

Combinatorial axes (8): grid_h/w, n_border_objs, n_interior_objs,
obj_shape, obj_size, palette_size, position_bias, asymmetry_force.
Degenerates: all_border, all_interior, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import (
    L_TROMINO_NE, L_TROMINO_NW, L_TROMINO_SE, L_TROMINO_SW,
    normalize, rect_cells,
)
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "6b4c9de41354"
VERSION = "1.1.0"
TASK_ID = "6b4c9de41354"
SUMMARY = "Objects on bg=0; rule recolors by border-touching status."

INVARIANTS = [
    "background is 0",
    "non-zero components separated by background",
    ">=1 object touches grid border",
    ">=1 object is fully interior",
]

OBJ_SHAPES = ("L_tromino", "rect_2x2", "single", "line",
              "L_5cell", "blob")
DEGENERATE_TEXTURES = ("all_border", "all_interior", "single_object")
HELPFUL_TEXTURES = OBJ_SHAPES

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":            {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "n_border_objs":     {"type": "int", "default": "rng 1..3", "valid": "0..4"},
    "n_interior_objs":   {"type": "int", "default": "rng 1..3", "valid": "0..4"},
    "obj_shape":         {"type": "str", "default": "rng helpful",
                          "valid": "|".join(OBJ_SHAPES)},
    "palette_size":      {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "position_bias":     {"type": "str", "default": "rng spread|corners|edges",
                          "valid": "spread|corners|edges"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "texture":           {"type": "str", "default": "alias for obj_shape",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_border = int(overrides.get("n_border_objs",
                                 ctx.draw_int("n_border_objs", 1, 3)))
    n_interior = int(overrides.get("n_interior_objs",
                                   ctx.draw_int("n_interior_objs", 1, 3)))
    n_palette = int(overrides.get("palette_size",
                                  ctx.draw_int("palette_size", 3, 5)))
    shape = (overrides.get("texture") or
             overrides.get("obj_shape")
             or ctx.draw_choice("obj_shape", list(OBJ_SHAPES)))
    palette = list(ctx.draw_distinct_colors("colors",
                                            n=max(2, min(8, n_palette)),
                                            exclude={0, 2, 8}))
    g = full_grid(h, w, 0)
    placed_b = 0
    for _ in range(n_border * 6):
        if placed_b >= n_border:
            break
        cells = _shape_cells(shape, rng)
        rh = max(r for r, _ in cells) + 1
        rw = max(c for _, c in cells) + 1
        if rh > h or rw > w:
            continue
        side = rng.choice(["top", "bottom", "left", "right"])
        if side == "top":
            rr, rc = 0, rng.randint(0, w - rw)
        elif side == "bottom":
            rr, rc = h - rh, rng.randint(0, w - rw)
        elif side == "left":
            rr, rc = rng.randint(0, h - rh), 0
        else:
            rr, rc = rng.randint(0, h - rh), w - rw
        ok = all(g[rr + dr][rc + dc] == 0 for dr, dc in cells)
        if ok:
            color = palette[placed_b % len(palette)]
            for dr, dc in cells:
                g[rr + dr][rc + dc] = color
            placed_b += 1
    placed_i = 0
    for _ in range(n_interior * 6):
        if placed_i >= n_interior:
            break
        cells = _shape_cells(shape, rng)
        color = palette[(placed_b + placed_i) % len(palette)]
        if place_no_overlap(rng, g, cells, color, bg=0,
                            margin=1, max_tries=30) is not None:
            placed_i += 1
    if placed_b == 0:
        g[0][0] = palette[0]
    if placed_i == 0 and h > 4 and w > 4:
        if g[h // 2][w // 2] == 0:
            g[h // 2][w // 2] = palette[-1]
    return g


def _shape_cells(shape, rng):
    if shape == "L_tromino":
        return list(rng.choice([L_TROMINO_NE, L_TROMINO_NW,
                                 L_TROMINO_SE, L_TROMINO_SW]))
    if shape == "rect_2x2":
        return normalize(rect_cells(2, 2))
    if shape == "single":
        return [(0, 0)]
    if shape == "line":
        n = rng.randint(2, 4)
        return [(0, c) for c in range(n)] if rng.random() < 0.5 else \
               [(r, 0) for r in range(n)]
    if shape == "L_5cell":
        return [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)]
    if shape == "blob":
        cells = [(0, 0)]
        for _ in range(rng.randint(3, 6)):
            r, c = rng.choice(cells)
            dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            new = (r + dr, c + dc)
            if new not in cells:
                cells.append(new)
        return normalize(cells)
    return list(L_TROMINO_NE)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([3, 4, 5, 6, 7, 9])
    if name == "all_border":
        for r, c in [(0, 0), (0, w - 2), (h - 2, 0), (h - 2, w - 2)]:
            for dr in range(2):
                for dc in range(2):
                    if r + dr < h and c + dc < w:
                        g[r + dr][c + dc] = color
        return g
    if name == "all_interior":
        for r, c in [(h // 3, w // 3), (h // 2, w // 2), (2 * h // 3, 2 * w // 3)]:
            if 1 <= r < h - 1 and 1 <= c < w - 1:
                g[r][c] = color
        return g
    if name == "single_object":
        cr, cc = h // 2, w // 2
        if 1 <= cr < h - 1 and 1 <= cc < w - 1:
            g[cr][cc] = color
            if cr + 1 < h - 1:
                g[cr + 1][cc] = color
        return g
    return g
