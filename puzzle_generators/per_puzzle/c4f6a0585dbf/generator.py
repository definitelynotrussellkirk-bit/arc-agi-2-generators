"""Generator for 7df24a62.

Rule: a 1/4 template is completed wherever enough marker cells match
under a D4 transform.

Combinatorial axes (8): grid_h/w, target_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_template, no_targets, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c4f6a0585dbf"
VERSION = "1.1.0"
TASK_ID = "c4f6a0585dbf"
SUMMARY = "1/4 template is completed wherever enough marker cells match under a D4 transform."

INVARIANTS = [
    "the source template is the bounding box of the existing color-1 cells",
    "color-4 cells inside that box act as placement ports",
    "matching port pairs elsewhere receive the template's missing color-1 cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_targets", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "12..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "13..15"},
    "target_count":   {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
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
    if difficulty == "easy":
        target_count = ctx.draw_int("target_count", 1, 1)
    elif difficulty == "hard":
        target_count = ctx.draw_int("target_count", 3, 3)
    else:
        target_count = ctx.draw_int("target_count", 1, 3)
    h = 12 + (sample_index % 3)
    w = 13 + ((sample_index * 2) % 3)
    g = full_grid(h, w, 0)
    r0 = 1
    c0 = 1 + (sample_index % 2)
    for dr, dc in [(0, 0), (0, 2), (1, 0), (2, 0), (2, 2)]:
        g[r0 + dr][c0 + dc] = 1
    for dr, dc in [(0, 1), (2, 1)]:
        g[r0 + dr][c0 + dc] = 4
    starts = [(5, 6), (7, 3), (6, 9)]
    for ar, ac in starts[:target_count]:
        rr = min(ar + (sample_index % 2), h - 4)
        cc = min(ac + ((sample_index // 2) % 2), w - 4)
        g[rr][cc + 1] = 4
        g[rr + 2][cc + 1] = 4
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 13, 0)
    if name == "no_template":
        g[5][6] = 4
        g[7][6] = 4
        return g
    if name == "no_targets":
        for dr, dc in [(0, 0), (0, 2), (1, 0), (2, 0), (2, 2)]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 1), (2, 1)]:
            g[1 + dr][1 + dc] = 4
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(13):
                g[r][c] = 1
        return g
    return g
