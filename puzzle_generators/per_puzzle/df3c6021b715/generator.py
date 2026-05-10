"""Generator for puzzle 1bfc4729.

Rule: 2 non-zero dots sorted by row. Top half is c1's frame border;
bottom half is c2's. Sides connect.

Combinatorial axes (8): grid_h/w, dot1_color, dot2_color,
dot1_position, dot2_position, palette_kind, anchor_corner,
asymmetry_force.
Degenerates: same_color, same_position, no_dots.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "df3c6021b715"
VERSION = "1.1.0"
TASK_ID = "df3c6021b715"
SUMMARY = "2 dots in upper/lower halves; rule frames in 2 colors."

INVARIANTS = [
    "background is 0",
    "exactly 2 non-zero cells",
    "first dot in upper half (row < h/2)",
    "second dot in lower half (row >= h/2)",
    "the two dots have distinct colors",
]

POSITION_BIASES = ("scattered", "left_aligned", "right_aligned",
                   "centered", "diagonal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_color", "same_position", "no_dots")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "dot1_color":     {"type": "color", "default": "rng (≠0,c2)",
                       "valid": "1..9"},
    "dot2_color":     {"type": "color", "default": "rng (≠0,c1)",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    palette = _build_palette(palette_kind, rng)
    c1 = int(overrides.get("dot1_color", palette[0]))
    c2 = int(overrides.get("dot2_color",
                           next((c for c in palette if c != c1),
                                2 if c1 != 2 else 3)))
    if c1 == c2:
        c2 = next((c for c in palette if c != c1),
                  2 if c1 != 2 else 3)
    g = full_grid(h, w, 0)
    r1, cc1 = _pick_upper(bias, h, w, rng)
    r2, cc2 = _pick_lower(bias, h, w, rng)
    g[r1][cc1] = c1
    g[r2][cc2] = c2
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _pick_upper(bias, h, w, rng):
    r = rng.randint(1, max(1, h // 2 - 1))
    if bias == "left_aligned":
        return r, rng.randint(1, max(1, w // 3))
    if bias == "right_aligned":
        return r, rng.randint(2 * w // 3, w - 2)
    if bias == "centered":
        return r, w // 2
    if bias == "diagonal":
        return r, max(1, min(w - 2, r))
    return r, rng.randint(1, w - 2)


def _pick_lower(bias, h, w, rng):
    r = rng.randint(h // 2 + 1, max(h // 2 + 1, h - 2))
    if bias == "left_aligned":
        return r, rng.randint(1, max(1, w // 3))
    if bias == "right_aligned":
        return r, rng.randint(2 * w // 3, w - 2)
    if bias == "centered":
        return r, w // 2
    if bias == "diagonal":
        return r, max(1, min(w - 2, r))
    return r, rng.randint(1, w - 2)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "same_color":
        c = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        g[1][1] = c
        g[h - 2][w - 2] = c
        return g
    if name == "same_position":
        # Both at same row → can't decide which is "upper"
        g[h // 2][1] = 3
        g[h // 2][w - 2] = 4
        return g
    if name == "no_dots":
        return g
    return g
