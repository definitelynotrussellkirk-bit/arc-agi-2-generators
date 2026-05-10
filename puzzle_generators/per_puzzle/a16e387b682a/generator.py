"""Generator for arc_puzzle_bank_third21:M16 — recolor closest-to-center blob.

Rule: pick the blob whose bbox center is closest to the grid center
(Chebyshev/Euclidean), recolor to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_blob, tied_distances.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "a16e387b682a"
VERSION = "1.1.0"
TASK_ID = "a16e387b682a"
SUMMARY = "3 distinct-color 2x2 blobs at strictly distinct distances from grid center."

INVARIANTS = [
    "background is 0",
    "3 distinct-color blobs",
    "all 3 have strictly distinct distances (bbox-center to grid-center)",
    "blobs are 4-disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "tied_distances")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "blobs_at_distinct_distances",
                       "valid": "blobs_at_distinct_distances"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w:
        return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 3)
    centers = []
    cr, cc = h // 2, w // 2
    used_dists = set()
    for color in palette:
        for _ in range(60):
            r1 = rng.randint(0, h - 2)
            c1 = rng.randint(0, w - 2)
            if not _free(g, r1, c1, r1 + 1, c1 + 1):
                continue
            br = r1; bc = c1
            d = (br - cr) ** 2 + (bc - cc) ** 2
            if d in used_dists:
                continue
            for r in range(r1, r1 + 2):
                for c in range(c1, c1 + 2):
                    g[r][c] = color
            used_dists.add(d)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # Empty grid — rule has no candidates to score.
        return g
    if name == "single_blob":
        # Only one blob — rule's "closest" is trivially that blob;
        # rule's selection branch never has to discriminate.
        for r in range(4, 6):
            for c in range(4, 6): g[r][c] = 4
        return g
    if name == "tied_distances":
        # Two blobs equidistant from center — rule's tie-break is
        # ambiguous; selection undefined.
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        for r in range(6, 8):
            for c in range(6, 8): g[r][c] = 6
        return g
    return g
