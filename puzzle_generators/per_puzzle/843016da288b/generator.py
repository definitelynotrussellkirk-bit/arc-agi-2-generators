"""Generator for arc_puzzle_bank_21_set2:S2_M3 — bounding-box outlines.

Rule: replace every 2-colored object by the rect-outline of its bbox in
color 2.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: solid_rects, single_blob, line_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "843016da288b"
VERSION = "1.1.0"
TASK_ID = "843016da288b"
SUMMARY = "2-3 small color-2 blobs whose bboxes don't fill (so outline ≠ identity)."

INVARIANTS = [
    "background is 0",
    "all non-zero cells are color 2",
    "every blob has at least one bbox cell that is empty (otherwise output = input)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("solid_rects", "single_blob", "line_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "non_rectangular_blobs",
                       "valid": "non_rectangular_blobs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        n = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n = 3
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        n = ctx.draw_int("n_blobs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    for _ in range(n):
        size = rng.randint(3, 5)
        cells = grow_blob(rng, h, w, used, size, max_attempts=80)
        if cells is None:
            continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb_h = max(rs) - min(rs) + 1
        bb_w = max(cs) - min(cs) + 1
        if bb_h * bb_w == len(cells):
            continue
        for r, c in cells:
            g[r][c] = 2
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "solid_rects":
        # solid rectangles → bbox outline equals the original (interior already filled),
        # rule is identity, no visible change
        for r in range(1, 4):
            for c in range(1, 4): g[r][c] = 2
        for r in range(5, 8):
            for c in range(5, 9): g[r][c] = 2
        return g
    if name == "single_blob":
        # one blob → only one outline drawn, no comparison/contrast
        for (r, c) in [(2, 3), (2, 4), (2, 5), (3, 5), (4, 5)]: g[r][c] = 2
        return g
    if name == "line_blobs":
        # 1×N or N×1 lines → bbox is the line itself; outline equals input, rule is identity
        for c in range(1, 6): g[2][c] = 2   # horizontal line
        for r in range(4, 8): g[r][8] = 2   # vertical line
        return g
    return g
