"""Generator for arc_additional_puzzle_bank_volume6:H39.

Rule: a bottom control strip composes transforms on a blue template,
then stamps the result at a maroon anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_ops,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_anchor, no_ops.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f2b7a9953d61"
VERSION = "1.1.0"
TASK_ID = "f2b7a9953d61"
SUMMARY = "A bottom control strip composes transforms on a blue template, then stamps the result at a maroon anchor."

INVARIANTS = [
    "there is one color-2 template above the control strip",
    "bottom-row controls are transform codes 1, 3, or 4",
    "one color-9 anchor marks the stamp position",
    "the output contains only the transformed green stamp",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_anchor", "no_ops")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_ops":          {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "template_top_anchor_right_ops_bottom",
                       "valid": "template_top_anchor_right_ops_bottom"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n_ops = ctx.draw_int("n_ops", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 17)
        n_ops = ctx.draw_int("n_ops", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 17)
        n_ops = ctx.draw_int("n_ops", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
        g[1 + dr][1 + dc] = 2
    g[h // 2][w - 5] = 9
    ops = [1, 3, 4]
    rng.shuffle(ops)
    for i in range(n_ops):
        g[h - 1][1 + 2 * i] = ops[i % len(ops)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_template":
        # ops + anchor present but no blue template → nothing to transform and stamp
        g[h // 2][w - 5] = 9
        g[h - 1][1] = 1
        g[h - 1][3] = 3
        return g
    if name == "no_anchor":
        # template + ops but no maroon anchor → no stamp position
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
            g[1 + dr][1 + dc] = 2
        g[h - 1][1] = 1; g[h - 1][3] = 4
        return g
    if name == "no_ops":
        # template + anchor but no transform codes → identity transform, no composition signal
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
            g[1 + dr][1 + dc] = 2
        g[h // 2][w - 5] = 9
        return g
    return g
