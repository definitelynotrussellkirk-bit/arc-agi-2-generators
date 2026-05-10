"""Generator for 6ca952ad.

Rule: bg=7. For each non-bg blob, if size >=4 drop so r2 = h-1; smaller
blobs stay in place.

Combinatorial axes (8): grid_h/w, n_big_blobs, n_small_blobs,
big_blob_shape, small_blob_shape, position_bias, palette_size,
inter_blob_margin.
Degenerates: all_small, all_big, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "f13d23b71bd4"
VERSION = "1.1.0"
TASK_ID = "f13d23b71bd4"
SUMMARY = "7-bg grid; rule drops blobs of size >=4 to bottom; smaller blobs stay."

INVARIANTS = [
    "background is 7",
    ">=1 big blob (size >=4) so 'drop' branch fires",
    ">=1 small blob (size <=3) so 'stay' branch fires",
    "blobs separated by 4-conn (so each is its own object)",
    "big blobs leave room above them (so dropping is visible)",
]

BIG_SHAPES = ("vertical_bar", "L_shape", "T_shape", "block_2x2",
              "diag", "wide_rect")
SMALL_SHAPES = ("single", "horizontal_pair", "vertical_pair",
                "L_triplet", "diag_pair")
DEGENERATE_TEXTURES = ("all_small", "all_big", "no_blobs")
HELPFUL_TEXTURES = ("balanced", "many_big", "many_small")

AXES = {
    "grid_h":             {"type": "int", "default": "rng 7..14", "valid": "6..18"},
    "grid_w":             {"type": "int", "default": "rng 7..14", "valid": "6..18"},
    "n_big_blobs":        {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "n_small_blobs":      {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "big_blob_shape":     {"type": "str", "default": "rng helpful",
                           "valid": "|".join(BIG_SHAPES)},
    "small_blob_shape":   {"type": "str", "default": "rng helpful",
                           "valid": "|".join(SMALL_SHAPES)},
    "position_bias":      {"type": "str", "default": "rng spread|top_biased",
                           "valid": "spread|top_biased"},
    "inter_blob_margin":  {"type": "int", "default": "1", "valid": "1..3"},
    "texture":            {"type": "str", "default": "rng helpful",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 7, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    texture = overrides.get("texture",
                            ctx.draw_choice("texture", list(HELPFUL_TEXTURES)))
    if texture == "many_big":
        n_big, n_small = 3, 1
    elif texture == "many_small":
        n_big, n_small = 1, 3
    else:
        n_big = int(overrides.get("n_big_blobs",
                                  ctx.draw_int("n_big_blobs", 1, 2)))
        n_small = int(overrides.get("n_small_blobs",
                                    ctx.draw_int("n_small_blobs", 1, 3)))
    n_big = max(1, min(4, n_big))
    n_small = max(1, min(5, n_small))
    big_shape = overrides.get("big_blob_shape",
                              ctx.draw_choice("big_blob_shape",
                                              list(BIG_SHAPES)))
    small_shape = overrides.get("small_blob_shape",
                                ctx.draw_choice("small_blob_shape",
                                                list(SMALL_SHAPES)))
    margin = int(overrides.get("inter_blob_margin", 1))
    palette = list(ctx.draw_distinct_colors("palette",
                                            n=max(2, n_big + n_small),
                                            exclude={7}))
    while len(palette) < n_big + n_small:
        palette.append(palette[0])
    g = full_grid(h, w, 7)
    placed_big = 0
    for i in range(n_big):
        cells = _big_cells(big_shape, h, w, rng)
        if place_no_overlap(rng, g, cells, palette[i], bg=7,
                            margin=margin, max_tries=40):
            placed_big += 1
    placed_small = 0
    for i in range(n_small):
        cells = _small_cells(small_shape, rng)
        color = palette[(n_big + i) % len(palette)]
        if place_no_overlap(rng, g, cells, color, bg=7,
                            margin=margin, max_tries=40):
            placed_small += 1
    if placed_big < 1:
        cells = normalize([(0, 0), (1, 0), (2, 0), (3, 0)])
        place_no_overlap(rng, g, cells, palette[0], bg=7,
                         margin=1, max_tries=20)
    if placed_small < 1:
        cells = normalize([(0, 0)])
        place_no_overlap(rng, g, cells,
                         palette[1] if len(palette) > 1 else palette[0],
                         bg=7, margin=1, max_tries=20)
    return g


def _big_cells(kind, h, w, rng):
    if kind == "vertical_bar":
        n = rng.randint(4, max(4, h // 2))
        return normalize([(i, 0) for i in range(n)])
    if kind == "L_shape":
        n = rng.randint(4, 5)
        cells = [(0, c) for c in range(min(3, n))]
        cells += [(r, 0) for r in range(1, n - len(cells) + 1)]
        return normalize(cells[:n])
    if kind == "T_shape":
        return normalize([(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)])
    if kind == "block_2x2":
        return normalize([(0, 0), (0, 1), (1, 0), (1, 1)])
    if kind == "diag":
        n = rng.randint(4, 5)
        return normalize([(i, i) for i in range(n)])
    if kind == "wide_rect":
        return normalize(rect_cells(2, rng.randint(3, 4)))
    return normalize([(0, 0), (1, 0), (2, 0), (3, 0)])


def _small_cells(kind, rng):
    if kind == "horizontal_pair":
        return normalize([(0, 0), (0, 1)])
    if kind == "vertical_pair":
        return normalize([(0, 0), (1, 0)])
    if kind == "L_triplet":
        return normalize([(0, 0), (1, 0), (1, 1)])
    if kind == "diag_pair":
        return normalize([(0, 0), (1, 1)])
    return normalize([(0, 0)])


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 7)
    palette = [c for c in range(1, 10) if c != 7]
    rng.shuffle(palette)
    if name == "all_small":
        for i, c in enumerate([1, 3, 5]):
            if c < w and i < len(palette):
                g[h // 2][c] = palette[i]
        return g
    if name == "all_big":
        for r in range(min(4, h)):
            g[r][2] = palette[0]
        for r in range(min(4, h)):
            if r + 5 < w:
                g[r][r + 5] = palette[1] if len(palette) > 1 else palette[0]
        return g
    if name == "no_blobs":
        return g
    return g
