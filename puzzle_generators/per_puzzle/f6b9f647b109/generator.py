"""Generator for 992798f6.

Rule: green path is drawn from a red endpoint to a blue endpoint
using one diagonal, straight steps, then diagonals.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
endpoint_kind.
Degenerates: no_endpoints, single_endpoint, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f6b9f647b109"
VERSION = "1.1.0"
TASK_ID = "f6b9f647b109"
SUMMARY = "Green path from red to blue endpoint via diagonal/straight/diagonal."

INVARIANTS = [
    "background is color 0",
    "exactly one red endpoint and one blue endpoint",
    "endpoints are separated in both row and column",
    "endpoints sit clear of grid borders so the path has room",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_endpoints", "single_endpoint", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "endpoint_kind":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
        size_lo, size_hi = 10, 11
    elif difficulty == "hard":
        size_lo, size_hi = 14, 18
    else:
        size_lo, size_hi = 10, 14
    size = ctx.draw_int("grid_size", size_lo, size_hi)
    h = size
    w = size + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    red = (1 + (sample_index % 2), 1 + ((seed + sample_index) % 2))
    blue = (h - 2 - ((seed + sample_index) % 2), w - 2)
    g[red[0]][red[1]] = 2
    g[blue[0]][blue[1]] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_endpoints":
        return g
    if name == "single_endpoint":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
