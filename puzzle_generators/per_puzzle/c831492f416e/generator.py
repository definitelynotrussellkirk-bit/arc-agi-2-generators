"""Generator for `arc_additional_puzzles_21_set13_bundle:E86` — each
non-bg color appears as exactly 2 cells (an aligned pair); rule fills
the segment between them inclusive.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_endpoint, off_axis_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c831492f416e"
VERSION = "1.1.0"
TASK_ID = "c831492f416e"
SUMMARY = "Aligned pairs of same-color endpoints; rule fills the segment between each pair."

INVARIANTS = [
    "background is 0",
    "2-4 distinct non-bg colors",
    "each color appears as exactly 2 cells",
    "each pair is row-aligned or column-aligned",
    "pairs don't overlap (no two pairs share any cell)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_endpoint", "off_axis_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "n_pairs":        {"type": "int", "default": "rng 2..3",  "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "axis_aligned_pairs",
                       "valid": "axis_aligned_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 15)
        w = ctx.draw_int("grid_w", 12, 15)
        n_pairs = ctx.draw_int("n_pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    palette = ctx.draw_distinct_colors("palette", n=n_pairs, exclude={0})
    rng = ctx.draw_rng("placement")

    g = full_grid(h, w, 0)
    placed = 0
    for color in palette:
        for _try in range(20):
            orient = rng.choice(["h", "v"])
            if orient == "h":
                r = rng.randint(0, h - 1)
                c1 = rng.randint(0, w - 4); c2 = rng.randint(c1 + 2, w - 1)
                if any(g[r][c] != 0 for c in range(c1, c2 + 1)): continue
                g[r][c1] = color; g[r][c2] = color
            else:
                c = rng.randint(0, w - 1)
                r1 = rng.randint(0, h - 4); r2 = rng.randint(r1 + 2, h - 1)
                if any(g[rr][c] != 0 for rr in range(r1, r2 + 1)): continue
                g[r1][c] = color; g[r2][c] = color
            placed += 1
            break
    if placed < 2:
        return [[0]]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no segments to fill.
        return g
    if name == "single_endpoint":
        # Color appears once — rule's "exactly 2 cells per color"
        # filter excludes; segment undefined.
        g[3][3] = 4
        return g
    if name == "off_axis_pair":
        # Two same-color cells not row- or column-aligned —
        # rule's segment cannot be drawn straight.
        g[2][2] = 4; g[5][7] = 4
        return g
    return g
