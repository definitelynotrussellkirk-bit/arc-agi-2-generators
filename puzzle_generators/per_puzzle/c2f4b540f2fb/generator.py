"""Generator for arc_puzzle_bank_21_set22_s:S22_E6 — copy max-x motif points to target frame.

Rule: only source motif points with maximum local x are copied to the
target frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_offsets,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source_frame, no_target_frame, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.local_frame import choose_frame, draw_marker_frame, frame_cells, gpos

GENERATOR_ID = "c2f4b540f2fb"
VERSION = "1.1.0"
TASK_ID = "c2f4b540f2fb"
SUMMARY = "Only source motif points with maximum local x are copied to the target frame."

INVARIANTS = [
    "background is 0",
    "source motif points are color 8",
    "target frame has room for the maximum-x motif subset",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source_frame", "no_target_frame", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_offsets":      {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "two_local_frames",
                       "valid": "two_local_frames"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

OFFSET_SETS = [
    [(1, 1), (2, 0), (2, 2)],
    [(0, 2), (2, 1), (3, 0), (3, 2)],
    [(1, 3), (2, 0), (3, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    offsets = rng.choice(OFFSET_SETS)
    so, svx, svy = choose_frame(rng, h, w, offsets)
    source_cells = set(frame_cells(so, svx, svy)) | {gpos(so, svx, svy, *uv) for uv in offsets}
    to, tvx, tvy = choose_frame(rng, h, w, offsets, forbidden=source_cells)
    draw_marker_frame(grid, so, svx, svy, (2, 3, 4))
    draw_marker_frame(grid, to, tvx, tvy, (5, 6, 7))
    for uv in offsets:
        r, c = gpos(so, svx, svy, *uv)
        grid[r][c] = 8
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_source_frame":
        # only target frame markers + 8-motif → no source frame to lift max-x from
        g[2][8] = 5; g[3][8] = 6; g[2][9] = 7
        g[1][1] = 8; g[2][2] = 8
        return g
    if name == "no_target_frame":
        # source frame + motif but no target frame → nowhere to copy max-x to
        g[1][1] = 2; g[2][1] = 3; g[1][2] = 4
        g[3][3] = 8; g[4][4] = 8
        return g
    if name == "no_motif":
        # both frames present but no 8-motif → no max-x subset to copy
        g[1][1] = 2; g[2][1] = 3; g[1][2] = 4
        g[6][7] = 5; g[7][7] = 6; g[6][8] = 7
        return g
    return g
