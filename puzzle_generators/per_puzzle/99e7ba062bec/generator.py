"""Generator for arc_additional_puzzles_21_set21_bundle:H142.

Rule: three blank-separated panels infer a transform from A to B and
apply it to C.

Combinatorial axes (8): grid_h, grid_w, palette_kind, command,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: identity_transform, A_B_unrelated, missing_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "99e7ba062bec"
VERSION = "1.1.0"
TASK_ID = "99e7ba062bec"
SUMMARY = "Three blank-separated panels infer a transform from A to B and apply it to C."

INVARIANTS = [
    "three panels are split by zero columns",
    "the cropped second panel is a transform of the cropped first panel",
    "the cropped third panel receives the same transform",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identity_transform", "A_B_unrelated", "missing_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "command":        {"type": "str", "default": "rng rot|flip",
                       "valid": "rot|flip"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "three_panels",
                       "valid": "three_panels"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _place(g, r, c, cells, color):
    for dr, dc in cells:
        g[r + dr][c + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    command = ctx.draw_choice("command", ["rot", "flip"])
    if "command" not in overrides:
        command = "rot" if sample_index % 2 == 0 else "flip"
    color = ctx.draw_color("color", exclude={0})
    g = full_grid(6, 13, 0)
    a = [(0, 0), (1, 0), (1, 1)]
    b = [(0, 0), (0, 1), (1, 0)] if command == "rot" else [(0, 1), (1, 0), (1, 1)]
    c = [(0, 0), (0, 1), (1, 1)]
    _place(g, 1, 0, a, color)
    _place(g, 1, 4, b, color)
    _place(g, 1, 9, c, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 13, 0)
    a = [(0, 0), (1, 0), (1, 1)]
    c = [(0, 0), (0, 1), (1, 1)]
    if name == "identity_transform":
        # A == B → inferred transform is identity, output equals C
        _place(g, 1, 0, a, 4)
        _place(g, 1, 4, a, 4)
        _place(g, 1, 9, c, 4)
        return g
    if name == "A_B_unrelated":
        # B is not any D4 transform of A → no transform can be inferred
        unrelated = [(0, 0), (0, 2), (1, 1)]
        _place(g, 1, 0, a, 4)
        _place(g, 1, 4, unrelated, 4)
        _place(g, 1, 9, c, 4)
        return g
    if name == "missing_panel":
        # only two panels populated → can't both infer and apply
        _place(g, 1, 0, a, 4)
        _place(g, 1, 4, a, 4)
        return g
    return g
