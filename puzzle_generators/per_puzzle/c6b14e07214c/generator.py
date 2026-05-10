"""Generator for arc_puzzle_bank_ninth21:H62.

Rule: a color-7 rectangular frame contains 4 colored seeds at corner-ish
interior positions; blank interior cells are filled by nearest seed
under Manhattan distance (color tie-break).

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_h, frame_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, single_seed, no_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "c6b14e07214c"
VERSION = "1.1.0"
TASK_ID = "c6b14e07214c"
SUMMARY = "Color-7 rectangular frame with 4 distinct seeds in interior corners."

INVARIANTS = [
    "background is 0",
    "one rectangular color-7 frame bounds the fill region",
    "four distinct non-7 seed colors sit just inside the frame corners",
    "interior blank cells are available for filling",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "single_seed", "no_interior")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..15"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_h":        {"type": "int", "default": "rng 7..9", "valid": "5..11"},
    "frame_w":        {"type": "int", "default": "rng 8..10", "valid": "5..12"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "interior_corners",
                       "valid": "interior_corners"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "density":        {"type": "str", "default": "frame_with_seeds",
                       "valid": "frame_with_seeds"},
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
        fh = ctx.draw_int("frame_h", 7, 7)
        fw = ctx.draw_int("frame_w", 8, 8)
    elif difficulty == "hard":
        fh = ctx.draw_int("frame_h", 8, 9)
        fw = ctx.draw_int("frame_w", 9, 10)
    else:
        fh = ctx.draw_int("frame_h", 7, 9)
        fw = ctx.draw_int("frame_w", 8, 10)
    g = full_grid(fh + 4, fw + 4, 0)
    draw_frame(g, 1, 1, fh, fw, 7)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 8, 9], 4)
    positions = [(2, 2), (2, fw - 1), (fh - 1, 2), (fh - 1, fw - 1)]
    rng.shuffle(positions)
    for color, (r, c) in zip(colors, positions):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    fh, fw = 8, 9
    g = full_grid(fh + 4, fw + 4, 0)
    if name == "no_frame":
        # 4 seeds floating without a 7-frame → rule has no fill region
        for r, c, v in [(3, 3, 1), (3, fw - 1, 2), (fh - 1, 3, 5), (fh - 1, fw - 1, 6)]:
            g[r][c] = v
        return g
    if name == "single_seed":
        # one seed → all interior cells trivially nearest to that seed
        draw_frame(g, 1, 1, fh, fw, 7)
        g[3][3] = 4
        return g
    if name == "no_interior":
        # frame is a 3x3 with no fillable interior
        draw_frame(g, 1, 1, 3, 3, 7)
        return g
    return g
