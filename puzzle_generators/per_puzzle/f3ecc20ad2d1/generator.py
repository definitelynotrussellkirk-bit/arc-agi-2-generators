"""Generator for arc_puzzle_bank_21_set13_s:S13_E5 — single holed component selector.

Rule: exactly one component has one enclosed hole; that object is cropped and recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, no_holed_object, multiple_holed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f3ecc20ad2d1"
VERSION = "1.1.0"
TASK_ID = "f3ecc20ad2d1"
SUMMARY = "Exactly one component has one enclosed hole; that object is cropped and recolored to 8."

INVARIANTS = [
    "background is 0",
    "there is exactly one component with one enclosed zero hole",
    "all distractor components have zero holes",
    "the one-hole component is cropped and recolored",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "no_holed_object", "multiple_holed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 11..14", "valid": "9..17"},
    "width":          {"type": "int", "default": "rng 13..16", "valid": "10..19"},
    "distractor_count": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "holed_with_solid_distractors",
                       "valid": "holed_with_solid_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_HOLED = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3)],
]
_SOLID = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
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


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh, sw = _size(shape)
    for _ in range(160):
        r0 = rng.randint(0, h - sh)
        c0 = rng.randint(0, w - sw)
        if _free(g, r0, c0, shape):
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
            return
    raise ValueError("could not place object")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 11, 11)
        w = ctx.draw_int("width", 13, 13)
        distractor_count = ctx.draw_int("distractor_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 14, 16)
        w = ctx.draw_int("width", 16, 18)
        distractor_count = ctx.draw_int("distractor_count", 3, 4)
    else:
        h = ctx.draw_int("height", 11, 14)
        w = ctx.draw_int("width", 13, 16)
        distractor_count = ctx.draw_int("distractor_count", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [2, 3, 4, 6]
    rng.shuffle(colors)
    _place(g, rng, rng.choice(_HOLED), colors[0])
    for color in colors[1:1 + distractor_count]:
        _place(g, rng, rng.choice(_SOLID), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has no candidates.
        return g
    if name == "no_holed_object":
        # Only solid distractors — rule's "exactly one holed"
        # filter excludes everything; output undefined.
        for r, c in [(2, 2), (2, 3), (3, 2), (3, 3)]: g[r][c] = 4
        for r, c in [(7, 8), (7, 9), (8, 8)]: g[r][c] = 6
        return g
    if name == "multiple_holed":
        # Two holed objects — rule's "exactly one" tie-break
        # ambiguous.
        for dr, dc in _HOLED[0]: g[1 + dr][1 + dc] = 4
        for dr, dc in _HOLED[0]: g[8 + dr][9 + dc] = 6
        return g
    return g
