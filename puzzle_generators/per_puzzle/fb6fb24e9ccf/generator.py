"""Generator for arc_puzzle_bank_eighteenth_21_bundle:easy_125_crop_the_nonzero_bounding_box.

Rule: crop the grid to the minimal nonzero bounding box.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_h, motif_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motif, full_grid_motif, multiple_motifs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fb6fb24e9ccf"
VERSION = "1.1.0"
TASK_ID = "fb6fb24e9ccf"

SUMMARY = "Crop to the minimal nonzero bounding box."

INVARIANTS = [
    "background is 0",
    "nonzero cells form a compact motif inside a larger frame",
    "there is at least one background margin outside the motif",
    "output dimensions equal the motif bounding box",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motif", "full_grid_motif", "multiple_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_h":        {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "motif_w":        {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "centered_motif_with_margin",
                       "valid": "centered_motif_with_margin"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "varied", "valid": "varied"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        mh = min(ctx.draw_int("motif_h", 3, 3), h - 2)
        mw = min(ctx.draw_int("motif_w", 3, 3), w - 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        mh = min(ctx.draw_int("motif_h", 4, 5), h - 2)
        mw = min(ctx.draw_int("motif_w", 4, 5), w - 2)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        mh = min(ctx.draw_int("motif_h", 3, 5), h - 2)
        mw = min(ctx.draw_int("motif_w", 3, 5), w - 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    top = rng.randint(1, h - mh - 1)
    left = rng.randint(1, w - mw - 1)
    cells = [(r, c) for r in range(mh) for c in range(mw)]
    count = rng.randint(max(2, min(mh, mw)), mh * mw)
    chosen = set(rng.sample(cells, count))
    chosen.add((0, 0))
    chosen.add((mh - 1, mw - 1))
    for r, c in chosen:
        g[top + r][left + c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_motif":
        # blank → no nonzero cells, bbox undefined
        return g
    if name == "full_grid_motif":
        # nonzero cells touch every row and column → bbox = full grid (rule is identity)
        for r in range(h):
            g[r][0] = 4; g[r][w - 1] = 6
        for c in range(w):
            g[0][c] = 3; g[h - 1][c] = 8
        return g
    if name == "multiple_motifs":
        # two separate motifs → bbox spans both, includes empty space between (rule keeps gap)
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[6][7] = 6; g[6][8] = 6; g[7][8] = 6
        return g
    return g
