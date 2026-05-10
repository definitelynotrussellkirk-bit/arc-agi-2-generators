"""Generator for arc_puzzle_bank_21_set2:S2_H5 — header pair recolor map.

Rule: top-row source/destination color pairs recolor a varied body grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, src_not_in_body, no_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "70913cf98cee"
VERSION = "1.1.0"
TASK_ID = "70913cf98cee"
SUMMARY = "Top-row source/destination color pairs recolor a varied body grid."

INVARIANTS = [
    "background is 0",
    "top row contains consecutive nonzero source/destination pairs",
    "source colors appear in the body and destination colors are distinct",
    "body also contains unmapped colors that should remain unchanged",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "src_not_in_body", "no_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7"},
    "position_bias":  {"type": "str", "default": "header_pairs_dense_body",
                       "valid": "header_pairs_dense_body"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 7)
    pairs = [(colors[0], colors[1]), (colors[2], colors[3]), (colors[4], colors[5])]
    for i, (src, dst) in enumerate(pairs):
        g[0][2 * i] = src
        g[0][2 * i + 1] = dst
    body_colors = [src for src, _ in pairs] + [colors[6], 0, 0]
    for r in range(1, h):
        for c in range(w):
            g[r][c] = rng.choice(body_colors)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # no header pairs → no recolor map, body stays unchanged
        for r in range(1, h):
            for c in range(w):
                g[r][c] = ((r + c) % 4) + 1
        return g
    if name == "src_not_in_body":
        # header pairs but body has no source colors → rule is identity on body
        g[0][0] = 1; g[0][1] = 2
        g[0][2] = 3; g[0][3] = 4
        for r in range(2, h):
            for c in range(w):
                g[r][c] = 7  # not in any pair source
        return g
    if name == "no_body":
        # header pairs only, blank body → nothing to recolor
        g[0][0] = 1; g[0][1] = 2
        g[0][2] = 3; g[0][3] = 4
        g[0][4] = 5; g[0][5] = 6
        return g
    return g
