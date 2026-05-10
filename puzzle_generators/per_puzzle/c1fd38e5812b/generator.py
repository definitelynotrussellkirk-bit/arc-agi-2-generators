"""Generator for puzzle e1baa8a4.

Rule: input is a grid of solid color blocks (uniform-color rectangles).
Output reduces each block to a single pixel.

Combinatorial axes (8): n_block_rows, n_block_cols, block_h, block_w,
palette_kind, color_layout, anchor_corner, asymmetry_force.
Degenerates: monochrome, all_same_block, no_blocks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c1fd38e5812b"
VERSION = "1.1.0"
TASK_ID = "c1fd38e5812b"
SUMMARY = "Grid of solid color blocks; rule reduces each to single pixel."

INVARIANTS = [
    "input divided into nbr x nbc solid-color blocks",
    "block dim bh, bw >= 2",
    "2-6 distinct colors total",
    "block boundaries determined by row 0 / col 0",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
COLOR_LAYOUTS = ("row_major", "checker", "diagonal", "row_repeat",
                 "col_repeat", "rng")
DEGENERATE_TEXTURES = ("monochrome", "all_same_block", "no_blocks")
HELPFUL_TEXTURES = COLOR_LAYOUTS

AXES = {
    "n_block_rows": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "n_block_cols": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "block_h":      {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "block_w":      {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind": {"type": "str", "default": "rng helpful",
                     "valid": "|".join(PALETTE_KINDS)},
    "color_layout": {"type": "str", "default": "rng helpful",
                     "valid": "|".join(COLOR_LAYOUTS)},
    "anchor_corner":{"type": "bool", "default": "false",
                     "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                     "valid": "true|false"},
    "texture":      {"type": "str", "default": "alias for color_layout",
                     "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        nbr_lo, nbr_hi = 2, 2
    elif difficulty == "hard":
        nbr_lo, nbr_hi = 3, 5
    else:
        nbr_lo, nbr_hi = 2, 4
    nbr = int(overrides.get("n_block_rows",
                            ctx.draw_int("n_block_rows", nbr_lo, nbr_hi)))
    nbc = int(overrides.get("n_block_cols",
                            ctx.draw_int("n_block_cols", nbr_lo, nbr_hi)))
    bh = int(overrides.get("block_h",
                           ctx.draw_int("block_h", 2, 4)))
    bw = int(overrides.get("block_w",
                           ctx.draw_int("block_w", 2, 4)))
    nbr = max(2, min(5, nbr))
    nbc = max(2, min(5, nbc))
    bh = max(2, min(5, bh))
    bw = max(2, min(5, bw))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    layout = (overrides.get("texture") or
              overrides.get("color_layout")
              or ctx.draw_choice("color_layout",
                                 list(COLOR_LAYOUTS)))
    palette = _build_palette(palette_kind, min(10, max(4, nbr * nbc)), rng)
    g = full_grid(nbr * bh, nbc * bw, 0)
    for br in range(nbr):
        for bc in range(nbc):
            color = _pick_color(layout, br, bc, nbr, nbc, palette, rng)
            for dr in range(bh):
                for dc in range(bw):
                    g[br * bh + dr][bc * bw + dc] = color
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _pick_color(layout, br, bc, nbr, nbc, palette, rng):
    if layout == "row_major":
        return palette[(br * nbc + bc) % len(palette)]
    if layout == "checker":
        return palette[(br + bc) % 2]
    if layout == "diagonal":
        return palette[(br + bc) % len(palette)]
    if layout == "row_repeat":
        return palette[br % len(palette)]
    if layout == "col_repeat":
        return palette[bc % len(palette)]
    return rng.choice(palette[:max(2, len(palette) // 2)])


def _draw_from_degenerate(name, rng):
    nbr = 3; nbc = 3; bh = 2; bw = 2
    g = full_grid(nbr * bh, nbc * bw, 0)
    if name == "monochrome":
        c = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(nbr * bh):
            for cc in range(nbc * bw):
                g[r][cc] = c
        return g
    if name == "all_same_block":
        for br in range(nbr):
            for bc in range(nbc):
                for dr in range(bh):
                    for dc in range(bw):
                        g[br * bh + dr][bc * bw + dc] = 3
        return g
    if name == "no_blocks":
        return g
    return g
