"""Generator for arc_puzzle_bank_eighth21:M55 — remove border-touching blobs.

Rule: drop blobs whose bbox touches any of the 4 grid borders. Keep
interior blobs.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_border_blobs, no_interior_blobs, all_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "f3672f3f540b"
VERSION = "1.1.0"
TASK_ID = "f3672f3f540b"
SUMMARY = "≥1 border-touching blob (dropped) + ≥1 interior blob (kept)."

INVARIANTS = [
    "background is 0",
    "≥1 blob touches some grid border",
    "≥1 blob is fully interior (no cell on any border)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_border_blobs", "no_interior_blobs", "all_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "border_plus_interior_mix",
                       "valid": "border_plus_interior_mix"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    for _ in range(40):
        c0 = rng.randint(0, w - 2)
        cells = {(0, c0), (0, c0 + 1), (1, c0)}
        if any(p in used for p in cells): continue
        for r, c in cells: g[r][c] = palette[0]
        used |= cells
        break
    interior_used = set(used)
    for r in range(h):
        interior_used.add((r, 0))
        interior_used.add((r, w - 1))
    for c in range(w):
        interior_used.add((0, c))
        interior_used.add((h - 1, c))
    for color in palette[1:]:
        cells = grow_blob(rng, h, w, interior_used, rng.randint(2, 4), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            interior_used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_border_blobs":
        # only interior blobs → rule fires zero times, output identical
        for (r, c) in [(2, 3), (2, 4), (3, 3)]: g[r][c] = 4
        for (r, c) in [(5, 6), (6, 6), (6, 7)]: g[r][c] = 6
        return g
    if name == "no_interior_blobs":
        # only border-touching blobs → all dropped, output blank
        for (r, c) in [(0, 1), (0, 2), (1, 1)]: g[r][c] = 4
        for (r, c) in [(h - 1, 5), (h - 1, 6), (h - 2, 5)]: g[r][c] = 6
        return g
    if name == "all_border":
        # every blob touches some border → output blank
        for (r, c) in [(0, 2), (1, 2)]: g[r][c] = 4
        for (r, c) in [(0, 8), (0, 9)]: g[r][c] = 6
        for (r, c) in [(h - 1, 4), (h - 1, 5)]: g[r][c] = 3
        return g
    return g
