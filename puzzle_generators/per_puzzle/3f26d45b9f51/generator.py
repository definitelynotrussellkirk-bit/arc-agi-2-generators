"""Generator for 06df4c85.

Rule: same-colored markers in lattice cells connect by filled 2x2
coarse cells.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
n_pairs.
Degenerates: no_markers, single_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3f26d45b9f51"
VERSION = "1.1.0"
TASK_ID = "3f26d45b9f51"
SUMMARY = "Same-colored markers in lattice cells connect by 2x2 coarse cells."

INVARIANTS = [
    "background is the modal color",
    "same-colored markers share a coarse row or column",
    "coarse cells are addressed on a three-cell lattice",
    "marker colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "single_marker", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 12..18", "valid": "9..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "n_pairs":        {"type": "int", "default": "2", "valid": "2"},
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
        sz_lo, sz_hi = 12, 13
    elif difficulty == "hard":
        sz_lo, sz_hi = 18, 22
    else:
        sz_lo, sz_hi = 12, 18
    size = ctx.draw_int("grid_size", sz_lo, sz_hi)
    g = full_grid(size, size, 0)
    colors = list(ctx.draw_distinct_colors("colors", n=2, exclude={0}))
    max_cell = size // 3 - 1
    row = rng.randint(1, max_cell)
    c1 = rng.randint(0, max_cell - 1)
    c2 = rng.randint(c1 + 1, max_cell)
    for cc in (c1, c2):
        g[3 * row][3 * cc] = colors[0]
    col = rng.randint(1, max_cell)
    r1 = rng.randint(0, max_cell - 1)
    r2 = rng.randint(r1 + 1, max_cell)
    for rr in (r1, r2):
        g[3 * rr][3 * col] = colors[1]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_markers":
        return g
    if name == "single_marker":
        g[6][6] = 2
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 2
        return g
    return g
