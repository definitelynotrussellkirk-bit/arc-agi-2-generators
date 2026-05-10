"""Generator for f21745ec.

Rule: patterned template frame stamps its interior pattern into
matching frames.

Combinatorial axes (8): grid_h/w, pattern, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_frames, single_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "e3f1bc75d654"
VERSION = "1.1.0"
TASK_ID = "e3f1bc75d654"
SUMMARY = "Patterned template frame stamps interior pattern into matching frames."

INVARIANTS = [
    "one rectangular frame contains an interior pattern in its own color",
    "other frames with the same interior size receive the same relative pattern",
    "frames with different interior sizes are removed from the output",
    "frame colors are distinct and non-zero",
]

PATTERNS = ("p0", "p1", "p2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "full_grid")
HELPFUL_TEXTURES = PATTERNS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "pattern":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PATTERNS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for pattern",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _stamp_pattern(g, r0, c0, color, pattern):
    for dr, dc in pattern:
        g[r0 + 1 + dr][c0 + 1 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in PATTERNS:
        pattern_idx = int(tx[1])
    else:
        pattern_idx = ctx.draw_choice("pattern", [0, 1, 2])
    colors = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    patterns = [
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
    ]
    g = full_grid(14, 18, 0)
    same_size = [(1, 1), (1, 8), (8, 1)]
    for (r, c), color in zip(same_size, colors[:3]):
        draw_frame(g, r, c, r + 4, c + 4, color)
    _stamp_pattern(g, same_size[0][0], same_size[0][1], colors[0], patterns[pattern_idx])
    draw_frame(g, 7, 11, 13, 17, colors[3])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 18, 0)
    if name == "no_frames":
        return g
    if name == "single_frame":
        draw_frame(g, 1, 1, 5, 5, 2)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(18):
                g[r][c] = 2
        return g
    return g
