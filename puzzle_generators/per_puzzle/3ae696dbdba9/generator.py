"""Generator for arc_puzzle_bank_21_set14_s:S14_E2.

Rule: connected components have per-column holes that are closed into
vertical spans.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, no_col_gap, single_cell_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3ae696dbdba9"
VERSION = "1.1.0"
TASK_ID = "3ae696dbdba9"
SUMMARY = "Connected components have per-column holes that are closed into vertical spans."

INVARIANTS = [
    "background is 0",
    "there are two to four separated nonzero components",
    "at least one component has a column gap between its topmost and bottommost cells",
    "outputs preserve component colors while filling column spans",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "no_col_gap", "single_cell_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "component_count":{"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "scattered_with_col_gaps",
                       "valid": "scattered_with_col_gaps"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BASE_SHAPES = [
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (2, 1), (2, 2)],
]
_SHAPES = [[(c, r) for r, c in shape] for shape in _BASE_SHAPES]


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
    raise ValueError("could not place column-span component")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 10, 10)
        w = ctx.draw_int("width", 10, 10)
        count = ctx.draw_int("component_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 16)
        w = ctx.draw_int("width", 13, 16)
        count = ctx.draw_int("component_count", 4, 5)
    else:
        h = ctx.draw_int("height", 10, 13)
        w = ctx.draw_int("width", 10, 13)
        count = ctx.draw_int("component_count", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [2, 3, 5, 7]
    rng.shuffle(colors)
    for color in colors[:count]:
        _place(g, rng, rng.choice(_SHAPES), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — rule has no columns to span.
        return g
    if name == "no_col_gap":
        # Solid contiguous components (every column already
        # filled top-to-bottom) — rule's "fill column gap" branch
        # never fires.
        for r in range(2, 5):
            for c in range(2, 4): g[r][c] = 4
        for r in range(6, 9):
            for c in range(7, 9): g[r][c] = 6
        return g
    if name == "single_cell_objects":
        # 1-cell objects — rule's per-column span has no gap.
        g[2][2] = 4; g[5][7] = 6; g[8][3] = 7
        return g
    return g
