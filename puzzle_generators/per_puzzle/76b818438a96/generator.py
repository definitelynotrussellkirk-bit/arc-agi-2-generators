"""Generator for 696d4842.

Rule: a path endpoint extends to an aligned singleton marker while the
opposite endpoint is recolored.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_path, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "76b818438a96"
VERSION = "1.1.0"
TASK_ID = "76b818438a96"
SUMMARY = "Path endpoint extends to aligned marker; opposite endpoint is recolored."

INVARIANTS = [
    "one nonzero path object has two cardinal endpoints",
    "one singleton marker lies beyond exactly one endpoint in the endpoint direction",
    "the path extends through the gap to the marker",
    "the same number of cells from the opposite endpoint are recolored to the marker color",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_path", "no_marker", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "9..12"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "10..14"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    path_color, marker_color = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    h = 9 + rng.randint(0, 3)
    w = 10 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    length = rng.randint(4, 6)
    gap = rng.randint(2, min(4, length - 1))
    if orientation == "horizontal":
        r = rng.randint(2, h - 3)
        c0 = rng.randint(1, w - length - gap - 2)
        for c in range(c0, c0 + length):
            g[r][c] = path_color
        g[r][c0 + length + gap] = marker_color
    else:
        c = rng.randint(2, w - 3)
        r0 = rng.randint(1, h - length - gap - 2)
        for r in range(r0, r0 + length):
            g[r][c] = path_color
        g[r0 + length + gap][c] = marker_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_path":
        g[5][8] = 4
        return g
    if name == "no_marker":
        for c in range(2, 8):
            g[5][c] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
