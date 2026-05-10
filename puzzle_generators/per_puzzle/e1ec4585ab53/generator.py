"""Generator for arc_additional_puzzles_21_set16_bundle:H112 — row/column command mosaic.

Rule: 6×6 input — (0, 3) and (0, 5) are column commands, (3, 0) and (5, 0) are
row commands; (3..5, 3..5) is a 3×3 source motif. Output is a 2×2 mosaic
where cell[r][c] = col_cmd[c](row_cmd[r](source)), packed with 1-cell gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_commands, no_motif, empty_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e1ec4585ab53"
VERSION = "1.1.0"
TASK_ID = "e1ec4585ab53"

SUMMARY = "6x6 grid: 2 row commands + 2 column commands + 3x3 source motif → 2x2 mosaic output."

INVARIANTS = [
    "background is 0",
    "(0, 3) and (0, 5) hold column transform codes (each 1..7)",
    "(3, 0) and (5, 0) hold row transform codes (each 1..7)",
    "rows 3-5, cols 3-5 hold a 3x3 source motif with 3-6 non-zero cells",
    "command cells are non-zero and distinct from row 0/col 0 padding",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_commands", "no_motif", "empty_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6..6"},
    "grid_w":         {"type": "int", "default": "6", "valid": "6..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_cells":    {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 5..7", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "command_strip_plus_3x3_motif",
                       "valid": "command_strip_plus_3x3_motif"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..7", "valid": "2..8"},
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
        n_motif_lo, n_motif_hi = 3, 4
    elif difficulty == "hard":
        n_motif_lo, n_motif_hi = 5, 6
    else:
        n_motif_lo, n_motif_hi = 3, 6
    rng = ctx.draw_rng("layout")
    g = full_grid(6, 6, 0)
    # commands: codes 1..7 (1 identity, 2 cw, 3 180, 4 transpose, 5 flip-lr, 6 flip-ud, 7 transpose-again, else anti-transpose)
    g[0][3] = rng.randint(1, 7)
    g[0][5] = rng.randint(1, 7)
    g[3][0] = rng.randint(1, 7)
    g[5][0] = rng.randint(1, 7)
    # 3x3 motif
    n_motif = rng.randint(n_motif_lo, n_motif_hi)
    cells = [(r, c) for r in range(3) for c in range(3)]
    chosen = rng.sample(cells, n_motif)
    motif_color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    for r, c in chosen:
        g[3 + r][3 + c] = motif_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 6, 0)
    if name == "no_commands":
        # motif present but no row/col command codes → no transforms defined
        for r in range(3):
            for c in range(3):
                g[3 + r][3 + c] = 4
        return g
    if name == "no_motif":
        # commands present but no source motif → nothing to transform
        g[0][3] = 1; g[0][5] = 2; g[3][0] = 3; g[5][0] = 4
        return g
    if name == "empty_grid":
        # everything blank → no commands and no motif
        return g
    return g
