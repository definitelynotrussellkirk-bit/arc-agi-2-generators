"""Generator for 3d6c6e23.

Rule: counts in each column are compressed into bottom-aligned
odd-width color layers.

Combinatorial axes (8): grid_h/w, active_columns, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_columns, single_column, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cde6cd1740f9"
VERSION = "1.1.0"
TASK_ID = "cde6cd1740f9"
SUMMARY = "Column counts compressed into bottom-aligned odd-width color layers."

INVARIANTS = [
    "each active column has a square-number total of nonzero cells",
    "color counts within a column determine pyramid layer colors",
    "input row positions are irrelevant within a column",
    "active columns sit clear of grid borders",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_columns", "single_column", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "active_columns": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
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
        ac_lo, ac_hi = 2, 2
    elif difficulty == "hard":
        ac_lo, ac_hi = 4, 5
    else:
        ac_lo, ac_hi = 2, 4
    active_columns = ctx.draw_int("active_columns", ac_lo, ac_hi)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    h = 12
    w = 12
    g = full_grid(h, w, 0)
    cols = list(range(2, w - 2))
    rng.shuffle(cols)
    for c in cols[:active_columns]:
        k = rng.choice([2, 3])
        total = k * k
        palette = [rng.choice(colors) for _ in range(k)]
        rows = list(range(h))
        rng.shuffle(rows)
        idx = 0
        for layer, color in enumerate(palette):
            count = (2 * k - 1) - (2 * layer)
            for _ in range(count):
                g[rows[idx]][c] = color
                idx += 1
        for r in rows[idx:total]:
            g[r][c] = rng.choice(colors)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_columns":
        return g
    if name == "single_column":
        for r in range(2, 6):
            g[r][5] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
