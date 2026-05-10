"""Generator for 3979b1a8.

Rule: 5×5 with 3 colors at (0,0), (0,1), (2,2). Output is fixed 10×10
pattern of indices {0,1,2} mapped through those 3 colors.

Combinatorial axes (8): grid_size, palette_kind, palette_size,
position_layout, anchor_corner, asymmetry_force, color_distribution,
fill_density.
Degenerates: monochrome, two_colors, four_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7d1e8744229a"
VERSION = "1.1.0"
TASK_ID = "7d1e8744229a"
SUMMARY = "5×5 with 3 colors at fixed positions; rule expands via 10×10 lookup."

INVARIANTS = [
    "h = w = 5",
    "exactly 3 distinct colors used",
    "(0,0), (0,1), (2,2) hold those 3 colors in distinct values",
]

PALETTE_KINDS = ("warm", "cool", "broad", "small")
COLOR_DISTRIBUTIONS = ("balanced", "skewed", "diag")
DEGENERATE_TEXTURES = ("monochrome", "two_colors", "four_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":          {"type": "int", "default": "5", "valid": "5"},
    "palette_kind":       {"type": "str", "default": "rng helpful",
                           "valid": "|".join(PALETTE_KINDS)},
    "palette_size":       {"type": "int", "default": "3", "valid": "3"},
    "color_distribution": {"type": "str", "default": "rng helpful",
                           "valid": "|".join(COLOR_DISTRIBUTIONS)},
    "fill_density":       {"type": "float", "default": "rng 0.4..0.7",
                           "valid": "0.2..1"},
    "anchor_corner":      {"type": "bool", "default": "true",
                           "valid": "true|false"},
    "asymmetry_force":    {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "include_decoy":      {"type": "bool", "default": "false",
                           "valid": "true|false"},
    "texture":            {"type": "str", "default": "alias for palette_kind",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
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
    palette = pool[:3]
    while len(palette) < 3:
        palette.append(palette[0])
    a, b, c = palette
    color_dist = overrides.get("color_distribution",
                               ctx.draw_choice("color_distribution",
                                               list(COLOR_DISTRIBUTIONS)))
    density = float(overrides.get("fill_density",
                                  ctx.draw_rng("fill_density")
                                  .uniform(0.4, 0.7)))
    g = full_grid(5, 5, 0)
    for r in range(5):
        for cc in range(5):
            if color_dist == "skewed":
                weights = [3, 2, 1]
            elif color_dist == "diag":
                weights = [3, 1, 1] if (r + cc) % 2 == 0 else [1, 3, 1]
            else:
                weights = [1, 1, 1]
            choices = [a] * weights[0] + [b] * weights[1] + [c] * weights[2]
            g[r][cc] = rng.choice(choices)
    g[0][0] = a
    g[0][1] = b
    g[2][2] = c
    return g


def _draw_from_degenerate(name, rng):
    palette = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(palette)
    g = full_grid(5, 5, 0)
    if name == "monochrome":
        c = palette[0]
        for r in range(5):
            for cc in range(5):
                g[r][cc] = c
        return g
    if name == "two_colors":
        a, b = palette[0], palette[1]
        for r in range(5):
            for cc in range(5):
                g[r][cc] = a if (r + cc) % 2 == 0 else b
        return g
    if name == "four_colors":
        for r in range(5):
            for cc in range(5):
                g[r][cc] = palette[(r + cc) % 4]
        return g
    return g
