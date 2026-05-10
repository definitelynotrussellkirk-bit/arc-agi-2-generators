"""Generator for arc_puzzle_bank_21_set15:S15_E7 — source-vs-candidates congruence indicator.

A source stencil is compared with ordered candidate components to produce a one-row congruence indicator.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_match (all 4 candidates equal source → indicator is
all-1, no contrast), no_match (no candidate equals source → indicator
is all-0, output trivial), no_source (no color-2 stencil → rule's
comparison has no anchor).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "75c10ce4046c"
VERSION = "1.1.0"
TASK_ID = "75c10ce4046c"
SUMMARY = "A source stencil is compared with ordered candidate components to produce a one-row congruence indicator."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-2 source component",
    "there are four candidate components in colors 3..6",
    "at least one candidate matches the source offsets and at least one does not",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_match", "no_match", "no_source")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 13..16", "valid": "10..18"},
    "matching_candidates": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "source_plus_4_candidates",
                       "valid": "source_plus_4_candidates"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
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
    for _ in range(160):
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
        w = ctx.draw_int("width", 13, 14)
        match_count = ctx.draw_int("matching_candidates", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 16)
        w = ctx.draw_int("width", 15, 18)
        match_count = ctx.draw_int("matching_candidates", 2, 3)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 13, 16)
        match_count = ctx.draw_int("matching_candidates", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    source = rng.choice(_SHAPES)
    _place(g, rng, source, 2)
    distractors = [s for s in _SHAPES if s != source]
    rng.shuffle(distractors)
    candidate_shapes = [source] * match_count + distractors[:4 - match_count]
    rng.shuffle(candidate_shapes)
    for color, shape in zip([3, 4, 5, 6], candidate_shapes):
        _place(g, rng, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "all_match":
        # All 4 candidates match the source → indicator is all-1;
        # rule has no contrast across positions.
        source = _SHAPES[0]
        _place(g, __import__("random").Random(0), source, 2)
        for color, c0 in zip([3, 4, 5, 6], [3, 6, 9, 12]):
            for dr, dc in source:
                if 7 + dr < h and c0 + dc < w:
                    g[7 + dr][c0 + dc - 1] = color
        return g
    if name == "no_match":
        # No candidate matches the source → indicator is all-0;
        # rule's "match found" branch never fires.
        source = _SHAPES[0]
        _place(g, __import__("random").Random(1), source, 2)
        for color, shape in zip([3, 4, 5, 6], _SHAPES[1:]):
            for dr, dc in shape:
                if 7 + dr < h and 1 + (color - 3) * 3 + dc < w:
                    g[7 + dr][1 + (color - 3) * 3 + dc] = color
        return g
    if name == "no_source":
        # No color-2 stencil — rule's comparison has no anchor;
        # output undefined.
        for color, shape in zip([3, 4, 5, 6], _SHAPES[:4]):
            for dr, dc in shape:
                if 4 + dr < h and 1 + (color - 3) * 3 + dc < w:
                    g[4 + dr][1 + (color - 3) * 3 + dc] = color
        return g
    return g
