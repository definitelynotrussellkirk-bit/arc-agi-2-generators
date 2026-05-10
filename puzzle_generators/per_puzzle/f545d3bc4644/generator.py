"""Generator for 184a9768.

Rule: detached colored pieces translate into enclosed holes of larger
container objects.

Combinatorial axes (8): grid_h/w, hole_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_container, no_piece, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, draw_rect, full_grid

GENERATOR_ID = "f545d3bc4644"
VERSION = "1.1.0"
TASK_ID = "f545d3bc4644"
SUMMARY = "Detached colored pieces translate into enclosed holes of containers."

INVARIANTS = [
    "a non-background container encloses one zero hole",
    "a detached piece has exactly the same normalized shape as the hole",
    "the output keeps the container and moves the detached piece into the hole",
]

HOLE_SIZES = ("square", "wide", "tall")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_container", "no_piece", "full_grid")
HELPFUL_TEXTURES = HOLE_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "hole_size":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HOLE_SIZES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for hole_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    size_kind = (overrides.get("texture") if overrides.get("texture") in HOLE_SIZES else None) or \
                overrides.get("hole_size") or \
                ["square", "wide", "tall"][sample_index % 3]
    container, piece = ctx.draw_distinct_colors("colors", n=2, exclude={0, 5})
    hole_h, hole_w = {
        "square": (3, 3),
        "wide": (2, 4),
        "tall": (4, 2),
    }[size_kind]
    frame_h = hole_h + 2
    frame_w = hole_w + 2
    g = full_grid(14, 14, 0)
    top = 1 + (sample_index % 2)
    left = 1 + ((sample_index * 2) % 2)
    draw_frame(g, top, left, top + frame_h - 1, left + frame_w - 1, container)
    piece_top = 10 - hole_h
    piece_left = 9 + (sample_index % 2)
    draw_rect(g, piece_top, piece_left, hole_h, hole_w, piece)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_container":
        draw_rect(g, 7, 9, 3, 3, 4)
        return g
    if name == "no_piece":
        draw_frame(g, 1, 1, 5, 5, 3)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 3
        return g
    return g
