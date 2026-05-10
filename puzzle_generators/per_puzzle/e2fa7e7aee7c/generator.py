"""Generator for arc_puzzle_bank_sixteenth21:E108 — equal endpoints distance 2 fill midpoint.

Rule: each motif of (color, 0, color) at distance 2 in a row or
column has its midpoint filled with the color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, triples, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_triples, midpoint_filled, distance_one.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e2fa7e7aee7c"
VERSION = "1.1.0"
TASK_ID = "e2fa7e7aee7c"

SUMMARY = "Equal endpoints at distance two fill their empty midpoint."

INVARIANTS = [
    "background is 0",
    "each motif is color, zero, same color in a row or column",
    "motifs are separated so only intended midpoints fill",
    "both horizontal and vertical orientations can appear",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_triples", "midpoint_filled", "distance_one")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "triples":        {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "axis_aligned_distance_two",
                       "valid": "axis_aligned_distance_two"},
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
        target = ctx.draw_int("triples", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
        target = ctx.draw_int("triples", 5, 8)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("triples", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(500):
        if placed >= target:
            break
        vertical = rng.randrange(2) == 0
        if vertical:
            r = rng.randint(0, h - 3)
            c = rng.randrange(w)
            motif = [(r, c), (r + 1, c), (r + 2, c)]
        else:
            r = rng.randrange(h)
            c = rng.randint(0, w - 3)
            motif = [(r, c), (r, c + 1), (r, c + 2)]
        guard = {
            (rr, cc)
            for mr, mc in motif
            for rr in range(max(0, mr - 1), min(h, mr + 2))
            for cc in range(max(0, mc - 1), min(w, mc + 2))
        }
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[motif[0][0]][motif[0][1]] = color
        g[motif[2][0]][motif[2][1]] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_triples":
        # Singletons only — no aligned pair to bridge.
        g[1][1] = 3; g[3][6] = 4; g[6][2] = 5
        return g
    if name == "midpoint_filled":
        # Endpoints + midpoint already non-zero (with a different color)
        # — rule's color-0-color motif never matches.
        g[2][1] = 4; g[2][3] = 4; g[2][2] = 7
        g[5][2] = 5; g[5][4] = 5; g[5][3] = 6
        return g
    if name == "distance_one":
        # Endpoints adjacent (distance 1, no zero between) — there's
        # no empty midpoint cell for the rule to fill.
        g[2][1] = 4; g[2][2] = 4
        g[5][3] = 5; g[5][4] = 5
        return g
    return g
