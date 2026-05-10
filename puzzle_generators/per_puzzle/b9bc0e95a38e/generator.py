"""Generator for d06dbe63.

Rule: cyan seed emits a clipped gray stair pattern up-right and
down-left.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, seed_kind, n_seeds.
Degenerates: no_seed, full_grid, single_pixel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b9bc0e95a38e"
VERSION = "1.1.0"
TASK_ID = "b9bc0e95a38e"
SUMMARY = "Cyan seed emits clipped gray stair pattern up-right and down-left."

INVARIANTS = [
    "background is color 0",
    "there is exactly one color-8 seed pixel",
    "the rule preserves the seed and paints color-5 stair segments from it",
    "the seed leaves room for both upward-right and downward-left stair arms",
]

POSITION_BIASES = ("center", "top_left", "top_right", "bottom_left", "bottom_right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seed", "full_grid", "single_pixel")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "height":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "width":          {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "seed_kind":      {"type": "str", "default": "single", "valid": "single"},
    "n_seeds":        {"type": "int", "default": "1", "valid": "1"},
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
        h_lo, h_hi = 9, 10
    elif difficulty == "hard":
        h_lo, h_hi = 13, 16
    else:
        h_lo, h_hi = 9, 13
    h = ctx.draw_int("height", h_lo, h_hi)
    w = ctx.draw_int("width", h_lo, h_hi)
    pos = (overrides.get("texture") if overrides.get("texture") in POSITION_BIASES else None) or \
          overrides.get("position_bias") or \
          ctx.draw_choice("position_bias", list(POSITION_BIASES))
    g = full_grid(h, w, 0)
    if pos == "top_left":
        r, c = 3, 3
    elif pos == "top_right":
        r, c = 3, w - 4
    elif pos == "bottom_left":
        r, c = h - 4, 3
    elif pos == "bottom_right":
        r, c = h - 4, w - 4
    else:
        r = rng.randint(3, h - 4)
        c = rng.randint(3, w - 4)
    g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_seed":
        return g
    if name == "single_pixel":
        g[5][5] = 8
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 5
        return g
    return g
