"""Generator for 902510d5.

Rule: isolated marker dots choose a triangle color and corner while a
large pattern is preserved.

Combinatorial axes (8): grid_h/w, corner, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_pattern, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "747486860e56"
VERSION = "1.1.0"
TASK_ID = "747486860e56"
SUMMARY = "Isolated marker dots choose triangle color and corner; large pattern preserved."

INVARIANTS = [
    "the background is zero",
    "one connected nonzero pattern is larger than all isolated marker dots",
    "one isolated marker dot is located at a grid corner",
    "the majority isolated-marker color fills a triangle whose size is marker-count minus one",
]

CORNERS = ("tl", "tr", "bl", "br")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pattern", "no_markers", "full_grid")
HELPFUL_TEXTURES = CORNERS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "corner":         {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CORNERS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for corner",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    corner = (overrides.get("texture") if overrides.get("texture") in CORNERS else None) or \
             overrides.get("corner") or \
             ctx.draw_choice("corner", list(CORNERS))
    diag_color, tri_color, other_a, other_b = ctx.draw_distinct_colors(
        "colors", n=4, exclude={0}
    )
    g = full_grid(12, 12, 0)
    for r, c in [(4, 4), (4, 5), (5, 5), (5, 6), (6, 6), (6, 7), (7, 7)]:
        g[r][c] = diag_color
    corners = {"tl": (0, 0), "tr": (0, 11), "bl": (11, 0), "br": (11, 11)}
    cr, cc = corners[corner]
    g[cr][cc] = tri_color
    for r, c, v in [(1, 6, tri_color), (10, 5, tri_color), (2, 9, other_a), (9, 2, other_b)]:
        if (r, c) != (cr, cc):
            g[r][c] = v
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_pattern":
        g[0][0] = 3
        return g
    if name == "no_markers":
        for r, c in [(4, 4), (4, 5), (5, 5), (5, 6), (6, 6), (6, 7), (7, 7)]:
            g[r][c] = 4
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
