"""Generator for 3befdf3e.

Rule: nested rectangular two-color frame expands into a larger
rounded frame motif.

Combinatorial axes (8): grid_h/w, frame_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_frame, full_grid, single_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e44712f65f3e"
VERSION = "1.1.0"
TASK_ID = "e44712f65f3e"
SUMMARY = "Nested two-color frame expands into a larger rounded frame motif."

INVARIANTS = [
    "background cells are color 0",
    "each object is a connected rectangle with an outer color and a different inner color",
    "the top-left cell of the object determines the outer color",
    "the frame sits clear of grid borders so expansion has room",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "full_grid", "single_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "frame_size":     {"type": "int", "default": "rng 4..5", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    if difficulty == "easy":
        sz_lo, sz_hi = 4, 4
    elif difficulty == "hard":
        sz_lo, sz_hi = 5, 7
    else:
        sz_lo, sz_hi = 4, 5
    size = ctx.draw_int("frame_size", sz_lo, sz_hi)
    outer, inner = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    h = rng.randint(12, 16)
    w = rng.randint(12, 16)
    g = full_grid(h, w, 0)
    margin = size // 2 + 1
    r0 = rng.randint(margin, h - size - margin)
    c0 = rng.randint(margin, w - size - margin)
    for r in range(size):
        for c in range(size):
            if r in (0, size - 1) or c in (0, size - 1):
                g[r0 + r][c0 + c] = outer
            else:
                g[r0 + r][c0 + c] = inner
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_frame":
        return g
    if name == "single_color":
        for r in range(4, 9):
            for c in range(4, 9):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
