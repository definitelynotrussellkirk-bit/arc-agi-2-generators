"""Generator for arc_additional_puzzle_bank_volume17:E118.

Rule: straight blue bars are recolored by orientation — horizontal to
yellow, vertical to orange.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_bars, texture.
Degenerates: no_bars, single_cells, non_straight.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "81a2a6d68649"
VERSION = "1.1.0"
TASK_ID = "81a2a6d68649"
SUMMARY = "Straight blue bars are recolored by orientation."

INVARIANTS = [
    "background is 0",
    "every blue component is a straight 1-cell-thick bar",
    "horizontal samples recolor to yellow and vertical samples recolor to orange",
    "bars are separated so blue components do not merge",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bars", "single_cells", "non_straight")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_bars":         {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "axis_aligned_bars",
                       "valid": "axis_aligned_bars"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_bars = ctx.draw_int("n_bars", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 18)
        w = ctx.draw_int("grid_w", 13, 18)
        n_bars = ctx.draw_int("n_bars", 5, 8)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_bars = ctx.draw_int("n_bars", 2, 5)
    rng = ctx.draw_rng("placement")
    horizontal = rng.choice([False, True])
    g = full_grid(h, w, 0)
    used: set[int] = set()
    made = 0
    for _ in range(200):
        if made >= n_bars:
            break
        if horizontal:
            choices = [r for r in range(h) if all(abs(r - rr) > 1 for rr in used)]
            if not choices:
                break
            r = rng.choice(choices)
            length = rng.randint(2, min(6, w))
            c = rng.randint(0, w - length)
            for dc in range(length):
                g[r][c + dc] = 1
            used.add(r)
        else:
            choices = [c for c in range(w) if all(abs(c - cc) > 1 for cc in used)]
            if not choices:
                break
            c = rng.choice(choices)
            length = rng.randint(2, min(6, h))
            r = rng.randint(0, h - length)
            for dr in range(length):
                g[r + dr][c] = 1
            used.add(c)
        made += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_bars":
        # Empty grid — rule has no bars to recolor.
        return g
    if name == "single_cells":
        # Length-1 components — orientation is undefined, rule's
        # "horizontal vs vertical" recolor mapping has no entry.
        g[2][2] = 1; g[5][7] = 1
        return g
    if name == "non_straight":
        # Bent components — rule's "straight 1-cell-thick" precondition
        # fails; orientation cannot be assigned.
        for r, c in [(2, 2), (3, 2), (4, 2), (4, 3), (4, 4)]: g[r][c] = 1
        return g
    return g
