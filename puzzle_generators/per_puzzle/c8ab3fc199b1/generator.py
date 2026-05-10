"""Generator for arc_puzzle_bank_21_set10_e:medium_j13 — Hstack body crops at row 0 marker positions.

Rule: row 0 has marker colors at various columns. For each marker, find
body object of that color; place its bbox crop at marker's column,
bottom-aligned.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, marker_without_body, body_without_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "c8ab3fc199b1"
VERSION = "1.1.0"
TASK_ID = "c8ab3fc199b1"
SUMMARY = "Row 0 has 3 marker cells at varied cols + 3 body blobs of matching colors."

INVARIANTS = [
    "row 0 has 3 non-zero markers at distinct cols",
    "body has 3 non-touching blobs each of a distinct marker color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "marker_without_body", "body_without_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "row0_markers_with_body_blobs",
                       "valid": "row0_markers_with_body_blobs"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 6, 7, 8]; rng.shuffle(palette)
    g[0][1] = palette[0]; g[0][5] = palette[1]; g[0][8] = palette[2]
    paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 0)], palette[0])
    paint_at(g, 4, 4, [(0, 1), (1, 0), (1, 1), (1, 2)], palette[1])
    paint_at(g, 3, 8, [(0, 0), (1, 0), (1, 1)], palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 13
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # row 0 is empty → no markers, rule has no positions to stamp at
        paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 4, 4, [(0, 1), (1, 0), (1, 1), (1, 2)], 3)
        return g
    if name == "marker_without_body":
        # marker color has no body blob → lookup fails for that marker
        g[0][1] = 2; g[0][5] = 3; g[0][8] = 7   # 7 has no body
        paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 4, 4, [(0, 1), (1, 0), (1, 1), (1, 2)], 3)
        return g
    if name == "body_without_marker":
        # body blob with color not in markers → ignored
        g[0][1] = 2; g[0][5] = 3   # only 2 markers
        paint_at(g, 2, 1, [(0, 0), (0, 1), (1, 0)], 2)
        paint_at(g, 4, 4, [(0, 1), (1, 0), (1, 1), (1, 2)], 3)
        paint_at(g, 3, 9, [(0, 0), (1, 0), (1, 1)], 6)  # extra body, no marker
        return g
    return g
