"""Generator for arc_additional_puzzles_21_set11_bundle:H75.

Rule: cmds = leading non-zero cells in row 0. Bbox-crop body (r ≥ 1).
Apply each cmd: 1=cw, 2=flip-lr, 3=flip-ud, else=transpose.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cmds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmds, no_motif, invalid_cmd.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "26879f28ee60"
VERSION = "1.1.0"
TASK_ID = "26879f28ee60"
SUMMARY = "Row 0 has 1-3 cmd cells in leading positions + small blob below."

INVARIANTS = [
    "row 0 starts with 1-3 non-zero cells (cmds ∈ 1..4) followed by 0s",
    "below row 0 is a small 2x2 multi-color motif",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmds", "no_motif", "invalid_cmd")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cmds":         {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "row0_cmds",
                       "valid": "row0_cmds"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        n_cmds = ctx.draw_int("n_cmds", 1, 1)
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        n_cmds = ctx.draw_int("n_cmds", 2, 3)
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        n_cmds = ctx.draw_int("n_cmds", 1, 3)
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    for i in range(n_cmds):
        g[0][i] = rng.randint(1, 4)
    g[3][3] = 1; g[3][4] = 2
    g[4][3] = 3; g[4][4] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_cmds":
        # row 0 is empty → no transform sequence, output is just the cropped body
        g[3][3] = 1; g[3][4] = 2
        g[4][3] = 3; g[4][4] = 4
        return g
    if name == "no_motif":
        # cmds present but no motif below → nothing to transform
        g[0][0] = 2; g[0][1] = 3
        return g
    if name == "invalid_cmd":
        # cmd value outside the 1-4 vocabulary → falls into default-transpose branch only
        g[0][0] = 7; g[0][1] = 9
        g[3][3] = 1; g[3][4] = 2
        g[4][3] = 3; g[4][4] = 4
        return g
    return g
