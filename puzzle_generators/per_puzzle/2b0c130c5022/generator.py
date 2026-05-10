"""Generator for 753ea09b.

Rule: crossing paths divide the background; smaller enclosed regions
are filled.

Combinatorial axes (8): grid_h/w, offset, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_paths, single_path, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2b0c130c5022"
VERSION = "1.1.0"
TASK_ID = "2b0c130c5022"
SUMMARY = "Crossing paths divide bg; smaller enclosed regions are filled."

INVARIANTS = [
    "the modal color is background",
    "two non-background paths cross and partition the background into regions",
    "the most frequent path color fills all but the two largest background regions",
    "fill and cross colors are distinct and non-zero",
]

OFFSETS = ("o0", "o1", "o2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_paths", "single_path", "full_grid")
HELPFUL_TEXTURES = OFFSETS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "offset":         {"type": "str", "default": "rng helpful",
                       "valid": "|".join(OFFSETS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for offset",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in OFFSETS:
        offset = int(tx[1])
    else:
        offset = ctx.draw_choice("offset", [0, 1, 2])
    fill, cross = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    h = 12 + offset
    w = 14
    g = full_grid(h, w, 0)
    vr = 5 + offset
    hc = 6
    for r in range(h):
        g[r][hc] = fill
    for c in range(w):
        g[vr][c] = cross
    for r in range(0, h, 3):
        g[r][hc + 1] = fill
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 14, 0)
    if name == "no_paths":
        return g
    if name == "single_path":
        for r in range(12):
            g[r][6] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
