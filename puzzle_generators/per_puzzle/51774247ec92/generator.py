"""Generator for arc_additional_puzzles_21_set18_bundle:M124 — apply cmd-rotation to first shape.

Rule: row 0 carries a single command (2..6). Below row 0, find the
top-leftmost connected component, crop it to bbox, and apply the
transform: 2=identity, 3=rot-cw, 4=rot-180, 5=flip-lr, 6=flip-ud.
Output is the transformed crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_command, no_motif, multiple_motifs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "51774247ec92"
VERSION = "1.1.0"
TASK_ID = "51774247ec92"
SUMMARY = "Cmd cell in row 0 + a single small motif (multi-color) below."

INVARIANTS = [
    "background is 0",
    "row 0 holds a single non-zero command in {2, 3, 4, 5, 6}",
    "exactly one connected component below row 0",
    "the motif uses 2-3 distinct colors so transforms are visible",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_command", "no_motif", "multiple_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "row0_cmd_one_motif_below",
                       "valid": "row0_cmd_one_motif_below"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOTIFS = [
    [(0, 0), (0, 1), (1, 0), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cmd = rng.choice([2, 3, 4, 5, 6])
    g[0][rng.randint(0, w - 1)] = cmd
    motif = rng.choice(_MOTIFS)
    sh = max(c[0] for c in motif) + 1
    sw = max(c[1] for c in motif) + 1
    palette = list(random_palette(rng, 3, exclude={cmd}))
    r0 = rng.randint(2, h - sh - 1)
    c0 = rng.randint(0, w - sw)
    cells_with_color = []
    for i, (dr, dc) in enumerate(motif):
        cells_with_color.append((dr, dc, palette[i % len(palette)]))
    paint_at(g, r0, c0, cells_with_color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_command":
        # Motif present but row 0 is empty — rule has no transform code
        # to look up.
        cells = [(0, 0, 4), (0, 1, 5), (1, 0, 6), (1, 2, 7)]
        paint_at(g, 3, 4, cells)
        return g
    if name == "no_motif":
        # Command set but no motif below — rule has nothing to crop and
        # transform.
        g[0][3] = 4
        return g
    if name == "multiple_motifs":
        # Two distinct motifs below — rule's "first shape" picker is
        # ambiguous about which to transform.
        g[0][3] = 3
        cells_a = [(0, 0, 4), (0, 1, 5), (1, 0, 6)]
        cells_b = [(0, 0, 4), (0, 1, 5), (1, 0, 7)]
        paint_at(g, 2, 1, cells_a)
        paint_at(g, 5, 7, cells_b)
        return g
    return g
