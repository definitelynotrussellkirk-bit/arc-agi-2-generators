"""Generator for arc_puzzle_bank_seventeenth_21_bundle:easy_116_fill_diagonal_segments.

Rule: each color appearing twice as endpoints of a 45-degree diagonal
fills the diagonal between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, segments, texture.
Degenerates: no_pairs, axis_aligned, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0db6c0c84cfa"
VERSION = "1.1.0"
TASK_ID = "0db6c0c84cfa"

SUMMARY = "Color pairs mark endpoints of separated diagonal segments."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "endpoints lie on a 45-degree diagonal",
    "intervening diagonal cells are initially blank",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "axis_aligned", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "segments":       {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= segments", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_diagonals",
                       "valid": "scattered_diagonals"},
    "n_distinct_colors": {"type": "int", "default": "= segments", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("segments", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 11, 15)
        target = ctx.draw_int("segments", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("segments", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    placed = 0
    for _ in range(400):
        if placed >= target:
            break
        span = rng.randint(2, min(4, h - 1, w - 1))
        down_right = rng.randrange(2) == 0
        r = rng.randint(0, h - span - 1)
        c = rng.randint(0, w - span - 1)
        if down_right:
            pts = [(r + d, c + d) for d in range(span + 1)]
        else:
            c = c + span
            pts = [(r + d, c - d) for d in range(span + 1)]
        cells = set(pts)
        guard = {
            (rr, cc)
            for cr, cc0 in cells
            for rr in range(max(0, cr - 1), min(h, cr + 2))
            for cc in range(max(0, cc0 - 1), min(w, cc0 + 2))
        }
        if guard & reserved:
            continue
        color = colors[placed % len(colors)]
        g[pts[0][0]][pts[0][1]] = color
        g[pts[-1][0]][pts[-1][1]] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no diagonal pairs to fill.
        return g
    if name == "axis_aligned":
        # Same color twice on row or column rather than a diagonal —
        # rule's 45-degree filter excludes them.
        g[3][2] = 4; g[3][7] = 4
        g[2][6] = 6; g[6][6] = 6
        return g
    if name == "single_endpoint":
        # Color appears once — rule's "exactly two endpoints"
        # filter excludes it.
        g[2][2] = 4
        return g
    return g
