"""Generator for arc_additional_puzzles_21_set22_bundle:H153 — color analogy transfer.

Rule: full-col color-1 dividers split into 3 panels. Panel A and panel B share the
same shape (after crop) but with a per-cell color mapping. Build the color map
from A→B and apply it to panel C's cropped shape; output the recolored C.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f5b97ca6690b"
VERSION = "1.0.0"
TASK_ID = "f5b97ca6690b"

SUMMARY = "3 NxN panels split by color-1 dividers; A→B is a consistent color map applied to C."

INVARIANTS = [
    "background is 0",
    "two full-height color-1 divider columns split the grid into three equal-width panels",
    "panels A and B share an identical shape (cropped) under a consistent A→B color permutation",
    "panel C contains a shape using a subset of A's colors so the map applies",
]

AXES = {
    "panel_n": {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "n_colors_used": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
    n = ctx.draw_int("panel_n", 5, 6)
    n_colors = ctx.draw_int("n_colors_used", 2, 3)
    rng = ctx.draw_rng("layout")
    h = n
    w = n * 3 + 2
    d1, d2 = n, 2 * n + 1

    for outer in range(40):
        # source palette + target palette (a permutation)
        src_palette = rng.sample([2, 3, 4, 5, 6, 7, 8], n_colors)
        tgt_palette = rng.sample([c for c in [2, 3, 4, 5, 6, 7, 8] if c not in src_palette], n_colors)
        cmap = dict(zip(src_palette, tgt_palette))

        # shape S inside an n×n panel
        k = rng.randint(4, max(4, n + 1))
        cells_s = _rand_cells(rng, n, k)
        # assign each cell a color from src_palette (must use ALL n_colors so the cmap is fully observable)
        per_cell_color = []
        # ensure each color appears at least once
        forced = list(src_palette)
        rng.shuffle(forced)
        for i, cell in enumerate(cells_s):
            if i < len(forced):
                per_cell_color.append(forced[i])
            else:
                per_cell_color.append(rng.choice(src_palette))

        # paint A
        g = full_grid(h, w, 0)
        for r in range(h):
            g[r][d1] = 9
            g[r][d2] = 9
        for (r, c), col in zip(cells_s, per_cell_color):
            g[r][c] = col
        # paint B (same shape, mapped colors)
        for (r, c), col in zip(cells_s, per_cell_color):
            g[r][d1 + 1 + c] = cmap[col]

        # panel C: independent shape using src_palette colors (so output is non-trivial)
        kc = rng.randint(3, max(3, n))
        cells_c = _rand_cells(rng, n, kc)
        for cell in cells_c:
            r, c = cell
            g[r][d2 + 1 + c] = rng.choice(src_palette)
        return g
    raise ValueError("could not realize 3-panel color analogy in 40 attempts")
