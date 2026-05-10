"""Generator for arc_puzzle_bank_21_set6_s:S6_M3 — deepest enclosing frame color.

Rule: each 1-dot is recolored by the smallest (deepest-nested) rect-
frame that strictly encloses it. If no frame encloses, the dot stays.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_dots, dot_outside_outer.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "47d385f6e696"
VERSION = "1.1.0"
TASK_ID = "47d385f6e696"
SUMMARY = "Two nested rect-frames + 3-4 1-dots scattered (some inside inner, some between)."

INVARIANTS = [
    "background is 0",
    "exactly two rect-frames, one fully nested inside the other",
    "each frame is a different color",
    "≥1 1-dot is enclosed by inner frame; ≥1 1-dot is between inner & outer; ≥1 1-dot may be outside outer",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_dots", "dot_outside_outer")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "nested_frames_with_dots",
                       "valid": "nested_frames_with_dots"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _stamp_outline(g, r1, c1, r2, c2, color):
    for c in range(c1, c2 + 1):
        g[r1][c] = color; g[r2][c] = color
    for r in range(r1, r2 + 1):
        g[r][c1] = color; g[r][c2] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    or1, oc1 = 1, 1
    or2, oc2 = h - 2, w - 2
    _stamp_outline(g, or1, oc1, or2, oc2, palette[0])
    ir1 = or1 + 2
    ic1 = oc1 + 2
    ir2 = or2 - 2
    ic2 = oc2 - 2
    if ir2 - ir1 < 2 or ic2 - ic1 < 2:
        return g
    _stamp_outline(g, ir1, ic1, ir2, ic2, palette[1])
    inside = [(r, c) for r in range(ir1 + 1, ir2) for c in range(ic1 + 1, ic2) if g[r][c] == 0]
    between = [(r, c) for r in range(or1 + 1, or2) for c in range(oc1 + 1, oc2)
               if not (ir1 <= r <= ir2 and ic1 <= c <= ic2) and g[r][c] == 0]
    if inside:
        r, c = rng.choice(inside); g[r][c] = 1
    if between:
        r, c = rng.choice(between); g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Dots but no frames — rule's recolor branch never fires;
        # output equals input.
        g[3][3] = 1; g[5][7] = 1
        return g
    if name == "no_dots":
        # Frames but no 1-dots — rule has no targets to recolor.
        _stamp_outline(g, 1, 1, 8, 10, 4)
        _stamp_outline(g, 3, 3, 6, 8, 6)
        return g
    if name == "dot_outside_outer":
        # 1-dots placed entirely outside both frames — rule's
        # recolor never fires; rule's effect is invisible.
        _stamp_outline(g, 1, 1, 5, 5, 4)
        _stamp_outline(g, 2, 2, 4, 4, 6)
        g[7][9] = 1; g[8][10] = 1
        return g
    return g
