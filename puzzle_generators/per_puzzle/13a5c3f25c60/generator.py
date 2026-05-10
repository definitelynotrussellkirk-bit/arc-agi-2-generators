"""Generator for arc_puzzle_bank_nineteenth_21_bundle:easy_133_recolor_source_to_target_from_corner_legend.

Rule: corner legend gives source and target colors for body recoloring.

Combinatorial axes (8): grid_h, grid_w, palette_kind, source_cells,
distractors, palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source_in_body, source_equals_target, missing_legend.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "13a5c3f25c60"
VERSION = "1.1.0"
TASK_ID = "13a5c3f25c60"
SUMMARY = "Corner legend gives source and target colors for body recoloring."

INVARIANTS = [
    "background is 0",
    "top-left cell is the source color",
    "top-right cell is a different target color",
    "at least one body cell uses the source color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source_in_body", "source_equals_target", "missing_legend")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "source_cells":   {"type": "int", "default": "rng 3..6", "valid": "1..20"},
    "distractors":    {"type": "int", "default": "rng 2..5", "valid": "0..20"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "corners_legend_with_body",
                       "valid": "corners_legend_with_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        source_target = ctx.draw_int("source_cells", 2, 3)
        distractor_target = ctx.draw_int("distractors", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        source_target = ctx.draw_int("source_cells", 5, 6)
        distractor_target = ctx.draw_int("distractors", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        source_target = ctx.draw_int("source_cells", 3, 6)
        distractor_target = ctx.draw_int("distractors", 2, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    source, target = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    g[0][0] = source
    g[0][w - 1] = target
    body = [(r, c) for r in range(1, h) for c in range(w)]
    rng.shuffle(body)
    for r, c in body[:source_target]:
        g[r][c] = source
    distractor_colors = [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in (source, target)]
    for r, c in body[source_target:source_target + distractor_target]:
        g[r][c] = rng.choice(distractor_colors)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_source_in_body":
        # legend present but body has no source-color cells → rule has nothing to recolor
        g[0][0] = 4         # source
        g[0][w - 1] = 6     # target
        # body uses only OTHER colors (no 4s)
        g[3][2] = 8; g[4][5] = 3; g[5][7] = 9
        return g
    if name == "source_equals_target":
        # source == target → recolor is identity (but rule still "fires", just invisible)
        g[0][0] = 4         # source
        g[0][w - 1] = 4     # target (same)
        g[3][2] = 4; g[5][6] = 4
        return g
    if name == "missing_legend":
        # no top-left or top-right marker → ambiguous which color is source/target
        g[3][2] = 4; g[4][5] = 4; g[5][7] = 6
        return g
    return g
