"""Generator for arc_puzzle_bank_twelfth_21_bundle:easy_83_complete_l_trominoes_to_2x2.

Rule: each L-tromino in a 2x2 box is completed to a solid 2x2 block.

Combinatorial axes (8): grid_h, grid_w, palette_kind, objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_trominoes, already_solid, trominoes_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "68e9f92d8e4b"
VERSION = "1.1.0"
TASK_ID = "68e9f92d8e4b"

SUMMARY = "Three-cell L trominoes inside 2x2 boxes are completed to solid blocks."

INVARIANTS = [
    "background is 0",
    "every component is a three-cell L in a 2x2 box",
    "components are separated",
    "each component is monochrome",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_trominoes", "already_solid", "trominoes_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "objects":        {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_l_trominoes",
                       "valid": "spaced_l_trominoes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free_box(g, r, c):
    h, w = len(g), len(g[0])
    for rr in range(max(0, r - 1), min(h, r + 3)):
        for cc in range(max(0, c - 1), min(w, c + 3)):
            if g[rr][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("objects", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        target = ctx.draw_int("objects", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 8, 12)
        target = ctx.draw_int("objects", 2, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(160):
        if placed >= target:
            break
        r, c = rng.randint(0, h - 2), rng.randint(0, w - 2)
        if not _free_box(g, r, c):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        missing = rng.choice([(0, 0), (0, 1), (1, 0), (1, 1)])
        for dr in (0, 1):
            for dc in (0, 1):
                if (dr, dc) != missing:
                    g[r + dr][c + dc] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_trominoes":
        # blank → no L shapes, rule has no effect
        return g
    if name == "already_solid":
        # solid 2x2 blocks (no missing corner) → predicate "L tromino" fails
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 4
        for r in range(2):
            for c in range(2): g[5 + r][5 + c] = 6
        return g
    if name == "trominoes_touching":
        # adjacent trominoes → fused into larger object, predicate "in 2x2 box" fails
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[2][2] = 4; g[2][3] = 4; g[3][3] = 4  # touches first
        return g
    return g
