"""Generator for arc_puzzle_bank_seventh21:M48 — 6 panels separated by 9-cols, find pair.

Rule: 6 panels separated by full color-9 columns; each has a small motif.

Combinatorial axes (8): panel_h, n_panels, palette_kind, panel_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, single_panel, all_panels_empty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9c3781759581"
VERSION = "1.1.0"
TASK_ID = "9c3781759581"
SUMMARY = "6 panels separated by full color-9 columns, each with a small motif."

INVARIANTS = [
    "background is 0",
    "panels separated by full color-9 columns of width 4",
    "each panel has a small motif (1-3 cells) in some non-{0, 9} color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "single_panel", "all_panels_empty")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_h":        {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "n_panels":       {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_w":        {"type": "int", "default": "4", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "rng 5..6", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "panel_grid",
                       "valid": "panel_grid"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..6", "valid": "2..7"},
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
        panel_h = ctx.draw_int("panel_h", 4, 4)
        n = ctx.draw_int("n_panels", 5, 5)
    elif difficulty == "hard":
        panel_h = ctx.draw_int("panel_h", 5, 5)
        n = ctx.draw_int("n_panels", 6, 6)
    else:
        panel_h = ctx.draw_int("panel_h", 4, 5)
        n = ctx.draw_int("n_panels", 5, 6)
    rng = ctx.draw_rng("layout")

    panel_w = 4
    h = panel_h
    w = panel_w * n + (n - 1)
    g = full_grid(h, w, 0)
    for k in range(1, n):
        c = panel_w * k + (k - 1)
        for r in range(h): g[r][c] = 9
    for k in range(n):
        c0 = k * (panel_w + 1)
        cells = _build_motif(rng, rng.randint(1, 3))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        if sh > h or sw > panel_w: continue
        color = rng.choice([2, 3, 4, 5, 6, 7])
        for r, c in cells:
            g[r - min(rs)][c0 + c - min(cs)] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 4, 23
    g = full_grid(h, w, 0)
    if name == "no_separators":
        # no full color-9 columns → panels can't be split, rule has no anchor
        for c in [2, 7, 12, 17]:
            for r in range(h):
                g[r][c] = 5
        return g
    if name == "single_panel":
        # only one panel, no separator → no comparison possible
        for r, c in [(1, 1), (1, 2), (2, 1)]:
            g[r][c] = 4
        return g
    if name == "all_panels_empty":
        # separators present but every panel is blank → nothing to compare
        for c in [4, 9, 14, 19]:
            for r in range(h):
                g[r][c] = 9
        return g
    return g
