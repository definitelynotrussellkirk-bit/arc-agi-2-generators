"""Generator for e21a174a.

Rule: 8-connected objects sorted by top row; rule reverses vertical
stacking.

Combinatorial axes (8): grid_h/w, n_objs, palette_kind, shape_variant,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_shape, no_objects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5d8cd44d79d0"
VERSION = "1.1.0"
TASK_ID = "5d8cd44d79d0"
SUMMARY = "2-3 stacked horizontal shapes at distinct row ranges, distinct colors."

INVARIANTS = [
    "2-3 objects, each within a few rows tall",
    "objects are 8-connected, distinct colors",
    "objects are vertically separated (no row overlap)",
]

SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 3),
     (2, 0), (2, 1), (2, 2), (2, 3)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_shape", "no_objects", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "n_objs":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_variant":  {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "scattered|stacked|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 8, 9
        no_lo, no_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
        no_lo, no_hi = 3, 4
    else:
        h_lo, h_hi = 9, 12
        no_lo, no_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    n_objs = int(overrides.get("n_objs",
                               ctx.draw_int("n_objs", no_lo, no_hi)))
    n_objs = max(2, min(4, n_objs))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_objs, rng)
    chosen_shapes = [rng.choice(SHAPES) for _ in range(n_objs)]
    cur_row = 1
    for shape, color in zip(chosen_shapes, palette):
        sh = max(r for r, c in shape) + 1
        sw = max(c for r, c in shape) + 1
        if cur_row + sh + 1 >= h:
            break
        c0 = rng.randint(1, max(1, w - sw - 1))
        for dr, dc in shape:
            g[cur_row + dr][c0 + dc] = color
        cur_row += sh + 1
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 11, 9
    g = full_grid(h, w, 0)
    if name == "same_shape":
        for dr, dc in SHAPES[0]:
            g[1 + dr][2 + dc] = 2
        for dr, dc in SHAPES[0]:
            g[5 + dr][2 + dc] = 2
        return g
    if name == "no_objects":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
