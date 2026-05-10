"""Generator for db118e2a.

Rule: framed interior motif is cropped to its content and copied into
two framed output positions.

Combinatorial axes (8): grid_h/w, motif, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_frame, no_motif, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "09681a814e86"
VERSION = "1.1.0"
TASK_ID = "09681a814e86"
SUMMARY = "Framed motif cropped and copied into two framed output positions."

INVARIANTS = [
    "the background is taken from the upper-left cell",
    "the top border reveals the frame color",
    "non-background interior cells define a compact motif bbox",
    "frame and motif colors are distinct and non-zero",
]

MOTIFS = ("corner", "diag", "bar")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_motif", "full_grid")
HELPFUL_TEXTURES = MOTIFS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "motif":          {"type": "str", "default": "rng helpful",
                       "valid": "|".join(MOTIFS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for motif",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    motif = (overrides.get("texture") if overrides.get("texture") in MOTIFS else None) or \
            overrides.get("motif") or \
            ctx.draw_choice("motif", list(MOTIFS))
    frame, a, b = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(9, 9, 0)
    draw_frame(g, 0, 0, 8, 8, frame)
    if motif == "corner":
        cells = [(3, 3, a), (3, 4, b), (4, 3, b)]
    elif motif == "diag":
        cells = [(2, 2, a), (3, 3, b), (4, 4, a)]
    else:
        cells = [(4, 3, a), (4, 4, b), (4, 5, a)]
    for r, c, color in cells:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_frame":
        g[4][4] = 2
        return g
    if name == "no_motif":
        draw_frame(g, 0, 0, 8, 8, 1)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 1
        return g
    return g
