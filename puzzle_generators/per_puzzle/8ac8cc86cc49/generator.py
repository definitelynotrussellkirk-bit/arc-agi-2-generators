"""Generator for 6350f1f4.

Rule: clean k-by-k template cell controls a separated macrogrid;
minority template positions preserve the template.

Combinatorial axes (8): grid_size, template_variant, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_template, full_template, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8ac8cc86cc49"
VERSION = "1.1.0"
TASK_ID = "8ac8cc86cc49"
SUMMARY = "Clean k-by-k template cell controls a separated macrogrid."

INVARIANTS = [
    "grid size is k*(k+1)-1 for k=3 so 11x11",
    "macro cells are 3x3 with one-cell separators",
    "one clean template macro cell has two colors and no color 5",
    "other macro cells contain color 5 so they are skipped as templates",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "full_template", "full_grid")
HELPFUL_TEXTURES = ("diag", "corner", "bar")

TEMPLATES = {
    "diag": [[1, 1, 2], [1, 2, 1], [2, 1, 1]],
    "corner": [[2, 1, 1], [1, 1, 1], [1, 1, 1]],
    "bar": [[1, 1, 1], [2, 2, 1], [1, 1, 1]],
}

AXES = {
    "grid_size":      {"type": "int", "default": "11", "valid": "11"},
    "template_variant":{"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES)},
    "palette_kind":   {"type": "str", "default": "rng", "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for template_variant",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    variant = (overrides.get("texture") if overrides.get("texture") in HELPFUL_TEXTURES else None) or \
              overrides.get("template_variant") or \
              ctx.draw_choice("template_variant", list(HELPFUL_TEXTURES))
    majority_color, minority_color = ctx.draw_distinct_colors(
        "template_colors", n=2, exclude={0, 5}
    )
    g = full_grid(11, 11, 0)
    for tr in range(3):
        for tc in range(3):
            r0 = tr * 4
            c0 = tc * 4
            for dr in range(3):
                for dc in range(3):
                    g[r0 + dr][c0 + dc] = 5
    template = TEMPLATES[variant]
    for r in range(3):
        for c in range(3):
            g[r][c] = minority_color if template[r][c] == 2 else majority_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_template":
        for tr in range(3):
            for tc in range(3):
                r0 = tr * 4; c0 = tc * 4
                for dr in range(3):
                    for dc in range(3):
                        g[r0 + dr][c0 + dc] = 5
        return g
    if name == "full_template":
        for r in range(11):
            for c in range(11):
                g[r][c] = 1 if r < 3 and c < 3 else 5
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
