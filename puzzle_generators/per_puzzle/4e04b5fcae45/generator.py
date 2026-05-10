"""Generator for arc_puzzle_bank_21_set13_s:S13_E4.

Combinatorial axes (8): height, width, palette_kind, symmetric_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, all_symmetric, all_asymmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4e04b5fcae45"
VERSION = "1.1.0"
TASK_ID = "4e04b5fcae45"
SUMMARY = "Horizontally symmetric components are recolored to 8 while asymmetric distractors remain."

INVARIANTS = [
    "background is 0",
    "there is at least one horizontally symmetric component",
    "there is at least one component without horizontal symmetry",
    "outputs preserve size and recolor only horizontal-symmetry components",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "all_symmetric", "all_asymmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "symmetric_count": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "mixed_sym_asym",
                       "valid": "mixed_sym_asym"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SYM_H = [
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2)],
]
_ASYM = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
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
        sym_count = ctx.draw_int("symmetric_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 16)
        w = ctx.draw_int("width", 14, 18)
        sym_count = ctx.draw_int("symmetric_count", 2, 3)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 12, 15)
        sym_count = ctx.draw_int("symmetric_count", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [2, 3, 4, 6]
    rng.shuffle(colors)
    for i in range(sym_count):
        _place(g, rng, rng.choice(_SYM_H), colors[i])
    for color in colors[sym_count:sym_count + 2]:
        _place(g, rng, rng.choice(_ASYM), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has no components to evaluate symmetry on.
        return g
    if name == "all_symmetric":
        # All components are LR-symmetric — every one gets recolored.
        for dr, dc in _SYM_H[0]: g[1 + dr][2 + dc] = 4
        for dr, dc in _SYM_H[1]: g[5 + dr][2 + dc] = 5
        for dr, dc in _SYM_H[2]: g[8 + dr][2 + dc] = 6
        return g
    if name == "all_asymmetric":
        # No symmetric components — rule recolors nothing (input == output).
        for dr, dc in _ASYM[0]: g[1 + dr][2 + dc] = 4
        for dr, dc in _ASYM[1]: g[5 + dr][2 + dc] = 5
        for dr, dc in _ASYM[2]: g[8 + dr][2 + dc] = 6
        return g
    return g
