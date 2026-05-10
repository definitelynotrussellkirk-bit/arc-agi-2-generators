"""Generator for puzzle 1d0a4b61.

Rule: zeros in a periodic 3x3 color tile are filled from matching
period positions.

Combinatorial axes (8): grid_size, n_holes, tile_kind, palette_kind,
hole_distribution, anchor_corner, asymmetry_force, period.
Degenerates: no_holes, all_holes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b72821d1508d"
VERSION = "1.1.0"
TASK_ID = "b72821d1508d"
SUMMARY = "3x3 periodic tile with holes; rule fills holes from matching period."

INVARIANTS = [
    "grid repeats a 3x3 nonzero tile",
    "top 3 rows preserve full tile (no holes)",
    "1+ holes in repeated copies (rows >=3)",
    "each hole has nonzero value at same period position",
]

TILE_KINDS = ("digits", "warm", "cool", "primary", "broad")
HOLE_DISTRIBUTIONS = ("scattered", "clustered", "row_focus",
                     "col_focus", "diagonal")
DEGENERATE_TEXTURES = ("no_holes", "all_holes", "full_grid")
HELPFUL_TEXTURES = HOLE_DISTRIBUTIONS

AXES = {
    "grid_size":         {"type": "int", "default": "rng 9..15", "valid": "6..21"},
    "n_holes":           {"type": "int", "default": "rng 3..8", "valid": "1..20"},
    "tile_kind":         {"type": "str", "default": "rng helpful",
                          "valid": "|".join(TILE_KINDS)},
    "hole_distribution": {"type": "str", "default": "rng helpful",
                          "valid": "|".join(HOLE_DISTRIBUTIONS)},
    "anchor_corner":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "asymmetry_force":   {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "include_decoy":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "period":            {"type": "int", "default": "3", "valid": "3"},
    "texture":           {"type": "str", "default": "alias for hole_distribution",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        size_lo, size_hi = 6, 9
    elif difficulty == "hard":
        size_lo, size_hi = 12, 21
    else:
        size_lo, size_hi = 9, 15
    size = int(overrides.get("grid_size",
                             ctx.draw_int("grid_size", size_lo, size_hi)))
    size = max(6, min(21, size))
    n_holes = int(overrides.get("n_holes",
                                ctx.draw_int("n_holes", 3, 8)))
    n_holes = max(1, min(20, n_holes))
    tile_kind = overrides.get("tile_kind",
                              ctx.draw_choice("tile_kind",
                                              list(TILE_KINDS)))
    distribution = (overrides.get("texture") or
                    overrides.get("hole_distribution")
                    or ctx.draw_choice("hole_distribution",
                                       list(HOLE_DISTRIBUTIONS)))
    tile = _build_tile(tile_kind, rng)
    g = full_grid(size, size, 0)
    for r in range(size):
        for c in range(size):
            g[r][c] = tile[r % 3][c % 3]
    candidates = _hole_candidates(distribution, size, rng)
    candidates = [(r, c) for r, c in candidates if r >= 3]
    rng.shuffle(candidates)
    for r, c in candidates[:n_holes]:
        g[r][c] = 0
    return g


def _build_tile(kind, rng):
    if kind == "digits":
        return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    while len(pool) < 9:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
    return [[pool[r * 3 + c] for c in range(3)] for r in range(3)]


def _hole_candidates(distribution, size, rng):
    if distribution == "clustered":
        cr = rng.randint(3, size - 1); cc = rng.randint(0, size - 1)
        cells = [(r, c) for r in range(size) for c in range(size)]
        cells.sort(key=lambda p: abs(p[0] - cr) + abs(p[1] - cc))
        return cells
    if distribution == "row_focus":
        rs = rng.sample(range(3, size), min(2, size - 3))
        cells = [(r, c) for r in rs for c in range(size)]
        rng.shuffle(cells)
        return cells
    if distribution == "col_focus":
        cs = rng.sample(range(size), min(2, size))
        cells = [(r, c) for c in cs for r in range(3, size)]
        rng.shuffle(cells)
        return cells
    if distribution == "diagonal":
        diag = [(i, i) for i in range(min(size, size))]
        anti = [(i, size - 1 - i) for i in range(size)]
        cells = list(set(diag + anti))
        rng.shuffle(cells)
        return cells
    cells = [(r, c) for r in range(3, size) for c in range(size)]
    rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, rng):
    size = 9
    g = full_grid(size, size, 0)
    tile = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    for r in range(size):
        for c in range(size):
            g[r][c] = tile[r % 3][c % 3]
    if name == "no_holes":
        return g
    if name == "all_holes":
        for r in range(3, size):
            for c in range(size):
                g[r][c] = 0
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = tile[r % 3][c % 3]
        return g
    return g
