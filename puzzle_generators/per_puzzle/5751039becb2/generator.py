"""Generator for arc_puzzle_bank_21_set6:easy_f05.

Keep only cells that have a same-color diagonal neighbor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, all_pairs, no_distractors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5751039becb2"
VERSION = "1.1.0"
TASK_ID = "5751039becb2"

SUMMARY = "Keep only cells that have a same-color diagonal neighbor."

INVARIANTS = [
    "background is 0",
    "some colors form diagonal pairs or chains",
    "singleton distractors have no same-color diagonal neighbor",
    "output erases the singleton distractors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "all_pairs", "no_distractors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 4..5", "valid": "3..7"},
    "position_bias":  {"type": "str", "default": "diagonal_pairs_plus_singletons",
                       "valid": "diagonal_pairs_plus_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..7"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("n_pairs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("n_pairs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(120):
        if placed >= target:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        dc = rng.choice([-1, 1])
        c2 = c + dc
        if c2 < 0 or c2 >= w:
            continue
        if g[r][c] == 0 and g[r + 1][c2] == 0:
            color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            g[r][c] = color
            g[r + 1][c2] = color
            placed += 1
    for color in rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2):
        for _ in range(40):
            r, c = rng.randrange(h), rng.randrange(w)
            if g[r][c] == 0:
                g[r][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # only singletons → rule erases everything
        g[1][2] = 4
        g[3][5] = 6
        g[5][7] = 7
        return g
    if name == "all_pairs":
        # all cells in pairs → rule keeps everything (no contrast)
        g[1][1] = 4; g[2][2] = 4
        g[3][5] = 6; g[4][6] = 6
        return g
    if name == "no_distractors":
        # pairs only, no singletons to erase → no signal for elimination
        g[1][1] = 4; g[2][2] = 4
        g[3][5] = 6; g[4][6] = 6
        return g
    return g
