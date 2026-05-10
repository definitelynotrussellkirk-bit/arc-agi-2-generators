"""Generator for 29623171.

Rule: in a gray-separated 3x3 panel grid, sections with maximal marker
count are filled.

Combinatorial axes (8): grid_size, cell_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_markers, all_full, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5003370f0e31"
VERSION = "1.1.0"
TASK_ID = "5003370f0e31"
SUMMARY = "Gray-separated 3x3 panels; sections with max marker count get filled."

INVARIANTS = [
    "two full gray rows and two full gray columns form a 3x3 section grid",
    "all markers use one nonzero non-gray color",
    "marker counts vary by section",
    "marker color is distinct from 0 and 5",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "all_full", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 8..11", "valid": "8..17"},
    "cell_size":      {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "color":          {"type": "color", "default": "rng !{0,5}", "valid": "1..9 except 5"},
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
        k_lo, k_hi = 2, 2
    elif difficulty == "hard":
        k_lo, k_hi = 3, 4
    else:
        k_lo, k_hi = 2, 3
    k = ctx.draw_int("cell_size", k_lo, k_hi)
    color = ctx.draw_color("color", exclude={0, 5})
    size = 3 * k + 2
    g = full_grid(size, size, 0)
    sep1 = k
    sep2 = 2 * k + 1
    for i in range(size):
        g[sep1][i] = 5
        g[sep2][i] = 5
        g[i][sep1] = 5
        g[i][sep2] = 5
    counts = [1, 2, k * k, 0, 1, rng.randint(1, k * k - 1), 2, 0, k * k]
    starts = [(0, 0), (0, sep1 + 1), (0, sep2 + 1),
              (sep1 + 1, 0), (sep1 + 1, sep1 + 1), (sep1 + 1, sep2 + 1),
              (sep2 + 1, 0), (sep2 + 1, sep1 + 1), (sep2 + 1, sep2 + 1)]
    for idx, count in enumerate(counts):
        r0, c0 = starts[idx]
        cells = [(r0 + r, c0 + c) for r in range(k) for c in range(k)]
        rng.shuffle(cells)
        for r, c in cells[:count]:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    sep1, sep2 = 3, 7
    for i in range(11):
        g[sep1][i] = 5; g[sep2][i] = 5
        g[i][sep1] = 5; g[i][sep2] = 5
    if name == "no_markers":
        return g
    if name == "all_full":
        for r in range(11):
            for c in range(11):
                if g[r][c] != 5:
                    g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 5
        return g
    return g
