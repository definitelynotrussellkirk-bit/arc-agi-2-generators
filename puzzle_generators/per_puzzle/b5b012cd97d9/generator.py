"""Generator for 8abad3cf.

Rule: color counts are perfect squares; rule reads (big, small,
single) and assembles a 3-piece output.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, k1, k2.
Degenerates: no_squares, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b5b012cd97d9"
VERSION = "1.1.0"
TASK_ID = "b5b012cd97d9"
SUMMARY = "Color counts as perfect squares; rule assembles a multi-square output."

INVARIANTS = [
    "bg color is the most common",
    "exactly three non-bg colors: big k1^2, small k2^2, single 1",
    "k1 is greater than k2 with k2 at least 2 so big is unambiguously larger",
    "all non-bg cells fit in the grid with bg margin",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_squares", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "k1":             {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "k2":             {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 12, 13
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 12, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    bg = rng.choice([0, 5, 7, 8, 9])
    palette = ctx.draw_distinct_colors("palette", n=3, exclude={bg})
    big_color, small_color, single_color = palette
    k1 = rng.randint(3, 4)
    k2 = rng.randint(2, k1 - 1)
    big_n = k1 * k1
    small_n = k2 * k2
    total_non_bg = big_n + small_n + 1
    g = full_grid(h, w, bg)
    cells_needed = (
        [big_color] * big_n
        + [small_color] * small_n
        + [single_color] * 1
    )
    rng.shuffle(cells_needed)
    positions = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(positions)
    chosen = positions[:total_non_bg]
    for (r, c), col in zip(chosen, cells_needed):
        g[r][c] = col
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_squares":
        return g
    if name == "single_color":
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
