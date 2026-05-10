"""Generator for 18b:m126 — select ranked object and scale2.

Rule: cell (0,0) holds a rank R. Among the multi-cell components
(sorted by size ascending), pick the R-th. Crop and scale 2x.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (≥2 components share a size → "R-th by size"
tie-break decides), out_of_range_rank (R > number of components →
rule's selector finds nothing), no_rank (cell (0,0) is bg → rule's
rank is undefined / defaults to 0).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "148cea0afb09"
VERSION = "1.1.0"
TASK_ID = "148cea0afb09"
SUMMARY = "Rank value at (0,0) + 3 multi-cell shapes (same color) with distinct sizes."

INVARIANTS = [
    "background is 0",
    "cell (0,0) is a small rank value (1, 2, or 3)",
    "exactly 3 multi-cell components, all in the same color, with strictly distinct cell counts",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "out_of_range_rank", "no_rank")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "rank_plus_three_components",
                       "valid": "rank_plus_three_components"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BY_SIZE = {
    4: [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
    ],
    5: [
        [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)],
    ],
    6: [
        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
    ],
    7: [
        [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
    ],
    8: [
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    ],
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 16)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rank = rng.randint(1, 3)
    g[0][0] = rank
    color = rng.choice([2, 3, 4, 6, 7, 8, 9])
    sizes = rng.sample([4, 5, 6, 7, 8], 3)
    for size in sizes:
        _place(g, rng, rng.choice(_BY_SIZE[size]), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # Two components share size 5 — "R-th by size" is ambiguous;
        # rule's tie-break decides.
        g[0][0] = 2
        for dr, dc in _BY_SIZE[4][0]: g[2 + dr][2 + dc] = 4
        for dr, dc in _BY_SIZE[5][0]: g[2 + dr][8 + dc] = 4
        for dr, dc in _BY_SIZE[5][1]: g[7 + dr][2 + dc] = 4
        return g
    if name == "out_of_range_rank":
        # R=5 but only 3 components — rule's selector finds nothing.
        g[0][0] = 5
        for dr, dc in _BY_SIZE[4][0]: g[2 + dr][2 + dc] = 4
        for dr, dc in _BY_SIZE[5][0]: g[2 + dr][8 + dc] = 4
        for dr, dc in _BY_SIZE[6][0]: g[7 + dr][3 + dc] = 4
        return g
    if name == "no_rank":
        # (0,0) is bg — rule's rank is undefined.
        for dr, dc in _BY_SIZE[4][0]: g[2 + dr][2 + dc] = 4
        for dr, dc in _BY_SIZE[5][0]: g[2 + dr][8 + dc] = 4
        for dr, dc in _BY_SIZE[6][0]: g[7 + dr][3 + dc] = 4
        return g
    return g
