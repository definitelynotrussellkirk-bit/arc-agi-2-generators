"""Generator for 4b:m24 — keep even-area blobs.

Rule: keep blobs with even cell count; drop odd-area blobs.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_even_blobs, no_odd_blobs, all_size_2.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "bbb0f21653d8"
VERSION = "1.1.0"
TASK_ID = "bbb0f21653d8"
SUMMARY = "≥1 even-area blob (kept) + ≥1 odd-area blob (dropped)."

INVARIANTS = [
    "background is 0",
    "≥1 blob with even cell count",
    "≥1 blob with odd cell count",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_even_blobs", "no_odd_blobs", "all_size_2")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "non_touching",
                       "valid": "non_touching"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
    sizes = [3, 4, 5]
    rng.shuffle(sizes)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
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
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_even_blobs":
        # all odd-area → rule drops everything, output blank
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 3
        for r, c in [(5, 5)]: g[r][c] = 5
        for r, c in [(7, 1), (7, 2), (7, 3), (8, 1), (8, 3)]: g[r][c] = 7
        return g
    if name == "no_odd_blobs":
        # all even-area → rule keeps everything, identity
        for r, c in [(1, 1), (1, 2)]: g[r][c] = 3
        for r, c in [(5, 5), (5, 6), (6, 5), (6, 6)]: g[r][c] = 5
        return g
    if name == "all_size_2":
        # all blobs size 2 → all kept, no contrast vs. dropped
        for r, c in [(1, 1), (1, 2)]: g[r][c] = 3
        for r, c in [(4, 5), (5, 5)]: g[r][c] = 5
        for r, c in [(7, 1), (7, 2)]: g[r][c] = 7
        return g
    return g
