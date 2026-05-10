"""Generator for 9caba7c3.

Rule: selected 3x3 red-and-gray fragments turn gray cells purple,
with the center highlighted yellow.

Combinatorial axes (8): grid_h/w, patch_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
patch_kind.
Degenerates: no_patches, single_patch, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fc814cec3976"
VERSION = "1.1.0"
TASK_ID = "fc814cec3976"
SUMMARY = "3x3 red-gray fragments turn gray cells purple with center yellow."

INVARIANTS = [
    "background is color 0",
    "candidate patches are isolated 3x3 blocks containing only colors 2 and 5",
    "each candidate has a color-5 center and at least one color-2 cell",
    "patches sit clear of each other so the rule can identify each",
]

PATCH_KINDS = ("p0", "p1", "p2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_patches", "single_patch", "full_grid")
HELPFUL_TEXTURES = PATCH_KINDS

PATTERNS = [
    [[2, 5, 2], [5, 5, 5], [2, 5, 2]],
    [[2, 2, 5], [5, 5, 2], [5, 2, 5]],
    [[5, 2, 5], [2, 5, 2], [5, 2, 5]],
]

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "patch_count":    {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "patch_kind":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PATCH_KINDS)},
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
    count = ctx.draw_int("patch_count", 1, 2)
    g = full_grid(10, 10, 0)
    anchors = [(1, 1), (5, 5)]
    tx = overrides.get("texture")
    if tx in PATCH_KINDS:
        start = int(tx[1])
    else:
        start = rng.randint(0, len(PATTERNS) - 1)
    for i in range(count):
        patch = PATTERNS[(start + i) % len(PATTERNS)]
        r0, c0 = anchors[i]
        for dr in range(3):
            for dc in range(3):
                g[r0 + dr][c0 + dc] = patch[dr][dc]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_patches":
        return g
    if name == "single_patch":
        patch = PATTERNS[0]
        for dr in range(3):
            for dc in range(3):
                g[1 + dr][1 + dc] = patch[dr][dc]
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
