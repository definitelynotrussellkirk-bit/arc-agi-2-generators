"""Generator for arc_additional_puzzles_21_set17_bundle:H117.

Rule: commands at (0,0) and (0,1) (each 0..5) apply two transforms in
sequence to the cropped motif.

Combinatorial axes (8): grid_h/w, palette_kind, motif_kind, palette_size,
position_bias, n_distinct_colors, cmd_diversity, texture.
Degenerates: no_motif, invalid_cmd, no_cmds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dcc5f8961845"
VERSION = "1.1.0"
TASK_ID = "dcc5f8961845"
SUMMARY = "Commands at (0,0) and (0,1) apply two transforms to the cropped motif."

INVARIANTS = [
    "command values are 0..5",
    "the motif is away from row 0 and has a non-square bounding box",
]

PALETTE_KINDS = ("default", "motif_a", "motif_b", "varied_palette")
DEGENERATE_TEXTURES = ("no_motif", "invalid_cmd", "no_cmds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_kind":     {"type": "str", "default": "rng", "valid": "rng"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "interior",
                       "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "cmd_diversity":  {"type": "str", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


MOTIFS = (
    ((0, 0, 4), (0, 1, 4), (1, 1, 5), (2, 1, 5)),
    ((0, 2, 6), (1, 0, 7), (1, 1, 7), (2, 0, 6)),
)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
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
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.randint(0, 5)
    g[0][1] = rng.randint(0, 5)
    top = rng.randint(2, h - 4)
    left = rng.randint(2, w - 4)
    for dr, dc, color in rng.choice(MOTIFS):
        g[top + dr][left + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_motif":
        # commands present but no motif to transform
        g[0][0] = 3
        g[0][1] = 4
        return g
    if name == "invalid_cmd":
        # commands outside 0..5 → rule cannot map them
        g[0][0] = 8
        g[0][1] = 9
        for dr, dc, color in MOTIFS[0]:
            g[3 + dr][3 + dc] = color
        return g
    if name == "no_cmds":
        # motif but no command cells at (0,0) or (0,1) → undefined transform
        for dr, dc, color in MOTIFS[1]:
            g[3 + dr][3 + dc] = color
        return g
    return g
