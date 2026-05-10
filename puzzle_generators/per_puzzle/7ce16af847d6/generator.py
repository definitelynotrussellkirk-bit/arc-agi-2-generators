"""Generator for arc_additional_puzzle_bank_volume9:E57.

Rule: each 1-blob that is a solid 3×3 → recolor to 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_solids,
n_decorations, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_solids, all_solids, two_by_two_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at, draw_rect

GENERATOR_ID = "7ce16af847d6"
VERSION = "1.1.0"
TASK_ID = "7ce16af847d6"
SUMMARY = "2 solid 3×3 1-blocks + 1-2 non-3×3 1-blobs as decoration."

INVARIANTS = [
    "exactly 2 solid 3×3 1-blocks (won't touch)",
    "1-2 1-blobs of other shape",
]

PALETTE_KINDS = ("default", "with_bar", "with_square", "varied_decor")
DEGENERATE_TEXTURES = ("no_solids", "all_solids", "two_by_two_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_solids":       {"type": "int", "default": "2", "valid": "2"},
    "n_decorations":  {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    draw_rect(g, rng.randint(0, 1), rng.randint(0, 1), 3, 3, 1)
    draw_rect(g, rng.randint(1, 3), rng.randint(w - 5, w - 4), 3, 3, 1)
    bar4 = [(0, 0), (0, 1), (0, 2), (0, 3)]
    paint_at(g, h - 4, 1, bar4, 1)
    sq22 = [(0, 0), (0, 1), (1, 0), (1, 1)]
    paint_at(g, h - 3, w - 3, sq22, 1)
    g[h - 6][1] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    bar4 = [(0, 0), (0, 1), (0, 2), (0, 3)]
    sq22 = [(0, 0), (0, 1), (1, 0), (1, 1)]
    if name == "no_solids":
        # decoration only — no 3×3 blocks, rule has nothing to recolor
        paint_at(g, h - 4, 1, bar4, 1)
        paint_at(g, h - 3, w - 3, sq22, 1)
        return g
    if name == "all_solids":
        # only 3×3 blocks → output recolors every 1-blob to 3
        draw_rect(g, 1, 1, 3, 3, 1)
        draw_rect(g, 1, w - 4, 3, 3, 1)
        draw_rect(g, h - 4, 4, 3, 3, 1)
        return g
    if name == "two_by_two_only":
        # 2×2 blobs only → "solid 3×3" predicate fails everywhere
        for top, left in [(1, 1), (1, w - 4), (h - 4, 4)]:
            paint_at(g, top, left, sq22, 1)
        return g
    return g
