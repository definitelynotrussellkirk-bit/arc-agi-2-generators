"""Generator for arc_puzzle_bank_21_set13_bundle:medium_m02 — corner marker chooses transform.

Rule: a single 9-marker at one of 4 grid corners. Crop the (single)
non-corner blob to its bbox, then apply a transform based on which
corner held the marker:
  TL → identity, TR → rotate-cw, BL → flip-lr, BR → rotate-180.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_blob, marker_in_middle.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "ec1c917f8de0"
VERSION = "1.1.0"
TASK_ID = "ec1c917f8de0"
SUMMARY = "9 at one corner + a non-rectangular blob away from corners."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell, at a corner (TL/TR/BL/BR)",
    "exactly one non-9 blob, non-rectangular (so all 4 transforms differ)",
    "blob doesn't touch any corner",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_blob", "marker_in_middle")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "corner_marker_blob_center",
                       "valid": "corner_marker_blob_center"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
    corner = rng.choice(corners)
    g[corner[0]][corner[1]] = 9
    used = {corner}
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    for _ in range(40):
        cells = grow_blob(rng, h, w, used, rng.randint(4, 6), max_attempts=20)
        if cells is None:
            continue
        if any(p in corners for p in cells):
            continue
        rs = [r for r, _ in cells]; cs = [c for _, c in cells]
        bb = (max(rs) - min(rs) + 1) * (max(cs) - min(cs) + 1)
        if bb == len(cells):
            continue
        for r, c in cells:
            g[r][c] = color
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # Blob present but no 9-marker at any corner — rule has no
        # transform code to apply.
        for r, c in [(3, 3), (3, 4), (4, 3), (4, 4), (5, 4)]:
            g[r][c] = 5
        return g
    if name == "no_blob":
        # 9-marker at corner but no blob — rule has nothing to transform.
        g[0][0] = 9
        return g
    if name == "marker_in_middle":
        # 9-marker placed mid-grid (not at a corner) — rule's
        # corner-determines-transform mapping has no entry for non-corners.
        g[3][4] = 9
        for r, c in [(5, 1), (5, 2), (6, 1), (6, 2), (7, 2)]:
            g[r][c] = 5
        return g
    return g
