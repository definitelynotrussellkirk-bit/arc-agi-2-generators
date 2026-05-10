"""Generator for arc_puzzle_bank_21_set16_s:S16_E3.

Two aligned endpoints with an odd-length segment produce the midpoint.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, even_length_segment, non_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b35816e8388b"
VERSION = "1.1.0"
TASK_ID = "b35816e8388b"
SUMMARY = "Two aligned endpoints with an odd-length segment produce the midpoint."

INVARIANTS = [
    "exactly two aligned nonzero endpoint cells are present",
    "segment length is odd, so there is a single lattice midpoint",
    "output paints only that midpoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "even_length_segment", "non_aligned")
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


def _odd_pair(rng, h: int, w: int, orientation: str):
    max_step = min(4, h - 1, w - 1)
    step = 4 if max_step >= 4 and rng.random() < 0.5 else 2
    if orientation == "h":
        r = rng.randrange(h)
        c1 = rng.randint(0, w - step - 1)
        return (r, c1), (r, c1 + step)
    if orientation == "v":
        c = rng.randrange(w)
        r1 = rng.randint(0, h - step - 1)
        return (r1, c), (r1 + step, c)
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
    (r1, c1), (r2, c2) = _odd_pair(rng, h, w, orientation)
    g[r1][c1] = 4
    g[r2][c2] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # blank → no segment to find midpoint of
        return g
    if name == "even_length_segment":
        # segment length 3 (even cell-count between endpoints) → no single midpoint
        g[3][1] = 4; g[3][4] = 4  # 3-cell gap between (even step), no integer midpoint
        return g
    if name == "non_aligned":
        # endpoints not h/v/diagonal aligned → no segment
        g[1][1] = 4; g[5][6] = 4
        return g
    return g
