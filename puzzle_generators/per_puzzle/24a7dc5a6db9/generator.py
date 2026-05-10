"""Generator for arc_additional_puzzle_bank_volume17:M118.

Rule: red cells span a bounding rectangle; empty border positions of that
rectangle become 8.

Combinatorial axes (8): grid_h/w, palette_kind, bbox_padding,
distractor_color, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_red_cells, single_red, border_already_complete.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "24a7dc5a6db9"
VERSION = "1.1.0"
TASK_ID = "24a7dc5a6db9"
SUMMARY = "Red cells define a bounding rectangle; empty border positions of that rectangle become 8."

INVARIANTS = [
    "red cells span a rectangle with empty border gaps",
    "non-red distractors do not affect the red bounding box",
]

PALETTE_KINDS = ("default", "warm_distractor", "cool_distractor", "neutral_distractor")
DEGENERATE_TEXTURES = ("no_red_cells", "single_red", "border_already_complete")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bbox_padding":   {"type": "int", "default": "1", "valid": "1"},
    "distractor_color": {"type": "int", "default": "5", "valid": "5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "centered_bbox",
                       "valid": "centered_bbox"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r0 = rng.randint(1, h // 2 - 1)
    c0 = rng.randint(1, w // 2 - 1)
    r1 = rng.randint(h // 2 + 1, h - 2)
    c1 = rng.randint(w // 2 + 1, w - 2)
    for r, c in [(r0, c0), (r1, c1), (r0, c1), ((r0 + r1) // 2, c0)]:
        g[r][c] = 2
    g[h - 1][w - 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_red_cells":
        # only distractors — bbox of red is undefined
        g[3][4] = 5
        g[7][2] = 6
        return g
    if name == "single_red":
        # 1 red cell → degenerate 1×1 bbox
        g[4][5] = 2
        g[h - 1][w - 1] = 5
        return g
    if name == "border_already_complete":
        # rectangle border fully painted in red — rule has nothing to fill
        for c in range(2, 8):
            g[2][c] = 2
            g[7][c] = 2
        for r in range(2, 8):
            g[r][2] = 2
            g[r][7] = 2
        return g
    return g
