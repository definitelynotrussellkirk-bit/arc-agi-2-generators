"""Generator for arc_puzzle_bank_21_set20_s:S20_H3 — 2 panels separated by 9-col.

Rule: 2 panels separated by full color-9 column; each has a motif. Output
based on inter-panel match.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_motifs, single_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5ec933db2c3a"
VERSION = "1.1.0"
TASK_ID = "5ec933db2c3a"

SUMMARY = "2 panels separated by a full color-9 column, each with a small motif."

INVARIANTS = [
    "background is 0",
    "panels separated by full color-9 column",
    "each panel has a small color-2 motif (2-5 cells)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_motifs", "single_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "9..21"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_size":     {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "9col_separated_2panels",
                       "valid": "9col_separated_2panels"},
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
        panel_h = ctx.draw_int("panel_h", 5, 6)
        panel_w = ctx.draw_int("panel_w", 6, 7)
    elif difficulty == "hard":
        panel_h = ctx.draw_int("panel_h", 6, 7)
        panel_w = ctx.draw_int("panel_w", 7, 8)
    else:
        panel_h = ctx.draw_int("panel_h", 5, 7)
        panel_w = ctx.draw_int("panel_w", 6, 8)
    rng = ctx.draw_rng("layout")

    h = panel_h
    w = panel_w * 2 + 1
    g = full_grid(h, w, 0)
    for r in range(h): g[r][panel_w] = 9
    for k in range(2):
        c0 = k * (panel_w + 1)
        cells = _build_motif(rng, rng.randint(3, 5))
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
        if sh > h or sw > panel_w: continue
        for r, c in cells:
            g[r - min(rs)][c0 + c - min(cs)] = 2
    return g


def _draw_from_degenerate(name, rng):
    h = 5; pw = 6
    w = pw * 2 + 1
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # missing 9-col → can't split into panels
        for r, c in [(1, 1), (2, 1), (2, 2)]: g[r][c] = 2
        for r, c in [(1, 8), (2, 8), (2, 9)]: g[r][c] = 2
        return g
    if name == "no_motifs":
        # divider only, both panels empty → nothing to compare
        for r in range(h): g[r][pw] = 9
        return g
    if name == "single_panel":
        # only one panel has motif → can't compare to second
        for r in range(h): g[r][pw] = 9
        for r, c in [(1, 1), (2, 1), (2, 2)]: g[r][c] = 2
        return g
    return g
