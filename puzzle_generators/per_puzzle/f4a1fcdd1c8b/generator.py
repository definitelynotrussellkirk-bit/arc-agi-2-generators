"""Generator for arc_puzzle_bank_21_set13_s:S13_E2.

Combinatorial axes (8): height, width, palette_kind, border_side,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_border_objects, no_interior_objects, all_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f4a1fcdd1c8b"
VERSION = "1.1.0"
TASK_ID = "f4a1fcdd1c8b"
SUMMARY = "Only components touching the grid border are kept; interior components are dropped."

INVARIANTS = [
    "background is 0",
    "at least one object touches the border",
    "at least one object is fully interior",
    "kept objects preserve their original colors and positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_border_objects", "no_interior_objects", "all_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 12..15", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "border_side":    {"type": "choice", "default": "rng top|left|bottom|right", "valid": "top|left|bottom|right"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "border_plus_interior",
                       "valid": "border_plus_interior"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]


def _size(shape):
    return max(r for r, _ in shape) + 1, max(c for _, c in shape) + 1


def _free(g, r0, c0, shape, pad=1):
    h, w = len(g), len(g[0])
    sh, sw = _size(shape)
    if r0 < 0 or c0 < 0 or r0 + sh > h or c0 + sw > w:
        return False
    for r in range(max(0, r0 - pad), min(h, r0 + sh + pad)):
        for c in range(max(0, c0 - pad), min(w, c0 + sw + pad)):
            if g[r][c] != 0:
                return False
    return True


def _paint(g, r0, c0, shape, color):
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = color


def _place_border(g, rng, shape, color, side):
    h, w = len(g), len(g[0])
    sh, sw = _size(shape)
    for _ in range(80):
        if side == "top":
            r0, c0 = 0, rng.randint(0, w - sw)
        elif side == "bottom":
            r0, c0 = h - sh, rng.randint(0, w - sw)
        elif side == "left":
            r0, c0 = rng.randint(0, h - sh), 0
        else:
            r0, c0 = rng.randint(0, h - sh), w - sw
        if _free(g, r0, c0, shape):
            _paint(g, r0, c0, shape, color)
            return
    raise ValueError("could not place border object")


def _place_interior(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh, sw = _size(shape)
    for _ in range(120):
        r0 = rng.randint(1, h - sh - 1)
        c0 = rng.randint(1, w - sw - 1)
        if _free(g, r0, c0, shape):
            _paint(g, r0, c0, shape, color)
            return
    raise ValueError("could not place interior object")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 16)
        w = ctx.draw_int("width", 15, 18)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 12, 15)
    side = ctx.draw_choice("border_side", ["top", "left", "bottom", "right"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [2, 3, 4]
    rng.shuffle(colors)
    _place_border(g, rng, rng.choice(_SHAPES), colors[0], side)
    _place_interior(g, rng, rng.choice(_SHAPES), colors[1])
    _place_interior(g, rng, rng.choice(_SHAPES), colors[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_border_objects":
        # All objects fully interior — rule keeps nothing.
        for dr, dc in _SHAPES[0]: g[3 + dr][3 + dc] = 3
        for dr, dc in _SHAPES[1]: g[3 + dr][8 + dc] = 4
        return g
    if name == "no_interior_objects":
        # All objects touch border — rule keeps everything (no drop).
        for dr, dc in _SHAPES[0]: g[0 + dr][2 + dc] = 3
        for dr, dc in _SHAPES[1]: g[h - 2 + dr][8 + dc] = 4
        return g
    if name == "all_border":
        # Every object touches a border — rule's filter is trivial.
        for dr, dc in _SHAPES[0]: g[0 + dr][1 + dc] = 3
        for dr, dc in _SHAPES[1]: g[0 + dr][6 + dc] = 4
        for dr, dc in _SHAPES[0]: g[h - 2 + dr][3 + dc] = 5
        return g
    return g
