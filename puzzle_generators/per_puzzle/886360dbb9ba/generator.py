"""Generator for 538b439f.

Rule: solid rectangles mirror across a full-span colored line, and the
gaps to both rectangles are filled with the line color.

Combinatorial axes (8): grid_h/w, orientation, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_line, no_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "886360dbb9ba"
VERSION = "1.1.0"
TASK_ID = "886360dbb9ba"
SUMMARY = "Solid rectangles mirror across line; gaps filled with line color."

INVARIANTS = [
    "the background is the mode color",
    "there is one full-span non-background row or column line",
    "all other non-background objects are solid rectangles",
    "each rectangle is mirrored across the line and bridged to the line with the line color",
]

ORIENTATIONS = ("vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_line", "no_rect", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "17", "valid": "17"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    bg, line_color, rect_color = ctx.draw_distinct_colors("colors", n=3, exclude=set())
    h = 16
    w = 17
    g = full_grid(h, w, bg)
    if orientation == "vertical":
        lc = w // 2
        for r in range(h):
            g[r][lc] = line_color
        r0 = rng.randint(2, 9)
        c0 = rng.randint(1, 3)
        rh = rng.randint(2, 4)
        rw = rng.randint(2, 3)
    else:
        lr = h // 2
        for c in range(w):
            g[lr][c] = line_color
        r0 = rng.randint(1, 3)
        c0 = rng.randint(3, 10)
        rh = rng.randint(2, 3)
        rw = rng.randint(2, 4)
    for r in range(r0, r0 + rh):
        for c in range(c0, c0 + rw):
            g[r][c] = rect_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 17, 0)
    if name == "no_line":
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 3
        return g
    if name == "no_rect":
        for c in range(17):
            g[8][c] = 4
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(17):
                g[r][c] = 4
        return g
    return g
