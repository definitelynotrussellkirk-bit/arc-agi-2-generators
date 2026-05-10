"""Generator for arc_additional_puzzle_bank_volume11:E74.

Isolated red seeds become green diagonal X shapes.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, only_distractors, seeds_on_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "98e38c175321"
VERSION = "1.1.0"
TASK_ID = "98e38c175321"
SUMMARY = "Isolated red seeds become green diagonal X shapes."

INVARIANTS = [
    "background is 0",
    "target red components are isolated singleton cells",
    "larger red components are optional distractors",
    "singleton seeds are separated so diagonal Xs remain readable",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "only_distractors", "seeds_on_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 2..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "isolated_red_singletons",
                       "valid": "isolated_red_singletons"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_seeds = ctx.draw_int("n_seeds", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_seeds = ctx.draw_int("n_seeds", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_seeds = ctx.draw_int("n_seeds", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    seeds: list[tuple[int, int]] = []
    for _ in range(200):
        if len(seeds) >= n_seeds:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in seeds):
            continue
        g[r][c] = 2
        seeds.append((r, c))
    if not seeds:
        g[2][2] = 2
    for r in range(1, h - 1):
        for c in range(1, w - 2):
            if g[r][c] == 0 and g[r][c + 1] == 0:
                if all(abs(r - rr) > 1 or abs(c - cc) > 2 for rr, cc in seeds):
                    g[r][c] = 2
                    g[r][c + 1] = 2
                    return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank → no singletons to expand into Xs
        return g
    if name == "only_distractors":
        # only multi-cell red components → no isolated singletons match
        for r, c in [(2, 2), (2, 3)]: g[r][c] = 2
        for r, c in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 2
        return g
    if name == "seeds_on_edge":
        # singleton at corner → diagonal X cells go out of bounds
        g[0][0] = 2
        g[0][8] = 2
        return g
    return g
