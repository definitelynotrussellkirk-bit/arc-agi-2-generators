"""Generator for additional_scaffolded:E2 — color-3 beacons paint diagonal halos.

Rule: color-3 beacon cells paint their diagonal neighbors with color 7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_beacons,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_beacons, beacons_at_corner, multi_cell_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f819e4f14fa6"
VERSION = "1.1.0"
TASK_ID = "f819e4f14fa6"
SUMMARY = "Color-3 beacon cells paint their diagonal neighbors with color 7."

INVARIANTS = [
    "background is 0",
    "input contains isolated color-3 beacon cells",
    "at least one beacon is interior and at least one may be near an edge",
    "beacons are spaced enough that their halos remain readable",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_beacons", "beacons_at_corner", "multi_cell_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..11", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 6..11", "valid": "3..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_beacons":      {"type": "int", "default": "rng 3..7", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_color3_singletons",
                       "valid": "spaced_color3_singletons"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
        n_beacons = ctx.draw_int("n_beacons", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_beacons = ctx.draw_int("n_beacons", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 6, 11)
        w = ctx.draw_int("grid_w", 6, 11)
        n_beacons = ctx.draw_int("n_beacons", 3, 7)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    cells: list[tuple[int, int]] = [(rng.randint(1, h - 2), rng.randint(1, w - 2))]
    for _ in range(160):
        if len(cells) >= n_beacons:
            break
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        if (r, c) in cells:
            continue
        if any(abs(r - rr) <= 1 and abs(c - cc) <= 1 for rr, cc in cells):
            continue
        cells.append((r, c))
    for r, c in cells:
        g[r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_beacons":
        # blank → no halos to paint
        return g
    if name == "beacons_at_corner":
        # beacons at corners → 3 of 4 diagonal neighbors are out of bounds
        g[0][0] = 3
        g[h - 1][w - 1] = 3
        return g
    if name == "multi_cell_blobs":
        # 3-color cells form blobs (not isolated singletons) → halos overlap/merge
        g[2][2] = 3; g[2][3] = 3   # adjacent
        g[5][5] = 3; g[6][5] = 3
        return g
    return g
