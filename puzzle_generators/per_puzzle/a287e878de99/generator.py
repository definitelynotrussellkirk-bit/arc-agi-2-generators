"""Generator for arc_puzzle_bank_21_set6_s:S6_E7.

Rule: only same-color path cells with exactly one orthogonal neighbor remain
(endpoints of non-branching paths).

Combinatorial axes (8): grid_h, grid_w, palette_kind, component_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_paths, branching_paths, single_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a287e878de99"
VERSION = "1.1.0"
TASK_ID = "a287e878de99"

SUMMARY = "Only same-color path cells with exactly one orthogonal neighbor remain."

INVARIANTS = [
    "background is 0",
    "all path cells are color 5",
    "every component is a non-branching orthogonal path",
    "endpoint cells have exactly one same-color cardinal neighbor",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_paths", "branching_paths", "single_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "component_count": {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_paths_color5",
                       "valid": "spaced_paths_color5"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_PATHS = [
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2)],
]


def _place_path(g, rng, cells, occupied):
    h = len(g)
    w = len(g[0])
    max_r = max(r for r, _ in cells)
    max_c = max(c for _, c in cells)
    for _ in range(300):
        r0 = rng.randint(0, h - max_r - 1)
        c0 = rng.randint(0, w - max_c - 1)
        placed = [(r0 + r, c0 + c) for r, c in cells]
        if any(g[r][c] != 0 for r, c in placed):
            continue
        if any(abs(r - rr) + abs(c - cc) <= 1 for r, c in placed for rr, cc in occupied):
            continue
        for r, c in placed:
            g[r][c] = 5
        occupied.update(placed)
        return
    raise ValueError("could not place path")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        count = ctx.draw_int("component_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        count = ctx.draw_int("component_count", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        count = ctx.draw_int("component_count", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    occupied = set()
    for _ in range(count):
        _place_path(g, rng, rng.choice(_PATHS), occupied)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_paths":
        # blank → no path cells, rule has no effect
        return g
    if name == "branching_paths":
        # path with branching (T-junction has 3 neighbors at junction) → predicate fails
        for (r, c) in [(2, 2), (2, 3), (2, 4), (3, 3), (4, 3)]: g[r][c] = 5  # T-shape
        return g
    if name == "single_cells":
        # isolated 1-cell paths (zero neighbors) → predicate "exactly 1 neighbor" fails
        g[1][2] = 5
        g[3][6] = 5
        g[5][8] = 5
        return g
    return g
