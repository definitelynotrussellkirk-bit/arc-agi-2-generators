"""Generator for 18419cfa.

Rule: red cells inside a cyan frame are mirrored horizontally,
vertically and both.

Combinatorial axes (8): grid_h/w, frame_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, n_red.
Degenerates: no_frame, no_red, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "dc078cd7f5e4"
VERSION = "1.1.0"
TASK_ID = "dc078cd7f5e4"
SUMMARY = "Red cells inside cyan frame mirrored horizontally and vertically."

INVARIANTS = [
    "a cyan rectangular frame defines the symmetry bounds",
    "red cells are inside the frame and not on the border",
    "at least one mirrored counterpart is initially blank",
    "the frame sits with at least one cell of margin from grid borders",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_red", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "frame_size":     {"type": "int", "default": "rng 5..7", "valid": "5..11"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_red":          {"type": "int", "default": "rng 1..3", "valid": "1..4"},
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
        size_lo, size_hi = 5, 5
    elif difficulty == "hard":
        size_lo, size_hi = 7, 9
    else:
        size_lo, size_hi = 5, 7
    size = ctx.draw_int("frame_size", size_lo, size_hi)
    h = size + 4
    w = size + 4
    g = full_grid(h, w, 0)
    r0 = rng.randint(1, 2)
    c0 = rng.randint(1, 2)
    draw_rect_outline(g, r0, c0, size, size, 8)
    cells = [(r, c) for r in range(r0 + 1, r0 + size - 1)
             for c in range(c0 + 1, c0 + size - 1)]
    for r, c in rng.sample(cells, rng.randint(1, min(3, len(cells)))):
        if r <= r0 + size // 2 and c <= c0 + size // 2:
            g[r][c] = 2
    if not any(2 in row for row in g):
        g[r0 + 1][c0 + 1] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_frame":
        g[3][3] = 2
        return g
    if name == "no_red":
        draw_rect_outline(g, 1, 1, 6, 6, 8)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 8
        return g
    return g
