"""Generator for arc_puzzle_bank_21_set22_s:S22_E4 — copy local 8 offset between frames.

Rule: one source-frame local 8 offset is copied into a target frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, offset_choice,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_source_8, no_target_frame, both_frames_have_8.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.local_frame import choose_frame, draw_marker_frame, frame_cells, gpos

GENERATOR_ID = "1e36fd36fdb1"
VERSION = "1.1.0"
TASK_ID = "1e36fd36fdb1"
SUMMARY = "One source-frame local 8 offset is copied into a target frame."

INVARIANTS = [
    "background is 0",
    "one source frame uses colors 2,3,4",
    "one target frame uses colors 5,6,7",
    "there is exactly one source-local color-8 motif cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_source_8", "no_target_frame", "both_frames_have_8")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "offset_choice":  {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "two_marker_frames_with_local_8",
                       "valid": "two_marker_frames_with_local_8"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

OFFSETS = [(2, 0), (0, 2), (1, 1), (2, 2), (3, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    uv = rng.choice(OFFSETS)
    so, svx, svy = choose_frame(rng, h, w, [uv])
    source_cells = set(frame_cells(so, svx, svy)) | {gpos(so, svx, svy, *uv)}
    to, tvx, tvy = choose_frame(rng, h, w, [uv], forbidden=source_cells)
    draw_marker_frame(grid, so, svx, svy, (2, 3, 4))
    draw_marker_frame(grid, to, tvx, tvy, (5, 6, 7))
    r, c = gpos(so, svx, svy, *uv)
    grid[r][c] = 8
    return grid


def _draw_from_degenerate(name, rng):
    import random
    rng2 = random.Random(0)
    h, w = 10, 12
    grid = full_grid(h, w, 0)
    uv = (2, 0)
    so, svx, svy = choose_frame(rng2, h, w, [uv])
    source_cells = set(frame_cells(so, svx, svy)) | {gpos(so, svx, svy, *uv)}
    to, tvx, tvy = choose_frame(rng2, h, w, [uv], forbidden=source_cells)
    if name == "no_source_8":
        # source frame but no 8-motif → nothing to copy
        draw_marker_frame(grid, so, svx, svy, (2, 3, 4))
        draw_marker_frame(grid, to, tvx, tvy, (5, 6, 7))
        return grid
    if name == "no_target_frame":
        # source frame + 8 but no target frame → no destination
        draw_marker_frame(grid, so, svx, svy, (2, 3, 4))
        r, c = gpos(so, svx, svy, *uv)
        grid[r][c] = 8
        return grid
    if name == "both_frames_have_8":
        # both frames already have 8 → ambiguous source/destination roles
        draw_marker_frame(grid, so, svx, svy, (2, 3, 4))
        draw_marker_frame(grid, to, tvx, tvy, (5, 6, 7))
        sr, sc = gpos(so, svx, svy, *uv)
        tr, tc = gpos(to, tvx, tvy, *uv)
        grid[sr][sc] = 8
        grid[tr][tc] = 8
        return grid
    return grid
