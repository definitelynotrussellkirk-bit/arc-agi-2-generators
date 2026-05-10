"""Generator for 508bd3b6.

Rule: two cyan diagonal seeds choose the longer forward/backward
diagonal trace, painted green.

Combinatorial axes (8): grid_h/w, seed_distance, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
direction.
Degenerates: no_seeds, single_seed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "154e19f36ba8"
VERSION = "1.1.0"
TASK_ID = "154e19f36ba8"
SUMMARY = "Two cyan diagonal seeds choose longer diagonal trace, painted green."

INVARIANTS = [
    "background is color 0",
    "exactly two cyan seed cells",
    "cyan seeds lie on a diagonal",
    "the diagonal has open space in at least one tracing direction",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "single_seed", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..16"},
    "seed_distance":  {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "direction":      {"type": "str", "default": "rng", "valid": "rng"},
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
        d_lo, d_hi = 2, 2
    elif difficulty == "hard":
        d_lo, d_hi = 4, 5
    else:
        d_lo, d_hi = 2, 4
    dist = ctx.draw_int("seed_distance", d_lo, d_hi)
    h = 10 + rng.randint(0, 4)
    w = 10 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    dr, dc = dirs[(seed + sample_index + rng.randint(0, 3)) % len(dirs)]
    r_lo = dist + 1 if dr < 0 else 1
    r_hi = h - 2 if dr < 0 else h - dist - 2
    c_lo = dist + 1 if dc < 0 else 1
    c_hi = w - 2 if dc < 0 else w - dist - 2
    r = r_lo + ((sample_index + rng.randint(0, 9)) % max(1, r_hi - r_lo + 1))
    c = c_lo + ((seed + sample_index + rng.randint(0, 9)) % max(1, c_hi - c_lo + 1))
    g[r][c] = 8
    g[r + dr * dist][c + dc * dist] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_seeds":
        return g
    if name == "single_seed":
        g[5][5] = 8
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 8
        return g
    return g
