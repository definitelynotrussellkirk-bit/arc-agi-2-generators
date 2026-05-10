"""Generator for arc_puzzle_bank_21_more:medium_b07 — Apply column gravity.

Rule: `(rule! (gravity g "down"))`
  Drop every non-zero cell straight down until it lands on another
  non-zero cell or the grid floor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_at_bottom, single_column_full, empty_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "557449d8b860"
VERSION = "1.1.0"
TASK_ID = "557449d8b860"
SUMMARY = "Sparse non-zero cells in a small grid; gravity pulls them down."

INVARIANTS = [
    "grid dimensions in [5, 10] x [5, 10]",
    "between 3 and 8 non-zero cells",
    "at least one non-zero cell has empty cells below it (output != input)",
    "non-zero cells use 1..9 colors (no 0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_at_bottom", "single_column_full", "empty_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..10", "valid": "5..15"},
    "grid_w":         {"type": "int", "default": "rng 5..10", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 3..8", "valid": "1..30"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper", "valid": "upper"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
        n_cells = ctx.draw_int("n_cells", 3, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
        n_cells = ctx.draw_int("n_cells", 6, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 10)
        w = ctx.draw_int("grid_w", 5, 10)
        n_cells = ctx.draw_int("n_cells", 3, min(8, h * w // 3))

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("placements")
    upper_bound = max(1, int(h * 0.6))
    positions: set[tuple[int, int]] = set()
    while len(positions) < n_cells:
        r = rng.randint(0, upper_bound - 1)
        c = rng.randint(0, w - 1)
        positions.add((r, c))

    color_rng = ctx.draw_rng("colors")
    for r, c in positions:
        g[r][c] = color_rng.randint(1, 9)

    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "already_at_bottom":
        # cells already sit on the floor → gravity is identity
        for c, v in [(1, 4), (3, 5), (5, 6), (7, 2)]:
            g[h - 1][c] = v
        return g
    if name == "single_column_full":
        # one column fully packed top-to-bottom → no movement possible
        for r in range(h):
            g[r][3] = 7
        return g
    if name == "empty_grid":
        # no cells → gravity has nothing to move
        return g
    return g
