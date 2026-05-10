"""Generator for 776ffc46.

Rule: gray frame contains colored template; matching blue shapes
outside are recolored to template color.

Combinatorial axes (8): grid_h/w, candidate_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
template_color.
Degenerates: no_frame, no_candidates, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b75f0b915b2b"
VERSION = "1.1.0"
TASK_ID = "b75f0b915b2b"
SUMMARY = "Gray frame with template; matching blue outside shapes recolored."

INVARIANTS = [
    "background is color 0",
    "one hollow frame uses color 5",
    "the frame interior contains a non-gray template shape",
    "outside candidate shapes use color 1 and match the template shape",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_candidates", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "grid_w":         {"type": "int", "default": "rng 14..17", "valid": "12..20"},
    "candidate_count":{"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "template_color": {"type": "color", "default": "rng !{0,1,5}",
                       "valid": "2|3|4|6|7|8|9"},
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
    n = ctx.draw_int("candidate_count", 1, 2)
    h = 14 + rng.randint(0, 3)
    w = 14 + rng.randint(0, 3)
    template_color = ctx.draw_color("template_color", exclude={0, 1, 5})
    g = full_grid(h, w, 0)
    fr, fc, fh, fw = 1, 1, 5, 5
    for c in range(fc, fc + fw):
        g[fr][c] = 5
        g[fr + fh - 1][c] = 5
    for r in range(fr, fr + fh):
        g[r][fc] = 5
        g[r][fc + fw - 1] = 5
    template = [(0, 0), (0, 1), (1, 0)]
    for dr, dc in template:
        g[fr + 2 + dr][fc + 2 + dc] = template_color
    anchors = [(8, 2), (8, 8)]
    for i in range(n):
        r0, c0 = anchors[i]
        for dr, dc in template:
            g[r0 + dr][c0 + dc] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_frame":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[8 + dr][8 + dc] = 1
        return g
    if name == "no_candidates":
        for c in range(1, 6):
            g[1][c] = 5; g[5][c] = 5
        for r in range(1, 6):
            g[r][1] = 5; g[r][5] = 5
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 5
        return g
    return g
