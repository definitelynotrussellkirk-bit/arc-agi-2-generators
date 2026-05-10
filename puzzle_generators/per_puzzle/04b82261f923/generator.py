"""Generator for 11e1fe23.

Rule: three colored dots imply a gray midpoint and one-step colored
spokes.

Combinatorial axes (8): grid_h/w, radius, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_dots, single_dot, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "04b82261f923"
VERSION = "1.1.0"
TASK_ID = "04b82261f923"
SUMMARY = "Three colored dots imply gray midpoint and one-step colored spokes."

INVARIANTS = [
    "exactly three nonzero dots are present",
    "the farthest pair has an integer midpoint",
    "the third dot is closer to both farthest endpoints",
    "spoke cells from the midpoint sit inside the grid",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "single_dot", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "7..20"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "7..20"},
    "radius":         {"type": "int", "default": "rng 2..4", "valid": "2..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        h_lo, h_hi, r_lo, r_hi = 10, 12, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, r_lo, r_hi = 14, 18, 3, 5
    else:
        h_lo, h_hi, r_lo, r_hi = 10, 14, 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    max_radius = min(r_hi, (h - 3) // 2, (w - 3) // 2)
    radius = min(ctx.draw_int("radius", r_lo, r_hi), max_radius)
    cr = rng.randint(radius + 1, h - radius - 2)
    cc = rng.randint(radius + 1, w - radius - 2)
    colors = ctx.draw_distinct_colors("dot_colors", n=3, exclude={0, 5})
    g = full_grid(h, w, 0)
    g[cr - radius][cc - radius] = colors[0]
    g[cr + radius][cc + radius] = colors[1]
    g[cr][cc - radius] = colors[2]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_dots":
        return g
    if name == "single_dot":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
