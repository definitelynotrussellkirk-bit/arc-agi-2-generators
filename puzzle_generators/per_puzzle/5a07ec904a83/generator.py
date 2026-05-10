"""Generator for puzzle ea786f4a.

Rule: bg = cell(0,0); rule scans for the first 0-cell. Output paints
an X through that 0-cell using bg color, with everything else 0.

Combinatorial axes (8): grid_h/w, bg_color, marker_position,
position_bias, decoy_palette_size, distance_from_corner,
edge_avoidance, anchor_corner.
Degenerates: marker_at_origin, no_marker, all_bg.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5a07ec904a83"
VERSION = "1.1.0"
TASK_ID = "5a07ec904a83"
SUMMARY = "Colored grid with one 0-marker; rule paints X through marker."

INVARIANTS = [
    "cell(0,0) non-zero (the bg)",
    "exactly one 0 cell, not at (0, 0)",
    "all other cells equal bg",
]

POSITION_BIAS = ("center", "corner", "edge", "spread")
DEGENERATE_TEXTURES = ("marker_at_origin", "no_marker", "all_bg")
HELPFUL_TEXTURES = POSITION_BIAS

AXES = {
    "grid_h":           {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "grid_w":           {"type": "int", "default": "rng 5..14", "valid": "3..18"},
    "bg_color":         {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "position_bias":    {"type": "str", "default": "rng helpful",
                         "valid": "|".join(POSITION_BIAS)},
    "marker_row":       {"type": "int", "default": "auto", "valid": "0..h-1"},
    "marker_col":       {"type": "int", "default": "auto", "valid": "0..w-1"},
    "edge_avoidance":   {"type": "bool", "default": "false",
                         "valid": "true|false"},
    "min_distance":     {"type": "int", "default": "1", "valid": "1..h-1"},
    "texture":          {"type": "str", "default": "alias for position_bias",
                         "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 6
    elif difficulty == "hard":
        h_lo, h_hi = 12, 18
    else:
        h_lo, h_hi = 5, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bgc = int(overrides.get("bg_color",
                            ctx.draw_color("bgc", exclude={0})))
    pos_bias = (overrides.get("texture") or overrides.get("position_bias")
                or ctx.draw_choice("position_bias", list(POSITION_BIAS)))
    edge_avoid = bool(overrides.get("edge_avoidance", False))
    min_dist = int(overrides.get("min_distance", 1))
    g = full_grid(h, w, bgc)
    inset = 1 if edge_avoid else 0
    rmin, rmax = inset, h - 1 - inset
    cmin, cmax = inset, w - 1 - inset
    if rmax < rmin: rmin, rmax = 0, h - 1
    if cmax < cmin: cmin, cmax = 0, w - 1
    if pos_bias == "center":
        r, c = h // 2, w // 2
    elif pos_bias == "corner":
        choices = [(0, w - 1), (h - 1, 0), (h - 1, w - 1)]
        r, c = rng.choice(choices)
    elif pos_bias == "edge":
        choices = [(0, rng.randint(1, w - 1)),
                   (h - 1, rng.randint(0, w - 1)),
                   (rng.randint(1, h - 1), 0),
                   (rng.randint(1, h - 1), w - 1)]
        r, c = rng.choice(choices)
    else:
        for _ in range(20):
            r = rng.randint(rmin, rmax); c = rng.randint(cmin, cmax)
            if (r, c) != (0, 0) and (r + c) >= min_dist:
                break
        else:
            r, c = h // 2, w // 2
    if (r, c) == (0, 0):
        r, c = 1, 1 if h > 1 and w > 1 else (0, 1)
    g[r][c] = 0
    return g


def _draw_from_degenerate(name, h, w, rng):
    bgc = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    g = full_grid(h, w, bgc)
    if name == "marker_at_origin":
        g[0][0] = 0
        if h > 1 and w > 1:
            g[h - 1][w - 1] = 0
        return g
    if name == "no_marker":
        return g
    if name == "all_bg":
        return g
    return g
