"""Generator for arc_puzzle_bank_21_set13_bundle:hard_m03 — connect markers in order.

Rule: collect single-cell markers in colors {2, 3, 4, 5, 6, 7}; connect
color 2 through mids (sorted asc) to color 3 by BFS shortest path; paint
background cells along path with color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_mids,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, no_mids, collinear_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dbee38495261"
VERSION = "1.1.0"
TASK_ID = "dbee38495261"

SUMMARY = "Single-cell markers in colors 2, 3, plus 1-3 mid colors; connected by L-paths."

INVARIANTS = [
    "background is 0",
    "exactly one cell each of color 2 and color 3",
    "1-3 additional mid-color markers from {4, 5, 6, 7}",
    "markers are 4-conn isolated and have non-trivial separation",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "no_mids", "collinear_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_mids":         {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "ordered_color_chain",
                       "valid": "ordered_color_chain"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "3..6"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        n_mids = ctx.draw_int("n_mids", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 16)
        n_mids = ctx.draw_int("n_mids", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_mids = ctx.draw_int("n_mids", 1, 3)
    rng = ctx.draw_rng("layout")
    mids = rng.sample([4, 5, 6, 7], n_mids)
    colors = [2] + mids + [3]

    for outer in range(40):
        g = full_grid(h, w, 0)
        placed = []
        ok = True
        for color in colors:
            placed_a = False
            for _ in range(120):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                if any(abs(r - pr) + abs(c - pc) < 3 for pr, pc in placed): continue
                g[r][c] = color
                placed.append((r, c))
                placed_a = True; break
            if not placed_a: ok = False; break
        if ok:
            return g
    raise ValueError("could not realize hard_m03 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # Mid markers only, no color-2 or color-3 — rule has no chain
        # endpoints to start/end the BFS path.
        g[2][3] = 4; g[5][7] = 5; g[8][2] = 6
        return g
    if name == "no_mids":
        # Only color-2 and color-3 (no mids) — rule's chain reduces to
        # a single direct path with no intermediate ordering.
        g[2][3] = 2; g[7][9] = 3
        return g
    if name == "collinear_markers":
        # Markers on the same row — L-paths collapse to straight
        # segments, removing the L-corner evidence of the rule.
        g[4][2] = 2; g[4][6] = 5; g[4][10] = 3
        return g
    return g
