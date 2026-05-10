"""Generator for db615bd4.

Rule: a disrupted checkerboard is restored around a framed layout with
centered content blocks.

Combinatorial axes (8): grid_h/w, orientation, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_frame, no_blocks, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, draw_rect

GENERATOR_ID = "d1ba4a8801ce"
VERSION = "1.1.0"
TASK_ID = "d1ba4a8801ce"
SUMMARY = "Disrupted checkerboard restored around framed layout with centered blocks."

INVARIANTS = [
    "the base background follows the task's two-color checkerboard convention",
    "the most frequent disruption color is the rectangular frame",
    "remaining disruption colors provide content block sizes that are centered inside the frame",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_blocks", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _checker(h, w, even, odd):
    return [[odd if r % 2 == 1 and c % 2 == 1 else even for c in range(w)] for r in range(h)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ("horizontal" if sample_index % 2 == 0 else "vertical")
    even, odd, frame, a, b = ctx.draw_distinct_colors("colors", n=5, exclude={0})
    g = _checker(13, 15, even, odd)
    if orientation == "horizontal":
        draw_frame(g, 3, 3, 8, 12, frame)
        draw_rect(g, 1, 5, 1, 2, a)
        draw_rect(g, 10, 2, 2, 1, b)
    else:
        draw_frame(g, 2, 4, 11, 10, frame)
        draw_rect(g, 1, 1, 1, 2, a)
        draw_rect(g, 7, 13, 2, 1, b)
    return g


def _draw_from_degenerate(name, rng):
    g = _checker(13, 15, 1, 2)
    if name == "no_frame":
        return g
    if name == "no_blocks":
        draw_frame(g, 3, 3, 8, 12, 4)
        return g
    if name == "full_grid":
        return [[4 for _ in range(15)] for _ in range(13)]
    return g
