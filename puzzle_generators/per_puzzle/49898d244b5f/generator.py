"""Generator for arc_puzzle_bank_sixteenth21:E112.

Rule: columns with exactly one nonzero seed are filled top-to-bottom in
that seed color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, columns,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, all_columns_have_multiple, columns_already_full.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "49898d244b5f"
VERSION = "1.1.0"
TASK_ID = "49898d244b5f"
SUMMARY = "Columns with one seed are filled top-to-bottom in that seed color."

INVARIANTS = [
    "background is 0",
    "active columns have exactly one nonzero seed",
    "columns with multiple nonzero cells are optional distractors",
    "output is drawn on a blank grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "all_columns_have_multiple", "columns_already_full")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "3..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "columns":        {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "single_seed_columns",
                       "valid": "single_seed_columns"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = min(ctx.draw_int("columns", 2, 3), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = min(ctx.draw_int("columns", 4, 5), w)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = min(ctx.draw_int("columns", 3, 5), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), target)
    for c in cols:
        r = rng.randrange(h)
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    distractors = [c for c in range(w) if c not in cols]
    rng.shuffle(distractors)
    for c in distractors[:rng.randint(0, min(2, len(distractors)))]:
        r0, r1 = rng.sample(range(h), 2)
        g[r0][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[r1][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank grid → no columns to fill, output is blank
        return g
    if name == "all_columns_have_multiple":
        # every active column has ≥2 nonzeros → predicate "exactly one seed" fails everywhere
        for c in [1, 3, 5, 7]:
            r0, r1 = rng_pick_two(c, h)
            g[r0][c] = (c % 8) + 1
            g[r1][c] = ((c + 3) % 8) + 1
        return g
    if name == "columns_already_full":
        # active columns are already filled top-to-bottom → rule is identity
        for c in [2, 5]:
            color = (c % 8) + 1
            for r in range(h):
                g[r][c] = color
        return g
    return g


def rng_pick_two(c, h):
    # deterministic pseudo-pair without rng (degenerate is rng-free): c-anchored
    a = c % h
    b = (c + 3) % h
    if a == b: b = (b + 1) % h
    return a, b
