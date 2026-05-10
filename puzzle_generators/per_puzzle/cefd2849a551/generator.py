"""Generator for arc_puzzle_bank_21_set6_s:S6_E2.

Rule: a single solid object is reduced to its 4-neighbor boundary.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_object, hollow_object, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cefd2849a551"
VERSION = "1.1.0"
TASK_ID = "cefd2849a551"

SUMMARY = "A single solid object is reduced to its four-neighbor boundary."

INVARIANTS = [
    "background is 0",
    "there is exactly one nonzero object",
    "the object is solid and 4-connected",
    "at least one object cell is interior and will be erased",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_object", "hollow_object", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_kind":     {"type": "choice", "default": "rng rect|step", "valid": "rect|step"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "single_solid_object",
                       "valid": "single_solid_object"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_rect(g, r0, c0, rh, rw, color):
    for r in range(r0, r0 + rh):
        for c in range(c0, c0 + rw):
            g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 11)
    shape_kind = ctx.draw_choice("shape_kind", ["rect", "step"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    if shape_kind == "rect":
        rh = rng.randint(4, min(6, h - 1))
        rw = rng.randint(4, min(6, w - 1))
        r0 = rng.randint(0, h - rh)
        c0 = rng.randint(0, w - rw)
        _draw_rect(g, r0, c0, rh, rw, 4)
    else:
        rh1 = rng.randint(3, min(4, h - 2))
        rw1 = rng.randint(3, min(5, w - 3))
        rh2 = rng.randint(2, min(3, h - rh1 + 1))
        rw2 = rng.randint(2, min(3, w - rw1 + 1))
        r0 = rng.randint(0, h - (rh1 + rh2 - 1))
        c0 = rng.randint(0, w - (rw1 + rw2 - 1))
        _draw_rect(g, r0, c0, rh1, rw1, 4)
        _draw_rect(g, r0 + rh1 - 1, c0 + rw1 - 1, rh2, rw2, 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_object":
        # blank → no object, rule has no boundary to extract
        return g
    if name == "hollow_object":
        # already a hollow ring → no interior cells to erase, rule is identity
        for c in range(1, 6): g[1][c] = 4; g[5][c] = 4
        for r in range(1, 6): g[r][1] = 4; g[r][5] = 4
        return g
    if name == "single_cell":
        # single cell → no interior, boundary equals object (identity)
        g[3][4] = 4
        return g
    return g
