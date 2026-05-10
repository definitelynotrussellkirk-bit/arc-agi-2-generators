"""Generator for arc_additional_puzzles_21_set14_bundle:H98 — color analogy transfer.

Rule: full-col color-1 dividers split into 3 panels. Panel A and panel B share the
same shape (after crop) but with a per-cell color mapping. Build the color map
from A→B and apply it to panel C's cropped shape; output the recolored C.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers (no color-1 separators → rule cannot identify
panels); identity_recolor (A == B — color map is identity); no_C_content
(panel C empty → rule's recolor input is empty).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6be78d0010df"
VERSION = "1.1.0"
TASK_ID = "6be78d0010df"

SUMMARY = "3 NxN panels split by color-1 dividers; A→B is a consistent color map applied to C."

INVARIANTS = [
    "background is 0",
    "two full-height color-1 divider columns split the grid into three equal-width panels",
    "panels A and B share an identical shape (cropped) under a consistent A→B color permutation",
    "panel C contains a shape using a subset of A's colors so the map applies",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "identity_recolor", "no_C_content")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_n":           {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "n_colors_used":     {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..5", "valid": "4..7"},
    "position_bias":     {"type": "str", "default": "three_panels_with_color_analogy",
                          "valid": "three_panels_with_color_analogy"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "4..7"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _rand_cells(rng, n, k):
    cells = [(rng.randint(0, n - 1), rng.randint(0, n - 1))]
    seen = set(cells)
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        n = ctx.draw_int("panel_n", 5, 5)
        n_colors = ctx.draw_int("n_colors_used", 2, 2)
    elif difficulty == "hard":
        n = ctx.draw_int("panel_n", 6, 6)
        n_colors = ctx.draw_int("n_colors_used", 3, 3)
    else:
        n = ctx.draw_int("panel_n", 5, 6)
        n_colors = ctx.draw_int("n_colors_used", 2, 3)
    rng = ctx.draw_rng("layout")
    h = n
    w = n * 3 + 2
    d1, d2 = n, 2 * n + 1

    for outer in range(40):
        src_palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n_colors)
        tgt_palette = rng.sample([c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c not in src_palette], n_colors)
        cmap = dict(zip(src_palette, tgt_palette))

        k = rng.randint(4, max(4, n + 1))
        cells_s = _rand_cells(rng, n, k)
        per_cell_color = []
        forced = list(src_palette)
        rng.shuffle(forced)
        for i, cell in enumerate(cells_s):
            if i < len(forced):
                per_cell_color.append(forced[i])
            else:
                per_cell_color.append(rng.choice(src_palette))

        g = full_grid(h, w, 0)
        for r in range(h):
            g[r][d1] = 1
            g[r][d2] = 1
        for (r, c), col in zip(cells_s, per_cell_color):
            g[r][c] = col
        for (r, c), col in zip(cells_s, per_cell_color):
            g[r][d1 + 1 + c] = cmap[col]

        kc = rng.randint(3, max(3, n))
        cells_c = _rand_cells(rng, n, kc)
        for cell in cells_c:
            r, c = cell
            g[r][d2 + 1 + c] = rng.choice(src_palette)
        return g
    raise ValueError("could not realize 3-panel color analogy in 40 attempts")


def _draw_from_degenerate(name, rng):
    n = 5
    h = n
    w = n * 3 + 2
    g = full_grid(h, w, 0)
    if name == "no_dividers":
        # No color-1 dividers — rule cannot identify panels.
        for r, c in [(0, 0), (1, 0), (1, 1)]:
            g[r][c] = 4
        return g
    if name == "identity_recolor":
        # A == B — recolor map is identity.
        for r in range(h):
            g[r][n] = 1
            g[r][2 * n + 1] = 1
        for r, c, color in [(0, 0, 4), (1, 0, 5), (1, 1, 4)]:
            g[r][c] = color
            g[r][n + 1 + c] = color
        for r, c in [(0, 0), (1, 0), (1, 1)]:
            g[r][2 * n + 2 + c] = 4
        return g
    if name == "no_C_content":
        # Panel C empty.
        for r in range(h):
            g[r][n] = 1
            g[r][2 * n + 1] = 1
        for r, c in [(0, 0), (1, 0), (1, 1)]:
            g[r][c] = 4
        for r, c in [(0, 1), (1, 0), (1, 1)]:
            g[r][n + 1 + c] = 6
        return g
    return g
