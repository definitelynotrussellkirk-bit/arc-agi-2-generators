"""Generator for arc_puzzle_bank_nineteenth21:E133.

Rule: separated components reduce to their bounding-box center cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_cell_objects, even_size_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "06206fc98d42"
VERSION = "1.1.0"
TASK_ID = "06206fc98d42"

SUMMARY = "Separated components reduce to their bounding-box center cells."

INVARIANTS = [
    "background is 0",
    "each component has size greater than 1",
    "component bounding boxes have clear central cells",
    "components are separated and use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_cell_objects", "even_size_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "objects":        {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_3x3_components",
                       "valid": "spaced_3x3_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
]


def _cells(top: int, left: int, shape: list[tuple[int, int]]) -> set[tuple[int, int]]:
    return {(top + r, left + c) for r, c in shape}


def _guard(cells: set[tuple[int, int]], h: int, w: int) -> set[tuple[int, int]]:
    return {
        (rr, cc)
        for r, c in cells
        for rr in range(max(0, r - 1), min(h, r + 2))
        for cc in range(max(0, c - 1), min(w, c + 2))
    }


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("objects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("objects", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("objects", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        shape = rng.choice(_SHAPES)
        top = rng.randint(0, h - 3)
        left = rng.randint(0, w - 3)
        cells = _cells(top, left, shape)
        guard = _guard(cells, h, w)
        if guard & reserved:
            continue
        for r, c in cells:
            g[r][c] = colors[placed % len(colors)]
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → no components, rule has no centers to extract
        return g
    if name == "single_cell_objects":
        # 1x1 objects → bbox center is the cell itself, rule is identity
        g[2][3] = 4
        g[5][6] = 6
        return g
    if name == "even_size_objects":
        # 2x2 components → no unique center, rule undefined
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 4
        for r in range(2):
            for c in range(2): g[5 + r][5 + c] = 6
        return g
    return g
