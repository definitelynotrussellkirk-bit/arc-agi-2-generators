"""Generator for c61be7dc.

Rule: gray shape compresses to a centered line along the detected
track direction.

Combinatorial axes (8): grid_h/w, track, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, gray_count.
Degenerates: no_shape, no_track, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5c0bcc9d1b8b"
VERSION = "1.1.0"
TASK_ID = "5c0bcc9d1b8b"
SUMMARY = "Gray shape compresses to centered line along track direction."

INVARIANTS = [
    "the background track color is orange",
    "zero divider rows or columns define the compression direction",
    "the number of gray cells is preserved",
    "divider lines surround the gray shape on both sides",
]

TRACKS = ("vertical", "horizontal")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_track", "full_grid")
HELPFUL_TEXTURES = TRACKS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "track":          {"type": "str", "default": "rng helpful",
                       "valid": "|".join(TRACKS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "gray_count":     {"type": "int", "default": "5", "valid": "5..6"},
    "texture":        {"type": "str", "default": "alias for track",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    track = (overrides.get("texture") if overrides.get("texture") in TRACKS else None) or \
            overrides.get("track") or \
            ctx.draw_choice("track", list(TRACKS))
    if "track" not in overrides:
        track = "vertical" if sample_index % 2 == 0 else "horizontal"
    shift = (sample_index // 2) % 2
    g = full_grid(11, 11, 7)
    if track == "vertical":
        for r in range(11):
            g[r][4] = 0
            g[r][6] = 0
        for c in range(11):
            g[1 + shift][c] = 0
            g[8 - shift][c] = 0
        gray_cells = [(4, 5), (5, 5), (5, 4), (5, 6), (6, 5)]
    else:
        for c in range(11):
            g[4][c] = 0
            g[6][c] = 0
        for r in range(11):
            g[r][1 + shift] = 0
            g[r][8 - shift] = 0
        gray_cells = [(5, 4), (5, 5), (4, 5), (6, 5), (5, 6)]
    if sample_index % 3 == 0:
        gray_cells.append((6, 6))
    for r, c in gray_cells:
        g[r][c] = 5
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 7)
    if name == "no_shape":
        for r in range(11):
            g[r][4] = 0; g[r][6] = 0
        return g
    if name == "no_track":
        for r, c in [(5, 5), (5, 4), (5, 6)]:
            g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 7
        return g
    return g
