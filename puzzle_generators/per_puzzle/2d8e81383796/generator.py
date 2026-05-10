"""Generator for arc_puzzle_bank_21_set14_s:S14_E5.

Combinatorial axes (8): height, width, palette_kind, distractor_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_target, no_distractors, tied_peaks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2d8e81383796"
VERSION = "1.1.0"
TASK_ID = "2d8e81383796"
SUMMARY = "Among several components, the one with the largest occupied column peak is cropped and recolored."

INVARIANTS = [
    "background is 0",
    "there are multiple separated nonzero components",
    "one component has a strictly highest column occupancy peak",
    "the target crop is recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_target", "no_distractors", "tied_peaks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "width":          {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "distractor_count": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "target_plus_distractors",
                       "valid": "target_plus_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TARGETS = [
    [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), (3, 2)],
]
_DISTRACTORS = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (0, 1)],
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
    raise ValueError("could not place component")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 12, 13)
        w = ctx.draw_int("width", 10, 11)
        distractor_count = ctx.draw_int("distractor_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 14, 17)
        w = ctx.draw_int("width", 12, 15)
        distractor_count = ctx.draw_int("distractor_count", 3, 4)
    else:
        h = ctx.draw_int("height", 12, 15)
        w = ctx.draw_int("width", 10, 13)
        distractor_count = ctx.draw_int("distractor_count", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [2, 3, 4, 5]
    rng.shuffle(colors)
    _place(g, rng, rng.choice(_TARGETS), colors[0])
    distractors = _DISTRACTORS[:]
    rng.shuffle(distractors)
    for color, shape in zip(colors[1:], distractors[:distractor_count]):
        _place(g, rng, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 11
    g = full_grid(h, w, 0)
    if name == "no_target":
        # Distractors only, no target with tall column peak — rule has no winner.
        for dr, dc in _DISTRACTORS[0]: g[2 + dr][2 + dc] = 3
        for dr, dc in _DISTRACTORS[1]: g[6 + dr][2 + dc] = 4
        return g
    if name == "no_distractors":
        # Single target, no distractors — rule's selection is trivial.
        for dr, dc in _TARGETS[0]: g[2 + dr][2 + dc] = 3
        return g
    if name == "tied_peaks":
        # Two targets share max column peak — winner is ambiguous.
        for dr, dc in _TARGETS[0]: g[2 + dr][2 + dc] = 3
        for dr, dc in _TARGETS[1]: g[2 + dr][7 + dc] = 4
        return g
    return g
