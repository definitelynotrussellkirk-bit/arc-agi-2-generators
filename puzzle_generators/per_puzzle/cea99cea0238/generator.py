"""Generator for arc_puzzle_bank_sixteenth_21_bundle:easy_106_fill_row_or_column_spans.

Rule: each color appearing exactly twice as endpoints sharing a row or
column has the span between them filled with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, spans, texture.
Degenerates: no_pairs, adjacent_pair, no_shared_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cea99cea0238"
VERSION = "1.1.0"
TASK_ID = "cea99cea0238"

SUMMARY = "Each color appears as exactly two aligned endpoints of one span."

INVARIANTS = [
    "background is 0",
    "every active color appears exactly twice",
    "the two cells for each color share a row or a column",
    "spans are separated so endpoint groups stay unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "adjacent_pair", "no_shared_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "spans":          {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "= spans", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_axis_endpoints",
                       "valid": "scattered_axis_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "= spans", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("spans", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 16)
        target = ctx.draw_int("spans", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        target = ctx.draw_int("spans", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(colors)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for color in colors:
        if placed >= target:
            break
        for _ in range(100):
            vertical = rng.randrange(2) == 0
            if vertical:
                c = rng.randrange(w)
                r0 = rng.randint(0, h - 3)
                r1 = rng.randint(r0 + 2, h - 1)
                cells = {(r, c) for r in range(r0, r1 + 1)}
                endpoints = [(r0, c), (r1, c)]
            else:
                r = rng.randrange(h)
                c0 = rng.randint(0, w - 3)
                c1 = rng.randint(c0 + 2, w - 1)
                cells = {(r, c) for c in range(c0, c1 + 1)}
                endpoints = [(r, c0), (r, c1)]
            if cells & reserved:
                continue
            for r, c in endpoints:
                g[r][c] = color
            reserved.update(cells)
            placed += 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no spans to fill.
        return g
    if name == "adjacent_pair":
        # Same color appears twice but adjacent — rule's "fill between"
        # produces zero filler cells; output equals input.
        g[3][2] = 4; g[3][3] = 4
        return g
    if name == "no_shared_axis":
        # Same color twice but on different rows AND different cols —
        # rule's row-or-col axis precondition fails.
        g[2][3] = 4; g[5][7] = 4
        return g
    return g
