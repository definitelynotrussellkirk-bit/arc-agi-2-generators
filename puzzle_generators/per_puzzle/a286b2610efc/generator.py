"""Generator for arc_puzzle_bank_fourteenth21:E94.

Combinatorial axes (8): grid_h, grid_w, palette_kind, dominoes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dominoes, dominoes_touching, no_extension_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a286b2610efc"
VERSION = "1.1.0"
TASK_ID = "a286b2610efc"

SUMMARY = "Place isolated adjacent dominoes with one empty extension cell."

INVARIANTS = [
    "background is 0",
    "each motif is a same-color horizontal or vertical adjacent pair",
    "one side of the pair has an empty extension cell",
    "motifs are separated so triplet completions do not interact",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dominoes", "dominoes_touching", "no_extension_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "dominoes":       {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "scattered_isolated",
                       "valid": "scattered_isolated"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("dominoes", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        target = ctx.draw_int("dominoes", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        target = ctx.draw_int("dominoes", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(400):
        if placed >= target:
            break
        horizontal = rng.randrange(2) == 0
        if horizontal:
            r = rng.randrange(h)
            c = rng.randint(0, w - 3)
            cells = [(r, c), (r, c + 1)]
            footprint = {(r, c), (r, c + 1), (r, c + 2)}
        else:
            r = rng.randint(0, h - 3)
            c = rng.randrange(w)
            cells = [(r, c), (r + 1, c)]
            footprint = {(r, c), (r + 1, c), (r + 2, c)}
        guard = {(rr, cc) for r0, c0 in footprint for rr in range(max(0, r0 - 1), min(h, r0 + 2))
                 for cc in range(max(0, c0 - 1), min(w, c0 + 2))}
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r, c in cells:
            g[r][c] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_dominoes":
        # Lone cells, no adjacent pairs — rule has no dominoes to extend.
        g[2][2] = 3; g[5][6] = 4
        return g
    if name == "dominoes_touching":
        # Two dominoes adjacent — extension cells overlap, ambiguous output.
        g[2][2] = 3; g[2][3] = 3
        g[2][5] = 4; g[2][6] = 4
        return g
    if name == "no_extension_room":
        # Domino flush against grid edge — no room to extend in either direction.
        g[0][0] = 3; g[0][1] = 3
        return g
    return g
