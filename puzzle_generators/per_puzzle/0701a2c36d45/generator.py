"""Generator for arc_puzzle_bank_21_set19_s:S19_H6.

Combinatorial axes (8): shape, codes, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_header, no_panels, mismatched_codes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0701a2c36d45"
VERSION = "1.1.0"
TASK_ID = "0701a2c36d45"
SUMMARY = "Rotate each panel by its header code and take the majority occupied shape."

INVARIANTS = [
    "row panels are separated by full color-9 rows",
    "the header row contains three rotation codes",
    "each lower panel is the inverse-rotated form of the same base shape",
    "after applying the header rotations, all three panels agree on the same occupancy",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_header", "no_panels", "mismatched_codes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "shape":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "codes":          {"type": "choice", "default": "rng", "valid": "three values in 1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "header_then_3_panels",
                       "valid": "header_then_3_panels"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)],
]


def _rot90(cells):
    if not cells:
        return []
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    norm = [(r - min_r, c - min_c) for r, c in cells]
    height = max(r for r, _ in norm) + 1
    raw = [(c, height - 1 - r) for r, c in norm]
    mr = min(r for r, _ in raw)
    mc = min(c for _, c in raw)
    return sorted((r - mr, c - mc) for r, c in raw)


def _rot(cells, turns):
    out = sorted(cells)
    for _ in range(turns % 4):
        out = _rot90(out)
    return out


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        shape = _SHAPES[ctx.draw_int("shape", 0, 1)]
    elif difficulty == "hard":
        shape = _SHAPES[ctx.draw_int("shape", 2, 3)]
    else:
        shape = _SHAPES[ctx.draw_int("shape", 0, len(_SHAPES) - 1)]
    codes = [rng.randint(1, 4) for _ in range(3)]
    colors = [2, 3, 4]
    g = full_grid(16, 4, 0)
    for i, code in enumerate(codes):
        g[0][i] = code
    for r in (1, 6, 11):
        for c in range(4):
            g[r][c] = 9
    for panel_idx, code in enumerate(codes):
        turns = {1: 0, 2: 1, 3: 2, 4: 3}[code]
        cells = _rot(shape, -turns)
        _paint(g, 2 + panel_idx * 5, 0, cells, colors[panel_idx])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 4, 0)
    if name == "no_header":
        # Header row empty — rule has no rotation codes to apply.
        for r in (1, 6, 11):
            for c in range(4): g[r][c] = 9
        _paint(g, 2, 0, _SHAPES[0], 2)
        _paint(g, 7, 0, _SHAPES[0], 3)
        _paint(g, 12, 0, _SHAPES[0], 4)
        return g
    if name == "no_panels":
        # Header present but panels empty — rule has nothing to rotate.
        g[0][0] = 1; g[0][1] = 2; g[0][2] = 3
        for r in (1, 6, 11):
            for c in range(4): g[r][c] = 9
        return g
    if name == "mismatched_codes":
        # Codes don't match panel rotations — output occupancies disagree.
        g[0][0] = 1; g[0][1] = 1; g[0][2] = 1
        for r in (1, 6, 11):
            for c in range(4): g[r][c] = 9
        _paint(g, 2, 0, _SHAPES[0], 2)
        _paint(g, 7, 0, _SHAPES[1], 3)
        _paint(g, 12, 0, _SHAPES[2], 4)
        return g
    return g
