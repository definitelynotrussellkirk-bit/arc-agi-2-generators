"""Generator for arc_additional_puzzle_bank_volume9:E59.

Rule: exact length-5 orange bars have their center cell recolored cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_bars, only_distractor, nonstraight_bar.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "150230bcddaf"
VERSION = "1.1.0"
TASK_ID = "150230bcddaf"
SUMMARY = "Exact length-5 orange bars have their center cell recolored cyan."

INVARIANTS = [
    "background is 0",
    "target orange components are straight bars of exactly length 5",
    "orange bars are separated so their component size remains exact",
    "optional distractor orange bars are not length 5",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bars", "only_distractor", "nonstraight_bar")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "6..24"},
    "n_bars":         {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "scattered_length5_bars",
                       "valid": "scattered_length5_bars"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _can_paint(g, cells):
    h = len(g)
    w = len(g[0])
    for r, c in cells:
        if not (0 <= r < h and 0 <= c < w) or g[r][c] != 0:
            return False
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] == 7:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_bars = ctx.draw_int("n_bars", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 22)
        w = ctx.draw_int("grid_w", 14, 22)
        n_bars = ctx.draw_int("n_bars", 4, 7)
    else:
        h = ctx.draw_int("grid_h", 9, 14)
        w = ctx.draw_int("grid_w", 9, 14)
        n_bars = ctx.draw_int("n_bars", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(400):
        if placed >= n_bars:
            break
        horizontal = rng.choice([True, False])
        if horizontal:
            r = rng.randint(1, h - 2)
            c = rng.randint(0, w - 5)
            cells = [(r, c + i) for i in range(5)]
        else:
            r = rng.randint(0, h - 5)
            c = rng.randint(1, w - 2)
            cells = [(r + i, c) for i in range(5)]
        if _can_paint(g, cells):
            for rr, cc in cells:
                g[rr][cc] = 7
            placed += 1
    if placed == 0:
        for c in range(1, 6):
            g[2][c] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_bars":
        # Empty grid — rule has no length-5 bars to mark.
        return g
    if name == "only_distractor":
        # Only length-3 / length-4 / length-7 orange bars (none
        # exactly 5) — rule's filter excludes; output equals input.
        for c in range(2, 5): g[2][c] = 7
        for c in range(2, 6): g[5][c] = 7
        for c in range(2, 9): g[8][c] = 7
        return g
    if name == "nonstraight_bar":
        # 5-cell L-shape orange object (not a straight bar) —
        # rule's "straight bar" filter excludes; rule's effect is
        # invisible despite cell count == 5.
        for c in range(2, 5): g[3][c] = 7
        g[4][4] = 7; g[5][4] = 7
        return g
    return g
