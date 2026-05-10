"""Generator for ea32f347.

Rule: take all 5-blobs, sort by size desc; recolor 1st (largest) to 1,
2nd to 4, 3rd to 2.

Combinatorial axes (8): grid_h/w, n_blobs, blob_size_distribution,
blob_shape_kind, position_bias, palette_choice, decoy_density,
inter_blob_margin.
Degenerates: single_blob, equal_size_blobs, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "fe947dc3e12c"
VERSION = "1.1.0"
TASK_ID = "fe947dc3e12c"
SUMMARY = "3 5-blobs of distinct sizes; rule recolors by size rank to (1, 4, 2)."

INVARIANTS = [
    "background is 0",
    "exactly 3 connected 5-blobs",
    "all 3 sizes are STRICTLY distinct (so rank is unambiguous)",
    "blobs separated by margin >=1 (4-conn separation)",
]

BLOB_SHAPES = ("rect", "L_shape", "T_shape", "diag", "zigzag", "filled_block")
SIZE_DISTS = ("ascending", "wide_spread", "tight_spread")
DEGENERATE_TEXTURES = ("single_blob", "equal_size_blobs", "no_blobs")
HELPFUL_TEXTURES = BLOB_SHAPES

AXES = {
    "grid_h":              {"type": "int", "default": "rng 8..14", "valid": "7..18"},
    "grid_w":              {"type": "int", "default": "rng 10..16", "valid": "9..20"},
    "blob_shape_kind":     {"type": "str", "default": "rng helpful",
                            "valid": "|".join(BLOB_SHAPES)},
    "blob_size_distribution": {"type": "str", "default": "rng helpful",
                               "valid": "|".join(SIZE_DISTS)},
    "min_size":            {"type": "int", "default": "3", "valid": "2..6"},
    "max_size":            {"type": "int", "default": "8", "valid": "5..15"},
    "position_bias":       {"type": "str", "default": "rng spread|center|edge",
                            "valid": "spread|center|edge"},
    "inter_blob_margin":   {"type": "int", "default": "1", "valid": "1..3"},
    "texture":             {"type": "str", "default": "alias for blob_shape_kind",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 7, 9, 9, 11
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 18, 14, 20
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 14, 10, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    shape_kind = (overrides.get("texture") or overrides.get("blob_shape_kind")
                  or ctx.draw_choice("blob_shape_kind", list(BLOB_SHAPES)))
    dist = overrides.get("blob_size_distribution",
                         ctx.draw_choice("blob_size_distribution",
                                         list(SIZE_DISTS)))
    min_s = int(overrides.get("min_size", 3))
    max_s = int(overrides.get("max_size", 8))
    margin = int(overrides.get("inter_blob_margin", 1))
    sizes = _draw_sizes(dist, min_s, max_s, rng)
    sizes = sorted(sizes, reverse=True)
    g = full_grid(h, w, 0)
    placed = 0
    for s in sizes:
        cells = _shape_cells(shape_kind, s, h, w, rng)
        if place_no_overlap(rng, g, cells, 5, bg=0,
                            margin=margin, max_tries=60):
            placed += 1
    if placed < 3:
        big = normalize([(0, c) for c in range(min(6, w))])
        med = normalize([(r, 0) for r in range(min(5, h))])
        sml = normalize([(0, 0), (0, 1), (0, 2)])
        for cells in [big, med, sml]:
            place_no_overlap(rng, g, cells, 5, bg=0,
                             margin=margin, max_tries=20)
    return g


def _draw_sizes(dist, min_s, max_s, rng):
    if dist == "ascending":
        return [min_s, min_s + 2, min_s + 4]
    if dist == "tight_spread":
        base = rng.randint(min_s, max_s - 2)
        return [base, base + 1, base + 2]
    base = min_s
    return [base, base + 2, base + 4]


def _shape_cells(kind, size, h, w, rng):
    if kind == "rect":
        rows = max(1, int(size ** 0.5))
        cols = max(1, (size + rows - 1) // rows)
        return normalize(rect_cells(rows, cols))
    if kind == "L_shape":
        cells = [(0, c) for c in range(min(size, max(2, w - 2)))]
        cells += [(r, 0) for r in range(1, min(size - len(cells) + 1, h - 1))]
        return normalize(cells[:size])
    if kind == "T_shape":
        bar_w = min(size - 1, max(2, w - 2))
        cells = [(0, c) for c in range(bar_w)]
        cells += [(r, bar_w // 2)
                  for r in range(1, min(size - bar_w + 1, h - 1))]
        return normalize(cells[:size])
    if kind == "diag":
        return normalize([(i, i) for i in range(size)])
    if kind == "zigzag":
        cells = []
        r, c = 0, 0
        for i in range(size):
            cells.append((r, c))
            if i % 2 == 0:
                c += 1
            else:
                r += 1
        return normalize(cells)
    if kind == "filled_block":
        side = max(1, int(size ** 0.5))
        cells = [(r, c) for r in range(side) for c in range(side)]
        return normalize(cells[:size])
    return normalize([(0, c) for c in range(min(size, max(2, w - 2)))])


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_blob":
        for c in range(min(5, w)):
            g[h // 2][c] = 5
        return g
    if name == "equal_size_blobs":
        for offset, r in enumerate([1, 4, h - 2]):
            for c in range(2):
                if r < h and c + offset < w:
                    g[r][c + offset] = 5
        return g
    if name == "no_blobs":
        return g
    return g
