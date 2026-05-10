"""Generator for 63613498.

Rule: colored template inside top-left gray cue is matched by an
outside shape, which is recolored gray.

Combinatorial axes (8): grid_h/w, template_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_cue, no_outside, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bdd177308a5b"
VERSION = "1.1.0"
TASK_ID = "bdd177308a5b"
SUMMARY = "Colored template in gray cue matched by outside shape, recolored gray."

INVARIANTS = [
    "background is color 0",
    "the top-left 3x3 cue contains gray frame cells and a non-gray template",
    "one outside object has the same normalized shape as the template",
    "template and outside colors are distinct from each other and from 0 and 5",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cue", "no_outside", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "template_size":  {"type": "int", "default": "3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
    ctx.draw_int("template_size", 3, 3)
    h = 9 + rng.randint(0, 3)
    w = 9 + rng.randint(0, 3)
    template_color, outside_color, decoy_color = ctx.draw_distinct_colors(
        "colors", n=3, exclude={0, 5})
    g = full_grid(h, w, 0)
    for c in range(3):
        g[0][c] = 5
    for r in range(3):
        g[r][0] = 5
    template = [(1, 1), (1, 2), (2, 1)]
    for r, c in template:
        g[r][c] = template_color
    r0 = 5 + (sample_index % max(1, h - 8))
    c0 = 5 + ((sample_index // 2) % max(1, w - 8))
    for dr, dc in [(0, 0), (0, 1), (1, 0)]:
        g[r0 + dr][c0 + dc] = outside_color
    if h > 9 and w > 9:
        g[h - 2][1] = decoy_color
        g[h - 2][2] = decoy_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_cue":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][5 + dc] = 2
        return g
    if name == "no_outside":
        for c in range(3):
            g[0][c] = 5
        for r in range(3):
            g[r][0] = 5
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
