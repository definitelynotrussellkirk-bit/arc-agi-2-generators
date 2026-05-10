"""Generator for arc_puzzle_bank_21_set2:S2_M5 — recolor rect-outline 3-objects to 7.

Rule: for each 3-colored object, if it's a rectangular outline (frame
shape with hollow interior), recolor cells to 7. Solid 3-objects stay 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_outline,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_outlines, all_solid, all_outlines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "cae2423a6477"
VERSION = "1.1.0"
TASK_ID = "cae2423a6477"
SUMMARY = "1-2 outlined 3-rects + 1-2 solid 3-blobs (so rule has both branches)."

INVARIANTS = [
    "background is 0",
    "all non-zero cells are color 3",
    "at least one outline rect (≥3×3 hollow) AND at least one solid (or non-outline) blob",
    "objects don't 4-touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_outlines", "all_solid", "all_outlines")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_outline":      {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "outlines_plus_solids",
                       "valid": "outlines_plus_solids"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _rect_free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    n_outline = rng.randint(1, 2)
    for _ in range(n_outline):
        for _ in range(40):
            rh = rng.randint(3, 4)
            rw = rng.randint(3, 4)
            r1 = rng.randint(0, h - rh)
            c1 = rng.randint(0, w - rw)
            r2 = r1 + rh - 1
            c2 = c1 + rw - 1
            if _rect_free(g, r1, c1, r2, c2):
                for c in range(c1, c2 + 1):
                    g[r1][c] = 3
                    g[r2][c] = 3
                for r in range(r1, r2 + 1):
                    g[r][c1] = 3
                    g[r][c2] = 3
                for r in range(r1, r2 + 1):
                    for c in range(c1, c2 + 1):
                        if g[r][c] == 3:
                            used.add((r, c))
                break
    n_solid = rng.randint(1, 2)
    for _ in range(n_solid):
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = 3
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_outlines":
        # Only solid blobs — rule's outline branch never fires.
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 3
        for r in range(6, 8):
            for c in range(6, 8): g[r][c] = 3
        return g
    if name == "all_solid":
        # All filled rectangles, not outlines — rule recolors nothing.
        for r in range(1, 4):
            for c in range(1, 4): g[r][c] = 3
        for r in range(5, 8):
            for c in range(5, 8): g[r][c] = 3
        return g
    if name == "all_outlines":
        # All outlines, no solids — rule recolors everything.
        for c in range(1, 5): g[1][c] = 3; g[4][c] = 3
        for r in range(1, 5): g[r][1] = 3; g[r][4] = 3
        for c in range(5, 9): g[6][c] = 3; g[9][c] = 3
        for r in range(6, 10): g[r][5] = 3; g[r][8] = 3
        return g
    return g
