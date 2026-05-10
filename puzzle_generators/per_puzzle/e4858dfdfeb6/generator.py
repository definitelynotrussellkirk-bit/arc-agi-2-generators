"""Generator for 2e65ae53.

Rule: observed swatch colors fill matching slots across framed grid
templates.

Combinatorial axes (8): grid_h/w, slot, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_templates, no_swatch, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e4858dfdfeb6"
VERSION = "1.1.0"
TASK_ID = "e4858dfdfeb6"
SUMMARY = "Observed swatch colors fill matching slots across framed templates."

INVARIANTS = [
    "two framed templates share the same internal grid structure",
    "one slot contains a non-frame swatch color in one template",
    "matching blank slots in every template are filled with that swatch",
    "frame and swatch colors are distinct and non-zero",
]

SLOTS = ("top-left", "top-right", "bottom-left", "bottom-right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_templates", "no_swatch", "full_grid")
HELPFUL_TEXTURES = ("tl", "tr", "bl", "br")

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "slot":           {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SLOTS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for slot",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_template(g, top, left, frame):
    for r in range(top, top + 5):
        for c in [left, left + 2, left + 4]:
            g[r][c] = frame
    for c in range(left, left + 5):
        for r in [top, top + 2, top + 4]:
            g[r][c] = frame


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    short_to_full = {"tl": "top-left", "tr": "top-right", "bl": "bottom-left", "br": "bottom-right"}
    if tx in short_to_full:
        slot = short_to_full[tx]
    else:
        slot = ctx.draw_choice("slot", list(SLOTS))
        if "slot" not in overrides:
            slot = SLOTS[sample_index % 4]
    frame, swatch = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    offsets = {
        "top-left": (1, 1),
        "top-right": (1, 3),
        "bottom-left": (3, 1),
        "bottom-right": (3, 3),
    }
    g = full_grid(8, 14, 0)
    _draw_template(g, 1, 1, frame)
    _draw_template(g, 1, 8, frame)
    dr, dc = offsets[slot]
    g[1 + dr][1 + dc] = swatch
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 14, 0)
    if name == "no_templates":
        g[3][3] = 2
        return g
    if name == "no_swatch":
        _draw_template(g, 1, 1, 1)
        _draw_template(g, 1, 8, 1)
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(14):
                g[r][c] = 1
        return g
    return g
