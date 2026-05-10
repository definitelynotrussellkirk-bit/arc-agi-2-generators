"""Generator for arc_puzzle_bank_21_set2:S2_H2 — marker count chooses nth largest.

Rule: count the blue 1-markers in the top row; that count selects the
nth largest green object by descending size rank.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rank,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, tied_sizes, more_markers_than_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c7070676c606"
VERSION = "1.1.0"
TASK_ID = "c7070676c606"
SUMMARY = "Blue top-row markers select one green object by descending size rank."

INVARIANTS = [
    "background is 0",
    "the top row contains only blue count markers",
    "there are four separated green objects below the top row",
    "green object sizes are distinct, so the requested rank is unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "tied_sizes", "more_markers_than_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rank":           {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "top_marker_body_bars",
                       "valid": "top_marker_body_bars"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 14, 15)
        rank = rng.randint(1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 16, 17)
        rank = rng.randint(3, 4)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 14, 17)
        rank = rng.randint(1, 4)
    g = full_grid(h, w, 0)
    for c in range(rank):
        g[0][c] = 1

    bars = [(2, 1, 7), (4, 2, 5), (6, 3, 4), (8, 4, 2)]
    rng.shuffle(bars)
    for r, c0, size in bars:
        if r >= h or c0 + size > w:
            raise ValueError("bar layout does not fit")
        for c in range(c0, c0 + size):
            g[r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 16
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # no blue markers in top row → rank undefined
        bars = [(2, 1, 7), (4, 2, 5), (6, 3, 4), (8, 4, 2)]
        for r, c0, size in bars:
            for c in range(c0, c0 + size): g[r][c] = 3
        return g
    if name == "tied_sizes":
        # green bars share sizes → rank is ambiguous
        for c in range(2): g[0][c] = 1
        for r, c0, size in [(2, 1, 4), (4, 2, 4), (6, 3, 2), (8, 4, 2)]:
            for c in range(c0, c0 + size): g[r][c] = 3
        return g
    if name == "more_markers_than_objects":
        # 5 markers but only 4 green objects → rank exceeds available rank
        for c in range(5): g[0][c] = 1
        bars = [(2, 1, 7), (4, 2, 5), (6, 3, 4), (8, 4, 2)]
        for r, c0, size in bars:
            for c in range(c0, c0 + size): g[r][c] = 3
        return g
    return g
