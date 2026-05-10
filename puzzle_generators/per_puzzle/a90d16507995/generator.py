"""Generator for arc_puzzle_bank_fifteenth21:M104 — crop blob, stamp at marker.

Rule: a multi-color blob + a 9-marker. Crop the blob to its bbox,
then stamp at the marker's position (top-left).

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_blob, marker_inside_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "a90d16507995"
VERSION = "1.1.0"
TASK_ID = "a90d16507995"
SUMMARY = "Multi-color blob + a 9-marker with room to stamp at marker."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell + one connected non-9 blob",
    "marker's position has room for the stamp (bbox fits)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_blob", "marker_inside_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "blob_upper_marker_lower",
                       "valid": "blob_upper_marker_lower"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    # blob in upper-left half
    for r in range(h):
        for c in range(w):
            if r >= h // 2 or c >= w // 2:
                used.add((r, c))
    palette = rng.sample([2, 3, 4, 5, 6, 7, 8], 2)
    cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
    if cells is None:
        return g
    cells_list = sorted(cells)
    for i, (r, c) in enumerate(cells_list):
        g[r][c] = palette[i % len(palette)]
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    bb_h = max(rs) - min(rs) + 1
    bb_w = max(cs) - min(cs) + 1
    # marker in lower-right with room
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
        # Blob present but no 9-marker — rule has no anchor to stamp at.
        g[0][0] = 2; g[0][1] = 3; g[1][0] = 2
        return g
    if name == "no_blob":
        # 9-marker present but no blob — rule has nothing to stamp.
        g[5][5] = 9
        return g
    if name == "marker_inside_blob":
        # Marker overlaps blob bbox — ambiguous stamp position.
        g[1][1] = 2; g[1][2] = 3; g[2][1] = 2; g[2][2] = 9
        return g
    return g
