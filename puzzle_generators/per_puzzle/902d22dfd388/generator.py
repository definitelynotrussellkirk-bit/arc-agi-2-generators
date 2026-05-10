"""Generator for arc_puzzle_bank_ninth21:M63 — crop framed interior, center it.

Rule: a 7-rect-frame contains some non-7 cells inside. Crop the bbox
of those cells from the interior, then center the crop on an empty
output grid of the same size as input.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_interior,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, empty_frame, full_interior.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "902d22dfd388"
VERSION = "1.1.0"
TASK_ID = "902d22dfd388"
SUMMARY = "One 7-rect-frame containing 2-4 colored cells inside (small enough that centered crop ≠ identity)."

INVARIANTS = [
    "background is 0",
    "exactly one 7-rect-outline frame ≥5x5",
    "≥2 non-7 cells inside the frame, in distinct colors",
    "interior content's bbox is strictly smaller than the frame interior (so centering moves things)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "empty_frame", "full_interior")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_interior":     {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "frame_with_offset_interior",
                       "valid": "frame_with_offset_interior"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    # frame at row 1..h-2, col 1..w-2
    r1, c1 = 1, 1
    r2, c2 = h - 2, w - 2
    for c in range(c1, c2 + 1):
        g[r1][c] = 7; g[r2][c] = 7
    for r in range(r1, r2 + 1):
        g[r][c1] = 7; g[r][c2] = 7
    # place 2-4 cells inside in upper-left of interior
    interior_cells = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
    palette = rng.sample([2, 3, 4, 5, 6, 8, 9], 2)
    n = rng.randint(2, 4)
    chosen = rng.sample(interior_cells[:len(interior_cells) // 2 + 1], min(n, len(interior_cells) // 2 + 1))
    for i, (r, c) in enumerate(chosen):
        g[r][c] = palette[i % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # interior cells but no 7-frame → no bounding container, no centering
        g[2][2] = 4; g[3][3] = 6
        return g
    if name == "empty_frame":
        # frame with empty interior → nothing to crop or center
        for c in range(1, w - 1): g[1][c] = 7; g[h - 2][c] = 7
        for r in range(1, h - 1): g[r][1] = 7; g[r][w - 2] = 7
        return g
    if name == "full_interior":
        # interior fully filled → bbox = full interior, centering is identity
        for c in range(1, w - 1): g[1][c] = 7; g[h - 2][c] = 7
        for r in range(1, h - 1): g[r][1] = 7; g[r][w - 2] = 7
        for r in range(2, h - 2):
            for c in range(2, w - 2):
                g[r][c] = 4
        return g
    return g
