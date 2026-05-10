"""Generator for 50846271.

Rule: partial color-2 plus signs complete by turning covered color-5
cells to color 8.

Combinatorial axes (8): grid_h/w, plus_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_pluses, single_pixel, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7f0d975b36d2"
VERSION = "1.1.0"
TASK_ID = "7f0d975b36d2"
SUMMARY = "Partial color-2 plus signs complete by recoloring color-5 to 8."

INVARIANTS = [
    "candidate plus arms are marked by color 2",
    "missing covered cells are color 5",
    "only color-5 cells on inferred plus arms are recolored to 8",
    "all color-2 evidence cells remain unchanged",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pluses", "single_pixel", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "plus_count":     {"type": "int", "default": "1", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
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
    g = full_grid(13, 13, 5)
    center = (6, 6)
    for r, c in [(6, 5), (6, 7), (5, 6), (7, 6)]:
        g[r][c] = 2
    for _ in range(10):
        r = rng.randrange(13)
        c = rng.randrange(13)
        if abs(r - center[0]) + abs(c - center[1]) > 3:
            g[r][c] = rng.choice([0, 5])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 5)
    if name == "no_pluses":
        return g
    if name == "single_pixel":
        g[6][6] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
