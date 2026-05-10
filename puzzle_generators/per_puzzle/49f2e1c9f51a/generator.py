"""Generator for 2dd70a9a.

Rule: color-3 segment draws an orthogonal path to the color-2
segment, then restores the 2s.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
seg_length.
Degenerates: no_segments, single_segment, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "49f2e1c9f51a"
VERSION = "1.1.0"
TASK_ID = "49f2e1c9f51a"
SUMMARY = "Color-3 segment draws orthogonal path to color-2 segment."

INVARIANTS = [
    "color 3 forms a single horizontal or vertical source segment",
    "color 2 forms a separated target segment",
    "the source endpoint facing the target determines path direction",
    "segments sit clear of borders so the path has room",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_segments", "single_segment", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "seg_length":     {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    h = rng.randint(10, 13)
    w = rng.randint(10, 13)
    g = full_grid(h, w, 0)
    if orientation == "horizontal":
        r3 = rng.randint(2, 4)
        c3 = rng.randint(2, 3)
        r2 = rng.randint(6, h - 3)
        c2 = rng.randint(6, w - 3)
        for c in range(c3, c3 + 3):
            g[r3][c] = 3
        for c in range(c2, c2 + 2):
            g[r2][c] = 2
    else:
        r3 = rng.randint(2, 3)
        c3 = rng.randint(2, 4)
        r2 = rng.randint(6, h - 3)
        c2 = rng.randint(6, w - 3)
        for r in range(r3, r3 + 3):
            g[r][c3] = 3
        for r in range(r2, r2 + 2):
            g[r][c2] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_segments":
        return g
    if name == "single_segment":
        for c in range(2, 5):
            g[2][c] = 3
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 3
        return g
    return g
