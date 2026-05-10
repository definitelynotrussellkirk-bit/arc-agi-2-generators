"""Generator for arc_puzzle_bank_21_set18_s:S18_E7.

Rule: pick the row whose endpoints have the longest min-to-max span; emit
only that span in the output.

Combinatorial axes (8): grid_h/w, palette_kind, num_active_rows,
palette_size, position_bias, n_distinct_colors, span_spread, texture.
Degenerates: only_one_row, all_same_span, no_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b6edfc119780"
VERSION = "1.1.0"
TASK_ID = "b6edfc119780"
SUMMARY = "Choose the row with the longest endpoint span and fill that span."

INVARIANTS = [
    "three active rows contain endpoint pairs",
    "one row has a unique longest min-to-max span",
    "only that longest span appears in the output",
]

PALETTE_KINDS = ("default", "wide_spread", "tight_spread", "varied_colors")
DEGENERATE_TEXTURES = ("only_one_row", "all_same_span", "no_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "width":          {"type": "int", "default": "rng 9..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_active_rows": {"type": "int", "default": "3", "valid": "3"},
    "span_spread":    {"type": "str", "default": "wide", "valid": "wide"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 6, 7)
        w = ctx.draw_int("width", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 7, 8)
        w = ctx.draw_int("width", 10, 11)
    else:
        h = ctx.draw_int("height", 6, 8)
        w = ctx.draw_int("width", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), 3)
    spans = [(0, w - 1), (1, w - 3), (2, w - 3)]
    rng.shuffle(spans[1:])
    for idx, (r, (c1, c2)) in enumerate(zip(rows, spans)):
        g[r][c1] = 2 + idx
        g[r][c2] = 2 + idx
        if c2 - c1 > 3 and rng.random() < 0.5:
            g[r][rng.randint(c1 + 1, c2 - 1)] = 2 + idx
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "only_one_row":
        # only 1 active row — trivial pick
        g[3][1] = 4
        g[3][8] = 4
        return g
    if name == "all_same_span":
        # all 3 rows same span — no unique longest
        for idx, r in enumerate([1, 3, 5]):
            g[r][1] = 2 + idx
            g[r][6] = 2 + idx
        return g
    if name == "no_endpoints":
        return g
    return g
