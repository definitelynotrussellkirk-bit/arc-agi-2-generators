"""Generator for arc_puzzle_bank_21_set17_bundle:easy_p05.

Matching horizontal or vertical endpoints with a one-cell zero gap are bridged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, gap_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_gaps, gap_already_filled, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4a6d26e0b6ae"
VERSION = "1.1.0"
TASK_ID = "4a6d26e0b6ae"
SUMMARY = "Separated one-cell orthogonal gaps between matching colors."

INVARIANTS = [
    "background is 0",
    "each motif is color-zero-same-color horizontally or vertically",
    "motifs are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_gaps", "gap_already_filled", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "gap_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_orthogonal_gaps",
                       "valid": "spaced_orthogonal_gaps"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        gap_count = ctx.draw_int("gap_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        gap_count = ctx.draw_int("gap_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        gap_count = ctx.draw_int("gap_count", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=gap_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for color in colors:
        for _ in range(300):
            horizontal = rng.choice([True, False])
            if horizontal:
                r = rng.randrange(h)
                c = rng.randint(0, w - 3)
                cells = [(r, c), (r, c + 1), (r, c + 2)]
                band = [(r, cc) for cc in range(max(0, c - 1), min(w, c + 4))]
            else:
                r = rng.randint(0, h - 3)
                c = rng.randrange(w)
                cells = [(r, c), (r + 1, c), (r + 2, c)]
                band = [(rr, c) for rr in range(max(0, r - 1), min(h, r + 4))]
            if all(g[rr][cc] == 0 for rr, cc in band):
                g[cells[0][0]][cells[0][1]] = color
                g[cells[2][0]][cells[2][1]] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_gaps":
        # blank → no endpoints to bridge, rule has no effect
        return g
    if name == "gap_already_filled":
        # the middle cell is non-zero already → bridging is a no-op
        g[2][2] = 4; g[2][3] = 4; g[2][4] = 4
        g[5][6] = 6; g[5][7] = 6; g[5][8] = 6
        return g
    if name == "mismatched_endpoints":
        # endpoints differ in color → rule's "same-color" predicate fails
        g[2][2] = 4; g[2][4] = 6
        g[5][6] = 3; g[5][8] = 8
        return g
    return g
