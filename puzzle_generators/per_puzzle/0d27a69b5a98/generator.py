"""Generator for arc_puzzle_bank_21_set14_bundle:medium_n02 — mirror objects across a 9-line.

Rule: a full-grid 9-line (vertical or horizontal) divides the grid.
Objects on one side get mirrored across the line into the other side.
Objects already present on both sides stay.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_line (no full-grid 9-line → rule's mirror axis is
undefined, no mirroring), no_objects (line present but no objects →
rule has nothing to mirror, output equals input), already_mirrored
(objects already exist symmetrically on both sides → rule's mirror
operation is identity, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "0d27a69b5a98"
VERSION = "1.1.0"
TASK_ID = "0d27a69b5a98"
SUMMARY = "Full-grid 9-line (vertical or horizontal) plus 1-2 small objects on the empty side."

INVARIANTS = [
    "background is 0",
    "exactly one full-grid 9-line (entire row or entire column is 9)",
    "1-2 small connected objects on one side of the line, none on the other",
    "objects fit within their side without crossing the line",
    "objects don't touch the 9-line or each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_line", "no_objects", "already_mirrored")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":            {"type": "int", "default": "rng 8..11", "valid": "7..16"},
    "n_objs":            {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":     {"type": "str", "default": "9line_plus_one_side_objects",
                          "valid": "9line_plus_one_side_objects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("n_objs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_objs", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        n = ctx.draw_int("n_objs", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    vertical = rng.random() < 0.5
    if vertical:
        line_c = rng.randint(3, w - 4)
        fill_box(g, 0, line_c, h - 1, line_c, 9)
        side_lo, side_hi = 0, line_c - 1
    else:
        line_r = rng.randint(3, h - 4)
        fill_box(g, line_r, 0, line_r, w - 1, 9)
        side_lo, side_hi = 0, line_r - 1
    palette = list(random_palette(rng, n, exclude={9}))
    placed: list[tuple[int, int, int, int]] = []
    for color in palette:
        shape = rng.choice(_SHAPES)
        sh = max(c[0] for c in shape) + 1
        sw = max(c[1] for c in shape) + 1
        for _ in range(80):
            if vertical:
                r0 = rng.randint(0, h - sh)
                c0 = rng.randint(0, side_hi - sw)
            else:
                r0 = rng.randint(0, side_hi - sh)
                c0 = rng.randint(0, w - sw)
            bb = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb, p) for p in placed): continue
            paint_at(g, r0, c0, shape, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_line":
        # No full-grid 9-line — rule's mirror axis is undefined;
        # no mirroring.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[5 + dr][6 + dc] = 6
        return g
    if name == "no_objects":
        # Line present but no objects — rule has nothing to mirror;
        # output equals input.
        for c in range(w):
            g[4][c] = 9
        return g
    if name == "already_mirrored":
        # Objects already exist symmetrically on both sides — rule's
        # mirror is identity; no contrast.
        for r in range(h):
            g[r][4] = 9
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][1 + dc] = 4
        for dr, dc in [(0, 0), (0, -1), (1, 0)]:
            g[2 + dr][7 + dc] = 4  # mirror across c=4
        return g
    return g
