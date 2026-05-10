"""Generator for arc_puzzle_bank_21_set5_s:S5_M4 — sort colors by area.

Rule: extract objects (4-conn). Output = a single row of object colors
sorted ascending by object size (cell count). Distinct sizes => stable
ranking; same color appears once per object.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes, single_blob, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "346c1552c4eb"
VERSION = "1.1.0"
TASK_ID = "346c1552c4eb"
SUMMARY = "3-5 distinct-color blobs of strictly distinct sizes, well-separated."

INVARIANTS = [
    "background is 0",
    "every blob is 4-connected and has a distinct size from every other blob",
    "every blob has a distinct color",
    "blobs are separated (not 4-touching) so connectivity doesn't merge them",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_blob", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("n_blobs", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_blobs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        n = ctx.draw_int("n_blobs", 3, 5)
    rng = ctx.draw_rng("layout")
    sizes = rng.sample(range(1, 8), n)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    for size, color in zip(sizes, palette):
        cells = grow_blob(rng, h, w, used, size, max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = color
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    import random
    rng = random.Random(0)
    h, w = 10, 10
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    if name == "tied_sizes":
        # multiple blobs share the same size → "strictly distinct sizes" invariant violated, sort ambiguous
        for color in (3, 5, 7):
            cells = grow_blob(rng, h, w, used, 3, max_attempts=80)
            if cells is None:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
        return g
    if name == "single_blob":
        # one blob → output is single-element row, sort is trivial
        cells = grow_blob(rng, h, w, used, 4, max_attempts=80)
        if cells:
            for r, c in cells:
                g[r][c] = 6
        return g
    if name == "no_blobs":
        # empty grid → output is empty row, ambiguous shape
        return g
    return g
