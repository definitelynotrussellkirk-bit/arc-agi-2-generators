"""Generator for arc_puzzle_bank_21_set15:S15_E5 — replay color-2 mask at color-3 target rect.

A color-2 source mask is replayed at the top-left corner of a single
color-3 target rectangle.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_source (no color-2 mask → rule has no pattern to
replay), no_target (no color-3 rectangle → rule has no anchor point
to replay at), source_outside_target (source bbox doesn't fit inside
target rect → rule's replay overflows or is undefined).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c286f4a2923f"
VERSION = "1.1.0"
TASK_ID = "c286f4a2923f"
SUMMARY = "A color-2 source mask is replayed at the top-left corner of a single color-3 target rectangle."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-2 source component",
    "there is exactly one solid color-3 target rectangle",
    "the source mask fits inside the target rectangle bbox",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source", "no_target", "source_outside_target")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":            {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":             {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "target_padding":    {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "source_mask_plus_target_rect",
                          "valid": "source_mask_plus_target_rect"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
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


def _paint_shape(g, r0, c0, shape, color):
    for dr, dc in shape:
        g[r0 + dr][c0 + dc] = color


def _paint_rect(g, r0, c0, rh, rw, color):
    for r in range(r0, r0 + rh):
        for c in range(c0, c0 + rw):
            g[r][c] = color


def _place_shape(g, rng, shape, color):
    sh, sw = _size(shape)
    h, w = len(g), len(g[0])
    for _ in range(120):
        r0 = rng.randint(0, h - sh)
        c0 = rng.randint(0, w - sw)
        if _free_box(g, r0, c0, sh, sw):
            _paint_shape(g, r0, c0, shape, color)
            return
    raise ValueError("could not place source")


def _place_rect(g, rng, rh, rw):
    h, w = len(g), len(g[0])
    for _ in range(120):
        r0 = rng.randint(0, h - rh)
        c0 = rng.randint(0, w - rw)
        if _free_box(g, r0, c0, rh, rw):
            _paint_rect(g, r0, c0, rh, rw, 3)
            return
    raise ValueError("could not place target")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 12, 13)
        pad = ctx.draw_int("target_padding", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 12, 13)
        w = ctx.draw_int("width", 14, 15)
        pad = ctx.draw_int("target_padding", 1, 2)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 12, 15)
        pad = ctx.draw_int("target_padding", 0, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shape = rng.choice(_SHAPES)
    sh, sw = _size(shape)
    _place_shape(g, rng, shape, 2)
    _place_rect(g, rng, sh + pad, sw + rng.randint(0, 2))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_source":
        # No color-2 — rule has no pattern to replay.
        for r in range(2, 5):
            for c in range(8, 11): g[r][c] = 3
        return g
    if name == "no_target":
        # No color-3 rectangle — rule has no anchor to replay at.
        for r, c in [(2, 2), (3, 2), (4, 2), (4, 3)]: g[r][c] = 2
        return g
    if name == "source_outside_target":
        # Source bbox is larger than target rect — replay overflows.
        for r, c in [(2, 2), (2, 3), (3, 2), (3, 3), (4, 2), (4, 3)]: g[r][c] = 2
        # tiny target
        for r in range(7, 8):
            for c in range(8, 9): g[r][c] = 3
        return g
    return g
