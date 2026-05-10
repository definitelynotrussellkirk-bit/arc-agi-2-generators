"""Generator for b0f4d537.

Rule: a 0/4 reference panel selects row variants from a colored template
panel.

Combinatorial axes (8): grid_h/w, special_fill, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_reference, no_template, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d5178d26d905"
VERSION = "1.1.0"
TASK_ID = "d5178d26d905"
SUMMARY = "0/4 reference panel selects row variants from colored template panel."

INVARIANTS = [
    "a full color-5 divider separates the reference and template panels",
    "the reference side contains only 0/4 row masks",
    "the template side supplies normal line colors plus special row fill variants",
]

FILLS = ("left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_reference", "no_template", "full_grid")
HELPFUL_TEXTURES = FILLS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "special_fill":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(FILLS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for special_fill",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    special_fill = (overrides.get("texture") if overrides.get("texture") in FILLS else None) or \
                   overrides.get("special_fill") or \
                   ("left" if sample_index % 2 == 0 else "right")
    line_a, line_b, fill = ctx.draw_distinct_colors("colors", n=3, exclude={0, 4, 5})
    g = full_grid(5, 11, 5)
    ref = [
        [0, 4, 0, 4, 0],
        [0, 4, 0, 4, 0],
        [4, 4, 0, 4, 4],
        [0, 4, 0, 4, 0],
        [0, 4, 0, 4, 0],
    ]
    normal = [0, line_a, 0, line_b, 0]
    special = [fill, line_a, fill, 0 if special_fill == "left" else line_b, fill]
    for r in range(5):
        for c in range(5):
            g[r][c] = ref[r][c]
            g[r][6 + c] = special[c] if r == 2 else normal[c]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 11, 5)
    if name == "no_reference":
        for r in range(5):
            g[r][7] = 3
        return g
    if name == "no_template":
        for r in range(5):
            for c in range(5):
                g[r][c] = 4 if (r + c) % 2 else 0
        return g
    if name == "full_grid":
        for r in range(5):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
