"""Generator for arc_puzzle_bank_21_set22_s:S22_E7.

Rule: a source-frame motif is encoded as a canonical four-position
occupancy strip — the (2,3,4) frame defines local coordinates and 8s
mark which canonical offsets are filled.

Combinatorial axes (8): grid_h/w, palette_kind, n_motif, palette_size,
position_bias, n_distinct_colors, frame_orientation, texture.
Degenerates: no_motif, full_motif, no_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.local_frame import choose_frame, draw_marker_frame, gpos

GENERATOR_ID = "2fb0197be694"
VERSION = "1.1.0"
TASK_ID = "2fb0197be694"
SUMMARY = "A source-frame motif is encoded as a canonical four-position occupancy strip."

INVARIANTS = [
    "background is 0",
    "one source frame uses colors 2,3,4",
    "motif points are drawn from the canonical E7 offset list",
]

PALETTE_KINDS = ("default", "axis_aligned", "rotated", "mirrored")
DEGENERATE_TEXTURES = ("no_motif", "full_motif", "no_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_motif":        {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "frame_relative", "valid": "frame_relative"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "frame_orientation": {"type": "str", "default": "rng", "valid": "rng"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

CANON = [(2, 0), (0, 2), (1, 1), (2, 2)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    offsets = rng.sample(CANON, rng.randint(1, len(CANON)))
    origin, vx, vy = choose_frame(rng, h, w, offsets)
    draw_marker_frame(grid, origin, vx, vy, (2, 3, 4))
    for uv in offsets:
        r, c = gpos(origin, vx, vy, *uv)
        grid[r][c] = 8
    return grid


def _draw_from_degenerate(name, rng):
    import random
    rng = rng or random.Random(0)
    h, w = 9, 9
    grid = full_grid(h, w, 0)
    if name == "no_motif":
        # frame present but no 8s → strip is all-empty
        origin, vx, vy = choose_frame(rng, h, w, [])
        draw_marker_frame(grid, origin, vx, vy, (2, 3, 4))
        return grid
    if name == "full_motif":
        # every canonical offset filled → strip is fully on
        origin, vx, vy = choose_frame(rng, h, w, CANON)
        draw_marker_frame(grid, origin, vx, vy, (2, 3, 4))
        for uv in CANON:
            r, c = gpos(origin, vx, vy, *uv)
            grid[r][c] = 8
        return grid
    if name == "no_frame":
        # 8s present but no (2,3,4) frame → motif positions undefined
        grid[2][2] = 8
        grid[3][3] = 8
        return grid
    return grid
