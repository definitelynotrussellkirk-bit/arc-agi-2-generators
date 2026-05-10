"""Generator for arc_additional_puzzles_21_set5:M30 — wrap motif crop in frame color.

Rule: cell (0,0) supplies the new frame color around the cropped nonzero
motif.

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame_color, no_motif, motif_touches_command.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e96f42608654"
VERSION = "1.1.0"
TASK_ID = "e96f42608654"
SUMMARY = "Cell (0,0) supplies the new frame color around the cropped nonzero motif."

INVARIANTS = [
    "the frame color is stored only at (0,0)",
    "the motif has a compact nonzero bounding box away from the command cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame_color", "no_motif", "motif_touches_command")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_color":    {"type": "color", "default": "rng nonzero", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "command_corner_motif_offset",
                       "valid": "command_corner_motif_offset"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 12)
    frame = ctx.draw_color("frame_color", exclude=[0])
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude=[0, frame]))
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = frame
    top = rng.randint(2, h - 5)
    left = rng.randint(2, w - 5)
    motif = [(0, 0, colors[0]), (0, 1, colors[1]), (1, 1, colors[1]), (2, 0, colors[2])]
    for dr, dc, color in motif:
        g[top + dr][left + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_frame_color":
        # (0,0) is 0 → no frame color provided, rule has no wrapper color
        g[3][3] = 4; g[3][4] = 6; g[4][4] = 6; g[5][3] = 7
        return g
    if name == "no_motif":
        # frame color present but no motif → rule has nothing to wrap
        g[0][0] = 4
        return g
    if name == "motif_touches_command":
        # motif extends to (0,0) → command cell is also part of motif, wrapping logic ambiguous
        g[0][0] = 4
        g[0][1] = 6; g[1][0] = 6; g[1][1] = 7
        return g
    return g
