"""Generator for 20_bundle:m139 — recolor by area parity.

Rule: blob with odd area → 3, even area → 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_odd, all_even, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "ea763f9c5b1d"
VERSION = "1.1.0"
TASK_ID = "ea763f9c5b1d"
SUMMARY = "≥1 even-area blob + ≥1 odd-area blob (both in same input color)."

INVARIANTS = [
    "background is 0",
    "≥1 blob with odd cell count, ≥1 blob with even cell count",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_odd", "all_even", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "mixed_parity_blobs",
                       "valid": "mixed_parity_blobs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = 6
    # one odd-area, one even-area
    sizes = [3, 4]
    rng.shuffle(sizes)
    used: set[tuple[int, int]] = set()
    for size in sizes + [rng.randint(2, 5)]:
        cells = grow_blob(rng, h, w, used, size, max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = color
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "all_odd":
        # all blobs odd-area → all recolor to 3 (uniform), no even-parity case
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 6   # size 3
        for (r, c) in [(1, 5), (1, 6), (2, 6)]: g[r][c] = 6   # size 3
        for (r, c) in [(6, 3), (6, 4), (7, 3), (7, 4), (8, 4)]: g[r][c] = 6   # size 5
        return g
    if name == "all_even":
        # all blobs even-area → all recolor to 4 (uniform), no odd-parity case
        for (r, c) in [(1, 1), (1, 2)]: g[r][c] = 6   # size 2
        for (r, c) in [(1, 5), (1, 6), (2, 5), (2, 6)]: g[r][c] = 6   # size 4
        for (r, c) in [(6, 3), (6, 4)]: g[r][c] = 6   # size 2
        return g
    if name == "no_blobs":
        # blank → no blobs to classify
        return g
    return g
