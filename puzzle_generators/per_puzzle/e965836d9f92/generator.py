"""Generator for 21b:hard_144 — build transform-recolor gallery.

Rule: row 0 cols 1+ hold transform codes; col 0 rows 1+ hold colors.
Body has a single prototype shape (largest non-bg component after
zeroing out the row/col-0 strips). Output is a (n_colors × n_codes)
gallery: prototype transformed by each code, recolored to each color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_codes (row 0 empty → gallery has 0 columns, output
collapses), no_colors (col 0 empty → gallery has 0 rows, output
collapses), no_prototype (body empty → rule's transform has no shape
to operate on).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e965836d9f92"
VERSION = "1.1.0"
TASK_ID = "e965836d9f92"

SUMMARY = "2-3 codes in row 0 + 2-3 colors in col 0 + 1 prototype shape in body."

INVARIANTS = [
    "background is 0",
    "row 0 cols 1+ hold 2-3 transform codes (1-5) at distinct cols",
    "col 0 rows 1+ hold 2-3 distinct colors at distinct rows",
    "body has exactly one multi-cell prototype shape",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_codes", "no_colors", "no_prototype")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "header_strips_plus_prototype",
                       "valid": "header_strips_plus_prototype"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "3..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 9)
        n_codes_lo, n_codes_hi = 2, 2
        n_colors_lo, n_colors_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 11, 14)
        n_codes_lo, n_codes_hi = 3, 4
        n_colors_lo, n_colors_hi = 3, 4
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        n_codes_lo, n_codes_hi = 2, 3
        n_colors_lo, n_colors_hi = 2, 3
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_codes = rng.randint(n_codes_lo, n_codes_hi)
    n_colors = rng.randint(n_colors_lo, n_colors_hi)
    code_cols = rng.sample(range(1, w), n_codes)
    color_rows = rng.sample(range(1, h), n_colors)
    palette = rng.sample([2, 3, 4, 6, 7, 8, 9], n_colors)
    for c in code_cols: g[0][c] = rng.randint(1, 5)
    for r, color in zip(color_rows, palette): g[r][0] = color
    proto_color = rng.choice([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in palette])
    shape = rng.choice(_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(2, h - sh); c0 = rng.randint(2, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = proto_color
        return g
    raise ValueError("could not place prototype")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_codes":
        # Row 0 empty — gallery has 0 columns; output collapses.
        g[2][0] = 3; g[5][0] = 6
        for dr, dc in _SHAPES[0]:
            g[3 + dr][4 + dc] = 9
        return g
    if name == "no_colors":
        # Col 0 empty — gallery has 0 rows; output collapses.
        g[0][3] = 1; g[0][7] = 2
        for dr, dc in _SHAPES[0]:
            g[3 + dr][4 + dc] = 9
        return g
    if name == "no_prototype":
        # Body empty — rule's transform has no shape to operate on.
        g[0][3] = 1; g[0][7] = 2
        g[2][0] = 3; g[5][0] = 6
        return g
    return g
