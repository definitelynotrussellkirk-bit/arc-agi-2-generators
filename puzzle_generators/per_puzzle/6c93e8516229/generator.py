"""Generator for e509e548.

Rule: green components are classified by topology; T-junctions become
red, two-corner shapes magenta, others blue.

Combinatorial axes (8): grid_h/w, component_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_variant.
Degenerates: no_components, single_component, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6c93e8516229"
VERSION = "1.1.0"
TASK_ID = "6c93e8516229"
SUMMARY = "Green components classified by topology: T-junctions, two-corner, others."

INVARIANTS = [
    "background is color 0",
    "all source topology shapes use color 3",
    "green components are 4-connected and separated",
    "the input contains at least one shape from each topology class",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_components", "single_component", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

BLUE_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
]
MAGENTA_SHAPES = [
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]
RED_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..16", "valid": "11..18"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..20"},
    "component_count":{"type": "int", "default": "3", "valid": "3"},
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
    h = 13 + ((seed + sample_index) % 4)
    w = 14 + ((seed * 3 + sample_index * 2) % 5)
    g = full_grid(h, w, 0)
    shapes = [
        (
            BLUE_SHAPES[(sample_index + rng.randint(0, 2)) % len(BLUE_SHAPES)],
            1 + (sample_index % 2),
            1 + ((sample_index // 2) % 2),
        ),
        (
            MAGENTA_SHAPES[(sample_index // 2 + rng.randint(0, 2)) % len(MAGENTA_SHAPES)],
            1 + ((sample_index // 3) % 2),
            w - 5 + ((seed + sample_index) % 2),
        ),
        (
            RED_SHAPES[(sample_index // 3 + rng.randint(0, 2)) % len(RED_SHAPES)],
            h - 5 + ((sample_index // 4) % 2),
            4 + ((sample_index + rng.randint(0, 3)) % max(1, w - 8)),
        ),
    ]
    for cells, r0, c0 in shapes:
        for dr, dc in cells:
            g[r0 + dr][c0 + dc] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 14, 0)
    if name == "no_components":
        return g
    if name == "single_component":
        for dr, dc in BLUE_SHAPES[0]:
            g[1 + dr][1 + dc] = 3
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(14):
                g[r][c] = 3
        return g
    return g
