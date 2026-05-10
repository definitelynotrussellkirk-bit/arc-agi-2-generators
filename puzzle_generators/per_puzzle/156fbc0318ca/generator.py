"""Generator for c35c1b4c.

Rule: local repair trigger for noisy convex blobs; one 3x3 patch
appears inside a small padded grid.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, patch_kind, n_distinct_colors.
Degenerates: no_patch, full_grid, single_pixel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paste

GENERATOR_ID = "156fbc0318ca"
VERSION = "1.1.0"
TASK_ID = "156fbc0318ca"
SUMMARY = "Radius-1 noisy-blob neighborhood inside a small padded grid."

INVARIANTS = [
    "background is 0",
    "one 3x3 neighborhood matches a known local repair context",
    "the patch sits with at least one row of bg margin from the border",
    "the patch contains a center cell to be repaired",
]

PATCH_KINDS = ("p0", "p1", "p2", "p3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_patch", "full_grid", "single_pixel")
HELPFUL_TEXTURES = PATCH_KINDS

_PATCHES = [
    [[3, 3, 3], [3, 0, 0], [3, 0, 0]],
    [[1, 0, 0], [1, 0, 0], [1, 6, 0]],
    [[2, 2, 2], [2, 0, 0], [2, 2, 1]],
    [[9, 9, 9], [9, 0, 9], [9, 9, 6]],
]

AXES = {
    "grid_size":      {"type": "int", "default": "rng 5..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "patch_kind":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PATCH_KINDS)},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for patch_kind",
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
        size_lo, size_hi = 5, 6
    elif difficulty == "hard":
        size_lo, size_hi = 8, 11
    else:
        size_lo, size_hi = 5, 8
    size = ctx.draw_int("grid_size", size_lo, size_hi)
    tx = overrides.get("texture")
    if tx in PATCH_KINDS:
        idx = int(tx[1])
        patch = [row[:] for row in _PATCHES[idx]]
    else:
        patch = [row[:] for row in rng.choice(_PATCHES)]
    g = full_grid(size, size, 0)
    r0 = rng.randint(1, size - 4)
    c0 = rng.randint(1, size - 4)
    paste(g, patch, r0, c0)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 6, 0)
    if name == "no_patch":
        return g
    if name == "single_pixel":
        g[3][3] = 2
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(6):
                g[r][c] = 2
        return g
    return g
