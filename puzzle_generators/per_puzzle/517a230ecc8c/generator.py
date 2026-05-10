"""Generator for arc_puzzle_bank_21_set7_s:S7_M7 — one-step object halo.

Rule: every 0-cell whose 4-orthogonal neighbors are all 0 OR all the
same (single) non-zero color — gets painted that color. Effectively
expands each blob by 1 cell in 4 cardinals.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, blob_on_border, halo_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "517a230ecc8c"
VERSION = "1.1.0"
TASK_ID = "517a230ecc8c"
SUMMARY = "2-3 distinct-color blobs spaced apart so their dilated halos don't overlap."

INVARIANTS = [
    "background is 0",
    "blobs separated by ≥3 cells in 4-norm (dilated halos disjoint)",
    "blobs not on grid border (so halos stay in-bounds)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "blob_on_border", "halo_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "spaced_blobs_interior",
                       "valid": "spaced_blobs_interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    for r in range(h):
        for c in range(w):
            if r < 1 or r >= h - 1 or c < 1 or c >= w - 1:
                used.add((r, c))
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=20)
            if cells is None:
                continue
            dilated = set()
            for r, c in cells:
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        dilated.add((r + dr, c + dc))
            if dilated & used:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= dilated
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no blobs to dilate; output equals input.
        return g
    if name == "blob_on_border":
        # Blob touches grid border — its halo would extend off-grid;
        # rule's expand-by-1 has no destination cells outside.
        for r, c in [(0, 0), (0, 1), (1, 0)]: g[r][c] = 4
        return g
    if name == "halo_overlap":
        # Two blobs of distinct colors so close that their 1-step
        # halos overlap on the same 0-cell — rule's "all same color"
        # neighborhood test produces ambiguous color for the overlap.
        for r, c in [(2, 2), (2, 3)]: g[r][c] = 4
        for r, c in [(2, 5), (2, 6)]: g[r][c] = 6
        return g
    return g
