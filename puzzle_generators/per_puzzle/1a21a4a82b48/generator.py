"""Generator for arc_puzzle_bank_21_set15:S15_E4.

Combinatorial axes (8): height, width, palette_kind, candidate_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source, no_match, multi_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1a21a4a82b48"
VERSION = "1.1.0"
TASK_ID = "1a21a4a82b48"
SUMMARY = "A color-2 source has exactly one top-left-congruent candidate among distractor components."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-2 source component",
    "exactly one candidate component in colors 3..6 has the same normalized offsets",
    "all distractor candidates have different normalized offsets",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_match", "multi_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "candidate_count": {"type": "int", "default": "4", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "5", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "source_plus_candidates",
                       "valid": "source_plus_candidates"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "4..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (2, 0)],
]


def _size(shape):
    return max(r for r, _ in shape) + 1, max(c for _, c in shape) + 1


def _free_box(g, r0, c0, sh, sw, pad=1):
    h, w = len(g), len(g[0])
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


def _place(g, rng, shape, color):
    sh, sw = _size(shape)
    h, w = len(g), len(g[0])
    for _ in range(120):
        r0 = rng.randint(0, h - sh)
        c0 = rng.randint(0, w - sw)
        if _free_box(g, r0, c0, sh, sw):
            _paint(g, r0, c0, shape, color)
            return
    raise ValueError("could not place component")


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
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    source = rng.choice(_SHAPES)
    _place(g, rng, source, 2)
    colors = [3, 4, 5, 6]
    rng.shuffle(colors)
    _place(g, rng, source, colors[0])
    distractors = [s for s in _SHAPES if s != source]
    rng.shuffle(distractors)
    for color, shape in zip(colors[1:], distractors[:3]):
        _place(g, rng, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_source":
        # No color-2 source — rule has no shape to compare against.
        for dr, dc in _SHAPES[0]: g[2 + dr][2 + dc] = 3
        for dr, dc in _SHAPES[1]: g[2 + dr][7 + dc] = 4
        return g
    if name == "no_match":
        # Source present but no candidate has the same shape — rule selects nothing.
        for dr, dc in _SHAPES[0]: g[2 + dr][2 + dc] = 2
        for dr, dc in _SHAPES[1]: g[2 + dr][7 + dc] = 3
        for dr, dc in _SHAPES[2]: g[6 + dr][2 + dc] = 4
        return g
    if name == "multi_match":
        # Two candidates match the source shape — match is non-unique.
        for dr, dc in _SHAPES[0]: g[2 + dr][2 + dc] = 2
        for dr, dc in _SHAPES[0]: g[2 + dr][7 + dc] = 3
        for dr, dc in _SHAPES[0]: g[7 + dr][2 + dc] = 4
        return g
    return g
