"""Generator for arc_additional_puzzles_21_set11_bundle:E77 — Stamp top-left 2×2 motif at every 9-marker.

Rule: motif = subgrid (0,0)-(1,1). Find all 9-cells (markers); paint
each marker location with the motif (top-left aligned), and erase
the 9s.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motif, no_markers, marker_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6b266391d6b7"
VERSION = "1.1.0"
TASK_ID = "6b266391d6b7"
SUMMARY = "Top-left 2×2 motif (4 colored cells) + 1-3 9-markers elsewhere."

INVARIANTS = [
    "top-left 2×2 cells form a motif (≥2 non-bg cells)",
    "1-3 isolated 9-markers in interior, with empty 2x2 at and after marker",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motif", "no_markers", "marker_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "tl_motif_with_markers",
                       "valid": "tl_motif_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 3)
    g[0][0] = pal[0]; g[0][1] = 0
    g[1][0] = pal[1]; g[1][1] = pal[2]
    n = rng.randint(2, 3)
    placed = []
    for _ in range(40):
        if len(placed) >= n: break
        r = rng.randint(2, h - 3); c = rng.randint(2, w - 3)
        if all(abs(r - pr) > 2 or abs(c - pc) > 2 for pr, pc in placed):
            g[r][c] = 9
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_motif":
        # markers exist but top-left 2x2 is blank → no motif to stamp
        g[3][4] = 9
        g[5][6] = 9
        return g
    if name == "no_markers":
        # motif present but no 9-markers → nothing to stamp at
        g[0][0] = 4; g[1][0] = 6; g[1][1] = 7
        return g
    if name == "marker_at_edge":
        # marker at right/bottom edge → 2x2 stamp would overflow grid bounds
        g[0][0] = 4; g[1][0] = 6; g[1][1] = 7
        g[h - 1][w - 1] = 9
        return g
    return g
