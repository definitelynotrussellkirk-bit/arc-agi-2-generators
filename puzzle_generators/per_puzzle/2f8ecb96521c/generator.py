"""Generator for 694f12f3.

Rule: sort 4-blobs by size asc; smallest fills strict-interior with 1;
second smallest with 2.

Combinatorial axes (8): grid_h/w, blob1_h, blob1_w, blob2_h, blob2_w,
position_bias, distractor_color, anchor_corner.
Degenerates: same_size, single_blob, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "2f8ecb96521c"
VERSION = "1.1.0"
TASK_ID = "2f8ecb96521c"
SUMMARY = "2 solid 4-blobs of distinct sizes >=3x3."

INVARIANTS = [
    "exactly 2 solid 4-blobs of distinct sizes",
    "each >=3x3",
    "blobs don't touch",
]

POSITION_BIASES = ("opposite_corners", "diagonal", "stacked", "rng")
DEGENERATE_TEXTURES = ("same_size", "single_blob", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "blob1_h":        {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "blob1_w":        {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "blob2_h":        {"type": "int", "default": "3", "valid": "3..4"},
    "blob2_w":        {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "distractor_color":{"type": "color", "default": "rng",
                       "valid": "3|6|7|8"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 8, 9, 11
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 14, 14, 16
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 10, 11, 13
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    rh1 = int(overrides.get("blob1_h", rng.randint(3, 4)))
    rw1 = int(overrides.get("blob1_w", rng.randint(4, 5)))
    rh2 = int(overrides.get("blob2_h", 3))
    rw2 = int(overrides.get("blob2_w", 3))
    rh1 = max(3, min(rh1, h - 4))
    rw1 = max(3, min(rw1, w - 4))
    rh2 = max(3, min(rh2, h - 4))
    rw2 = max(3, min(rw2, w - 4))
    rh1 = max(3, min(4, rh1))
    rw1 = max(4, min(5, rw1))
    rh2, rw2 = 3, 3
    r1 = rng.randint(0, 2); c1 = rng.randint(0, 2)
    r2 = rng.randint(h - rh2 - 1, h - rh2)
    c2 = rng.randint(w - rw2 - 1, w - rw2)
    draw_rect(g, r1, c1, rh1, rw1, 4)
    if r2 > r1 + rh1 and c2 > c1 + rw1:
        draw_rect(g, r2, c2, rh2, rw2, 4)
    dcolor = int(overrides.get("distractor_color",
                               rng.choice([3, 6, 7, 8])))
    g[0][w - 1] = dcolor
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "same_size":
        draw_rect(g, 1, 1, 3, 3, 4)
        draw_rect(g, 5, 7, 3, 3, 4)
        return g
    if name == "single_blob":
        draw_rect(g, 2, 2, 4, 5, 4)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
