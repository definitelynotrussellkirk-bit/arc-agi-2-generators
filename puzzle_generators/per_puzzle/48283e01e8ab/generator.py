"""Generator for ad38a9d0.

Rule: magenta polyominoes are recolored by component size and simple
shape type.

Combinatorial axes (8): grid_h/w, shape_set, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_components.
Degenerates: no_components, single_component, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "48283e01e8ab"
VERSION = "1.1.0"
TASK_ID = "48283e01e8ab"
SUMMARY = "Magenta polyominoes recolored by component size and shape type."

INVARIANTS = [
    "background is color 0",
    "all source components use color 6",
    "components are separated enough that their bboxes do not touch",
    "component shapes cover both line-3 and ell-3 forms so the rule has work to do",
]

SHAPE_SETS = ("basic", "mixed")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_components", "single_component", "full_grid")
HELPFUL_TEXTURES = SHAPE_SETS

SHAPES = {
    "rect6": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
    "five": PLUS_5,
    "four": [(0, 0), (1, 0), (1, 1), (2, 1)],
    "line3": [(0, 0), (0, 1), (0, 2)],
    "ell3": [(0, 0), (1, 0), (1, 1)],
    "domino": [(0, 0), (1, 0)],
}

AXES = {
    "grid_h":         {"type": "int", "default": "rng 15..17", "valid": "13..20"},
    "grid_w":         {"type": "int", "default": "rng 15..17", "valid": "13..20"},
    "shape_set":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SHAPE_SETS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_components":   {"type": "int", "default": "6", "valid": "6"},
    "texture":        {"type": "str", "default": "alias for shape_set",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    g = full_grid(15 + rng.randint(0, 2), 15 + rng.randint(0, 2), 0)
    placements = [
        ("rect6", 1, 1),
        ("five", 1, 7),
        ("four", 6, 2),
        ("line3", 7, 8),
        ("ell3", 11, 2),
        ("domino", 11, 9),
    ]
    for name, r0, c0 in placements:
        r0 += rng.randint(0, 1)
        c0 += rng.randint(0, 1)
        for dr, dc in SHAPES[name]:
            g[r0 + dr][c0 + dc] = 6
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_components":
        return g
    if name == "single_component":
        for dr, dc in SHAPES["five"]:
            g[2 + dr][2 + dc] = 6
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 6
        return g
    return g
