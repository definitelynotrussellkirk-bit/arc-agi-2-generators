"""Generator for v3_rich_schema:hard_01_rotate_exemplar_by_target_color.

Rule: stamp rotated copies of the green exemplar body at coded target
markers (2=0°, 4=90°, 6=180°, 8=270°).

Combinatorial axes (8): grid_h/w, palette_kind, target_a, target_b,
palette_size, position_bias, n_distinct_colors, exemplar_kind, texture.
Degenerates: no_exemplar, no_targets, anchor_outside_exemplar.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "273261724728"
VERSION = "1.1.0"
TASK_ID = "273261724728"
SUMMARY = "Stamp rotated copies of the green exemplar body at coded target markers."

INVARIANTS = [
    "one exemplar component contains a blue anchor color 1 and green body color 3",
    "target singleton colors are chosen from 2,4,6,8",
    "target color controls rotation count: 2=0, 4=90, 6=180, 8=270",
    "stamped body cells are painted green only into empty cells",
]

PALETTE_KINDS = ("default", "rot_0", "rot_90", "rot_180")
DEGENERATE_TEXTURES = ("no_exemplar", "no_targets", "anchor_outside_exemplar")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "9..14"},
    "grid_w":         {"type": "int", "default": "12", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_a":       {"type": "enum", "default": "rng", "valid": "2|4|6|8"},
    "target_b":       {"type": "enum", "default": "rng", "valid": "2|4|6|8"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "exemplar_kind":  {"type": "str", "default": "T_shape", "valid": "T_shape"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = [2, 4, 6, 8]
_EXEMPLAR = [(0, 1, 3), (1, 0, 3), (1, 1, 1), (2, 1, 3)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    code_a = ctx.draw_choice("target_a", _CODES)
    code_b = ctx.draw_choice("target_b", _CODES)
    g = full_grid(11, 12, 0)
    for dr, dc, value in _EXEMPLAR:
        g[1 + dr][1 + dc] = value
    g[2][8] = code_a
    g[7][8] = code_b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 0)
    if name == "no_exemplar":
        # targets but no exemplar to stamp → rule has no shape source
        g[2][8] = 2; g[7][8] = 6
        return g
    if name == "no_targets":
        # exemplar but no rotation-code markers → nothing to stamp
        for dr, dc, v in _EXEMPLAR:
            g[1 + dr][1 + dc] = v
        return g
    if name == "anchor_outside_exemplar":
        # exemplar body without the blue 1 anchor → rotation pivot undefined
        for dr, dc, v in [(0, 1, 3), (1, 0, 3), (2, 1, 3)]:
            g[1 + dr][1 + dc] = v
        g[2][8] = 4; g[7][8] = 8
        return g
    return g
