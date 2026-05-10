"""Generator for arc_additional_puzzles_21_set22_bundle:M148: crop largest component.

Rule: among disconnected nonzero components, the unique largest is
cropped out.

Combinatorial axes (8): grid_h, grid_w, palette_kind, large_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_largest, single_component, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.blobs import grow_blob
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "82babb933dc3"
VERSION = "1.1.0"
TASK_ID = "82babb933dc3"
SUMMARY = "Several disconnected nonzero components; the unique largest component is cropped out."
INVARIANTS = [
    "nonzero components are separated by background",
    "one component has strictly largest area",
    "component colors are preserved inside the eventual crop",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_largest", "single_component", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "large_size":     {"type": "int", "default": "rng 7..11", "valid": "4..20"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "spread_distinct_sizes",
                       "valid": "spread_distinct_sizes"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        large_size = ctx.draw_int("large_size", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
        large_size = ctx.draw_int("large_size", 9, 11)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 10, 15)
        large_size = ctx.draw_int("large_size", 7, 11)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    used = set()
    sizes = [large_size, max(2, large_size // 2), max(1, large_size // 2 - 1)]
    colors = [4, 5, 6, 7, 8, 9]
    for i, size in enumerate(sizes):
        cells = grow_blob(rng, h, w, used, size)
        if cells is None:
            continue
        used |= cells
        for j, (r, c) in enumerate(sorted(cells)):
            g[r][c] = colors[(i + j) % len(colors)] if i == 0 else colors[i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "tied_largest":
        # two equal-size large components → "largest" ambiguous
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3)]: g[r][c] = 4
        for (r, c) in [(7, 7), (7, 8), (8, 7), (8, 8), (7, 9)]: g[r][c] = 6
        return g
    if name == "single_component":
        # one component → trivially largest, crop is just that component's bbox
        for (r, c) in [(3, 3), (3, 4), (4, 3), (4, 4), (5, 4)]: g[r][c] = 4
        return g
    if name == "no_components":
        # blank grid → no components to crop
        return g
    return g
