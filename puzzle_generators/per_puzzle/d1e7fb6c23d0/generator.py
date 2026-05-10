"""Generator for arc_puzzle_bank_sixteenth21:E111.

Rule: each horizontal length-2 domino extends one cell to the right
in the same color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, dominoes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dominoes, dominoes_at_right_edge, longer_runs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d1e7fb6c23d0"
VERSION = "1.1.0"
TASK_ID = "d1e7fb6c23d0"
SUMMARY = "Exact horizontal dominoes extend one cell to the right."

INVARIANTS = [
    "background is 0",
    "each active row contains an exact length-two horizontal run",
    "the cell immediately right of each domino is empty",
    "longer same-color runs are not generated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dominoes", "dominoes_at_right_edge", "longer_runs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "dominoes":       {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "free_left_room_right",
                       "valid": "free_left_room_right"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 7, 9)
        target = min(ctx.draw_int("dominoes", 2, 2), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        target = min(ctx.draw_int("dominoes", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 11)
        target = min(ctx.draw_int("dominoes", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), target)
    for r in rows:
        c = rng.randint(0, w - 3)
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[r][c] = color
        g[r][c + 1] = color
        if c >= 2 and rng.randrange(3) == 0:
            g[r][rng.randrange(0, c)] = rng.choice([x for x in range(1, 10) if x != color])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_dominoes":
        # only singletons, no length-2 runs → rule has no targets
        g[1][2] = 3
        g[3][5] = 4
        g[5][1] = 6
        return g
    if name == "dominoes_at_right_edge":
        # domino flush against right edge → no room for one-cell extension
        g[1][w - 2] = 3; g[1][w - 1] = 3
        g[4][w - 2] = 5; g[4][w - 1] = 5
        return g
    if name == "longer_runs":
        # length-3 run instead of dominoes → invariant violated, rule input ambiguous
        g[2][1] = 4; g[2][2] = 4; g[2][3] = 4
        g[5][2] = 6; g[5][3] = 6; g[5][4] = 6
        return g
    return g
