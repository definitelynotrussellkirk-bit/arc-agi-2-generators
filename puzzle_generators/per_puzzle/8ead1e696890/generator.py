"""Generator for arc_puzzle_bank_ninth_21_bundle:easy_60_keep_border_touching_components.

Rule: keep border-touching components, drop interior ones.

Combinatorial axes (8): grid_h, grid_w, palette_kind, interior_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_border, all_interior, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8ead1e696890"
VERSION = "1.1.0"
TASK_ID = "8ead1e696890"
SUMMARY = "Border-touching components are mixed with interior components."

INVARIANTS = [
    "background is 0",
    "at least two components touch the outer border",
    "at least one component is fully interior",
    "components are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_border", "all_interior", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "interior_objects": {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "border_plus_interior",
                       "valid": "border_plus_interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0)],
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


def _paint(g: list[list[int]], cells: set[tuple[int, int]], color: int) -> None:
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        interior_target = ctx.draw_int("interior_objects", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        interior_target = ctx.draw_int("interior_objects", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        interior_target = ctx.draw_int("interior_objects", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], interior_target + 2)

    border_specs = [
        (0, rng.randint(0, w - 3), [(0, 0), (0, 1), (1, 0)]),
        (h - 2, w - 2, [(0, 1), (1, 0), (1, 1)]),
    ]
    for i, (top, left, shape) in enumerate(border_specs):
        cells = _cells(top, left, shape)
        _paint(g, cells, colors[i])
        reserved.update(_guard(cells, h, w))

    placed = 0
    for _ in range(300):
        if placed >= interior_target:
            break
        shape = rng.choice(_SHAPES)
        max_r = h - 2 - max(r for r, _ in shape)
        max_c = w - 2 - max(c for _, c in shape)
        top = rng.randint(1, max_r)
        left = rng.randint(1, max_c)
        cells = _cells(top, left, shape)
        guard = _guard(cells, h, w)
        if guard & reserved:
            continue
        _paint(g, cells, colors[placed + 2])
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "all_border":
        # all components touch the border → rule keeps everything, no contrast
        _paint(g, {(0, 1), (0, 2), (1, 1)}, 4)
        _paint(g, {(h - 1, w - 3), (h - 1, w - 2)}, 6)
        _paint(g, {(3, 0), (4, 0)}, 3)
        _paint(g, {(2, w - 1), (3, w - 1)}, 8)
        return g
    if name == "all_interior":
        # no component touches the border → rule erases everything, output is empty
        _paint(g, {(3, 3), (3, 4), (4, 3)}, 4)
        _paint(g, {(6, 6), (6, 7), (7, 7)}, 6)
        _paint(g, {(5, 1), (5, 2)}, 3)
        return g
    if name == "no_components":
        # blank grid → rule has nothing to keep or drop, output is empty
        return g
    return g
