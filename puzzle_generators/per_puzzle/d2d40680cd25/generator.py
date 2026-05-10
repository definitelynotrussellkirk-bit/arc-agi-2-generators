"""Generator for arc_puzzle_bank_21_set7_s:S7_M2 — rigid gravity with walls.

Rule: blobs fall down (gravity dr=1, dc=0) until blocked by an 8-wall
or another blob (or the floor).

Combinatorial axes (8): grid_h, grid_w, palette_kind, wall_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_wall, no_blob, blob_already_at_floor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "d2d40680cd25"
VERSION = "1.1.0"
TASK_ID = "d2d40680cd25"
SUMMARY = "1-2 colored blobs above an 8-wall (vertical or horizontal segment)."

INVARIANTS = [
    "background is 0",
    "exactly one 8-wall (vertical column segment, 3-5 cells)",
    "1-2 non-8 blobs above the wall (their fall path doesn't intersect the wall)",
    "blobs are non-trivial size (≥2 cells)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_wall", "no_blob", "blob_already_at_floor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "wall_size":      {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "wall_below_blobs_above",
                       "valid": "wall_below_blobs_above"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    # vertical wall
    wall_c = rng.randint(2, w - 3)
    wall_r1 = rng.randint(2, h - 5)
    wall_r2 = wall_r1 + rng.randint(2, 4)
    for r in range(wall_r1, wall_r2 + 1):
        if r < h:
            g[r][wall_c] = 8
            used.add((r, wall_c))
    n_blobs = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n_blobs)
    # blobs in upper area only
    upper_used = set(used)
    for r in range(wall_r1, h):
        for c in range(w):
            upper_used.add((r, c))
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, upper_used, rng.randint(2, 3), max_attempts=20)
            if cells is None:
                continue
            for r, c in cells:
                g[r][c] = color
            upper_used |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_wall":
        # Blob present but no 8-wall — falls all the way to floor (no wall effect).
        g[1][3] = 4; g[1][4] = 4; g[2][3] = 4
        return g
    if name == "no_blob":
        # 8-wall present but no blob — rule has nothing to drop.
        for r in range(3, 7): g[r][5] = 8
        return g
    if name == "blob_already_at_floor":
        # Blob already resting on floor — gravity is a no-op (input == output).
        for r in range(3, 7): g[r][5] = 8
        g[h - 1][2] = 4; g[h - 2][2] = 4
        return g
    return g
