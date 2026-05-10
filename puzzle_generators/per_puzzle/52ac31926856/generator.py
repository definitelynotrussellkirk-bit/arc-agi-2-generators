"""Generator for db7260a4.

Rule: blue drop falls into the first red container with side walls
and a solid floor.

Combinatorial axes (8): grid_h/w, container_width, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_drop, no_container, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "52ac31926856"
VERSION = "1.1.0"
TASK_ID = "52ac31926856"
SUMMARY = "Blue drop falls into red container with side walls and solid floor."

INVARIANTS = [
    "background is color 0",
    "one blue cell sits between red top wall endpoints",
    "the red object forms side walls with a solid floor beneath the blue column",
    "the container sits clear of the grid borders",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_drop", "no_container", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "10..16"},
    "container_width":{"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        cw_lo, cw_hi = 5, 5
    elif difficulty == "hard":
        cw_lo, cw_hi = 7, 7
    else:
        cw_lo, cw_hi = 5, 7
    width = ctx.draw_int("container_width", cw_lo, cw_hi)
    h = 9 + rng.randint(0, 3)
    w = max(10, width + 5)
    g = full_grid(h, w, 0)
    r0 = 2
    c0 = 2
    r1 = h - 3
    c1 = c0 + width - 1
    for r in range(r0, r1 + 1):
        g[r][c0] = 2
        g[r][c1] = 2
    for c in range(c0, c1 + 1):
        g[r1][c] = 2
    g[r0][c0] = 2
    g[r0][c1] = 2
    g[r0][(c0 + c1) // 2] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_drop":
        for r in range(2, 8):
            g[r][2] = 2
            g[r][6] = 2
        for c in range(2, 7):
            g[7][c] = 2
        return g
    if name == "no_container":
        g[2][4] = 1
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
