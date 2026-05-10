"""Generator for arc_puzzle_bank_21_set4:S4_E2 — recolor lowest red object to green.

Rule: the red object whose bounding box reaches lowest is recolored
green; higher red objects remain red.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_object, tied_bottom.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "34e41cf35fde"
VERSION = "1.1.0"
TASK_ID = "34e41cf35fde"

SUMMARY = "The red object whose bounding box reaches lowest is recolored green."

INVARIANTS = [
    "background is 0",
    "all objects are red",
    "exactly one red object has the greatest bottom row",
    "all higher red objects remain red",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "tied_bottom")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "lowest_then_higher",
                       "valid": "lowest_then_higher"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]


def _paint(g, cells, r0, c0):
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = 2


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    low_shape = rng.choice(_SHAPES)
    low_h = max(r for r, _ in low_shape) + 1
    low_w = max(c for _, c in low_shape) + 1
    low_r = h - low_h - rng.randint(0, 1)
    low_c = rng.randint(1, w - low_w - 1)
    _paint(g, low_shape, low_r, low_c)
    for _ in range(2):
        cells = rng.choice(_SHAPES)
        max_r = max(r for r, _ in cells)
        for _attempt in range(300):
            r0 = rng.randint(1, max(1, low_r - max_r - 2))
            c0 = rng.randint(1, w - max(c for _, c in cells) - 2)
            placed = [(r0 + r, c0 + c) for r, c in cells]
            if any(g[r][c] != 0 for r, c in placed):
                continue
            if any(abs(r - rr) <= 1 and abs(c - cc) <= 1
                   for r, c in placed
                   for rr, row in enumerate(g) for cc, v in enumerate(row) if v == 2):
                continue
            _paint(g, cells, r0, c0)
            break
        else:
            raise ValueError("could not place higher red object")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # Empty grid — no red objects to compare.
        return g
    if name == "single_object":
        # Only one red object — "lowest" pick is trivial; no contrast
        # with higher objects.
        for r, c in [(7, 4), (7, 5), (8, 4), (8, 5)]: g[r][c] = 2
        return g
    if name == "tied_bottom":
        # Two red objects share the same lowest bottom row — rule's
        # strictly-lowest pick is ambiguous.
        for r, c in [(7, 1), (7, 2), (8, 1), (8, 2)]: g[r][c] = 2
        for r, c in [(7, 7), (7, 8), (8, 7), (8, 8)]: g[r][c] = 2
        return g
    return g
