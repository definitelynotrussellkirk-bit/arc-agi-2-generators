"""Generator for arc_puzzle_bank_sixth21:H41.

Rule: the left panel is a binary mask, the full 9 column is a separator, and
the right panel supplies the colors. Output the right panel values only where
the corresponding left-panel cell is nonzero.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8921bea21bbb"
VERSION = "1.1.0"
TASK_ID = "8921bea21bbb"

SUMMARY = "Apply a nonzero left-panel mask to the colored right panel."

INVARIANTS = [
    "background is 0",
    "a full column of 9 separates two equal-size panels",
    "left-panel nonzero cells define the keep mask",
    "right-panel nonzero cells carry the output colors",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 5..7", "valid": "4..9"},
    "panel_w": {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "mask_fill": {"type": "int", "default": "rng 35..70 percent", "valid": "15..90"},
    "right_fill": {"type": "int", "default": "rng 45..85 percent", "valid": "20..95"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    h = ctx.draw_int("grid_h", 5, 7)
    panel_w = ctx.draw_int("panel_w", 4, 6)
    mask_fill = ctx.draw_int("mask_fill", 35, 70)
    right_fill = ctx.draw_int("right_fill", 45, 85)
    rng = ctx.draw_rng("layout")

    sep = panel_w
    g = full_grid(h, panel_w * 2 + 1, 0)
    for r in range(h):
        g[r][sep] = 9

    mask_colors = [1, 2, 3, 4, 5, 6, 7, 8]
    right_colors = [1, 2, 3, 4, 5, 6, 7, 8]
    for r in range(h):
        for c in range(panel_w):
            if rng.randrange(100) < mask_fill:
                g[r][c] = rng.choice(mask_colors)
            if rng.randrange(100) < right_fill:
                g[r][sep + 1 + c] = rng.choice(right_colors)

    # Force one visibly kept cell and one visibly removed cell.
    g[0][0] = rng.choice(mask_colors)
    g[0][sep + 1] = rng.choice(right_colors)
    g[h - 1][panel_w - 1] = 0
    g[h - 1][sep + panel_w] = rng.choice(right_colors)
    return g
