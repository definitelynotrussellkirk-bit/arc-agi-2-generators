"""Generator for 358ba94e.

Rule: among same-color objects, the one with unique bbox hole count is
cropped out.

Combinatorial axes (8): grid_h/w, color, ring_position, palette_kind,
n_solid, anchor_corner, asymmetry_force, palette_size.
Degenerates: all_same, no_ring, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, draw_rect_outline, full_grid

GENERATOR_ID = "07ae7be573fc"
VERSION = "1.1.0"
TASK_ID = "07ae7be573fc"
SUMMARY = "Same-color objects with one unique-hole-count; rule crops the unique one."

INVARIANTS = [
    "all nonzero cells use the same color",
    "at least two objects share one hole count",
    "one object has a unique hole count in its bounding box",
    "the output is the crop of that unique-hole-count object",
]

POSITION_BIASES = ("scattered", "centered", "row_aligned", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("all_same", "no_ring", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "14", "valid": "10..18"},
    "color":          {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "ring_position":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_solid":        {"type": "int", "default": "2", "valid": "2..4"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for ring_position",
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
        h, w = 10, 12
    elif difficulty == "hard":
        h, w = 16, 18
    else:
        h, w = 12, 14
    h = int(overrides.get("grid_h", h))
    w = int(overrides.get("grid_w", w))
    color = int(overrides.get("color",
                              ctx.draw_color("color", exclude={0})))
    g = full_grid(h, w, 0)
    draw_rect(g, 1, 1, 2, 2, color)
    draw_rect(g, 1, 6 + rng.randint(0, 1), 2, 2, color)
    bias = (overrides.get("texture") or
            overrides.get("ring_position")
            or ctx.draw_choice("ring_position", list(POSITION_BIASES)))
    if bias == "centered":
        ring_r = h // 2
        ring_c = w // 2 - 1
    elif bias == "row_aligned":
        ring_r = 6
        ring_c = rng.randint(2, max(2, w - 5))
    else:
        ring_r = rng.randint(min(h - 4, 6), h - 4)
        ring_c = rng.randint(2, max(2, w - 5))
    if ring_r + 3 < h and ring_c + 3 < w:
        draw_rect_outline(g, ring_r, ring_c, 3, 3, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "all_same":
        draw_rect(g, 1, 1, 2, 2, 3)
        draw_rect(g, 1, 6, 2, 2, 3)
        draw_rect(g, 6, 4, 2, 2, 3)
        return g
    if name == "no_ring":
        draw_rect(g, 1, 1, 2, 2, 3)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
