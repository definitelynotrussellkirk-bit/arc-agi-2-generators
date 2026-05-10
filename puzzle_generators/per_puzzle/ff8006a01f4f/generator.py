"""Generator for arc_puzzle_bank_21_set8_s:S8_E7.

Rule: each row's leading nonzero prefix is repeated to fill the row width.

Combinatorial axes (8): grid_h/w, palette_kind, prefix_len,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: prefix_full_width, all_zero_grid, single_color_prefixes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ff8006a01f4f"
VERSION = "1.1.0"
TASK_ID = "ff8006a01f4f"
SUMMARY = "Each row's initial nonzero seed prefix is repeated across the whole row."

INVARIANTS = [
    "background is 0",
    "each active row starts with a contiguous nonzero prefix",
    "the rest of each active row begins blank",
    "outputs repeat the prefix pattern to the row width",
]

PALETTE_KINDS = ("varied_lengths", "stepped_lengths", "monocolor_prefixes", "rainbow")
DEGENERATE_TEXTURES = ("prefix_full_width", "all_zero_grid", "single_color_prefixes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "prefix_len":     {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "position_bias":  {"type": "str", "default": "leftmost", "valid": "leftmost"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 12)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = [2, 3, 4, 6, 7, 9]
    for r in range(h):
        length = rng.randint(2, min(4, w - 2))
        for c in range(length):
            g[r][c] = palette[(r + c) % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    palette = [2, 3, 4, 6, 7, 9]
    if name == "prefix_full_width":
        for r in range(h):
            for c in range(w):
                g[r][c] = palette[(r + c) % len(palette)]
        return g
    if name == "all_zero_grid":
        return g
    if name == "single_color_prefixes":
        for r in range(h):
            for c in range(2):
                g[r][c] = 3
        return g
    return g
