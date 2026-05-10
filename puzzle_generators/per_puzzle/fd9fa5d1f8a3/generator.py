"""Generator for arc_puzzle_bank_nineteenth_21_bundle:easy_129_expand_singletons_to_radius1_pluses.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_singletons,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_singletons, multi_cell_blob, on_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fd9fa5d1f8a3"
VERSION = "1.1.0"
TASK_ID = "fd9fa5d1f8a3"

SUMMARY = "Place isolated colored singleton cells that expand to radius-1 pluses."

INVARIANTS = [
    "background is 0",
    "each source cell is a singleton",
    "source cells are interior so all four cardinal neighbors exist",
    "source cells are separated so plus expansions do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_singletons", "multi_cell_blob", "on_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_singletons":   {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "isolated_interior_singletons",
                       "valid": "isolated_interior_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _guard(r: int, c: int, h: int, w: int) -> set[tuple[int, int]]:
    return {
        (rr, cc)
        for rr in range(max(0, r - 2), min(h, r + 3))
        for cc in range(max(0, c - 2), min(w, c + 3))
    }


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("singletons", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("singletons", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("singletons", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        guard = _guard(r, c, h, w)
        if guard & reserved:
            continue
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_singletons":
        # blank → no singletons to expand
        return g
    if name == "multi_cell_blob":
        # multi-cell blob → not singleton, "singleton" precondition fails
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        return g
    if name == "on_edge":
        # singleton at corner → plus expansion goes out of bounds
        g[0][0] = 4
        g[7][7] = 6
        return g
    return g
