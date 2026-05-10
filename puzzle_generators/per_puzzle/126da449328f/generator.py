"""Generator for arc_puzzle_bank_21_set13_bundle:easy_m04.

Rule: each seed extends in the direction of its uniquely nearest border.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, seed_at_center, seed_equidistant.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "126da449328f"
VERSION = "1.1.0"
TASK_ID = "126da449328f"
SUMMARY = "Colored singleton seeds with unique nearest grid borders."

INVARIANTS = [
    "background is 0",
    "all nonzero cells are singleton seeds",
    "each seed has a unique nearest border",
    "projected rays do not cross another seed",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "seed_at_center", "seed_equidistant")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "seed_count":     {"type": "int", "default": "rng 3..5", "valid": "1..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "scattered_seeds",
                       "valid": "scattered_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _nearest_is_unique(h, w, r, c):
    ds = [r, h - 1 - r, c, w - 1 - c]
    return ds.count(min(ds)) == 1


def _ray_cells(h, w, r, c):
    ds = [r, h - 1 - r, c, w - 1 - c]
    idx = ds.index(min(ds))
    if idx == 0:
        return [(rr, c) for rr in range(0, r + 1)]
    if idx == 1:
        return [(rr, c) for rr in range(r, h)]
    if idx == 2:
        return [(r, cc) for cc in range(0, c + 1)]
    return [(r, cc) for cc in range(c, w)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        seed_count = ctx.draw_int("seed_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
        seed_count = ctx.draw_int("seed_count", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        seed_count = ctx.draw_int("seed_count", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=seed_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    rays = []
    placed = 0
    for color in colors:
        for _ in range(300):
            r = rng.randrange(h)
            c = rng.randrange(w)
            ray = _ray_cells(h, w, r, c)
            if (
                g[r][c] == 0
                and _nearest_is_unique(h, w, r, c)
                and all(not (set(ray) & set(prev)) for prev in rays)
            ):
                g[r][c] = color
                rays.append(ray)
                placed += 1
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # Empty grid — rule has no seeds to extend.
        return g
    if name == "seed_at_center":
        # Seed exactly equidistant from all 4 borders — rule's
        # "unique nearest border" precondition fails; ray direction
        # is undefined.
        g[4][4] = 4
        return g
    if name == "seed_equidistant":
        # Seed equidistant from 2 borders (corner-equidistant) —
        # rule's tie-break is ambiguous.
        g[2][2] = 4
        return g
    return g
