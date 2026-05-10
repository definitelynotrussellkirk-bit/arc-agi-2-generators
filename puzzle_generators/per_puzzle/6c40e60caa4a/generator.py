"""Generator for additional_scaffolded:H6.

Rule: nested 1-frames share a red seed; only the deepest seeded frame
fills.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, single_frame, seed_outside_inner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "6c40e60caa4a"
VERSION = "1.1.0"
TASK_ID = "6c40e60caa4a"
SUMMARY = "Nested 1-frames share a red seed; only the deepest seeded frame fills."

INVARIANTS = [
    "background is 0",
    "all frames are exact 1-colored rectangular outlines",
    "a red seed lies inside both the outer and inner frame",
    "the inner frame is strictly nested and therefore deepest",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "single_frame", "seed_outside_inner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 15..21", "valid": "13..24"},
    "grid_w":         {"type": "int", "default": "rng 15..21", "valid": "13..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "nested", "valid": "nested"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 15, 17)
        w = ctx.draw_int("grid_w", 15, 17)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 19, 21)
        w = ctx.draw_int("grid_w", 19, 21)
    else:
        h = ctx.draw_int("grid_h", 15, 21)
        w = ctx.draw_int("grid_w", 15, 21)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    draw_frame(g, 1, 1, h - 2, w - 2, 1)

    r1 = rng.randint(4, 5)
    c1 = rng.randint(4, 5)
    r2 = h - 1 - rng.randint(4, 5)
    c2 = w - 1 - rng.randint(4, 5)
    if r2 - r1 < 4 or c2 - c1 < 4:
        raise ValueError("inner frame too small")
    draw_frame(g, r1, c1, r2, c2, 1)
    g[rng.randint(r1 + 2, r2 - 2)][rng.randint(c1 + 2, c2 - 2)] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # no red seed inside any frame → "deepest seeded" predicate has no qualifier
        draw_frame(g, 1, 1, h - 2, w - 2, 1)
        draw_frame(g, 5, 5, h - 6, w - 6, 1)
        return g
    if name == "single_frame":
        # only outer frame, no nesting → "deepest" trivially equals the only frame
        draw_frame(g, 1, 1, h - 2, w - 2, 1)
        g[h // 2][w // 2] = 2
        return g
    if name == "seed_outside_inner":
        # seed lies between outer and inner frame → only outer qualifies, inner is empty
        draw_frame(g, 1, 1, h - 2, w - 2, 1)
        draw_frame(g, 5, 5, h - 6, w - 6, 1)
        g[2][2] = 2  # outside inner frame
        return g
    return g
