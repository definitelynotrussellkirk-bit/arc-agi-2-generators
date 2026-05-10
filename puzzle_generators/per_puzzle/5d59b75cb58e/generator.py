"""Generator for arc_puzzle_bank_21_set4:S4_M3 — main-diagonal mirror (transpose-add).

Rule: every non-zero cell at (r, c) gets its mirror at (c, r) painted
(transpose). Original cells stay.

Combinatorial axes (8): side, palette_kind, n_blobs, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: blob_on_diagonal, blob_already_symmetric, empty_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "5d59b75cb58e"
VERSION = "1.1.0"
TASK_ID = "5d59b75cb58e"
SUMMARY = "Square grid with a small blob away from main diagonal (transpose differs)."

INVARIANTS = [
    "background is 0",
    "grid is square (h == w)",
    "blob is asymmetric across the main diagonal so transpose-add is non-trivial",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("blob_on_diagonal", "blob_already_symmetric", "empty_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "side":           {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "1..3"},
    "blob_size":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "off_diagonal",
                       "valid": "off_diagonal"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..3"},
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
        n = ctx.draw_int("side", 7, 7)
    elif difficulty == "hard":
        n = ctx.draw_int("side", 8, 9)
    else:
        n = ctx.draw_int("side", 7, 9)
    h = w = n
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 2)
    used: set[tuple[int, int]] = set()
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=20)
            if cells is None:
                continue
            if any(r == c for r, c in cells):
                continue
            mirrors = {(c, r) for r, c in cells}
            if mirrors & cells:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells | mirrors
            break
    return g


def _draw_from_degenerate(name, rng):
    h = w = 8
    g = full_grid(h, w, 0)
    if name == "blob_on_diagonal":
        # blob includes diagonal cells → transpose-add coincides with itself there, no clean signal
        for r, c in [(2, 2), (3, 3), (4, 4)]:
            g[r][c] = 4
        return g
    if name == "blob_already_symmetric":
        # blob and its transpose-mirror both painted → rule is identity on this input
        pairs = [(1, 5), (5, 1), (2, 6), (6, 2)]
        for r, c in pairs:
            g[r][c] = 7
        return g
    if name == "empty_grid":
        # no nonzero cells → transpose has nothing to add
        return g
    return g
