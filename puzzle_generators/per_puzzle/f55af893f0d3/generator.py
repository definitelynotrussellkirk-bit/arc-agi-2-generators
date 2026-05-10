"""Generator for arc_additional_puzzle_bank_volume10:E68.

An orange motif left of a magenta divider is mirrored as cyan on the right.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_motif, motif_on_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f55af893f0d3"
VERSION = "1.1.0"
TASK_ID = "f55af893f0d3"
SUMMARY = "An orange motif left of a magenta divider is mirrored as cyan on the right."

INVARIANTS = [
    "background is 0",
    "there is a full-height magenta divider column",
    "all orange source cells lie to the left of the divider",
    "the mirrored right-side cells are initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_motif", "motif_on_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "7..25"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 4..8", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "left_motif_with_divider",
                       "valid": "left_motif_with_divider"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n_cells = ctx.draw_int("n_cells", 3, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 15)
        n_cells = ctx.draw_int("n_cells", 6, 8)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 9, 15)
        n_cells = ctx.draw_int("n_cells", 4, 8)
    rng = ctx.draw_rng("placement")
    axis = rng.randint(3, w - 4)
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][axis] = 6
    left_cols = list(range(max(0, 2 * axis - (w - 1)), axis))
    if not left_cols:
        left_cols = [axis - 1]
    start = (rng.randint(1, h - 2), rng.choice(left_cols))
    cells = {start}
    for _ in range(n_cells * 4):
        if len(cells) >= n_cells:
            break
        r, c = rng.choice(list(cells))
        dr, dc = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and nc in left_cols:
            cells.add((nr, nc))
    for r, c in cells:
        g[r][c] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # motif but no magenta divider → no axis to mirror across
        for r, c in [(2, 2), (2, 3), (3, 3)]: g[r][c] = 7
        return g
    if name == "no_motif":
        # divider but no orange source → nothing to mirror
        for r in range(h):
            g[r][5] = 6
        return g
    if name == "motif_on_divider":
        # motif overlaps divider → ambiguous left/right
        for r in range(h):
            g[r][5] = 6
        for r, c in [(2, 4), (2, 5), (3, 5)]: g[r][c] = 7
        return g
    return g
