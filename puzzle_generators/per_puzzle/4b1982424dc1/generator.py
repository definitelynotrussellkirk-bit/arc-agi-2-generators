"""Generator for additional_bank:E5 — extend horizontal length-3 8-bars.

Rule: each exact horizontal length-3 bar of color 8 is extended one cell
at each open end.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_bars,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_bars, all_distractors, bars_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4b1982424dc1"
VERSION = "1.1.0"
TASK_ID = "4b1982424dc1"
SUMMARY = "Exact horizontal length-3 bars of color 8 are extended one cell at each open end."

INVARIANTS = [
    "background is 0",
    "target objects are exact horizontal length-3 bars of color 8",
    "bar endpoints have open background cells when in-bounds",
    "optional distractors are not horizontal length-3 bars",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bars", "all_distractors", "bars_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_bars":         {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "horiz_3bars_with_room_at_ends",
                       "valid": "horiz_3bars_with_room_at_ends"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n_bars = ctx.draw_int("n_bars", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        n_bars = ctx.draw_int("n_bars", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        n_bars = ctx.draw_int("n_bars", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    used_rows: set[int] = set()
    for _ in range(n_bars):
        rows = [r for r in range(h) if r not in used_rows]
        if not rows:
            break
        r = rows[rng.randint(0, len(rows) - 1)]
        c = rng.randint(1, w - 4)
        for dc in range(3):
            g[r][c + dc] = 8
        used_rows.add(r)
    if h >= 3:
        g[0][0] = g[1][0] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_bars":
        # no length-3 bars → rule has nothing to extend
        g[2][1] = 8; g[2][2] = 8   # length-2
        g[4][5] = 8                  # singleton
        return g
    if name == "all_distractors":
        # only distractors (vertical bars, 4-bars, scattered 8s) → no length-3 horiz bars
        g[1][1] = 8; g[2][1] = 8; g[3][1] = 8   # vertical
        g[5][3] = 8; g[5][4] = 8; g[5][5] = 8; g[5][6] = 8   # length-4
        g[2][8] = 8                              # singleton
        return g
    if name == "bars_at_edge":
        # length-3 bars touching grid edge → extension would clip out of bounds
        g[1][0] = 8; g[1][1] = 8; g[1][2] = 8   # left edge
        g[4][w - 3] = 8; g[4][w - 2] = 8; g[4][w - 1] = 8   # right edge
        return g
    return g
