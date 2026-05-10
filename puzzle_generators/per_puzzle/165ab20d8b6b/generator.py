"""Generator for arc_puzzle_bank_21_set18_bundle:medium_p04 — orthogonal contact shell.

Rule: each blob → paint its 4-orthogonal neighbor cells (that are 0)
with the blob's color. The blob itself is erased.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, single_cell_blobs, blob_at_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "165ab20d8b6b"
VERSION = "1.1.0"
TASK_ID = "165ab20d8b6b"
SUMMARY = "2-3 distinct-color blobs (size ≥ 2) with room around them for the shell."

INVARIANTS = [
    "background is 0",
    "blobs of size >= 2 (so shell is non-trivial)",
    "blobs are 4-disjoint and have at least one ortho neighbor cell that is 0",
    "blobs don't touch the grid border (so shell stays in-bounds)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "single_cell_blobs", "blob_at_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "interior_blobs_with_shell_room",
                       "valid": "interior_blobs_with_shell_room"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_blobs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("n_blobs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("n_blobs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    # reserve border so blobs don't touch edges
    for r in range(h):
        used.add((r, 0)); used.add((r, w - 1))
    for c in range(w):
        used.add((0, c)); used.add((h - 1, c))
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in palette:
        for _ in range(40):
            cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=20)
            if cells is None:
                continue
            for r, c in cells:
                g[r][c] = color
            used |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no blobs to expand into shells
        return g
    if name == "single_cell_blobs":
        # size-1 blobs → shell rule still applies but no internal structure
        g[3][3] = 4
        g[6][7] = 6
        return g
    if name == "blob_at_border":
        # blob touches grid border → shell would extend out of bounds
        g[0][0] = 4; g[0][1] = 4
        g[h - 1][w - 1] = 6; g[h - 1][w - 2] = 6
        return g
    return g
