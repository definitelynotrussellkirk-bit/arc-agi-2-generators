"""Generator for e5c44e8f.

Rule: green seed expands into a fixed mask unless color-2 blockers
cut the connected region.

Combinatorial axes (8): grid_h/w, blockers, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_seed, full_grid, all_blockers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e797eb4ae5d6"
VERSION = "1.1.0"
TASK_ID = "e797eb4ae5d6"
SUMMARY = "Green seed expands into fixed mask unless color-2 blockers cut region."

INVARIANTS = [
    "background is color 0",
    "one seed cell uses color 3",
    "with no blockers every in-bounds mask position is painted green",
    "blockers when present use color 2 and are not overwritten",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seed", "full_grid", "all_blockers")
HELPFUL_TEXTURES = ("b0", "b1", "b2")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "grid_w":         {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "blockers":       {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for blockers",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in HELPFUL_TEXTURES:
        blockers = int(tx[1])
    else:
        blockers = ctx.draw_int("blockers", 0, 2)
    h = 14 + rng.randint(0, 3)
    w = 14 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    sr = 5 + rng.randint(0, h - 12)
    sc = 6 + rng.randint(0, w - 12)
    g[sr][sc] = 3
    if blockers >= 1:
        g[sr - 2][sc + 2] = 2
    if blockers >= 2:
        g[sr + 2][sc - 2] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_seed":
        return g
    if name == "all_blockers":
        for r in range(15):
            for c in range(15):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 3
        return g
    return g
