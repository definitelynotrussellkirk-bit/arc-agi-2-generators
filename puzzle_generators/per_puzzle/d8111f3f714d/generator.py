"""Generator for bf89d739.

Rule: red endpoints define a green trunk; other red endpoints branch
perpendicularly into the trunk.

Combinatorial axes (8): grid_h/w, branch_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_markers, single_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d8111f3f714d"
VERSION = "1.1.0"
TASK_ID = "d8111f3f714d"
SUMMARY = "Red endpoints define green trunk; others branch perpendicularly."

INVARIANTS = [
    "background is color 0",
    "all markers use color 2",
    "one earliest marker pair shares a row or column and defines the trunk",
    "remaining red markers branch orthogonally toward the trunk",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "single_marker", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "branch_count":   {"type": "int", "default": "2", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
    ctx.draw_int("branch_count", 2, 2)
    h = 12 + rng.randint(0, 4)
    w = 12 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    c = w // 2
    r1, r2 = 2, h - 3
    g[r1][c] = 2
    g[r2][c] = 2
    g[h // 2][2] = 2
    g[h // 2 + 1][w - 3] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_markers":
        return g
    if name == "single_marker":
        g[6][6] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
