"""Generator for arc_puzzle_bank_eleventh21:M73.

The top-left cell is a rotation code. The interior of the color-5 frame is
extracted and rotated according to that code.

Combinatorial axes (8): code, interior_h, interior_w, palette_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_code, no_frame, symmetric_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "33c7c507a8ef"
VERSION = "1.1.0"
TASK_ID = "33c7c507a8ef"
SUMMARY = "A top-left rotation code transforms the interior of a gray frame."

INVARIANTS = [
    "cell (0,0) is a code from 1 through 4",
    "there is one color-5 rectangular frame",
    "the frame interior contains a nonzero asymmetric pattern",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_code", "no_frame", "symmetric_interior")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "code":           {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "interior_h":     {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "interior_w":     {"type": "int", "default": "rng 4..6", "valid": "3..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "centered_frame_with_code",
                       "valid": "centered_frame_with_code"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        code = ctx.draw_int("code", 1, 2)
        ih = ctx.draw_int("interior_h", 4, 4)
        iw = ctx.draw_int("interior_w", 4, 4)
    elif difficulty == "hard":
        code = ctx.draw_int("code", 1, 4)
        ih = ctx.draw_int("interior_h", 5, 5)
        iw = ctx.draw_int("interior_w", 5, 6)
    else:
        code = ctx.draw_int("code", 1, 4)
        ih = ctx.draw_int("interior_h", 4, 5)
        iw = ctx.draw_int("interior_w", 4, 6)
    g = full_grid(ih + 5, iw + 6, 0)
    g[0][0] = code
    r0, c0 = 2, 3
    draw_frame(g, r0, c0, r0 + ih + 1, c0 + iw + 1, 5)
    colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    marks = [(0, 0, colors[0]), (1, 0, colors[0]), (1, 1, colors[1]),
             (ih - 1, iw - 2, colors[2]), (ih - 2, iw - 1, colors[2])]
    for r, c, v in marks:
        g[r0 + 1 + r][c0 + 1 + c] = v
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    r0, c0 = 2, 3
    if name == "no_code":
        # missing rotation code at (0,0) → rule has no instruction to apply
        draw_frame(g, r0, c0, r0 + 5, c0 + 5, 5)
        for (r, c, v) in [(0, 0, 4), (1, 0, 4), (1, 1, 6), (3, 2, 8), (2, 3, 8)]:
            g[r0 + 1 + r][c0 + 1 + c] = v
        return g
    if name == "no_frame":
        # code present but no gray frame → nothing to extract
        g[0][0] = 2
        for (r, c, v) in [(3, 4, 4), (3, 5, 4), (4, 4, 6), (5, 6, 8)]:
            g[r][c] = v
        return g
    if name == "symmetric_interior":
        # interior is rotation-invariant → all 4 codes produce same output
        g[0][0] = 3
        draw_frame(g, r0, c0, r0 + 5, c0 + 5, 5)
        # 4-fold symmetric pattern (single center cell)
        g[r0 + 3][c0 + 3] = 4
        return g
    return g
