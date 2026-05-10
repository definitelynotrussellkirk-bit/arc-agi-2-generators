"""Generator for v3_rich_schema:easy_01_exact_horizontal_triples — recolor exact-3 horizontal runs.

Rule: each horizontal run of color-2 of EXACTLY length 3 is recolored to 7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_triples,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_triples, all_distractors, vertical_triples.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8a57e8877de1"
VERSION = "1.1.0"
TASK_ID = "8a57e8877de1"

SUMMARY = "Horizontal color-2 runs of exact length 3 + 0-1 distractor runs of other lengths."

INVARIANTS = [
    "background is 0",
    "1-3 horizontal color-2 runs of EXACT length 3 in distinct rows",
    "0-1 distractor horizontal color-2 runs of length 2 or 4 (won't match the rule)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_triples", "all_distractors", "vertical_triples")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_triples":      {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "horizontal_triples_with_distractors",
                       "valid": "horizontal_triples_with_distractors"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
        n_triples = ctx.draw_int("n_triples", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        n_triples = ctx.draw_int("n_triples", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 10)
        n_triples = ctx.draw_int("n_triples", 1, min(3, h - 1))
    n_distract = ctx.draw_int("n_distract", 0, 1)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), n_triples + n_distract)
    triple_rows = rows[:n_triples]
    distract_rows = rows[n_triples:]
    for r in triple_rows:
        c0 = rng.randint(0, w - 3)
        for c in range(c0, c0 + 3):
            g[r][c] = 2
    for r in distract_rows:
        length = rng.choice([2, 4])
        if w - length < 0: continue
        c0 = rng.randint(0, w - length)
        for c in range(c0, c0 + length):
            g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_triples":
        # blank → no exact-3 runs to recolor
        return g
    if name == "all_distractors":
        # only length-2 and length-4 runs → "exact length 3" precondition fails
        for c in range(2, 4): g[1][c] = 2
        for c in range(2, 6): g[3][c] = 2
        return g
    if name == "vertical_triples":
        # vertical runs only → "horizontal" precondition fails
        for r in range(1, 4): g[r][3] = 2
        return g
    return g
