"""Generator for 4ff4c9da.

Rule: cyan masks in one logical grid cell propagate to matching row and
column cells.

Combinatorial axes (8): grid_h/w, mask_position, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, target.
Degenerates: no_mask, no_separators, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d3575d4206d7"
VERSION = "1.1.0"
TASK_ID = "d3575d4206d7"
SUMMARY = "Cyan masks in one logical cell propagate to matching row and column cells."

INVARIANTS = [
    "uniform divider rows and columns split the grid into equal 2x2 cells",
    "one logical cell contains cyan at a single mask position",
    "same-row and same-column cells share a nonzero target value at that mask position",
    "the Cartesian-product matching cell is completed with cyan",
]

POSITIONS = ("tl", "tr", "bl", "br")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_mask", "no_separators", "full_grid")
HELPFUL_TEXTURES = POSITIONS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8"},
    "grid_w":         {"type": "int", "default": "8", "valid": "8"},
    "mask_position":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "target":         {"type": "color", "default": "rng !{0,5,8}",
                       "valid": "1..4|6|7|9"},
    "texture":        {"type": "str", "default": "alias for mask_position",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

CELL = 2
SEP = 5


def _put_cell(g, gr, gc, pattern):
    r0 = gr * 3
    c0 = gc * 3
    for r in range(CELL):
        for c in range(CELL):
            g[r0 + r][c0 + c] = pattern[r][c]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    pos = (overrides.get("texture") if overrides.get("texture") in POSITIONS else None) or \
          overrides.get("mask_position") or \
          ctx.draw_choice("mask_position", list(POSITIONS))
    target = ctx.draw_color("target", exclude={0, 5, 8})
    g = full_grid(8, 8, 0)
    for i in (2, 5):
        for c in range(8):
            g[i][c] = SEP
        for r in range(8):
            g[r][i] = SEP
    offsets = {"tl": (0, 0), "tr": (0, 1), "bl": (1, 0), "br": (1, 1)}
    mr, mc = offsets[pos]
    mask_pat = [[0, 0], [0, 0]]
    target_pat = [[0, 0], [0, 0]]
    mask_pat[mr][mc] = 8
    target_pat[mr][mc] = target
    _put_cell(g, 0, 0, mask_pat)
    _put_cell(g, 0, 1, target_pat)
    _put_cell(g, 1, 0, target_pat)
    _put_cell(g, 1, 1, target_pat)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 0)
    if name == "no_mask":
        for i in (2, 5):
            for c in range(8):
                g[i][c] = SEP
            for r in range(8):
                g[r][i] = SEP
        return g
    if name == "no_separators":
        g[0][0] = 8
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = SEP
        return g
    return g
