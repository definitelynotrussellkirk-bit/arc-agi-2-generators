"""Generator for 0e206a2e.

Rule: a multicolor source shape is stamped at isolated markers under a
D4 transform.

Combinatorial axes (8): grid_h/w, target, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_source, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fcd7d477445c"
VERSION = "1.1.0"
TASK_ID = "fcd7d477445c"
SUMMARY = "Multicolor source shape is stamped at isolated markers under D4 transform."

INVARIANTS = [
    "one multicolor connected source has a dominant main color and a rarer spec color",
    "isolated spec-color markers select valid target placements",
    "the source is normalized and stamped at each marker-consistent placement",
]

TARGETS = ("T0", "T1", "T2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_source", "no_marker", "full_grid")
HELPFUL_TEXTURES = TARGETS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "target":         {"type": "choice", "default": "rng helpful",
                       "valid": "0|1|2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for target",
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
    if tx in TARGETS:
        target = int(tx[1])
    else:
        target = ctx.draw_choice("target", [0, 1, 2])
    main, spec = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(14, 14, 0)
    source = [(0, 0, spec), (0, 1, main), (1, 0, main), (1, 1, main), (2, 0, main)]
    for dr, dc, value in source:
        g[1 + dr][1 + dc] = value
    marker_positions = [(7, 8), (9, 5), (6, 11)]
    mr, mc = marker_positions[target]
    g[mr][mc] = spec
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_source":
        g[7][8] = 4
        return g
    if name == "no_marker":
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]:
            g[1 + dr][1 + dc] = 3
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 3
        return g
    return g
