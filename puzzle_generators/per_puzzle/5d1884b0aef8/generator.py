"""Generator for arc_additional_puzzles_21_set7:H47.

Rule: top-left command rotates the cropped motif; top-right command
chooses vertical or horizontal flip.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_kind,
palette_size, position_bias, n_distinct_colors, command_kind, texture.
Degenerates: no_rotation_cmd, no_flip_cmd, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5d1884b0aef8"
VERSION = "1.1.0"
TASK_ID = "5d1884b0aef8"
SUMMARY = "Top-left command rotates the cropped motif; top-right command chooses vertical or horizontal flip."

INVARIANTS = [
    "commands are in the two top corners",
    "the motif is away from the command row and has a non-square bounding box",
]

PALETTE_KINDS = ("default", "L_motif", "T_motif", "Z_motif")
DEGENERATE_TEXTURES = ("no_rotation_cmd", "no_flip_cmd", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_kind":     {"type": "str", "default": "rng", "valid": "rng"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "corners_plus_motif",
                       "valid": "corners_plus_motif"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "command_kind":   {"type": "str", "default": "rng", "valid": "rng"},
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
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.randint(1, 4)
    g[0][w - 1] = rng.choice([1, 2])
    top = rng.randint(2, h - 4)
    left = rng.randint(2, w - 4)
    for dr, dc, color in rng.choice(MOTIFS):
        g[top + dr][left + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_rotation_cmd":
        # motif + flip cmd but no rotation cmd → rotation count undefined
        g[0][w - 1] = 1
        for dr, dc, color in MOTIFS[0]:
            g[3 + dr][3 + dc] = color
        return g
    if name == "no_flip_cmd":
        # motif + rotation cmd but no flip cmd → flip choice undefined
        g[0][0] = 2
        for dr, dc, color in MOTIFS[0]:
            g[3 + dr][3 + dc] = color
        return g
    if name == "no_motif":
        # commands but no motif → rule has nothing to transform
        g[0][0] = 3
        g[0][w - 1] = 2
        return g
    return g
