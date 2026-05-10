"""Generator for arc_puzzle_bank_sixteenth21:M110 — transplant blob into frame.

Rule: a blob outside the frame + a 5-rect-frame. Output: empty grid +
blob moved inside the frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_blob, blob_inside_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "dded62bb9e3a"
VERSION = "1.1.0"
TASK_ID = "dded62bb9e3a"
SUMMARY = "A 5-frame ≥4×4 + a blob outside it that fits inside the interior."

INVARIANTS = [
    "background is 0",
    "exactly one rect-frame in color 5",
    "exactly one non-5 blob outside the frame",
    "blob's bbox fits inside the frame interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_blob", "blob_inside_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "5frame_with_external_blob",
                       "valid": "5frame_with_external_blob"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    fh = rng.randint(4, 5); fw = rng.randint(4, 5)
    r1 = h - fh; c1 = w - fw
    r2 = r1 + fh - 1; c2 = c1 + fw - 1
    for c in range(c1, c2 + 1):
        g[r1][c] = 5; g[r2][c] = 5
    for r in range(r1, r2 + 1):
        g[r][c1] = 5; g[r][c2] = 5
    used = {(r, c) for r in range(h) for c in range(w) if g[r][c] != 0}
    for r in range(h):
        for c in range(w):
            if r >= r1 - 1 or c >= c1 - 1:
                used.add((r, c))
    color = rng.choice([2, 3, 4, 6, 7, 8, 9])
    cells = grow_blob(rng, h, w, used, rng.randint(2, 3), max_attempts=80)
    if cells:
        for r, c in cells:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # blob without 5-frame → no destination container
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        return g
    if name == "no_blob":
        # frame only, no blob → nothing to transplant
        for c in range(4, 9): g[3][c] = 5; g[7][c] = 5
        for r in range(3, 8): g[r][4] = 5; g[r][8] = 5
        return g
    if name == "blob_inside_frame":
        # blob already inside frame → "outside" precondition fails
        for c in range(4, 9): g[3][c] = 5; g[7][c] = 5
        for r in range(3, 8): g[r][4] = 5; g[r][8] = 5
        for r, c in [(5, 6), (5, 7), (6, 6)]: g[r][c] = 4
        return g
    return g
