"""Generator for arc_puzzle_bank_21_set8_s:S8_E4.

Rule: each row's first-cell header rotates that row's body to the right
by k mod width.

Combinatorial axes (8): grid_h, grid_w, palette_kind, body_length,
palette_size, position_bias, n_distinct_colors, shift_distribution, texture.
Degenerates: zero_shift, no_body, header_in_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "703a842c8e24"
VERSION = "1.1.0"
TASK_ID = "703a842c8e24"
SUMMARY = "Each row's first-cell header rotates that row's body to the right by k mod width."

INVARIANTS = [
    "background is 0",
    "each row begins with a nonzero shift key",
    "row bodies contain a short nonzero pattern followed by zeros",
    "at least one row has a nonzero effective shift",
]

PALETTE_KINDS = ("default", "small_shift", "wraparound_shift", "mixed_shift")
DEGENERATE_TEXTURES = ("zero_shift", "no_body", "header_in_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "body_length":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "rows", "valid": "rows"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..6", "valid": "1..9"},
    "shift_distribution": {"type": "str", "default": "uniform", "valid": "uniform"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 4, 7)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    body_w = w - 1
    palette = [2, 3, 4, 6, 7, 9]
    for r in range(h):
        k = rng.randint(1, min(4, body_w - 1))
        g[r][0] = k
        length = rng.randint(2, min(4, body_w))
        for i in range(length):
            g[r][1 + i] = palette[(r + i) % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 9
    g = full_grid(h, w, 0)
    palette = [2, 3, 4, 6, 7, 9]
    if name == "zero_shift":
        # k = 0 in headers (or k mod width == 0) → rule is identity
        for r in range(h):
            g[r][0] = w - 1
            for i in range(2):
                g[r][1 + i] = palette[(r + i) % len(palette)]
        return g
    if name == "no_body":
        # only headers, no body cells → there is nothing to shift
        for r in range(h):
            g[r][0] = 2
        return g
    if name == "header_in_body":
        # headers exist but body's first cell shares the same column as the header → ambiguity
        for r in range(h):
            g[r][0] = 3
            g[r][0] = palette[r % len(palette)]
            for i in range(2):
                g[r][1 + i] = palette[(r + i) % len(palette)]
        return g
    return g
