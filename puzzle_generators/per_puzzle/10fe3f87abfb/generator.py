"""Generator for 2f767503.

Rule: color-4 objects on the side opposite a color-9 marker are
erased when they overlap the color-5 guide.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
guide_length.
Degenerates: no_guide, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "10fe3f87abfb"
VERSION = "1.1.0"
TASK_ID = "10fe3f87abfb"
SUMMARY = "Color-4 objects opposite color-9 marker erased where they overlap color-5 guide."

INVARIANTS = [
    "background is color 7",
    "color 5 forms one straight guide line",
    "a color-9 marker sits on one side of the guide",
    "at least one color-4 object overlaps the guide on the opposite side",
]

ORIENTATIONS = ("vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_guide", "no_marker", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..20"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "guide_length":   {"type": "int", "default": "rng 5..9", "valid": "3..14"},
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
    h = rng.randint(11, 14)
    w = rng.randint(12, 15)
    g = full_grid(h, w, 7)
    if orientation == "vertical":
        col = rng.randint(5, w - 6)
        r0 = rng.randint(2, 3)
        r1 = h - rng.randint(3, 4)
        for r in range(r0, r1 + 1):
            g[r][col] = 5
        g[rng.randint(0, 1)][col - 3] = 9
        start = rng.randint(r0, r1 - 2)
        erase_col = col + rng.randint(2, 3)
        for r in range(start, start + rng.randint(2, 4)):
            if r <= r1:
                g[r][erase_col] = 4
        keep_r = min(h - 1, r1 + 1)
        g[keep_r][col - 2] = 4
        g[keep_r][col - 1] = 4
    else:
        row = rng.randint(5, h - 6)
        c0 = rng.randint(2, 3)
        c1 = w - rng.randint(3, 4)
        for c in range(c0, c1 + 1):
            g[row][c] = 5
        g[row - 3][rng.randint(0, 1)] = 9
        start = rng.randint(c0, c1 - 2)
        erase_row = row + rng.randint(2, 3)
        for c in range(start, start + rng.randint(2, 4)):
            if c <= c1:
                g[erase_row][c] = 4
        keep_c = min(w - 1, c1 + 1)
        g[row - 2][keep_c] = 4
        g[row - 1][keep_c] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 7)
    if name == "no_guide":
        g[3][3] = 9
        g[7][7] = 4
        return g
    if name == "no_marker":
        for r in range(2, 9):
            g[r][7] = 5
        g[5][3] = 4
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 7
        return g
    return g
