"""Generator for puzzle 705dfdee.

Rule: 4-connected components in bg=0; recolor each based on whether
its bbox touches the grid border. Border-touching → 2, interior → 8.

Combinatorial axes (8): grid_h/w, n_border_objs, n_interior_objs,
obj_color_kind, obj_size_range, obj_shape, position_bias,
asymmetry_force.
Degenerates: all_border, all_interior, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "04c98e3e35bb"
VERSION = "1.1.0"
TASK_ID = "04c98e3e35bb"
SUMMARY = "Objects on bg=0; rule recolors by border-touching status."

INVARIANTS = [
    "background is 0",
    ">=2 4-connected objects",
    ">=1 object touches grid border",
    ">=1 object is strictly interior",
]

OBJ_SHAPES = ("rect", "L", "T", "plus", "blob", "line", "single")
DEGENERATE_TEXTURES = ("all_border", "all_interior", "single_object")
HELPFUL_TEXTURES = OBJ_SHAPES

AXES = {
    "grid_h":           {"type": "int", "default": "rng 12..18", "valid": "8..25"},
    "grid_w":           {"type": "int", "default": "rng 12..18", "valid": "8..25"},
    "n_border_objs":    {"type": "int", "default": "rng 1..3", "valid": "0..4"},
    "n_interior_objs":  {"type": "int", "default": "rng 1..3", "valid": "0..4"},
    "obj_size_min":     {"type": "int", "default": "2", "valid": "1..5"},
    "obj_size_max":     {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "obj_shape":        {"type": "str", "default": "rng helpful",
                         "valid": "|".join(OBJ_SHAPES)},
    "obj_color":        {"type": "color", "default": "rng (≠0,2,8)",
                         "valid": "1..9 (≠2,8)"},
    "asymmetry_force":  {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for obj_shape",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 8, 12
    elif difficulty == "hard":
        h_lo, h_hi = 18, 25
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_border = int(overrides.get("n_border_objs",
                                 ctx.draw_int("n_border_objs", 1, 3)))
    n_interior = int(overrides.get("n_interior_objs",
                                   ctx.draw_int("n_interior_objs", 1, 3)))
    n_border = max(1, min(4, n_border))
    n_interior = max(1, min(4, n_interior))
    color = int(overrides.get("obj_color",
                              ctx.draw_color("obj_color",
                                             exclude={0, 2, 8})))
    shape = (overrides.get("texture") or
             overrides.get("obj_shape")
             or ctx.draw_choice("obj_shape", list(OBJ_SHAPES)))
    s_min = int(overrides.get("obj_size_min", 2))
    s_max = int(overrides.get("obj_size_max",
                              ctx.draw_int("obj_size_max", 3, 5)))
    s_min = max(1, min(s_min, 5))
    s_max = max(s_min, min(6, s_max))
    g = full_grid(h, w, 0)
    placed_b = 0
    for _ in range(n_border * 6):
        if placed_b >= n_border:
            break
        cells = _shape_cells(shape, s_min, s_max, rng)
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
            for dr, dc in cells:
                g[rr + dr][rc + dc] = color
            placed_b += 1
    placed_i = 0
    for _ in range(n_interior * 8):
        if placed_i >= n_interior:
            break
        cells = _shape_cells(shape, s_min, s_max, rng)
        if place_no_overlap(rng, g, cells, color, bg=0,
                            margin=1, max_tries=30) is not None:
            placed_i += 1
    if placed_b == 0:
        g[0][0] = color
    if placed_i == 0:
        cr, cc = h // 2, w // 2
        if g[cr][cc] == 0:
            g[cr][cc] = color
    return g


def _shape_cells(shape, s_min, s_max, rng):
    if shape == "rect":
        rh = rng.randint(s_min, s_max); rw = rng.randint(s_min, s_max)
        return normalize(rect_cells(rh, rw))
    if shape == "L":
        n = rng.randint(s_min, s_max)
        return normalize([(0, c) for c in range(n)] + [(r, 0) for r in range(1, n)])
    if shape == "T":
        n = max(3, rng.randint(s_min, s_max))
        cells = [(0, c) for c in range(n)] + [(r, n // 2) for r in range(1, n)]
        return normalize(cells)
    if shape == "plus":
        n = max(2, rng.randint(s_min, s_max))
        return normalize([(0, c) for c in range(-n + 1, n)]
                         + [(r, 0) for r in range(-n + 1, n)])
    if shape == "blob":
        cells = [(0, 0)]
        for _ in range(rng.randint(s_min * 2, s_max * 3)):
            r, c = rng.choice(cells)
            dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            new_cell = (r + dr, c + dc)
            if new_cell not in cells:
                cells.append(new_cell)
        return normalize(cells)
    if shape == "line":
        n = rng.randint(s_min + 1, s_max + 1)
        if rng.random() < 0.5:
            return [(0, c) for c in range(n)]
        return [(r, 0) for r in range(n)]
    if shape == "single":
        return [(0, 0)]
    rh = rng.randint(s_min, s_max); rw = rng.randint(s_min, s_max)
    return normalize(rect_cells(rh, rw))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 3, 4, 5, 6, 7, 9])
    if name == "all_border":
        # Place 3 objects all on borders
        for r, c in [(0, 0), (0, w - 2), (h - 2, w // 2)]:
            for dr in range(2):
                for dc in range(2):
                    if r + dr < h and c + dc < w:
                        g[r + dr][c + dc] = color
        return g
    if name == "all_interior":
        for r, c in [(h // 3, w // 3), (h // 2, w // 2),
                     (2 * h // 3, 2 * w // 3)]:
            if 1 <= r < h - 1 and 1 <= c < w - 1:
                g[r][c] = color
        return g
    if name == "single_object":
        cr, cc = h // 2, w // 2
        for dr in range(2):
            for dc in range(2):
                if cr + dr < h - 1 and cc + dc < w - 1:
                    g[cr + dr][cc + dc] = color
        return g
    return g
