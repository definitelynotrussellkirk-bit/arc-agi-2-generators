"""Generator for arc_puzzle_bank_twelfth21:E79.

Rule: each blank center with four same-color diagonal arms is filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, diamonds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_diamonds, partial_diagonals, mismatched_diagonals.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ee5295e1813b"
VERSION = "1.1.0"
TASK_ID = "ee5295e1813b"

SUMMARY = "Same-color diagonal diamond arms fill their empty center."

INVARIANTS = [
    "background is 0",
    "diamond centers are zero in the input",
    "all four diagonal neighbors around a center share one nonzero color",
    "diamond patterns are spaced apart",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_diamonds", "partial_diagonals", "mismatched_diagonals")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "diamonds":       {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_diamonds",
                       "valid": "spaced_diamonds"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _far(center, centers):
    r, c = center
    return all(max(abs(r - rr), abs(c - cc)) >= 3 for rr, cc in centers)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("diamonds", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("diamonds", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("diamonds", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    centers = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(centers)
    used = []
    for r, c in centers:
        if len(used) >= target:
            break
        if not _far((r, c), used):
            continue
        used.append((r, c))
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            g[r + dr][c + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_diamonds":
        # blank → no diamond corners, rule has no centers to fill
        return g
    if name == "partial_diagonals":
        # 3 of 4 diagonals → predicate fails
        g[2][2] = 4; g[2][4] = 4; g[4][2] = 4
        g[5][6] = 6; g[5][8] = 6; g[7][8] = 6
        return g
    if name == "mismatched_diagonals":
        # 4 diagonals in different colors → predicate fails
        g[2][2] = 4; g[2][4] = 6; g[4][2] = 3; g[4][4] = 8
        return g
    return g
