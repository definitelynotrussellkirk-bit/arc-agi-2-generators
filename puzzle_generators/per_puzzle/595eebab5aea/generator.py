"""Generator for 11b:hard_76 — rank components by area and stack.

Rule: top row holds K rank colors. Body shapes sorted by size desc
(top K). Each top-K shape is recolored to the i-th rank color and
vstacked center-aligned with 1-row gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (≥2 body shapes share a size → "rank by size
desc" tie-break decides), no_rank_row (row 0 empty → rule's recolor
map is undefined), single_body_shape (only 1 body shape → 2 rank
colors are unused).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "595eebab5aea"
VERSION = "1.1.0"
TASK_ID = "595eebab5aea"
SUMMARY = "Top row K rank colors + 3 body shapes with strictly distinct sizes."

INVARIANTS = [
    "background is 0",
    "row 0 has 3 isolated rank-color cells (distinct colors), rest of row 0 is bg",
    "body has 3 multi-cell shapes with strictly distinct sizes (and non-rank colors)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "no_rank_row", "single_body_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "11..18"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "12..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "6", "valid": "6..6"},
    "position_bias":  {"type": "str", "default": "ranks_plus_three_body_shapes",
                       "valid": "ranks_plus_three_body_shapes"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BY_SIZE = {
    3: [[(0, 0), (0, 1), (1, 0)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)]],
    5: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]],
    6: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]],
    7: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]],
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
        r0 = rng.randint(2, h - sh); c0 = rng.randint(0, w - sw)
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
        h = ctx.draw_int("grid_h", 12, 12)
        w = ctx.draw_int("grid_w", 13, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 16)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 13, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette_pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rank_colors = rng.sample(palette_pool, 3)
    body_colors = rng.sample([c for c in palette_pool if c not in rank_colors], 3)
    rank_cols = rng.sample(range(0, w), 3)
    for col, color in zip(rank_cols, rank_colors): g[0][col] = color
    sizes = rng.sample([3, 4, 5, 6, 7], 3)
    for size, color in zip(sizes, body_colors):
        _place(g, rng, rng.choice(_BY_SIZE[size]), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 14
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # Two body shapes share size 4 — "rank by size desc"
        # tie-break decides; output ambiguous.
        for col, color in zip([2, 6, 10], [1, 3, 5]): g[0][col] = color
        for dr, dc in _BY_SIZE[4][0]: g[3 + dr][1 + dc] = 7
        for dr, dc in _BY_SIZE[4][0]: g[3 + dr][7 + dc] = 8
        for dr, dc in _BY_SIZE[6][0]: g[8 + dr][3 + dc] = 9
        return g
    if name == "no_rank_row":
        # Row 0 empty — rule's recolor map is undefined.
        for dr, dc in _BY_SIZE[3][0]: g[3 + dr][1 + dc] = 7
        for dr, dc in _BY_SIZE[5][0]: g[3 + dr][7 + dc] = 8
        for dr, dc in _BY_SIZE[6][0]: g[9 + dr][3 + dc] = 9
        return g
    if name == "single_body_shape":
        # Only 1 body shape — 2 of 3 rank colors unused.
        for col, color in zip([2, 6, 10], [1, 3, 5]): g[0][col] = color
        for dr, dc in _BY_SIZE[5][0]: g[5 + dr][5 + dc] = 7
        return g
    return g
