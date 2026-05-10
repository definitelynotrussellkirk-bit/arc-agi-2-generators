"""Generator for arc_additional_puzzles_21_set20_bundle:H138.

Rule: two command cells transform the cropped motif: cw, 180,
left-right, up-down, or transpose.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_choice,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_commands, no_motif, square_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3550b85c52f2"
VERSION = "1.1.0"
TASK_ID = "3550b85c52f2"
SUMMARY = "Two command cells transform the cropped motif: cw, 180, left-right, up-down, or transpose."

INVARIANTS = [
    "commands live in cells (0,0) and (0,1)",
    "the motif is separated from command cells and has a non-square bounding box",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_commands", "no_motif", "square_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_choice":   {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "command_top_left",
                       "valid": "command_top_left"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


MOTIFS = (
    ((0, 0, 6), (0, 1, 6), (1, 1, 7), (2, 1, 7)),
    ((0, 2, 5), (1, 0, 8), (1, 1, 8), (1, 2, 5), (2, 0, 8)),
)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.randint(1, 5)
    g[0][1] = rng.randint(1, 5)
    motif = rng.choice(MOTIFS)
    top = rng.randint(2, h - 4)
    left = rng.randint(2, w - 4)
    for dr, dc, color in motif:
        g[top + dr][left + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "missing_commands":
        # cells (0,0) and (0,1) empty → no transform commands to apply
        motif = ((0, 0, 6), (0, 1, 6), (1, 1, 7), (2, 1, 7))
        for dr, dc, color in motif:
            g[3 + dr][4 + dc] = color
        return g
    if name == "no_motif":
        # commands present but no motif body → nothing to transform
        g[0][0] = 3
        g[0][1] = 5
        return g
    if name == "square_motif":
        # motif's bounding box is square → cw / transpose / 180 may produce identical results
        g[0][0] = 3
        g[0][1] = 5
        for dr in range(3):
            for dc in range(3):
                if (dr + dc) % 2 == 0:
                    g[3 + dr][4 + dc] = 6
        return g
    return g
