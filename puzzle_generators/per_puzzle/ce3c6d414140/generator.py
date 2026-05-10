"""Generator for puzzle 025d127b.

Rule: hollow parallelogram-style shapes on bg=0. Output shifts the
top row right by one cell, leaves the rest in place.

Combinatorial axes (8): grid_h/w, n_objs, shape_size_min,
shape_size_max, palette_kind, palette_size, position_bias,
anchor_corner.
Degenerates: no_objs, single_obj, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_cells
from puzzle_generators.helpers.indices import (
    all_indices, connect, neighborhood_4, shift_cells,
)

GENERATOR_ID = "ce3c6d414140"
VERSION = "1.1.0"
TASK_ID = "ce3c6d414140"
SUMMARY = "Hollow parallelograms; rule shifts top edge right by one."

INVARIANTS = [
    "background is 0",
    ">=1 hollow parallelogram shapes",
    "each shape fits in-grid with bg margin",
    "shapes don't touch (>=1 bg between)",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary", "rng")
DEGENERATE_TEXTURES = ("no_objs", "single_obj", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..16", "valid": "5..28"},
    "grid_w":         {"type": "int", "default": "rng 10..16", "valid": "5..28"},
    "n_objs":         {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "shape_size_min": {"type": "int", "default": "3", "valid": "3..6"},
    "shape_size_max": {"type": "int", "default": "rng 4..6", "valid": "3..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _parallelogram(oh: int, ow: int):
    """Hollow parallelogram anchored at origin."""
    top = connect((0, 0), (0, ow - 1))
    left = connect((1, 0), (oh - 2, oh - 3))
    right = connect((1, ow), (oh - 2, ow + oh - 3))
    bot = connect((oh - 1, oh - 2), (oh - 1, oh - 3 + ow))
    return top | left | right | bot


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 9
    elif difficulty == "hard":
        h_lo, h_hi = 16, 28
    else:
        h_lo, h_hi = 10, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_objs = int(overrides.get("n_objs",
                               ctx.draw_int("n_objs", 1, 3)))
    n_objs = max(1, min(6, n_objs))
    s_min = int(overrides.get("shape_size_min", 3))
    s_max = int(overrides.get("shape_size_max",
                              ctx.draw_int("shape_size_max", 4, 6)))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size", 1, 3)))
    palette = _build_palette(palette_kind, max(1, min(6, palette_size)),
                             rng)
    g = full_grid(h, w, 0)
    free = all_indices(h, w)
    placed = 0
    for _ in range(5 * n_objs):
        if placed >= n_objs:
            break
        oh = rng.randint(s_min, s_max)
        ow = rng.randint(s_min, s_max)
        cands = [ij for ij in free
                 if ij[0] + oh <= h and ij[1] + ow + oh - 2 <= w]
        if not cands:
            continue
        loc = rng.choice(cands)
        shape = shift_cells(_parallelogram(oh, ow), loc)
        if not shape.issubset(free):
            continue
        free -= shape
        free -= neighborhood_4(shape)
        paint_cells(g, shape, rng.choice(palette))
        placed += 1
    if placed == 0:
        # Force at least one
        oh = ow = 4
        if h >= oh and w >= ow + oh - 2:
            shape = shift_cells(_parallelogram(oh, ow), (0, 0))
            paint_cells(g, shape, palette[0])
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_objs":
        return g
    if name == "single_obj":
        oh = ow = 4
        if h >= oh and w >= ow + oh - 2:
            shape = shift_cells(_parallelogram(oh, ow), (0, 0))
            paint_cells(g, shape, 3)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
