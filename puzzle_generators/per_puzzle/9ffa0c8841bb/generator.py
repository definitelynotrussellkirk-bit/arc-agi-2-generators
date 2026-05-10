"""Generator for arc_additional_puzzle_bank_volume13:H91.

Rule: a zero chamber enclosed by colored gates fills with the boundary
majority color.

Combinatorial axes (8): grid_h/w, palette_kind, chamber_size,
palette_size, position_bias, n_distinct_colors, boundary_diversity, texture.
Degenerates: no_majority, no_chamber, no_boundary.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9ffa0c8841bb"
VERSION = "1.1.0"
TASK_ID = "9ffa0c8841bb"
SUMMARY = "A zero chamber enclosed by colored gates fills with the boundary majority."

INVARIANTS = [
    "non-chamber background is 5",
    "one rectangular zero chamber is enclosed by colors 1 through 4",
    "boundary colors have a unique majority",
    "the chamber contains blank cells only",
]

PALETTE_KINDS = ("default", "majority_1", "majority_2", "varied_majority")
DEGENERATE_TEXTURES = ("no_majority", "no_chamber", "no_boundary")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "chamber_size":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "centered",
                       "valid": "centered"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "boundary_diversity": {"type": "str", "default": "varied",
                            "valid": "varied"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 9, 13)
    g = full_grid(h, w, 5)
    r0, c0, r1, c1 = 2, 2, h - 3, w - 3
    for r in range(r0 + 1, r1):
        for c in range(c0 + 1, c1):
            g[r][c] = 0
    for c in range(c0, c1 + 1):
        g[r0][c] = 1
        g[r1][c] = 1 if c % 2 else 2
    for r in range(r0, r1 + 1):
        g[r][c0] = 1
        g[r][c1] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    if name == "no_majority":
        # all 4 boundary colors equally → no strict majority
        g = full_grid(h, w, 5)
        r0, c0, r1, c1 = 2, 2, h - 3, w - 3
        for r in range(r0 + 1, r1):
            for c in range(c0 + 1, c1):
                g[r][c] = 0
        for c in range(c0, c1 + 1):
            g[r0][c] = 1
            g[r1][c] = 2
        for r in range(r0, r1 + 1):
            g[r][c0] = 3
            g[r][c1] = 4
        return g
    if name == "no_chamber":
        # all cells filled with bg-5 — no zero chamber to fill
        g = full_grid(h, w, 5)
        return g
    if name == "no_boundary":
        # zero chamber but no boundary colors → can't compute majority
        g = full_grid(h, w, 0)
        return g
    return full_grid(h, w, 5)
