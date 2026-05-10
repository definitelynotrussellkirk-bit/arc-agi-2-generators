"""Generator for puzzle b0c4d837.

Rule: 2 vertical 5-pillars; count fully-empty rows between them.
Output 3x3 grid with first N spiral positions = 8.

Combinatorial axes (8): grid_h/w, c1, c2, pillar_h_min, pillar_h_max,
position_bias, anchor_corner, asymmetry_force.
Degenerates: no_pillars, single_pillar, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c1ae510562f9"
VERSION = "1.1.0"
TASK_ID = "c1ae510562f9"
SUMMARY = "2 vertical 5-pillars; rule outputs 3x3 spiral by empty-row count."

INVARIANTS = [
    "background is 0",
    "exactly 2 vertical 5-pillars at distinct cols",
    ">=1 empty row in middle col range",
    "pillar heights >=2",
]

POSITION_BIASES = ("balanced", "left_heavy", "right_heavy", "tall_short",
                   "centered")
DEGENERATE_TEXTURES = ("no_pillars", "single_pillar", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "6..14"},
    "pillar_h_min":   {"type": "int", "default": "2", "valid": "2..6"},
    "pillar_h_max":   {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "c1":             {"type": "int", "default": "rng 1..2",
                       "valid": "0..w/2"},
    "c2":             {"type": "int", "default": "rng w-3..w-2",
                       "valid": "w/2..w-1"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 11, 16
    else:
        h_lo, h_hi = 6, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    h_min = int(overrides.get("pillar_h_min", 2))
    h_max = int(overrides.get("pillar_h_max",
                              ctx.draw_int("pillar_h_max", 4, 6)))
    h_min = max(2, min(h - 1, h_min))
    h_max = max(h_min, min(h - 1, h_max))
    c1 = int(overrides.get("c1", rng.randint(1, max(1, w // 2 - 1))))
    c2 = int(overrides.get("c2", rng.randint(w // 2, max(w // 2, w - 2))))
    if c1 == c2:
        c2 = (c1 + 2) % w
    g = full_grid(h, w, 0)
    if bias == "tall_short":
        h1 = h_max
        h2 = h_min
    elif bias == "left_heavy":
        h1 = h_max
        h2 = h_min
    elif bias == "right_heavy":
        h1 = h_min
        h2 = h_max
    elif bias == "centered":
        h1 = (h_min + h_max) // 2
        h2 = (h_min + h_max) // 2 + 1
    else:
        h1 = rng.randint(h_min, h_max)
        h2 = rng.randint(h_min, h_max)
    h1 = max(2, min(h - 1, h1))
    h2 = max(2, min(h - 1, h2))
    r0_1 = rng.randint(0, h - h1)
    r0_2 = rng.randint(0, h - h2)
    for i in range(h1):
        g[r0_1 + i][c1] = 5
    for i in range(h2):
        g[r0_2 + i][c2] = 5
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_pillars":
        return g
    if name == "single_pillar":
        for r in range(h):
            g[r][w // 2] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
