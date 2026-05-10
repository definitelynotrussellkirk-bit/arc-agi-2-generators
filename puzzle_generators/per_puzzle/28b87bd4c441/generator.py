"""Generator for arc_additional_puzzles_21_set3:M21 — Move 5-blob to align top-left with marker-2.

Rule: marker = first cell of color 2; obj = first 5-blob. dr/dc shift =
(marker - obj.top-left). Output is empty grid + shifted 5-blob.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_blob, marker_inside_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "28b87bd4c441"
VERSION = "1.1.0"
TASK_ID = "28b87bd4c441"
SUMMARY = "5-blob upper-left + 2-marker lower-right with enough room to shift the blob in-bounds."

INVARIANTS = [
    "exactly one 5-blob in upper-left quadrant",
    "exactly one 2-marker downstream from blob's top-left, leaving room",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_blob", "marker_inside_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "blob_upper_left_marker_lower_right",
                       "valid": "blob_upper_left_marker_lower_right"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    blob_h = rng.randint(2, 3); blob_w = rng.randint(2, 3)
    or1 = rng.randint(0, h // 3)
    oc1 = rng.randint(0, w // 3)
    cells = [(or1, oc1)]
    target = rng.randint(3, blob_h * blob_w)
    while len(cells) < target:
        rb, cb = rng.choice(cells)
        dr, dc = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nr, nc = rb + dr, cb + dc
        if (or1 <= nr <= or1 + blob_h - 1) and (oc1 <= nc <= oc1 + blob_w - 1) and (nr, nc) not in cells:
            cells.append((nr, nc))
        elif len(cells) > 3 and rng.random() < 0.05:
            break
    for r, c in cells: g[r][c] = 5
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    or1, oc1 = min(rs), min(cs); or2, oc2 = max(rs), max(cs)
    obh = or2 - or1 + 1; obw = oc2 - oc1 + 1
    for _ in range(40):
        mr = rng.randint(or1 + 2, h - obh)
        mc = rng.randint(oc1 + 2, w - obw)
        if (mr, mc) in cells: continue
        if g[mr][mc] != 0: continue
        g[mr][mc] = 2
        return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # blob present but no 2-marker → no destination, rule has no instruction
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 5
        return g
    if name == "no_blob":
        # marker present but no 5-blob → rule has nothing to move
        g[5][7] = 2
        return g
    if name == "marker_inside_blob":
        # marker overlaps a blob cell → shift = (0, 0), rule is identity
        for (r, c) in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 5
        g[2][2] = 2  # overrides one of the 5-cells; marker at blob.top-left → shift=(0,0)
        return g
    return g
