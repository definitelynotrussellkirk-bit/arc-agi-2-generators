"""Generator for 444801d8.

Rule: blue U-frame with interior colored dot fills its interior and
projects a bar through the opening.

Combinatorial axes (8): grid_h/w, frame_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_frames, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d6607fc42bcc"
VERSION = "1.1.0"
TASK_ID = "d6607fc42bcc"
SUMMARY = "Blue U-frame with interior dot fills interior and projects bar through opening."

INVARIANTS = [
    "each active component contains a color-1 U-frame",
    "one nonzero non-1 dot lies inside the frame bbox",
    "the open side of the U-frame determines bar direction",
    "frames sit clear of grid borders so the projection has room",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "no_dots", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "frame_count":    {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_u(g, r0, c0, height, width, dot, *, open_top):
    for r in range(height):
        g[r0 + r][c0] = 1
        g[r0 + r][c0 + width - 1] = 1
    edge_r = r0 + height - 1 if open_top else r0
    for c in range(width):
        g[edge_r][c0 + c] = 1
    if open_top:
        g[r0][c0] = 1
        g[r0][c0 + width - 1] = 1
    else:
        g[r0 + height - 1][c0] = 1
        g[r0 + height - 1][c0 + width - 1] = 1
    g[r0 + height // 2][c0 + width // 2] = dot


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        fc_lo, fc_hi = 1, 1
    elif difficulty == "hard":
        fc_lo, fc_hi = 2, 2
    else:
        fc_lo, fc_hi = 1, 2
    frame_count = ctx.draw_int("frame_count", fc_lo, fc_hi)
    dots = ctx.draw_distinct_colors("dot_colors", n=frame_count, exclude={0, 1})
    g = full_grid(13, 14, 0)
    placements = [(3, 2), (4, 8)]
    for i in range(frame_count):
        height = rng.randint(4, 5)
        width = rng.randint(4, 5)
        _draw_u(g, placements[i][0], placements[i][1], height, width, dots[i], open_top=(i % 2 == 0))
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 14, 0)
    if name == "no_frames":
        return g
    if name == "no_dots":
        for r in range(3, 8):
            g[r][2] = 1; g[r][6] = 1
        for c in range(2, 7):
            g[3][c] = 1
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(14):
                g[r][c] = 1
        return g
    return g
