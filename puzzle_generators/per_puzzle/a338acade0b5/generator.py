"""Generator for arc_puzzle_bank_21_set16_s:S16_E7.

A pair's segment length becomes a one-row bar of 8s.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, single_endpoint, non_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a338acade0b5"
VERSION = "1.1.0"
TASK_ID = "a338acade0b5"
SUMMARY = "A pair's segment length becomes a one-row bar of 8s."

INVARIANTS = [
    "exactly two aligned nonzero endpoint cells are present",
    "the segment may be horizontal, vertical, or diagonal",
    "output is a 1-row bar whose length equals the segment length",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "single_endpoint", "non_aligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "choice", "default": "rng h|v|d",
                       "valid": "h|v|d"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "two_aligned_endpoints",
                       "valid": "two_aligned_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _pair(rng, h: int, w: int, orientation: str):
    if orientation == "h":
        r = rng.randrange(h)
        c1 = rng.randint(0, w - 5)
        c2 = rng.randint(c1 + 3, w - 1)
        return (r, c1), (r, c2)
    if orientation == "v":
        c = rng.randrange(w)
        r1 = rng.randint(0, h - 5)
        r2 = rng.randint(r1 + 3, h - 1)
        return (r1, c), (r2, c)
    step = rng.randint(3, min(h, w) - 1)
    r1 = rng.randint(0, h - step - 1)
    c1 = rng.randint(0, w - step - 1)
    dr = rng.choice([1, -1])
    if dr < 0:
        r1 += step
    return (r1, c1), (r1 + dr * step, c1 + step)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 7, 7)
        w = ctx.draw_int("width", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 8, 9)
        w = ctx.draw_int("width", 8, 9)
    else:
        h = ctx.draw_int("height", 7, 9)
        w = ctx.draw_int("width", 7, 9)
    orientation = ctx.draw_choice("orientation", ["h", "v", "d"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    (r1, c1), (r2, c2) = _pair(rng, h, w, orientation)
    g[r1][c1] = 6
    g[r2][c2] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # blank → no endpoints to define segment length
        return g
    if name == "single_endpoint":
        # 1 endpoint → can't measure segment length
        g[3][3] = 6
        return g
    if name == "non_aligned":
        # endpoints not aligned → no segment direction defined
        g[1][1] = 6; g[5][6] = 6
        return g
    return g
