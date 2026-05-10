"""Generator for arc_puzzle_bank_21_set20_s:S20_H6 — 3 panels separated by 9-col.

Rule: 3 panels separated by full color-9 column; each has a motif.

Combinatorial axes (8): panel_h, panel_w, palette_kind, motif_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, empty_panels, single_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "75b8cb3d5e9b"
VERSION = "1.1.0"
TASK_ID = "75b8cb3d5e9b"

SUMMARY = "3 panels separated by full color-9 columns, each with a small motif."

INVARIANTS = [
    "background is 0",
    "panels separated by full color-9 columns",
    "each panel has a small motif in some color (2-5 cells)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "empty_panels", "single_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_h":        {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "panel_w":        {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_size":     {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "3_horizontal_panels_9divs",
                       "valid": "3_horizontal_panels_9divs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        panel_h = ctx.draw_int("panel_h", 4, 4)
        panel_w = ctx.draw_int("panel_w", 4, 4)
    else:
        panel_h = ctx.draw_int("panel_h", 3, 4)
        panel_w = ctx.draw_int("panel_w", 3, 4)
    rng = ctx.draw_rng("layout")

    n = 3
    h = panel_h
    w = panel_w * n + (n - 1)
    g = full_grid(h, w, 0)
    for k in range(1, n):
        c = panel_w * k + (k - 1)
        for r in range(h): g[r][c] = 9
    color = rng.choice([2, 3, 4, 5, 6, 7])
    for k in range(n):
        c0 = k * (panel_w + 1)
        cells = _build_motif(rng, rng.randint(2, min(4, panel_h * panel_w - 1)))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        if sh > h or sw > panel_w: continue
        for r, c in cells:
            g[r - min(rs)][c0 + c - min(cs)] = color
    return g


def _draw_from_degenerate(name, rng):
    panel_h, panel_w, n = 3, 3, 3
    h = panel_h
    w = panel_w * n + (n - 1)
    g = full_grid(h, w, 0)
    if name == "no_dividers":
        for k in range(n):
            c0 = k * panel_w
            g[1][c0 + 1] = 4
        return g
    if name == "empty_panels":
        for k in range(1, n):
            c = panel_w * k + (k - 1)
            for r in range(h): g[r][c] = 9
        return g
    if name == "single_panel":
        g[1][1] = 4
        return g
    return g
