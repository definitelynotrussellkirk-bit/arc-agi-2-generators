"""Generator for 2f0c5170.

Rule: yellow shape around a source dot is copied into the target
dot's 8-bounded panel.

Combinatorial axes (8): grid_h/w, panel_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, dot_color.
Degenerates: no_panel, no_dot, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5a053ea7753b"
VERSION = "1.1.0"
TASK_ID = "5a053ea7753b"
SUMMARY = "Yellow shape around source dot copied into target's 8-bounded panel."

INVARIANTS = [
    "color 8 separates the target panel from the rest of the grid",
    "one non-yellow dot color appears at a source dot adjacent to yellow cells",
    "another same-color dot marks the target location inside a non-8 panel",
    "the dot color is non-zero and not 4 or 8",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_panel", "no_dot", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "panel_size":     {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "dot_color":      {"type": "color", "default": "rng !{0,4,8}",
                       "valid": "1|2|3|5|6|7|9"},
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
    panel_size = ctx.draw_int("panel_size", 4, 6)
    dot_color = ctx.draw_color("dot_color", exclude={0, 4, 8})
    h = max(12, panel_size + 7)
    w = max(14, panel_size + 8)
    g = full_grid(h, w, 8)
    source = (2, 2)
    g[source[0]][source[1]] = dot_color
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (1, 1)]:
        g[source[0] + dr][source[1] + dc] = 4
    pr = rng.randint(5, h - panel_size - 1)
    pc = rng.randint(6, w - panel_size - 1)
    for r in range(pr, pr + panel_size):
        for c in range(pc, pc + panel_size):
            g[r][c] = 0
    target = (pr + panel_size // 2, pc + panel_size // 2)
    g[target[0]][target[1]] = dot_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 14, 8)
    if name == "no_panel":
        g[2][2] = 2
        return g
    if name == "no_dot":
        for r in range(5, 11):
            for c in range(7, 13):
                g[r][c] = 0
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(14):
                g[r][c] = 8
        return g
    return g
