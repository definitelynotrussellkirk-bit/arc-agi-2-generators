"""Generator for arc_puzzle_bank_nineteenth21:E130.

Rule: erase isolated single-cell components; keep multi-cell components.

Combinatorial axes (8): grid_h, grid_w, palette_kind, singletons, objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_singletons, no_objects, all_singletons.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b765f6c9ebeb"
VERSION = "1.1.0"
TASK_ID = "b765f6c9ebeb"

SUMMARY = "Mix isolated singleton cells with multi-cell components."

INVARIANTS = [
    "background is 0",
    "single-cell components are isolated and will be erased",
    "multi-cell components have size at least 2 and are preserved",
    "same-color components are not adjacent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_singletons", "no_objects", "all_singletons")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "singletons":     {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "objects":        {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "mixed_singletons_and_objects",
                       "valid": "mixed_singletons_and_objects"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_OBJECT_SHAPES = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        singleton_target = ctx.draw_int("singletons", 2, 2)
        object_target = ctx.draw_int("objects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        singleton_target = ctx.draw_int("singletons", 3, 4)
        object_target = ctx.draw_int("objects", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        singleton_target = ctx.draw_int("singletons", 2, 4)
        object_target = ctx.draw_int("objects", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    placed = 0
    for _ in range(300):
        if placed >= object_target:
            break
        shape = rng.choice(_OBJECT_SHAPES)
        top = rng.randint(0, h - 1 - max(r for r, _ in shape))
        left = rng.randint(0, w - 1 - max(c for _, c in shape))
        cells = _cells(top, left, shape)
        guard = _guard(cells, h, w)
        if guard & reserved:
            continue
        color = rng.choice(colors)
        for r, c in cells:
            g[r][c] = color
        reserved.update(guard)
        placed += 1

    placed = 0
    for _ in range(400):
        if placed >= singleton_target:
            break
        r = rng.randrange(h)
        c = rng.randrange(w)
        cells = {(r, c)}
        guard = _guard(cells, h, w)
        if guard & reserved:
            continue
        g[r][c] = rng.choice(colors)
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_singletons":
        # only multi-cell objects → rule fires zero times, output identical
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        for (r, c) in [(5, 5), (5, 6)]: g[r][c] = 6
        return g
    if name == "no_objects":
        # only singletons → all erased, output blank
        g[1][2] = 4; g[3][5] = 6; g[5][7] = 3; g[6][1] = 8
        return g
    if name == "all_singletons":
        # every cell is its own component → every cell erased, output blank
        g[1][2] = 4; g[3][5] = 6; g[5][7] = 3; g[6][1] = 8; g[2][6] = 7
        return g
    return g
