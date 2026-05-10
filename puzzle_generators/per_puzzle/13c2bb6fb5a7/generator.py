"""Generator for arc_additional_puzzle_bank_volume14:E95.

Rule: extract subgrid bounded by min/max row/col of all non-bg cells
(crop-to-content via subgrid).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, content_fills_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import normalize, rect_cells
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "13c2bb6fb5a7"
VERSION = "1.1.0"
TASK_ID = "13c2bb6fb5a7"
SUMMARY = "Sparse non-bg content with bg padding; rule crops to the bbox of the non-bg cells."

INVARIANTS = [
    "background is 0",
    ">=1 non-bg cell",
    "non-bg content has at least 1 cell of bg margin from some grid edge",
    "input grid larger than the content bbox (so cropping shrinks)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "content_fills_grid", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..16", "valid": "6..22"},
    "grid_w":         {"type": "int", "default": "rng 9..16", "valid": "6..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
        n = ctx.draw_int("n_objects", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 16)
        w = ctx.draw_int("grid_w", 14, 16)
        n = ctx.draw_int("n_objects", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 16)
        w = ctx.draw_int("grid_w", 9, 16)
        n = ctx.draw_int("n_objects", 1, 3)
    palette_n = ctx.draw_int("fg_palette", 2, 5)
    palette = ctx.draw_distinct_colors("palette", n=palette_n, exclude={0})

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("placement")
    placed = 0
    for i in range(n):
        rh = rng.randint(1, max(1, h // 4))
        rw = rng.randint(1, max(1, w // 4))
        cells = normalize(rect_cells(rh, rw))
        color = palette[i % len(palette)]
        if place_no_overlap(rng, g, cells, color, bg=0, margin=1, max_tries=30):
            placed += 1
    if placed == 0:
        rr = rng.randint(1, h - 2); rc = rng.randint(1, w - 2)
        g[rr][rc] = palette[0]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # no non-bg cells → bbox undefined, rule output is empty/ambiguous
        return g
    if name == "content_fills_grid":
        # non-bg content already spans full grid → crop is identity
        for r in range(h):
            for c in range(w):
                g[r][c] = 1 + ((r + c) % 5)
        return g
    if name == "single_cell":
        # one non-bg cell → output is 1×1, trivial cropping
        g[6][6] = 7
        return g
    return g
