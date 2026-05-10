"""Generator for arc_puzzle_bank_21_set14_bundle:medium_n06 — corner-9 transform code + motif crop.

Rule: a color-9 marker at one of 4 corners encodes a transform code
(TL=0, TR=1, BR=2, BL=3). The grid (without the corner-9) is cropped to
its non-zero bbox and transformed by code.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_motif, marker_in_middle.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ad6ae79cd803"
VERSION = "1.1.0"
TASK_ID = "ad6ae79cd803"

SUMMARY = "Color-9 marker at a corner + 1 small motif in another color elsewhere."

INVARIANTS = [
    "background is 0",
    "exactly one color-9 marker at a corner",
    "exactly one connected motif (3-5 cells) in some non-{0, 9} color away from corners",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_motif", "marker_in_middle")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "corner_9_motif_inside",
                       "valid": "corner_9_motif_inside"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    corner = rng.choice([(0, 0), (0, w - 1), (h - 1, w - 1), (h - 1, 0)])
    g[corner[0]][corner[1]] = 9
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    cells = _build_motif(rng, rng.randint(3, 5))
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    sh = max(rs) - min(rs) + 1; sw = max(cs) - min(cs) + 1
    for _ in range(80):
        r0 = rng.randint(2, h - sh - 2) if h - sh > 2 else 2
        c0 = rng.randint(2, w - sw - 2) if w - sw > 2 else 2
        cells_p = [(r0 + r - min(rs), c0 + c - min(cs)) for r, c in cells]
        if any(g[r][c] != 0 for r, c in cells_p): continue
        for r, c in cells_p:
            g[r][c] = color
        return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # Motif but no 9-corner — rule has no transform code to apply.
        for r, c in [(3, 3), (3, 4), (4, 4)]: g[r][c] = 4
        return g
    if name == "no_motif":
        # Corner-9 but no motif — rule has nothing to crop and transform.
        g[0][0] = 9
        return g
    if name == "marker_in_middle":
        # 9-marker placed mid-grid (not at a corner) — rule's
        # corner-determines-transform mapping has no entry for non-corners.
        g[3][4] = 9
        for r, c in [(5, 1), (5, 2), (6, 1), (6, 2), (7, 2)]: g[r][c] = 4
        return g
    return g
