"""Generator for arc_additional_puzzles_21_set15_bundle:E99.

Rule: 5-cells form walls. Each chamber (connected region of non-5
cells) gets filled with whichever non-{0,5} color appears in it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_marker, conflicting_markers, no_chambers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "01bdf9b8d2db"
VERSION = "1.1.0"
TASK_ID = "01bdf9b8d2db"
SUMMARY = "5-walls form 2-3 chambers; each has 1-2 marker cells of distinct colors."

INVARIANTS = [
    "5-walls form ≥2 distinct chambers",
    "each chamber has exactly 1 distinct non-{0,5} marker color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_marker", "conflicting_markers", "no_chambers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "chamber_center",
                       "valid": "chamber_center"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "1_marker_per", "valid": "1_marker_per"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    h = 4; w = 10
    g = full_grid(h, w, 0)
    # Border walls
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    # 1-2 vertical dividers
    div = rng.choice([4, 5])
    for r in range(h):
        g[r][div] = 5
    # Markers
    pal = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    g[1 + rng.randint(0, 1)][1 + rng.randint(0, div - 2)] = pal[0]
    g[1 + rng.randint(0, 1)][div + 1 + rng.randint(0, w - div - 3)] = pal[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 4, 10
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    div = 5
    for r in range(h):
        g[r][div] = 5
    if name == "missing_marker":
        # one chamber has no marker → its fill color is undefined
        g[1][2] = 3
        # right chamber empty
        return g
    if name == "conflicting_markers":
        # one chamber has two different marker colors → fill is ambiguous
        g[1][1] = 3; g[2][3] = 7
        g[1][6] = 4
        return g
    if name == "no_chambers":
        # remove the divider → no separate chambers, rule has nothing to partition
        for r in range(h):
            g[r][div] = 0
        g[1][2] = 3
        g[2][7] = 4
        return g
    return g
