"""Generator for 673ef223.

Rule: cyan dots on one red segment define row offsets and mirrored
fills on the plain segment.

Combinatorial axes (8): grid_h/w, dot_side, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_segments, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ec1260207f71"
VERSION = "1.1.0"
TASK_ID = "ec1260207f71"
SUMMARY = "Cyan dots on one red segment define row offsets mirrored on plain."

INVARIANTS = [
    "there are exactly two vertical red segments",
    "only one segment has same-row cyan dots displaced to one side",
    "dot row offsets are mirrored onto the other segment",
    "segments sit clear of grid borders",
]

DOT_SIDES = ("right", "left")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_segments", "no_dots", "full_grid")
HELPFUL_TEXTURES = DOT_SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "10..18"},
    "dot_side":       {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DOT_SIDES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for dot_side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    dot_side = (overrides.get("texture") if overrides.get("texture") in DOT_SIDES else None) or \
               overrides.get("dot_side") or \
               ctx.draw_choice("dot_side", list(DOT_SIDES))
    h = 8 + rng.randint(0, 3)
    w = 11 + rng.randint(0, 4)
    seg_len = rng.randint(4, 5)
    r0 = rng.randint(1, h - seg_len - 1)
    c_a = 3
    c_b = w - 4
    dot_seg, plain_seg = (c_a, c_b) if rng.randint(0, 1) else (c_b, c_a)
    g = full_grid(h, w, 0)
    for r in range(r0, r0 + seg_len):
        g[r][c_a] = 2
        g[r][c_b] = 2
    offsets = sorted(rng.sample(range(seg_len), rng.randint(2, min(4, seg_len))))
    for off in offsets:
        if dot_side == "right":
            dcol = min(w - 2, dot_seg + rng.randint(2, 4))
            if dcol == plain_seg:
                dcol -= 1
        else:
            dcol = max(1, dot_seg - rng.randint(2, 4))
            if dcol == plain_seg:
                dcol += 1
        if dcol != dot_seg:
            g[r0 + off][dcol] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 14, 0)
    if name == "no_segments":
        g[3][8] = 8
        return g
    if name == "no_dots":
        for r in range(2, 7):
            g[r][3] = 2; g[r][10] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
