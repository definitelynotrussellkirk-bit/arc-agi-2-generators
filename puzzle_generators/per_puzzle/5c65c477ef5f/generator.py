"""Generator for arc_puzzle_bank_21_set13_s:S13_E6 — smallest asymmetric → 8.

The smallest object with no horizontal or vertical symmetry is cropped and
recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_symmetric (no asymmetric components → rule's selector
finds nothing, output equals input), tied_smallest_asym (≥2 asymmetric
components share min size → "smallest" tie-break decides), single_asym
(only one asymmetric component → trivially selected, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5c65c477ef5f"
VERSION = "1.1.0"
TASK_ID = "5c65c477ef5f"
SUMMARY = "The smallest object with no horizontal or vertical symmetry is cropped and recolored to 8."

INVARIANTS = [
    "background is 0",
    "there is one strictly smallest asymmetric component",
    "larger asymmetric components and symmetric distractors may also appear",
    "the selected asymmetric crop is recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_symmetric", "tied_smallest_asym", "single_asym")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "asym_distractors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "asym_target_plus_distractors",
                       "valid": "asym_target_plus_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TARGET = [(0, 0), (1, 0), (1, 1)]
_ASYM_BIG = [
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)],
]
_SYMMETRIC = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
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
        h = ctx.draw_int("height", 10, 11)
        w = ctx.draw_int("width", 12, 13)
        asym_count = ctx.draw_int("asym_distractors", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 16)
        w = ctx.draw_int("width", 15, 18)
        asym_count = ctx.draw_int("asym_distractors", 2, 3)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 12, 15)
        asym_count = ctx.draw_int("asym_distractors", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [2, 3, 4, 5]
    rng.shuffle(colors)
    _place(g, rng, _TARGET, colors[0])
    big = _ASYM_BIG[:]
    rng.shuffle(big)
    for color, shape in zip(colors[1:], big[:asym_count]):
        _place(g, rng, shape, color)
    _place(g, rng, rng.choice(_SYMMETRIC), colors[-1])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "all_symmetric":
        # No asymmetric components — rule's "smallest asymmetric"
        # selector finds nothing; output equals input.
        for dr, dc in _SYMMETRIC[0]:
            g[1 + dr][2 + dc] = 2
        for dr, dc in _SYMMETRIC[1]:
            g[6 + dr][8 + dc] = 4
        return g
    if name == "tied_smallest_asym":
        # Two asymmetric components share min size → "smallest"
        # is ambiguous; tie-break decides.
        for dr, dc in _TARGET:
            g[2 + dr][2 + dc] = 2
        for dr, dc in _TARGET:
            g[2 + dr][8 + dc] = 3
        for dr, dc in _ASYM_BIG[0]:
            g[7 + dr][3 + dc] = 4
        return g
    if name == "single_asym":
        # Only one asymmetric component — trivially selected; no
        # cross-candidate contrast.
        for dr, dc in _TARGET:
            g[3 + dr][4 + dc] = 6
        for dr, dc in _SYMMETRIC[0]:
            g[7 + dr][8 + dc] = 5
        return g
    return g
