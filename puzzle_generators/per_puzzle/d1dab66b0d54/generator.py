"""Generator for puzzle 5168d44c.

Rule: 2 cells of 3 (anchor pair) aligned in row/col, spacing = step.
For each 2-cell, move it by (dr, dc) in step direction.

Combinatorial axes (8): grid_h/w, anchor_orientation, spacing, c3_pos,
n_twos, twos_position, anchor_corner, decoy_color.
Degenerates: no_anchors, no_twos, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d1dab66b0d54"
VERSION = "1.1.0"
TASK_ID = "d1dab66b0d54"
SUMMARY = "3-anchor pair + 2-line; rule shifts 2-line by anchor spacing."

INVARIANTS = [
    "background is 0",
    "exactly 2 cells of color 3, aligned in row OR col, >=2 cells apart",
    ">=2 cells of color 2 forming a line",
    "shifted 2-line stays in-bounds",
]

ANCHOR_ORIENTATIONS = ("col", "row")
TWOS_POSITIONS = ("below", "above", "left", "right")
DEGENERATE_TEXTURES = ("no_anchors", "no_twos", "full_grid")
HELPFUL_TEXTURES = ANCHOR_ORIENTATIONS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 6..10",
                           "valid": "5..14"},
    "grid_w":             {"type": "int", "default": "rng 7..11",
                           "valid": "6..16"},
    "anchor_orientation": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(ANCHOR_ORIENTATIONS)},
    "spacing":            {"type": "int", "default": "rng 2..3",
                           "valid": "1..5"},
    "n_twos":             {"type": "int", "default": "rng 2..3",
                           "valid": "1..5"},
    "twos_position":      {"type": "str", "default": "rng",
                           "valid": "|".join(TWOS_POSITIONS)},
    "anchor_corner":      {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "decoy_color":        {"type": "color", "default": "rng [4,6,7,8]",
                           "valid": "1..9 (≠2,3)"},
    "texture":            {"type": "str", "default": "alias for anchor_orientation",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 10, 14
    else:
        h_lo, h_hi = 6, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 1)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    orientation = (overrides.get("texture") or
                   overrides.get("anchor_orientation")
                   or ctx.draw_choice("anchor_orientation",
                                      list(ANCHOR_ORIENTATIONS)))
    spacing = int(overrides.get("spacing",
                                ctx.draw_int("spacing", 2, 3)))
    spacing = max(1, min(5, spacing))
    n_twos = int(overrides.get("n_twos",
                               ctx.draw_int("n_twos", 2, 3)))
    n_twos = max(1, min(5, n_twos))
    g = full_grid(h, w, 0)
    if orientation == "col":
        c3 = rng.randint(2, max(2, w - 3))
        r3a = rng.randint(0, max(0, h - spacing - 2))
        g[r3a][c3] = 3
        g[r3a + spacing][c3] = 3
        r2 = rng.randint(max(spacing, h - 2), h - 1)
        c0 = rng.randint(1, max(1, w - n_twos - 1))
        for i in range(n_twos):
            if c0 + i < w and g[r2][c0 + i] == 0:
                g[r2][c0 + i] = 2
    else:
        r3 = rng.randint(2, max(2, h - 3))
        c3a = rng.randint(0, max(0, w - spacing - 2))
        g[r3][c3a] = 3
        g[r3][c3a + spacing] = 3
        c2 = rng.randint(max(spacing, w - 2), w - 1)
        r0 = rng.randint(1, max(1, h - n_twos - 1))
        for i in range(n_twos):
            if r0 + i < h and g[r0 + i][c2] == 0:
                g[r0 + i][c2] = 2
    decoy = int(overrides.get("decoy_color",
                              rng.choice([4, 6, 7, 8])))
    if decoy in (2, 3):
        decoy = 4
    if g[0][0] == 0:
        g[0][0] = decoy
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "no_anchors":
        # Just 2-cells, no 3 pair
        for c in range(2, 5):
            if c < w:
                g[h - 2][c] = 2
        return g
    if name == "no_twos":
        # Just anchors, no 2-line
        c = w // 2
        g[1][c] = 3
        g[3][c] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2 if (r + c) % 2 == 0 else 3
        return g
    return g
