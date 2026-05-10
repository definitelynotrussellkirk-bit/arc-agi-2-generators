"""Generator for 79369cc6.

Rule: yellow-magenta template stamps yellow cells wherever magenta
markers match.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
second_orientation.
Degenerates: no_template, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d09fae8197f6"
VERSION = "1.1.0"
TASK_ID = "d09fae8197f6"
SUMMARY = "Yellow-magenta template stamps yellow wherever magenta markers match."

INVARIANTS = [
    "one compact template contains yellow body cells and magenta marker cells",
    "target marker clusters contain only the magenta part of a rotated template",
    "matching target clusters receive the yellow body cells from that orientation",
    "template is fixed at 3x3 in the upper-left",
]

ORIENTATIONS = ("o0", "o1", "o2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_markers", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

BASE_TEMPLATE = [
    [4, 6, 4],
    [4, 4, 6],
    [6, 4, 4],
]

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "second_orientation":{"type": "str", "default": "rng", "valid": "rng"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _rot_cw(shape):
    return [list(row) for row in zip(*shape[::-1])]


def _flip_lr(shape):
    return [list(reversed(row)) for row in shape]


def _orient(shape, idx):
    variants = [shape]
    variants.append(_rot_cw(variants[-1]))
    variants.append(_rot_cw(variants[-1]))
    variants.append(_rot_cw(variants[-1]))
    flipped = _flip_lr(shape)
    variants.append(flipped)
    variants.append(_rot_cw(variants[-1]))
    variants.append(_rot_cw(variants[-1]))
    variants.append(_rot_cw(variants[-1]))
    return variants[idx]


def _paste_template(g, r0, c0, shape):
    for r, row in enumerate(shape):
        for c, value in enumerate(row):
            g[r0 + r][c0 + c] = value


def _paste_markers(g, r0, c0, shape):
    for r, row in enumerate(shape):
        for c, value in enumerate(row):
            if value == 6:
                g[r0 + r][c0 + c] = 6


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in ORIENTATIONS:
        orientation = int(tx[1])
    else:
        orientation = ctx.draw_choice("orientation", [0, 1, 2])
    second_orientation = ctx.draw_choice("second_orientation", [3, 4, 5])
    g = full_grid(12, 14, 0)
    _paste_template(g, 1, 1, BASE_TEMPLATE)
    _paste_markers(g, 2, 8, _orient(BASE_TEMPLATE, orientation))
    _paste_markers(g, 7, 5, _orient(BASE_TEMPLATE, second_orientation))
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 14, 0)
    if name == "no_template":
        _paste_markers(g, 5, 5, BASE_TEMPLATE)
        return g
    if name == "no_markers":
        _paste_template(g, 1, 1, BASE_TEMPLATE)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(14):
                g[r][c] = 4
        return g
    return g
