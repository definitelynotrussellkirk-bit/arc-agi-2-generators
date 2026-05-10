"""Generator for arc_additional_puzzle_bank_volume7:M44 — Fill 4-frame interior with 8 if width = count of 2s.

Rule: k = count of 2-cells. For each 4-frame (hollow rect), if its width
== k, paint interior cells with 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, k,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_2s, no_matching_frame, all_frames_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "98f448f4ed98"
VERSION = "1.1.0"
TASK_ID = "98f448f4ed98"
SUMMARY = "k 2-cells in row 0 + 2 4-frames (one with width=k, one with different width)."

INVARIANTS = [
    "row 0 has between 2 and 5 cells of color 2",
    "2 closed 4-frames with widths k and !=k",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_2s", "no_matching_frame", "all_frames_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "k":              {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "row0_2s_with_2_4frames",
                       "valid": "row0_2s_with_2_4frames"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 13, 14)
        k = ctx.draw_int("k", 4, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 14, 15)
        k = ctx.draw_int("k", 5, 5)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 15)
        k = ctx.draw_int("k", 4, 5)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = list(range(w)); rng.shuffle(cols)
    for c in cols[:k]:
        g[0][c] = 2
    # Frame width k (matching)
    draw_frame(g, 1, 1, 5, 1 + k - 1, 4)
    # Frame width different (k+1 or k-1)
    other_k = k + 1 if k < 5 else k - 1
    draw_frame(g, 2, w - other_k - 1, 6, w - 2, 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_2s":
        # row 0 has no 2-cells → k=0, no frame matches width 0
        draw_frame(g, 1, 1, 5, 4, 4)
        draw_frame(g, 2, w - 6, 6, w - 2, 4)
        return g
    if name == "no_matching_frame":
        # k=4 but neither frame is width-4 → rule never fires
        for c in range(4): g[0][c] = 2   # k = 4
        draw_frame(g, 1, 1, 5, 3, 4)              # width 3
        draw_frame(g, 2, w - 7, 6, w - 2, 4)      # width 6
        return g
    if name == "all_frames_match":
        # both frames have width = k → both interiors get filled
        for c in range(4): g[0][c] = 2   # k = 4
        draw_frame(g, 1, 1, 5, 4, 4)              # width 4
        draw_frame(g, 2, w - 5, 6, w - 2, 4)      # width 4
        return g
    return g
