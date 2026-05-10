"""Generator for arc_puzzle_bank_eleventh_21_bundle:easy_73_crop_nonzero_bounding_box.

Rule: crop the grid to the minimal nonzero bounding box.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_h, motif_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motif, full_grid_motif, multiple_motifs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fd93f1d51f8b"
VERSION = "1.1.0"
TASK_ID = "fd93f1d51f8b"

SUMMARY = "Embed a small multicolor motif inside a larger zero grid for bbox cropping."

INVARIANTS = [
    "background is 0",
    "one nonzero motif sits strictly inside a larger canvas",
    "output is the motif's nonzero bounding box",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motif", "full_grid_motif", "multiple_motifs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_h":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "motif_w":        {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "centered_motif_with_margin",
                       "valid": "centered_motif_with_margin"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        mh = min(ctx.draw_int("motif_h", 2, 3), h - 2)
        mw = min(ctx.draw_int("motif_w", 2, 3), w - 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        mh = min(ctx.draw_int("motif_h", 3, 4), h - 2)
        mw = min(ctx.draw_int("motif_w", 4, 5), w - 2)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        mh = min(ctx.draw_int("motif_h", 2, 4), h - 2)
        mw = min(ctx.draw_int("motif_w", 2, 5), w - 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    top = rng.randint(1, h - mh - 1)
    left = rng.randint(1, w - mw - 1)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], k=rng.randint(1, 3))
    cells = {(0, 0), (mh - 1, mw - 1)}
    for _ in range(rng.randint(2, max(2, mh * mw - 1))):
        cells.add((rng.randrange(mh), rng.randrange(mw)))
    for r, c in cells:
        g[top + r][left + c] = rng.choice(colors)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_motif":
        # blank → no nonzero bbox, rule undefined
        return g
    if name == "full_grid_motif":
        # bbox spans whole grid → rule is identity
        for r in range(h):
            g[r][0] = 4; g[r][w - 1] = 6
        for c in range(w):
            g[0][c] = 3; g[h - 1][c] = 8
        return g
    if name == "multiple_motifs":
        # multiple separated motifs → bbox includes empty space between them
        g[1][1] = 4; g[1][2] = 4
        g[6][7] = 6; g[6][8] = 6
        return g
    return g
