"""Generator for 712bf12e.

Rule: bottom red starts trace upward paths, turning right when a gray
blocker is directly above.

Combinatorial axes (8): grid_h/w, start_count, blocker_density,
position_bias, palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_starts, no_blockers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "45922a9666b2"
VERSION = "1.1.0"
TASK_ID = "45922a9666b2"
SUMMARY = "Bottom red starts trace upward, turning right when blocked by gray."

INVARIANTS = [
    "background is color 0",
    "all starts are red cells on the bottom row",
    "gray cells act as blockers",
    "paths move upward unless blocked, then move right",
]

POSITION_BIASES = ("scattered", "even_spacing", "left_lean", "right_lean")
DEGENERATE_TEXTURES = ("no_starts", "no_blockers", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "start_count":    {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "blocker_density":{"type": "float", "default": "1.0", "valid": "0.5..1.0"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
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
        h_lo, h_hi = 8, 10
        sc_lo, sc_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
        sc_lo, sc_hi = 3, 5
    else:
        h_lo, h_hi = 10, 14
        sc_lo, sc_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    n = ctx.draw_int("start_count", sc_lo, sc_hi)
    n = max(1, min(min(w // 2, 5), n))
    g = full_grid(h, w, 0)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "even_spacing":
        start_cols = [1 + i * (w // (n + 1)) for i in range(n)]
    elif bias == "left_lean":
        start_cols = sorted(rng.sample(range(1, max(2, w // 2)), n))
    elif bias == "right_lean":
        start_cols = sorted(rng.sample(range(max(1, w // 2), w - 1), n))
    else:
        start_cols = [1 + i * 3 + ((sample_index + i) % 2) for i in range(n)]
    start_cols = [min(w - 2, max(0, c)) for c in start_cols]
    blocker_density = float(overrides.get("blocker_density", 1.0))
    for c in start_cols:
        g[h - 1][c] = 2
        if rng.random() <= blocker_density:
            block_r = h - 3 - ((seed + c + sample_index) % 3)
            if block_r > 1 and c + 1 < w:
                g[block_r][c] = 5
                g[block_r - 1][c + 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_starts":
        g[5][5] = 5
        return g
    if name == "no_blockers":
        g[h - 1][3] = 2
        g[h - 1][7] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
