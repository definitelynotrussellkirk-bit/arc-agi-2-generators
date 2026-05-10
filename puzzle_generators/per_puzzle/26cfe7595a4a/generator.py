"""Generator for additional_bank:E6.

Rule: a compact multicolor nonzero motif is padded by background;
output is a tight crop to that motif's bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: full_grid, single_color, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "26cfe7595a4a"
VERSION = "1.1.0"
TASK_ID = "26cfe7595a4a"
SUMMARY = "A compact multicolor nonzero motif is padded by background for tight cropping."

INVARIANTS = [
    "background is 0",
    "there are multiple nonzero cells",
    "nonzero cells sit inside a smaller bbox than the input grid",
    "the motif uses at least two nonzero colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("full_grid", "single_color", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_size":     {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "padded_interior",
                       "valid": "padded_interior"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "compact", "valid": "compact"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 7, 11)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    rng = ctx.draw_rng("motif")
    g = full_grid(h, w, 0)
    mh = rng.randint(2, min(4, h - 2))
    mw = rng.randint(2, min(4, w - 2))
    rr = rng.randint(1, h - mh - 1)
    rc = rng.randint(1, w - mw - 1)
    for r in range(mh):
        for c in range(mw):
            if rng.random() < 0.7 or (r, c) in ((0, 0), (mh - 1, mw - 1)):
                g[rr + r][rc + c] = colors[(r + c) % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "full_grid":
        # entire grid is nonzero → no padding to crop, output equals input
        for r in range(h):
            for c in range(w):
                g[r][c] = ((r + c) % 2 + 2)
        return g
    if name == "single_color":
        # motif uses just one color → multicolor invariant violated
        for r, c in [(2, 2), (2, 3), (3, 2), (3, 3), (4, 4)]:
            g[r][c] = 5
        return g
    if name == "no_motif":
        # no nonzero cells → bbox is undefined, crop is empty/identity
        return g
    return g
