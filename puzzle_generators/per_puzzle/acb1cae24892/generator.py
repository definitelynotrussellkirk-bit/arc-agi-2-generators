"""Generator for v2_meta_puzzles:M2 — connect same-color pairs with line or rect outline.

Rule: each non-bg color has exactly 2 markers.
  - Same row → fill the row segment between them with that color.
  - Same col → fill the col segment.
  - Different row AND different col → paint the rectangle outline
    bounded by the two markers in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: single_marker (only 1 marker per color → rule's
"connect 2 markers" branch finds no second endpoint, no fill),
no_markers (grid is all bg → rule has no pairs to connect),
markers_adjacent (markers are adjacent (gap < 2) → rule's segment
fill is empty/single-cell, no visible connection).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "acb1cae24892"
VERSION = "1.1.0"
TASK_ID = "acb1cae24892"
SUMMARY = "1-2 distinct colors, each with 2 markers (same row, same col, or diagonal corners)."

INVARIANTS = [
    "background is 0",
    "1-2 distinct colors, each with exactly 2 markers",
    "each pair is either same-row+gap, same-col+gap, or diagonal-corners",
    "pairs use distinct rows/cols (no cross interference)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_marker", "no_markers", "markers_adjacent")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":            {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "n_colors":          {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":     {"type": "str", "default": "color_pair_endpoints",
                          "valid": "color_pair_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_colors", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 10)
        n = ctx.draw_int("n_colors", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        n = ctx.draw_int("n_colors", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, n))
    busy_rows: set[int] = set()
    busy_cols: set[int] = set()
    for color in palette:
        for _ in range(60):
            mode = rng.choice(["row", "col", "rect"])
            if mode == "row":
                r = rng.randint(0, h - 1)
                if r in busy_rows: continue
                cs = sorted(rng.sample(range(w), 2))
                if cs[1] - cs[0] < 2: continue
                if cs[0] in busy_cols or cs[1] in busy_cols: continue
                g[r][cs[0]] = color; g[r][cs[1]] = color
                busy_rows.add(r)
                busy_cols.update(cs)
                break
            elif mode == "col":
                c = rng.randint(0, w - 1)
                if c in busy_cols: continue
                rs = sorted(rng.sample(range(h), 2))
                if rs[1] - rs[0] < 2: continue
                if rs[0] in busy_rows or rs[1] in busy_rows: continue
                g[rs[0]][c] = color; g[rs[1]][c] = color
                busy_cols.add(c)
                busy_rows.update(rs)
                break
            else:
                rs = sorted(rng.sample(range(h), 2))
                cs = sorted(rng.sample(range(w), 2))
                if rs[1] - rs[0] < 2 or cs[1] - cs[0] < 2: continue
                if any(r in busy_rows for r in rs) or any(c in busy_cols for c in cs): continue
                g[rs[0]][cs[0]] = color
                g[rs[1]][cs[1]] = color
                busy_rows.update(rs)
                busy_cols.update(cs)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "single_marker":
        # Only 1 marker per color — rule's "connect 2 markers" branch
        # finds no pair; no fill.
        g[1][1] = 4
        g[5][6] = 6
        return g
    if name == "no_markers":
        # No markers at all — rule has no pairs; output equals input.
        return g
    if name == "markers_adjacent":
        # Markers are adjacent (gap < 2) — rule's segment fill is
        # empty (no cells between); no visible connection.
        g[2][2] = 4; g[2][3] = 4
        g[5][5] = 6; g[5][6] = 6
        return g
    return g
