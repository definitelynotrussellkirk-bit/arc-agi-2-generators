"""Generator for 14b:m97 — sort cropped objects by width, pack.

Rule: sort blobs by bbox-width, pack horizontally.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, tied_widths.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "7b3c2eaee231"
VERSION = "1.1.0"
TASK_ID = "7b3c2eaee231"
SUMMARY = "3 distinct-color blobs of strictly distinct widths."

INVARIANTS = [
    "background is 0",
    "3 distinct-color blobs with strictly distinct bbox widths",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "tied_widths")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "distinct_width_blobs",
                       "valid": "distinct_width_blobs"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    used: set[tuple[int, int]] = set()
    seen_widths = set()
    for color in palette:
        for _ in range(60):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=20)
            if cells is None:
                continue
            cs = [c for _, c in cells]
            bb_w = max(cs) - min(cs) + 1
            if bb_w in seen_widths:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            seen_widths.add(bb_w)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no blobs to sort
        return g
    if name == "single_blob":
        # one blob → trivially sorted, no sort signal
        for r, c in [(2, 3), (2, 4), (3, 4)]: g[r][c] = 4
        return g
    if name == "tied_widths":
        # 2 blobs share width → "strictly distinct widths" precondition fails
        for r, c in [(1, 1), (1, 2)]: g[r][c] = 4  # width 2
        for r, c in [(4, 6), (4, 7)]: g[r][c] = 6  # width 2 (tie)
        return g
    return g
