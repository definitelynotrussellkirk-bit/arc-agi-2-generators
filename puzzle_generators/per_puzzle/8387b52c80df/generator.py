"""Generator for v0_original:hard_02.

Rule: a hollow rectangular frame contains a single non-frame seed; fill
the frame's interior with the seed's color.

Combinatorial axes (8): grid_h/w, palette_kind, frame_color, seed_color,
seed_col, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_seed, multiple_seeds, no_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8387b52c80df"
VERSION = "1.1.0"
TASK_ID = "8387b52c80df"
SUMMARY = "Fill each hollow rectangular frame interior with its enclosed seed color."

INVARIANTS = [
    "there is one hollow rectangular frame",
    "the frame contains exactly one non-frame nonzero seed color",
    "the frame border color is preserved",
    "the interior zeros adopt the seed color",
]

PALETTE_KINDS = ("default", "warm_frame", "cool_frame", "primary_frame")
DEGENERATE_TEXTURES = ("no_seed", "multiple_seeds", "no_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6"},
    "grid_w":         {"type": "int", "default": "7", "valid": "7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_col":       {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "frame_color":    {"type": "int", "default": "rng",
                       "valid": "1..4|6..8"},
    "seed_color":     {"type": "int", "default": "rng", "valid": "5..9"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "centered",
                       "valid": "centered"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        seed_col = ctx.draw_int("seed_col", 2, 2)
    elif difficulty == "hard":
        seed_col = ctx.draw_int("seed_col", 3, 4)
    else:
        seed_col = ctx.draw_int("seed_col", 2, 4)
    frame_color = rng.choice([1, 2, 3, 4, 6, 7, 8])
    seed_color = rng.choice([5, 6, 7, 8, 9])
    if seed_color == frame_color:
        seed_color = 9 if frame_color != 9 else 5
    g = full_grid(6, 7, 0)
    for c in range(1, 5):
        g[1][c] = frame_color
        g[4][c] = frame_color
    for r in range(1, 5):
        g[r][1] = frame_color
        g[r][4] = frame_color
    g[2][seed_col] = seed_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 7, 0)
    frame_color = 3
    if name == "no_seed":
        # frame but no seed inside — interior fill color undefined
        for c in range(1, 5):
            g[1][c] = frame_color
            g[4][c] = frame_color
        for r in range(1, 5):
            g[r][1] = frame_color
            g[r][4] = frame_color
        return g
    if name == "multiple_seeds":
        # frame with 2 different seeds — fill color ambiguous
        for c in range(1, 5):
            g[1][c] = frame_color
            g[4][c] = frame_color
        for r in range(1, 5):
            g[r][1] = frame_color
            g[r][4] = frame_color
        g[2][2] = 5
        g[3][3] = 7
        return g
    if name == "no_frame":
        # seed without enclosing frame — rule has no region to fill
        g[2][3] = 5
        return g
    return g
