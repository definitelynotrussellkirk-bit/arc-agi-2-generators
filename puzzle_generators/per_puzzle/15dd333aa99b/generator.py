"""Generator for arc_additional_puzzle_bank_volume11:E72.

Rule: equal-colored endpoint pairs in a row or column are bridged into
full segments.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_pairs, texture.
Degenerates: no_pairs, adjacent_pair, no_shared_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "15dd333aa99b"
VERSION = "1.1.0"
TASK_ID = "15dd333aa99b"
SUMMARY = "Equal-colored endpoint pairs in a row or column are bridged into full segments."

INVARIANTS = [
    "background is 0",
    "each active nonzero color appears exactly twice",
    "paired markers are aligned horizontally or vertically with clear space between",
    "different colored segments are placed on separate rows or columns",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "adjacent_pair", "no_shared_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..4", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "= n_pairs", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "scattered_axis_pairs",
                       "valid": "scattered_axis_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= n_pairs", "valid": "1..7"},
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
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 18)
        w = ctx.draw_int("grid_w", 13, 18)
        n_pairs = ctx.draw_int("n_pairs", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_pairs = ctx.draw_int("n_pairs", 2, 4)
    rng = ctx.draw_rng("placement")
    colors = list(range(1, 10))
    rng.shuffle(colors)
    g = full_grid(h, w, 0)
    used_rows: set[int] = set()
    horizontal = rng.choice([False, True])
    made = 0
    for color in colors:
        if made >= n_pairs:
            break
        if horizontal and len(used_rows) < h:
            choices = [r for r in range(h) if r not in used_rows]
            r = rng.choice(choices)
            c1 = rng.randint(0, w - 4)
            c2 = rng.randint(c1 + 2, w - 1)
            g[r][c1] = color
            g[r][c2] = color
            used_rows.add(r)
            made += 1
        elif not horizontal and len(used_rows) < w:
            choices = [c for c in range(w) if c not in used_rows]
            c = rng.choice(choices)
            r1 = rng.randint(0, h - 4)
            r2 = rng.randint(r1 + 2, h - 1)
            g[r1][c] = color
            g[r2][c] = color
            used_rows.add(c)
            made += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — no pair to bridge.
        return g
    if name == "adjacent_pair":
        # Pair shares an axis but is adjacent — rule's bridge has no
        # interior cells.
        g[3][2] = 4; g[3][3] = 4
        return g
    if name == "no_shared_axis":
        # Pair has matching color but lies on different rows AND cols
        # — rule's "in-row OR in-col" precondition fails.
        g[2][3] = 4; g[7][8] = 4
        return g
    return g
