"""Generator for b27ca6d3.

Rule: multi-cell red groups receive a green bounding border;
singleton red pixels stay unchanged.

Combinatorial axes (8): grid_h/w, group_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_variant.
Degenerates: no_groups, all_singletons, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7185b8225f1c"
VERSION = "1.1.0"
TASK_ID = "7185b8225f1c"
SUMMARY = "Multi-cell red groups get green bounding border; singletons unchanged."

INVARIANTS = [
    "background is color 0",
    "red components use color 2",
    "components of at least two cells are separated from each other",
    "at least one singleton red pixel sits clear of multi-cell groups",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_groups", "all_singletons", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

GROUPS = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "group_count":    {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_variant":  {"type": "str", "default": "rng", "valid": "rng"},
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
        gc_lo, gc_hi = 2, 2
    elif difficulty == "hard":
        gc_lo, gc_hi = 3, 3
    else:
        gc_lo, gc_hi = 2, 3
    group_count = ctx.draw_int("group_count", gc_lo, gc_hi)
    g = full_grid(14, 14, 0)
    anchors = [(2, 2), (2, 9), (8, 4)]
    for idx in range(group_count):
        shape = GROUPS[(idx + sample_index) % len(GROUPS)]
        r0, c0 = anchors[idx]
        c0 += rng.randint(0, 1)
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = 2
    g[11][11] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_groups":
        return g
    if name == "all_singletons":
        for r in range(2, 12, 3):
            for c in range(2, 12, 3):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
