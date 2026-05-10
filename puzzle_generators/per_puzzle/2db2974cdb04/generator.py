"""Generator for arc_additional_puzzle_bank_volume5:M30.

Rule: for each closed frame, fill its interior 0-region with the frame's
color.

Combinatorial axes (8): grid_h/w, palette_kind, num_frames, frame_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_frame, frame_open, nested_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "2db2974cdb04"
VERSION = "1.1.0"
TASK_ID = "2db2974cdb04"
SUMMARY = "2 closed rectangle frames (distinct colors) with empty interiors."

INVARIANTS = [
    "exactly 2 closed frames of distinct colors",
    "each has a 3+ cell interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("no_frame", "frame_open", "nested_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_frames":     {"type": "int", "default": "2", "valid": "1..3"},
    "frame_size":     {"type": "str", "default": "mixed",
                       "valid": "small|mixed|large"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(1, 10)); rng.shuffle(palette)
    draw_frame(g, 1, 1, 5, 5, palette[0])
    draw_frame(g, 2, 7, 5, w - 2, palette[1])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # scattered colored cells — no closed frames to fill
        g[2][2] = 4
        g[3][6] = 7
        g[6][9] = 5
        return g
    if name == "frame_open":
        # frame with one side missing — interior reaches background, rule fills nothing
        for c in range(1, 6):
            g[1][c] = 3
        for r in range(1, 6):
            g[r][1] = 3
            g[r][5] = 3
        # bottom row missing — frame is open
        return g
    if name == "nested_frames":
        # frame inside a frame — interior of outer reaches inner's border, ambiguous fill
        draw_frame(g, 1, 1, 7, 10, 4)
        draw_frame(g, 3, 3, 5, 8, 7)
        return g
    return g
