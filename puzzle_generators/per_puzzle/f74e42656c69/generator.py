"""Generator for arc_puzzle_bank_21_set7_s:S7_E7.

Rule: count disconnected color-1 components → 1xN bar of 1s.

Combinatorial axes (8): grid_h, grid_w, palette_kind, component_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, single_blob, components_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f74e42656c69"
VERSION = "1.1.0"
TASK_ID = "f74e42656c69"
SUMMARY = "The number of disconnected color-1 components is encoded as a one-row bar of 1s."

INVARIANTS = [
    "background is 0",
    "only color 1 is used",
    "there are two to six isolated color-1 singleton components",
    "output width equals the component count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "single_blob", "components_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "component_count": {"type": "int", "default": "rng 2..6", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "isolated", "valid": "isolated"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _far(cells, r, c):
    return all(abs(r - rr) + abs(c - cc) >= 2 for rr, cc in cells)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        count = ctx.draw_int("component_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        count = ctx.draw_int("component_count", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 11)
        count = ctx.draw_int("component_count", 2, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = []
    for _ in range(count):
        for _attempt in range(100):
            r = rng.randrange(h)
            c = rng.randrange(w)
            if g[r][c] == 0 and _far(placed, r, c):
                g[r][c] = 1
                placed.append((r, c))
                break
        else:
            raise ValueError("could not place isolated component")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_components":
        # zero color-1 cells → output bar has length 0, ambiguous shape
        return g
    if name == "single_blob":
        # one large connected blob → count is 1, no comparison signal across multiple objects
        for r, c in [(2, 3), (2, 4), (3, 3), (3, 4), (4, 3)]:
            g[r][c] = 1
        return g
    if name == "components_touching":
        # adjacent cells form one component, not two → counting under "isolated" invariant breaks
        for r, c in [(2, 2), (2, 3), (4, 5), (4, 6), (4, 7)]:
            g[r][c] = 1
        return g
    return g
