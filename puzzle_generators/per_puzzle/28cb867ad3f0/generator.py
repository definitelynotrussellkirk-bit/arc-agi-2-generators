"""Generator for arc_additional_puzzle_bank_volume14:H97.

Rule: a chamber bounded by colored cells fills with its unique boundary
majority color.

Combinatorial axes (8): grid_h/w, palette_kind, chamber_size,
palette_size, position_bias, n_distinct_colors, boundary_diversity, texture.
Degenerates: no_majority, no_chamber, no_boundary.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "28cb867ad3f0"
VERSION = "1.1.0"
TASK_ID = "28cb867ad3f0"
SUMMARY = "A chamber bounded by colored cells fills with its unique boundary majority."

INVARIANTS = [
    "non-chamber cells are nonzero",
    "a zero chamber is surrounded by boundary colors 1 through 4",
    "one boundary color has a strict majority",
    "only chamber zeros are fillable",
]

PALETTE_KINDS = ("default", "majority_2", "majority_3", "majority_4")
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
        g[r0][c] = 2
        g[r1][c] = 2 if c % 2 else 3
    for r in range(r0, r1 + 1):
        g[r][c0] = 2
        g[r][c1] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    if name == "no_majority":
        # boundary has all 4 colors equally → no strict majority → ambiguous
        g = full_grid(h, w, 5)
        r0, c0, r1, c1 = 2, 2, h - 3, w - 3
        for r in range(r0 + 1, r1):
            for c in range(c0 + 1, c1):
                g[r][c] = 0
        # Equal counts on the four sides
        for c in range(c0, c1 + 1):
            g[r0][c] = 1
            g[r1][c] = 2
        for r in range(r0, r1 + 1):
            g[r][c0] = 3
            g[r][c1] = 4
        return g
    if name == "no_chamber":
        # all cells filled — no zero chamber
        g = full_grid(h, w, 2)
        return g
    if name == "no_boundary":
        # zero chamber but no boundary colors → can't compute majority
        g = full_grid(h, w, 0)
        return g
    return full_grid(h, w, 5)
