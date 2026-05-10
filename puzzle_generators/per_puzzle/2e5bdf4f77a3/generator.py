"""Generator for arc_puzzle_bank_21_set23_s:S23_H1 — 2x3 grid of panels separated by 9-walls.

Rule: 2 rows x 3 cols of panels separated by full color-9 row/col walls.
Each panel has a small motif; output is one-hot of which target panel matches
a rotated reference.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, empty_panels, all_identical.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2e5bdf4f77a3"
VERSION = "1.1.0"
TASK_ID = "2e5bdf4f77a3"

SUMMARY = "2 rows × 3 cols of panels separated by full color-9 row/col walls; each panel has a small motif."

INVARIANTS = [
    "background is 0",
    "panels arranged 2 rows × 3 cols, separated by full color-9 row/col dividers",
    "each panel has a small motif (2-4 cells) in some non-{0, 9} color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "empty_panels", "all_identical")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_h":        {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "panel_w":        {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "2x3_panel_lattice",
                       "valid": "2x3_panel_lattice"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _build_motif(rng, k):
    cells = [(0, 0)]; seen = {(0, 0)}
    while len(cells) < k:
        r, c = rng.choice(cells)
        dr, dc = rng.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        nr, nc = r + dr, c + dc
        if (nr, nc) not in seen:
            cells.append((nr, nc)); seen.add((nr, nc))
    return cells


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        panel_h = ctx.draw_int("panel_h", 3, 3)
        panel_w = ctx.draw_int("panel_w", 3, 3)
    elif difficulty == "hard":
        panel_h = ctx.draw_int("panel_h", 4, 5)
        panel_w = ctx.draw_int("panel_w", 4, 5)
    else:
        panel_h = ctx.draw_int("panel_h", 3, 4)
        panel_w = ctx.draw_int("panel_w", 3, 4)
    rng = ctx.draw_rng("layout")

    h = panel_h * 2 + 1
    w = panel_w * 3 + 2
    g = full_grid(h, w, 0)
    div_r = panel_h
    for c in range(w): g[div_r][c] = 9
    for k in range(1, 3):
        col = panel_w * k + (k - 1)
        for r in range(h): g[r][col] = 9
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    for pr in range(2):
        for pc in range(3):
            r0 = pr * (panel_h + 1)
            c0 = pc * (panel_w + 1)
            cells = _build_motif(rng, rng.randint(2, min(4, panel_h * panel_w - 1)))
            rs = [r for r, _ in cells]; cs = [c for _, c in cells]
            sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
            if sh > panel_h or sw > panel_w: continue
            for r, c in cells:
                g[r0 + r - min(rs)][c0 + c - min(cs)] = color
    return g


def _draw_from_degenerate(name, rng):
    panel_h = 3; panel_w = 3
    h = panel_h * 2 + 1
    w = panel_w * 3 + 2
    g = full_grid(h, w, 0)
    if name == "no_separators":
        # Motifs but no 9-dividers — rule's panel decomposition
        # fails.
        g[1][1] = 4; g[1][5] = 4; g[1][9] = 4
        g[5][1] = 4; g[5][5] = 4; g[5][9] = 4
        return g
    div_r = panel_h
    for c in range(w): g[div_r][c] = 9
    for k in range(1, 3):
        col = panel_w * k + (k - 1)
        for r in range(h): g[r][col] = 9
    if name == "empty_panels":
        # Separators but no motifs in any panel — rule has no
        # shapes to compare.
        return g
    if name == "all_identical":
        # All 6 panels have identical motif — rule's matching
        # selector finds no unique target.
        for pr in range(2):
            for pc in range(3):
                r0 = pr * (panel_h + 1)
                c0 = pc * (panel_w + 1)
                g[r0][c0] = 4; g[r0 + 1][c0] = 4; g[r0 + 1][c0 + 1] = 4
        return g
    return g
