"""Generator for arc_puzzle_bank_thirteenth21:M85 — move blob to 9-marker.

Rule: a 9-marker + a single non-9 blob. Output: empty grid with the
blob moved so its top-left corner lands at the marker's position.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_blob, marker_on_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "ce40117f40f9"
VERSION = "1.1.0"
TASK_ID = "ce40117f40f9"
SUMMARY = "Single blob in upper-left + 9-marker in lower-right with room to move."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell + one non-9 blob",
    "blob's bbox can be placed at marker's position without OOB",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_blob", "marker_on_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    # blob in upper-left
    used: set[tuple[int, int]] = set()
    for r in range(h):
        for c in range(w):
            if r >= h // 2 or c >= w // 2:
                used.add((r, c))
    cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if cells is None:
        return g
    for r, c in cells:
        g[r][c] = color
    # 9-marker in lower-right area
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    bb_h = max(rs) - min(rs) + 1
    bb_w = max(cs) - min(cs) + 1
    for _ in range(40):
        mr = rng.randint(h // 2, h - bb_h)
        mc = rng.randint(w // 2, w - bb_w)
        if g[mr][mc] == 0:
            g[mr][mc] = 9
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # blob but no 9-marker → no destination, blob can't move
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        return g
    if name == "no_blob":
        # marker but no blob → nothing to move
        g[5][6] = 9
        return g
    if name == "marker_on_blob":
        # marker overlaps blob's bbox → ambiguous source/destination
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[1][1] = 9  # overwrite blob cell with marker
        return g
    return g
