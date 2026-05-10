"""Generator for arc_additional_puzzles_21_set16_bundle:H111 — legend-ordered canonical gallery.

Rule: row 0 is the color order. Body has one connected component per legend
color. Each component is canonicalized (lex-min over 6 dihedral transforms)
and the canonical crops are concatenated left-to-right in legend order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend (row 0 empty → rule has no order); no_body
(legend present but no body shapes → rule has nothing to crop);
legend_color_no_shape (a legend color has no body shape → rule's
body lookup returns nothing for that slot).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fc8c7392a146"
VERSION = "1.1.0"
TASK_ID = "fc8c7392a146"

SUMMARY = "Top-row legend (2-3 colors); body has one shape per legend color; output is canonical gallery."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-3 distinct non-zero colors at distinct columns",
    "body has exactly one isolated 4-conn shape per legend color, in that color",
    "shapes are sized 3-5 cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_body", "legend_color_no_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 14..18", "valid": "12..24"},
    "n_legend":          {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":     {"type": "str", "default": "row0_legend_with_body_shapes",
                          "valid": "row0_legend_with_body_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 14, 15)
        n_legend = ctx.draw_int("n_legend", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 16, 18)
        n_legend = ctx.draw_int("n_legend", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 14, 18)
        n_legend = ctx.draw_int("n_legend", 2, 3)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([2, 3, 4, 6, 7, 8, 9], n_legend)

    for outer in range(40):
        g = full_grid(h, w, 0)
        cols0 = rng.sample(range(w), n_legend)
        cols0.sort()
        for col, color in zip(cols0, palette):
            g[0][col] = color
        ok = True
        for color in palette:
            shape = rng.choice(_SHAPES)
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            placed = False
            for _ in range(80):
                r0 = rng.randint(2, h - sh)
                c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1):
                    continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                placed = True
                break
            if not placed:
                ok = False
                break
        if ok:
            return g
    raise ValueError("could not place legend shapes in 40 attempts")


def _draw_from_degenerate(name, rng):
    h, w = 9, 15
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Row 0 empty — rule has no order.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[3 + dr][8 + dc] = 6
        return g
    if name == "no_body":
        # Legend present but no body shapes.
        g[0][2] = 4; g[0][8] = 6
        return g
    if name == "legend_color_no_shape":
        # Legend has color 4, 6 but body only has color-4 shape (no color-6).
        g[0][2] = 4; g[0][8] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][2 + dc] = 4
        return g
    return g
