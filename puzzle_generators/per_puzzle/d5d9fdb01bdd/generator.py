"""Generator for arc_puzzle_bank_21_set16_bundle:easy_p07.

The output is the transpose of the tight crop around all nonzero cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, crop_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_nonzero, content_fills_grid, single_cell_content.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d5d9fdb01bdd"
VERSION = "1.1.0"
TASK_ID = "d5d9fdb01bdd"
SUMMARY = "Sparse active pattern embedded in a zero border, then crop-transposed."

INVARIANTS = [
    "background is 0",
    "nonzero cells occupy a proper interior bounding box",
    "active pattern has multiple colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_nonzero", "content_fills_grid", "single_cell_content")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "crop_h":         {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "palette_size":   {"type": "int", "default": "4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "2..6"},
    "density":        {"type": "str", "default": "medium", "valid": "medium"},
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
        ch = min(ctx.draw_int("crop_h", 3, 4), h - 2)
        cw = min(ctx.draw_int("crop_w", 4, 5), w - 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        ch = min(ctx.draw_int("crop_h", 4, 5), h - 2)
        cw = min(ctx.draw_int("crop_w", 5, 6), w - 2)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 8, 12)
        ch = min(ctx.draw_int("crop_h", 3, 5), h - 2)
        cw = min(ctx.draw_int("crop_w", 4, 6), w - 2)
    colors = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    r0 = rng.randint(1, h - ch - 1)
    c0 = rng.randint(1, w - cw - 1)
    positions = [(r0 + r, c0 + c) for r in range(ch) for c in range(cw)]
    rng.shuffle(positions)
    for i, (r, c) in enumerate(positions[:max(5, (ch * cw) // 2)]):
        g[r][c] = colors[i % len(colors)]
    for i, (r, c) in enumerate([(r0, c0), (r0, c0 + cw - 1), (r0 + ch - 1, c0), (r0 + ch - 1, c0 + cw - 1)]):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_nonzero":
        # no nonzero cells → bbox empty, transpose+crop is undefined
        return g
    if name == "content_fills_grid":
        # nonzero cells span the full grid → crop is identity, only transpose flips
        for r in range(h):
            for c in range(w):
                g[r][c] = 1 + ((r * 3 + c) % 4)
        return g
    if name == "single_cell_content":
        # exactly one nonzero cell → crop is 1×1, transpose is identity
        g[3][5] = 6
        return g
    return g
