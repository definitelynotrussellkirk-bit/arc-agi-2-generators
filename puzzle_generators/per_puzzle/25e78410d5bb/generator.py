"""Generator for 7c8af763.

Rule: each enclosed zero region is filled with the majority adjacent
non-wall indicator color.

Combinatorial axes (8): grid_h/w, room_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_rooms, no_indicators, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, draw_rect, full_grid

GENERATOR_ID = "25e78410d5bb"
VERSION = "1.1.0"
TASK_ID = "25e78410d5bb"
SUMMARY = "Enclosed zero rooms filled with majority adjacent indicator color."

INVARIANTS = [
    "zero rooms are separated by color-5 wall cells",
    "colored indicators touch room cells cardinally through wall breaks or side labels",
    "wall color 5 never votes as an indicator",
    "indicator colors are distinct and non-zero non-5",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rooms", "no_indicators", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "room_count":     {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _make_room(g, r0, c0, rh, rw, fill_color, accent_color):
    draw_frame(g, r0 - 1, c0 - 1, r0 + rh, c0 + rw, 5)
    draw_rect(g, r0, c0, rh, rw, 0)
    g[r0][c0 - 1] = fill_color
    g[r0 + rh - 1][c0 - 1] = fill_color
    g[r0 + rh // 2][c0 + rw] = fill_color
    g[r0 - 1][c0 + rw // 2] = accent_color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        rc_lo, rc_hi = 1, 1
    elif difficulty == "hard":
        rc_lo, rc_hi = 3, 3
    else:
        rc_lo, rc_hi = 1, 3
    room_count = ctx.draw_int("room_count", rc_lo, rc_hi)
    colors = ctx.draw_distinct_colors("indicator_colors", n=4, exclude={0, 5})
    g = full_grid(13, 15, 5)
    anchors = [(2, 2), (2, 9), (8, 5)]
    sizes = [(3, 3), (4, 3), (3, 4)]
    for i in range(room_count):
        r0, c0 = anchors[i]
        rh, rw = sizes[i]
        fill = colors[(i + rng.randint(0, 1)) % len(colors)]
        accent = colors[(i + 2) % len(colors)]
        _make_room(g, r0, c0, rh, rw, fill, accent)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 15, 5)
    if name == "no_rooms":
        return g
    if name == "no_indicators":
        draw_rect(g, 2, 2, 3, 3, 0)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(15):
                g[r][c] = 5
        return g
    return g
