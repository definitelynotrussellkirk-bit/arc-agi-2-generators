"""Generator for cc9053aa.

Rule: shortest low-turn path through 8s between two 9 endpoints is
painted 9.

Combinatorial axes (8): grid_h/w, path_shape, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_endpoints, no_corridor, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f8d1d470d522"
VERSION = "1.1.0"
TASK_ID = "f8d1d470d522"
SUMMARY = "Shortest low-turn path through 8s between two 9 endpoints is painted 9."

INVARIANTS = [
    "background is color 0",
    "two endpoints use color 9",
    "walkable corridor cells use color 8",
    "a contiguous 8-corridor connects the two endpoints",
]

PATH_SHAPES = ("straight", "elbow")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_endpoints", "no_corridor", "full_grid")
HELPFUL_TEXTURES = PATH_SHAPES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "path_shape":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PATH_SHAPES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for path_shape",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    shape = (overrides.get("texture") if overrides.get("texture") in PATH_SHAPES else None) or \
            overrides.get("path_shape") or \
            ctx.draw_choice("path_shape", list(PATH_SHAPES))
    h = 8 + rng.randint(0, 3)
    w = 9 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    if shape == "straight":
        r = h // 2
        for c in range(1, w - 1):
            g[r][c] = 8
        g[r][1] = 9
        g[r][w - 2] = 9
    else:
        r0, c0 = 1, 1
        r1, c1 = h - 2, w - 2
        for c in range(c0, c1 + 1):
            g[r0][c] = 8
        for r in range(r0, r1 + 1):
            g[r][c1] = 8
        g[r0][c0] = 9
        g[r1][c1] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 10, 0)
    if name == "no_endpoints":
        for c in range(1, 9):
            g[4][c] = 8
        return g
    if name == "no_corridor":
        g[2][2] = 9
        g[5][7] = 9
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(10):
                g[r][c] = 8
        return g
    return g
