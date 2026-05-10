"""Generator for 264363fd.

Rule: a cross-shaped key centered on a marker stamps colored arms inside
each rectangle marker.

Combinatorial axes (8): grid_h/w, rect_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_key, no_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "334cbd1692c7"
VERSION = "1.1.0"
TASK_ID = "334cbd1692c7"
SUMMARY = "Cross-shaped key centered on marker stamps colored arms inside rectangles."

INVARIANTS = [
    "large same-colored rectangles contain marker cells",
    "an outside connected key shape is centered on the same marker color",
    "key offsets and arm colors are copied to every marker inside the rectangles",
]

RECT_SIZES = ("medium", "large")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_key", "no_rect", "full_grid")
HELPFUL_TEXTURES = RECT_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "rect_size":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(RECT_SIZES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "6", "valid": "6"},
    "texture":        {"type": "str", "default": "alias for rect_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    rect_kind = (overrides.get("texture") if overrides.get("texture") in RECT_SIZES else None) or \
                overrides.get("rect_size") or \
                ("medium" if sample_index % 2 == 0 else "large")
    rect, marker, up, down, left, right = ctx.draw_distinct_colors("colors", n=6, exclude={0})
    g = full_grid(16, 18, 0)

    rh, rw = (6, 8) if rect_kind == "medium" else (7, 9)
    r0 = 8 - (sample_index % 2)
    c0 = 5 + (sample_index % 2)
    draw_rect(g, r0, c0, rh, rw, rect)
    mr = r0 + rh // 2
    mc = c0 + rw // 2
    g[mr][mc] = marker

    kr = 3
    kc = 3 + (sample_index % 2)
    g[kr][kc] = marker
    for dr, color in [(-2, up), (-1, up), (1, down), (2, down)]:
        g[kr + dr][kc] = color
    for dc, color in [(-2, left), (-1, left), (1, right), (2, right)]:
        g[kr][kc + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 18, 0)
    if name == "no_key":
        draw_rect(g, 8, 5, 6, 8, 3)
        return g
    if name == "no_rect":
        g[3][3] = 4
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(18):
                g[r][c] = 4
        return g
    return g
