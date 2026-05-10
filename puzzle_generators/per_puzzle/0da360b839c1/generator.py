"""Generator for arc_puzzle_bank_seventh21:M49 — point-reflect about 9-anchor.

Rule: a 9-cell is the anchor. Every other non-zero cell is reflected
through the anchor: (r, c) → (2*ar - r, 2*ac - c). Original cells are
erased; the 9-cell stays.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, anchor_only, reflection_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0da360b839c1"
VERSION = "1.1.0"
TASK_ID = "0da360b839c1"
SUMMARY = "Single 9-anchor + a small multi-color blob; reflected positions are in-bounds."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell (anchor) at the grid center area",
    "non-9 cells reflect through anchor and stay in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "anchor_only", "reflection_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "anchor_center_cells_one_side",
                       "valid": "anchor_center_cells_one_side"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    ar = h // 2 + rng.choice([-1, 0, 0, 1])
    ac = w // 2 + rng.choice([-1, 0, 0, 1])
    g[ar][ac] = 9
    used = {(ar, ac)}
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 2)
    for color in palette:
        for _ in range(40):
            dr = rng.randint(-min(ar, h - 1 - ar), 0) if ar > 0 else 0
            dc = rng.randint(-min(ac, w - 1 - ac), 0) if ac > 0 else 0
            r = ar + dr
            c = ac + dc
            if (r, c) in used or g[r][c] != 0:
                continue
            mr = 2 * ar - r
            mc = 2 * ac - c
            if not (0 <= mr < h and 0 <= mc < w):
                continue
            g[r][c] = color
            used.add((r, c))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # Cells but no 9-anchor — rule has no center to reflect about.
        g[2][3] = 4; g[5][1] = 6
        return g
    if name == "anchor_only":
        # 9-anchor but no cells to reflect — rule has nothing to do.
        g[h // 2][w // 2] = 9
        return g
    if name == "reflection_oob":
        # 9-anchor near corner with cells whose reflection lands
        # out of bounds — rule's reflection cannot be drawn.
        g[1][1] = 9
        g[0][0] = 4
        g[0][1] = 6
        return g
    return g
