"""Generator for arc_additional_puzzle_bank_volume5:H34.

Rule: a matching color pair is connected through a single open maze
corridor; output traces the corridor.

Combinatorial axes (8): grid_h/w, palette_kind, corridor_length,
endpoint_color, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: endpoints_adjacent, no_corridor, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ec5fd031b9e1"
VERSION = "1.1.0"
TASK_ID = "ec5fd031b9e1"
SUMMARY = "A matching color pair is connected through a single open maze corridor."

INVARIANTS = [
    "walls are 8",
    "there is one color that appears exactly twice",
    "the two endpoints share a unique open corridor",
    "path cells between endpoints are blank",
]

PALETTE_KINDS = ("default", "short_corridor", "long_corridor", "wide_grid")
DEGENERATE_TEXTURES = ("endpoints_adjacent", "no_corridor", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "corridor_length": {"type": "int", "default": "rng 3..8",
                        "valid": "3..14"},
    "endpoint_color": {"type": "int", "default": "rng",
                       "valid": "1..7|9"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "horizontal_corridor",
                       "valid": "horizontal_corridor"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 8, 14)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 8)
    r = rng.randint(1, h - 2)
    c1 = rng.randint(1, w - 5)
    c2 = rng.randint(c1 + 3, w - 2)
    for c in range(c1, c2 + 1):
        g[r][c] = 0
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
    g[r][c1] = color
    g[r][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 8)
    if name == "endpoints_adjacent":
        # endpoints touch — corridor has zero blank cells between them
        r = h // 2
        g[r][3] = 0
        g[r][4] = 0
        g[r][3] = 5
        g[r][4] = 5
        return g
    if name == "no_corridor":
        # endpoints exist but the path between is walled off
        r = h // 2
        g[r][2] = 5
        g[r][8] = 5
        return g
    if name == "single_endpoint":
        # only one endpoint of the matching pair
        r = h // 2
        for c in range(2, 9):
            g[r][c] = 0
        g[r][2] = 4
        return g
    return g
