"""Generator for arc_puzzle_bank_21_set13_s:S13_E3.

Rule: the component with the widest bounding box is cropped and recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, single_component, tied_widest.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ddaee6c28dd7"
VERSION = "1.1.0"
TASK_ID = "ddaee6c28dd7"
SUMMARY = "The component with the widest bounding box is cropped and recolored to 8."

INVARIANTS = [
    "background is 0",
    "there are multiple separated components",
    "one component has a strictly widest bounding box",
    "distractors are narrower than the target",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "single_component", "tied_widest")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 14..17", "valid": "11..20"},
    "distractor_count": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "wide_with_narrow_distractors",
                       "valid": "wide_with_narrow_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_WIDE = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
]
_NARROW = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1)],
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
    for _ in range(120):
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
        h = ctx.draw_int("height", 10, 10)
        w = ctx.draw_int("width", 14, 14)
        distractor_count = ctx.draw_int("distractor_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 15)
        w = ctx.draw_int("width", 17, 19)
        distractor_count = ctx.draw_int("distractor_count", 3, 4)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 14, 17)
        distractor_count = ctx.draw_int("distractor_count", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [2, 3, 4, 5]
    rng.shuffle(colors)
    _place(g, rng, rng.choice(_WIDE), colors[0])
    for color in colors[1:1 + distractor_count]:
        _place(g, rng, rng.choice(_NARROW), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has no candidates.
        return g
    if name == "single_component":
        # Only one component — rule's selection is trivial; no
        # discrimination needed.
        for r, c in [(2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]: g[r][c] = 4
        return g
    if name == "tied_widest":
        # Two components share the same maximum width — rule's
        # "strictly widest" tie-break ambiguous.
        for r, c in [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]: g[r][c] = 4
        for r, c in [(7, 6), (7, 7), (7, 8), (7, 9), (7, 10)]: g[r][c] = 6
        return g
    return g
