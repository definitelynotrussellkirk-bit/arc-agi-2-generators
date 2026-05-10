"""Generator for arc_puzzle_bank_21_set4_d:hard_d07.

Each rectangular frame contains a small interior pattern. The rule extracts the
interiors, crops them to content, sorts by frame color, and builds a gallery.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, empty_interiors, equal_frame_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "a99e79b52aa4"
VERSION = "1.1.0"
TASK_ID = "a99e79b52aa4"
SUMMARY = "Extract framed interior patterns and concatenate them by frame color."

INVARIANTS = [
    "there are two or three hollow rectangular frames with distinct colors",
    "each frame interior contains non-frame colored cells",
    "interior patterns are separated from their frame borders",
    "the output is a top-aligned gallery sorted by frame color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "empty_interiors", "equal_frame_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15..15"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "position_bias":  {"type": "str", "default": "three_frames_with_interiors",
                       "valid": "three_frames_with_interiors"},
    "n_distinct_colors": {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_FRAME_BOXES = [
    (1, 1, 6, 6),
    (1, 9, 6, 14),
    (8, 4, 13, 9),
]

_PATTERNS = [
    [(1, 1, 8), (1, 2, 8), (2, 1, 5)],
    [(1, 1, 6), (2, 1, 6), (2, 2, 7), (3, 2, 7)],
    [(1, 2, 3), (2, 1, 3), (2, 2, 9), (2, 3, 9)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        n_frames = ctx.draw_int("n_frames", 3, 3)
    else:
        n_frames = ctx.draw_int("n_frames", 2, 3)
    frame_colors = rng.sample([1, 2, 4, 5, 6, 7], n_frames)
    g = full_grid(15, 16, 0)
    for box, color, pattern in zip(_FRAME_BOXES, frame_colors, _PATTERNS):
        r1, c1, r2, c2 = box
        draw_frame(g, r1, c1, r2, c2, color)
        for dr, dc, value in pattern:
            g[r1 + dr][c1 + dc] = value if value != color else 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 16, 0)
    if name == "no_frames":
        # patterns scattered without frames → no boundaries to extract by
        for r, c, v in [(2, 2, 8), (5, 5, 6), (10, 7, 3)]:
            g[r][c] = v
        return g
    if name == "empty_interiors":
        # frames present but no interior patterns → nothing to extract
        for box, color in zip(_FRAME_BOXES[:2], [1, 2]):
            r1, c1, r2, c2 = box
            draw_frame(g, r1, c1, r2, c2, color)
        return g
    if name == "equal_frame_colors":
        # 2 frames share color → "distinct frame colors" precondition fails
        for box in _FRAME_BOXES[:2]:
            r1, c1, r2, c2 = box
            draw_frame(g, r1, c1, r2, c2, 1)
        for r, c, v in [(2, 2, 8), (3, 11, 6)]:
            g[r][c] = v
        return g
    return g
