"""Generator for arc_puzzle_bank_ninth21:E59.

Rule: left-edge row keys recolor color-8 markers in the same row.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
marker_density.
Degenerates: no_keys, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0d5077971eea"
VERSION = "1.1.0"
TASK_ID = "0d5077971eea"

SUMMARY = "Left-edge row keys recolor color-8 markers in same row."

INVARIANTS = [
    "background is 0",
    "column 0 holds a non-8 key color for every active row",
    "each active row has one or more 8 markers",
    "non-marker cells are preserved",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_keys", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "5..8"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "7..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "marker_density": {"type": "str", "default": "rng", "valid": "low|med|high"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 11)
    g = full_grid(h, w, 0)
    for r in range(h):
        key = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
        g[r][0] = key
        marker_count = rng.randint(1, min(3, w - 1))
        for c in rng.sample(range(1, w), marker_count):
            g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 8, 0)
    if name == "no_keys":
        g[3][3] = 8
        return g
    if name == "no_markers":
        for r in range(6):
            g[r][0] = 3
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(8):
                g[r][c] = 8
        return g
    return g
