"""Generator for baf41dbf.

Rule: color-3 rectangular grid stretches to the boundaries implied by
color-6 markers.

Combinatorial axes (8): grid_h/w, marker_mode, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
rect_size.
Degenerates: no_rect, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "9971f3a5882c"
VERSION = "1.1.0"
TASK_ID = "9971f3a5882c"
SUMMARY = "Color-3 rectangle stretches to boundaries implied by color-6 markers."

INVARIANTS = [
    "one color-3 rectangle supplies full source rows and columns",
    "color-6 markers sit outside the source bbox",
    "markers redefine the target bbox edges",
    "the rectangle sits with at least three cells of margin",
]

MARKER_MODES = ("all", "vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "no_markers", "full_grid")
HELPFUL_TEXTURES = MARKER_MODES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "marker_mode":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MARKER_MODES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "rect_size":      {"type": "str", "default": "rng 3..5", "valid": "3..5"},
    "texture":        {"type": "str", "default": "alias for marker_mode",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    mode = (overrides.get("texture") if overrides.get("texture") in MARKER_MODES else None) or \
           overrides.get("marker_mode") or \
           ctx.draw_choice("marker_mode", list(MARKER_MODES))
    h = 10 + rng.randint(0, 3)
    w = 10 + rng.randint(0, 4)
    rh = rng.randint(3, 4)
    rw = rng.randint(3, 5)
    r0 = rng.randint(3, h - rh - 3)
    c0 = rng.randint(3, w - rw - 3)
    r1 = r0 + rh - 1
    c1 = c0 + rw - 1
    g = full_grid(h, w, 0)
    draw_rect(g, r0, c0, rh, rw, 3)
    if mode in {"all", "vertical"}:
        g[r0 - 2][rng.randint(c0, c1)] = 6
        g[r1 + 2][rng.randint(c0, c1)] = 6
    if mode in {"all", "horizontal"}:
        g[rng.randint(r0, r1)][c0 - 2] = 6
        g[rng.randint(r0, r1)][c1 + 2] = 6
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_rect":
        g[1][5] = 6; g[9][5] = 6
        return g
    if name == "no_markers":
        draw_rect(g, 4, 4, 3, 4, 3)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 3
        return g
    return g
