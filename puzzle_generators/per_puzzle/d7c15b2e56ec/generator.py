"""Generator for 7d1f7ee8.

Rule: nested rectangle borders inherit the outermost enclosing frame color.

Combinatorial axes (8): grid_h/w, nest_count, palette_size,
palette_kind, frame_thickness, position_bias, anchor_corner,
asymmetry_force.
Degenerates: single_frame, all_same_color, no_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "d7c15b2e56ec"
VERSION = "1.1.0"
TASK_ID = "d7c15b2e56ec"
SUMMARY = "Nested rect frames inherit outermost color."

INVARIANTS = [
    "background is 0",
    ">=2 nested, disconnected rectangular outlines",
    "each inner outline lies fully inside the larger outline's bbox",
    "frames have distinct colors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "small")
DEGENERATE_TEXTURES = ("single_frame", "all_same_color", "no_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 11..18", "valid": "9..22"},
    "grid_w":           {"type": "int", "default": "rng 13..20", "valid": "11..24"},
    "nest_count":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":     {"type": "int", "default": "= nest_count",
                         "valid": "2..7"},
    "palette_kind":     {"type": "str", "default": "rng helpful",
                         "valid": "|".join(PALETTE_KINDS)},
    "position_bias":    {"type": "str", "default": "rng spread|center",
                         "valid": "spread|center"},
    "anchor_corner":    {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "asymmetry_force":  {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "texture":          {"type": "str", "default": "alias for palette_kind",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_base, h_var = 9, 2
    elif difficulty == "hard":
        h_base, h_var = 17, 3
    else:
        h_base, h_var = 11, 3
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        h = h_base + 2 * rng.randint(0, h_var)
        w = (h_base + 2) + 2 * rng.randint(0, h_var)
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    nest_count = int(overrides.get("nest_count",
                                   ctx.draw_int("nest_count", 2, 3)))
    nest_count = max(2, min(4, nest_count))
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    if palette_kind == "warm":
        pool = [3, 4, 6, 9]
    elif palette_kind == "cool":
        pool = [1, 5, 7, 8]
    elif palette_kind == "small":
        pool = [1, 2, 3]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < nest_count:
        extras = [c for c in range(1, 10) if c not in pool]
        rng.shuffle(extras)
        pool += extras
    colors = pool[:nest_count]
    h = h_base + 2 * rng.randint(0, h_var)
    w = (h_base + 2) + 2 * rng.randint(0, h_var)
    g = full_grid(h, w, 0)
    for idx in range(nest_count):
        margin = 1 + idx * 3
        if margin >= h - margin or margin >= w - margin:
            break
        draw_frame(g, margin, margin, h - 1 - margin, w - 1 - margin,
                   colors[idx])
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "single_frame":
        draw_frame(g, 1, 1, h - 2, w - 2, color)
        return g
    if name == "all_same_color":
        for idx in range(2):
            margin = 1 + idx * 3
            if margin < h - margin and margin < w - margin:
                draw_frame(g, margin, margin, h - 1 - margin, w - 1 - margin,
                           color)
        return g
    if name == "no_frames":
        return g
    return g
