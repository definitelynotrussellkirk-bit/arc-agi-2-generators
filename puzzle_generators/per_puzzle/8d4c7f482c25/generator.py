"""Generator for arc_puzzle_bank_21_set17_bundle:easy_p01.

Seven cells of a 3x3 ring are present; the missing ring cell is completed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ring_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rings, complete_rings, two_holes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8d4c7f482c25"
VERSION = "1.1.0"
TASK_ID = "8d4c7f482c25"
SUMMARY = "Separated one-hole 3x3 rings with zero centers."

INVARIANTS = [
    "background is 0",
    "each motif is a 3x3 ring with exactly one missing ring cell",
    "ring centers are zero",
    "ring neighborhoods are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rings", "complete_rings", "two_holes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ring_count":     {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "one_hole_3x3_rings",
                       "valid": "one_hole_3x3_rings"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


RING = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]


def _zone(r, c):
    return {(rr, cc) for rr in range(r - 1, r + 4) for cc in range(c - 1, c + 4)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        ring_count = ctx.draw_int("ring_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        ring_count = ctx.draw_int("ring_count", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 12)
        ring_count = ctx.draw_int("ring_count", 2, 3)
    colors = ctx.draw_distinct_colors("colors", n=ring_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    occupied = set()
    for color in colors:
        for _ in range(300):
            r = rng.randint(0, h - 3)
            c = rng.randint(0, w - 3)
            zone = _zone(r, c)
            if zone & occupied:
                continue
            missing = rng.randrange(len(RING))
            for i, (dr, dc) in enumerate(RING):
                if i != missing:
                    g[r + dr][c + dc] = color
            occupied |= zone
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_rings":
        # blank → no 3x3 rings to complete
        return g
    if name == "complete_rings":
        # rings already complete → no hole to fill, identity
        for dr, dc in RING:
            g[1 + dr][1 + dc] = 4
            g[5 + dr][5 + dc] = 6
        return g
    if name == "two_holes":
        # two missing cells per ring → ambiguous which to complete
        for i, (dr, dc) in enumerate(RING):
            if i not in (0, 4):
                g[1 + dr][1 + dc] = 4
        return g
    return g
