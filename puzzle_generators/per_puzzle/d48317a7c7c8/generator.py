"""Generator for arc_additional_puzzle_bank_volume8:E53.

Rule: each length-3 yellow bar gets cyan caps just beyond both ends.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_bars, only_distractor, nonstraight_bar.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d48317a7c7c8"
VERSION = "1.1.0"
TASK_ID = "d48317a7c7c8"
SUMMARY = "Exact length-3 yellow bars get cyan caps just beyond both ends."

INVARIANTS = [
    "background is 0",
    "target yellow components are straight bars of exactly length 3",
    "bar cap cells are in bounds and empty",
    "same-color bars are separated so they stay distinct components",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bars", "only_distractor", "nonstraight_bar")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "n_bars":         {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "scattered_length3_bars",
                       "valid": "scattered_length3_bars"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_neighborhood(g, cells):
    h = len(g)
    w = len(g[0])
    for r, c in cells:
        if not (0 <= r < h and 0 <= c < w) or g[r][c] != 0:
            return False
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] == 4:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_bars = ctx.draw_int("n_bars", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 22)
        w = ctx.draw_int("grid_w", 13, 22)
        n_bars = ctx.draw_int("n_bars", 4, 7)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_bars = ctx.draw_int("n_bars", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(300):
        if placed >= n_bars:
            break
        horizontal = rng.choice([True, False])
        if horizontal:
            r = rng.randint(1, h - 2)
            c = rng.randint(1, w - 4)
            bar = [(r, c + i) for i in range(3)]
            caps = [(r, c - 1), (r, c + 3)]
        else:
            r = rng.randint(1, h - 4)
            c = rng.randint(1, w - 2)
            bar = [(r + i, c) for i in range(3)]
            caps = [(r - 1, c), (r + 3, c)]
        if _clear_neighborhood(g, bar + caps):
            for rr, cc in bar:
                g[rr][cc] = 4
            placed += 1
    if placed == 0:
        g[2][2] = 4
        g[2][3] = 4
        g[2][4] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_bars":
        # Empty grid — rule has no length-3 yellow bars to cap.
        return g
    if name == "only_distractor":
        # Only length-2 / length-4 / length-5 yellow bars (none
        # exactly 3) — rule's filter excludes; output equals input.
        for c in range(2, 4): g[2][c] = 4
        for c in range(2, 6): g[5][c] = 4
        for c in range(2, 7): g[8][c] = 4
        return g
    if name == "nonstraight_bar":
        # Yellow L-shape with 3 cells (not a straight bar) —
        # rule's "straight bar" filter excludes; rule's caps
        # never appear despite cell count == 3.
        for c in range(2, 4): g[3][c] = 4
        g[4][3] = 4
        return g
    return g
