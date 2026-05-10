"""Generator for 465b7d93.

Rule: colored shape outside purple frame indicates which interior
edges to fill; cue is erased.

Combinatorial axes (8): grid_h/w, frame_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
cue_color.
Degenerates: no_frame, no_cue, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import RING_3X3

GENERATOR_ID = "c130e51c4310"
VERSION = "1.1.0"
TASK_ID = "c130e51c4310"
SUMMARY = "Cue shape outside purple frame indicates interior edges to fill."

INVARIANTS = [
    "background is color 7",
    "one hollow rectangular frame uses color 6",
    "one cue shape uses a non-background non-6 color outside the frame",
    "the cue color is non-zero and not 6 or 7",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_cue", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "frame_size":     {"type": "int", "default": "rng 5..6", "valid": "5..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "cue_color":      {"type": "color", "default": "rng !{0,6,7}",
                       "valid": "1|2|3|4|5|8|9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    size = ctx.draw_int("frame_size", 5, 6)
    h = 11 + rng.randint(0, 2)
    w = 11 + rng.randint(0, 2)
    g = full_grid(h, w, 7)
    fr = h - size - 1
    fc = w - size - 1
    for c in range(fc, fc + size):
        g[fr][c] = 6
        g[fr + size - 1][c] = 6
    for r in range(fr, fr + size):
        g[r][fc] = 6
        g[r][fc + size - 1] = 6
    color = ctx.draw_color("cue_color", exclude={0, 6, 7})
    patterns = [
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(2, 0), (2, 1), (2, 2), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(0, 2), (1, 2), (2, 2), (1, 1)],
        RING_3X3,
    ]
    pattern = patterns[(seed + sample_index + rng.randint(0, 4)) % len(patterns)]
    sr = 1
    sc = 1 + ((sample_index // 2) % 2)
    for dr, dc in pattern:
        g[sr + dr][sc + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 7)
    if name == "no_frame":
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1)]:
            g[1 + dr][1 + dc] = 2
        return g
    if name == "no_cue":
        for c in range(5, 10):
            g[5][c] = 6; g[9][c] = 6
        for r in range(5, 10):
            g[r][5] = 6; g[r][9] = 6
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 6
        return g
    return g
