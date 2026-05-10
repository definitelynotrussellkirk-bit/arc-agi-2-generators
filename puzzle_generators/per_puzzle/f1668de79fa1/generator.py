"""Generator for arc_puzzle_bank_21_set15:S15_E3.

Rule: a color-2 template is horizontally mirrored and stamped at a
single color-1 marker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template (no color-2 shape → rule has no source);
no_marker (template present but no color-1 → rule has no
destination); lr_symmetric_template (template invariant under
hmirror → mirrored stamp identical to original, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f1668de79fa1"
VERSION = "1.1.0"
TASK_ID = "f1668de79fa1"
SUMMARY = "A color-2 template is horizontally mirrored and stamped at a single color-1 marker."

INVARIANTS = [
    "background is 0",
    "there is exactly one asymmetric color-2 template component",
    "there is exactly one color-1 marker cell",
    "the mirrored stamp fits at the marker",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_marker", "lr_symmetric_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":            {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "template_with_marker",
                          "valid": "template_with_marker"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 1), (1, 1), (2, 0), (2, 1)],
]


def _size(shape):
    return max(r for r, _ in shape) + 1, max(c for _, c in shape) + 1


def _hmirror(shape):
    _, sw = _size(shape)
    return sorted((r, sw - 1 - c) for r, c in shape)


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


def _place_shape(g, rng, shape, color):
    sh, sw = _size(shape)
    h, w = len(g), len(g[0])
    for _ in range(80):
        r0 = rng.randint(0, h - sh)
        c0 = rng.randint(0, w - sw)
        if _free_box(g, r0, c0, sh, sw):
            _paint(g, r0, c0, shape, color)
            return
    raise ValueError("could not place template")


def _place_marker(g, rng, stamp_shape):
    sh, sw = _size(stamp_shape)
    h, w = len(g), len(g[0])
    for _ in range(120):
        r = rng.randint(0, h - sh)
        c = rng.randint(0, w - sw)
        if g[r][c] == 0 and _free_box(g, r, c, 1, 1):
            g[r][c] = 1
            return
    raise ValueError("could not place marker")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 8, 9)
        w = ctx.draw_int("width", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 12, 13)
    else:
        h = ctx.draw_int("height", 8, 11)
        w = ctx.draw_int("width", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shape = rng.choice(_SHAPES)
    _place_shape(g, rng, shape, 2)
    _place_marker(g, rng, _hmirror(shape))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_template":
        # No color-2 template — rule has no source.
        g[5][5] = 1
        return g
    if name == "no_marker":
        # Template present but no color-1 marker — no destination.
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
            g[1 + dr][1 + dc] = 2
        return g
    if name == "lr_symmetric_template":
        # T-shape symmetric under h-mirror — mirrored stamp identical.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1)]:
            g[1 + dr][1 + dc] = 2
        g[5][7] = 1
        return g
    return g
