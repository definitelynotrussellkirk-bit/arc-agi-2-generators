"""Generator for arc_puzzle_bank_21_set19_s:S19_H1 — dihedral-match matrix.

Rule: panels separated by full color-9 columns. Output is N×N where
(r, c) = 8 if panel-r's normalized cells match any dihedral variant of
panel-c's cells.

Combinatorial axes (8): grid_h, n_panels, palette_kind, motif_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, empty_panels, single_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "35c7e1c0d116"
VERSION = "1.1.0"
TASK_ID = "35c7e1c0d116"

SUMMARY = "3-4 panels separated by full color-9 columns; each panel has a small motif."

INVARIANTS = [
    "background is 0",
    "panels separated by full color-9 columns of width 4",
    "each panel has a small motif (2-4 cells) in some non-{0, 9} color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "empty_panels", "single_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "n_panels":       {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_size":     {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "horizontal_panels_9divs",
                       "valid": "horizontal_panels_9divs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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
        h = ctx.draw_int("grid_h", 4, 4)
        n = ctx.draw_int("n_panels", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        n = ctx.draw_int("n_panels", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 4, 5)
        n = ctx.draw_int("n_panels", 3, 4)
    rng = ctx.draw_rng("layout")

    panel_w = 4
    w = panel_w * n + (n - 1)

    g = full_grid(h, w, 0)
    for k in range(1, n):
        c = panel_w * k + (k - 1)
        for r in range(h): g[r][c] = 9
    for k in range(n):
        c0 = k * (panel_w + 1)
        cells = _build_motif(rng, rng.randint(2, 4))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        if sh > h or sw > panel_w: continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        for r, c in cells:
            g[r - min(rs)][c0 + c - min(cs)] = color
    return g


def _draw_from_degenerate(name, rng):
    h, panel_w, n = 4, 4, 3
    w = panel_w * n + (n - 1)
    g = full_grid(h, w, 0)
    if name == "no_dividers":
        # Motifs but no 9-column dividers — panels can't be segmented.
        for k in range(n):
            c0 = k * panel_w
            g[1][c0 + 1] = [4, 6, 7][k]
        return g
    if name == "empty_panels":
        # Dividers present but every panel empty — rule has nothing
        # to compare across panels.
        for k in range(1, n):
            c = panel_w * k + (k - 1)
            for r in range(h): g[r][c] = 9
        return g
    if name == "single_panel":
        # Just one motif and no dividers — N=1 trivially yields a 1x1
        # output, removing the cross-panel comparison evidence.
        g[1][1] = 4
        return g
    return g
