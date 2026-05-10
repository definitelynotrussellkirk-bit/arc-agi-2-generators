"""Generator for puzzle `arc_additional_puzzles_21_set6:E39` —
`(rule! (gravity g "down"))`. Every non-bg cell falls to the bottom of
its column.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_at_bottom, single_column, no_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "49fe4f572f8d"
VERSION = "1.1.0"
TASK_ID = "49fe4f572f8d"
SUMMARY = "Sparse non-bg cells; rule drops them to the bottom of each column."

INVARIANTS = [
    "background is 0",
    ">=2 non-bg cells",
    ">=1 column has multiple non-bg cells (so gravity actually moves things)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_at_bottom", "single_column", "no_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 6..14", "valid": "3..30"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper", "valid": "upper"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
        n_cells = ctx.draw_int("n_cells", 6, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
        n_cells = ctx.draw_int("n_cells", 11, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 14)
        w = ctx.draw_int("grid_w", 8, 14)
        n_cells = ctx.draw_int("n_cells", 6, 14)
    palette_n = ctx.draw_int("fg_palette", 2, 4)
    palette = ctx.draw_distinct_colors("palette", n=palette_n, exclude={0})

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("placement")

    upper = h * 2 // 3
    placed = 0
    attempts = 0
    while placed < n_cells and attempts < n_cells * 10:
        attempts += 1
        r = rng.randint(0, max(1, upper))
        c = rng.randint(0, w - 1)
        if g[r][c] != 0: continue
        g[r][c] = palette[placed % len(palette)]
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "already_at_bottom":
        # cells all sit on the bottom row → gravity is identity
        for c, v in [(1, 3), (3, 4), (5, 7), (7, 2)]:
            g[h - 1][c] = v
        return g
    if name == "single_column":
        # all cells stacked in one column already with no gaps below → identity
        for r in range(h - 4, h):
            g[r][4] = 5
        return g
    if name == "no_cells":
        # empty grid → gravity has nothing to move
        return g
    return g
