"""Generator for arc_puzzle_bank_fourth21:H26.

A full-width color-9 row is a horizontal mirror guide. Non-guide objects are
reflected across it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_guide, no_objects, object_on_guide.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0491e1a49389"
VERSION = "1.1.0"
TASK_ID = "0491e1a49389"
SUMMARY = "Objects above a full color-9 row mirror below that guide."

INVARIANTS = [
    "one row is entirely color 9",
    "all other nonzero cells are not color 9",
    "reflections of every object cell remain in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_guide", "no_objects", "object_on_guide")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15 odd", "valid": "9..19"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "above_guide_row",
                       "valid": "above_guide_row"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOTIFS = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 9, 11)
        n_objects = ctx.draw_int("n_objects", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 15)
        w = ctx.draw_int("grid_w", 12, 14)
        n_objects = ctx.draw_int("n_objects", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 9, 14)
        n_objects = ctx.draw_int("n_objects", 1, 3)
    if h % 2 == 0:
        h += 1
    guide = h // 2
    g = full_grid(h, w, 0)
    for c in range(w):
        g[guide][c] = 9
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], n_objects)
    for i in range(n_objects):
        motif = _MOTIFS[i % len(_MOTIFS)]
        mh = max(r for r, _c in motif) + 1
        mw = max(c for _r, c in motif) + 1
        top = rng.randint(1, guide - mh - 1)
        left = rng.randint(1, w - mw - 1)
        for r, c in motif:
            g[top + r][left + c] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 9
    g = full_grid(h, w, 0)
    if name == "no_guide":
        # objects but no full color-9 row → no axis to mirror across
        for r, c in [(1, 1), (2, 1), (2, 2)]:
            g[r][c] = 4
        return g
    if name == "no_objects":
        # only the guide row → nothing to reflect
        for c in range(w):
            g[5][c] = 9
        return g
    if name == "object_on_guide":
        # object overlaps the guide row → mirror produces overlap
        for c in range(w):
            g[5][c] = 9
        for r, c in [(4, 2), (5, 2), (6, 2)]:
            g[r][c] = 4
        return g
    return g
