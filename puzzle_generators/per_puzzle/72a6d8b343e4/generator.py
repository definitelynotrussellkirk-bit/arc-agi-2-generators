"""Generator for v2_meta_puzzles:M7 — connect aligned same-color pairs (axial).

Rule: for each color appearing exactly 2 times, if those 2 cells are
axially aligned (same row or column), draw a line between them in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_pairs, texture.
Degenerates: no_pairs, no_shared_axis, adjacent_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "72a6d8b343e4"
VERSION = "1.1.0"
TASK_ID = "72a6d8b343e4"

SUMMARY = "1-3 pairs of cells in distinct colors, each pair axially aligned (same row or column)."

INVARIANTS = [
    "background is 0",
    "1-3 pairs of cells in distinct colors; each pair shares a row or column with ≥2 cells of separation",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "no_shared_axis", "adjacent_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "= n_pairs", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "axially_aligned_pairs",
                       "valid": "axially_aligned_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= n_pairs", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_pairs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 12)
        n = ctx.draw_int("n_pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
        n = ctx.draw_int("n_pairs", 1, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
        ok = True
        for color in colors:
            placed = False
            for _ in range(80):
                vert = rng.choice([True, False])
                if vert:
                    c = rng.randint(0, w - 1)
                    r1 = rng.randint(0, h - 4); r2 = rng.randint(r1 + 2, h - 1)
                    if g[r1][c] != 0 or g[r2][c] != 0: continue
                    if any(g[r][c] != 0 for r in range(r1 + 1, r2)): continue
                    g[r1][c] = color; g[r2][c] = color
                else:
                    r = rng.randint(0, h - 1)
                    c1 = rng.randint(0, w - 4); c2 = rng.randint(c1 + 2, w - 1)
                    if g[r][c1] != 0 or g[r][c2] != 0: continue
                    if any(g[r][c] != 0 for c in range(c1 + 1, c2)): continue
                    g[r][c1] = color; g[r][c2] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no pairs to connect.
        return g
    if name == "no_shared_axis":
        # Pair has matching color but on different rows AND cols —
        # rule's "axially aligned" precondition fails.
        g[1][2] = 4; g[5][6] = 4
        return g
    if name == "adjacent_pair":
        # Pair shares a row but is adjacent — rule's "fill between"
        # produces zero filler cells.
        g[3][2] = 4; g[3][3] = 4
        return g
    return g
