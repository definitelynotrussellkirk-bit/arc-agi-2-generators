"""Generator for arc_additional_puzzle_bank_volume6:M36.

Rule: top two rows define color substitutions that apply only to rows 2
and below.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_mapping_rows, mapping_self_loop, no_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4fb2a3c35698"
VERSION = "1.1.0"
TASK_ID = "4fb2a3c35698"
SUMMARY = "Top two rows define color substitutions that apply only to rows 2 and below."

INVARIANTS = [
    "mapping columns have nonzero source and destination colors",
    "body rows contain source colors to be replaced",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_mapping_rows", "mapping_self_loop", "no_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pairs":          {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "header_then_body",
                       "valid": "header_then_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "density":        {"type": "str", "default": "dense_body", "valid": "dense_body"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n = min(ctx.draw_int("pairs", 3, 3), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n = min(ctx.draw_int("pairs", 4, 5), w)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        n = min(ctx.draw_int("pairs", 3, 5), w)
    rng = ctx.draw_rng("layout")
    colors = list(ctx.draw_distinct_colors("colors", n=n + 1, exclude=[0]))
    g = full_grid(h, w, 0)
    for c in range(n):
        g[0][c] = colors[c]
        g[1][c] = colors[(c + 1) % len(colors)]
    for r in range(2, h):
        for c in range(w):
            if rng.random() < 0.65:
                g[r][c] = rng.choice(colors[:n])
    g[2][0] = colors[0]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_mapping_rows":
        # body content but no top-2-row mapping → rule has no substitutions defined
        for r in range(2, h):
            for c in range(w):
                if (r + c) % 2: g[r][c] = 4
        return g
    if name == "mapping_self_loop":
        # mapping has src == dst for every column → rule is identity on body
        for c in range(3):
            g[0][c] = 4 + c
            g[1][c] = 4 + c
        for r in range(2, h):
            for c in range(w):
                if (r + c) % 2: g[r][c] = 4 + (c % 3)
        return g
    if name == "no_body":
        # mapping rows present but body is empty → rule has nothing to substitute in
        for c in range(3):
            g[0][c] = 4 + c
            g[1][c] = 5 + c
        return g
    return g
