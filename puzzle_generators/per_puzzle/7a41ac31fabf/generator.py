"""Generator for arc_puzzle_bank_fourth21:E27.

Rule: each X motif (center + 4 diagonals same color) gets its center
highlighted.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_xs, partial_xs, mixed_corner_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7a41ac31fabf"
VERSION = "1.1.0"
TASK_ID = "7a41ac31fabf"
SUMMARY = "Place separated same-color X motifs whose centers are highlighted."

INVARIANTS = [
    "background is 0",
    "each active motif has a non-8 center",
    "the four diagonal neighbors around the center share the center color",
    "motif footprints are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_xs", "partial_xs", "mixed_corner_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motifs":         {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "spaced_xs",
                       "valid": "spaced_xs"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_DIAGS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("motifs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("motifs", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("motifs", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        cells = {(r, c)} | {(r + dr, c + dc) for dr, dc in _DIAGS}
        guard = {
            (rr, cc)
            for cr, cc0 in cells
            for rr in range(max(0, cr - 1), min(h, cr + 2))
            for cc in range(max(0, cc0 - 1), min(w, cc0 + 2))
        }
        if guard & reserved:
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        for rr, cc in cells:
            g[rr][cc] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_xs":
        # blank grid → no X motifs to highlight, rule is identity
        return g
    if name == "partial_xs":
        # only 3 of 4 diagonals → predicate fails, no center highlighted
        # missing top-right diagonal around (3, 3)
        for (r, c) in [(3, 3), (2, 2), (4, 2), (4, 4)]: g[r][c] = 4
        return g
    if name == "mixed_corner_colors":
        # 4 diagonals present but with mixed colors → predicate "all same color" fails
        for (r, c, col) in [(3, 3, 4), (2, 2, 4), (2, 4, 6), (4, 2, 4), (4, 4, 4)]: g[r][c] = col
        return g
    return g
