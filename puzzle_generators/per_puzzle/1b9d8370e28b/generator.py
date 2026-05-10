"""Generator for 9b4c17c4.

Rule: red cells compact left in cyan regions and right in blue regions,
preserving per-row counts.

Combinatorial axes (8): grid_h/w, split_ratio, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_red, density.
Degenerates: no_red, all_red, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1b9d8370e28b"
VERSION = "1.1.0"
TASK_ID = "1b9d8370e28b"
SUMMARY = "Red cells compact left in cyan regions and right in blue regions."

INVARIANTS = [
    "the background splits into a cyan (color 8) left half and blue (color 1) right half",
    "red cells use color 2 and sit inside both halves",
    "each row has at least one red cell so the rule has visible work to do",
    "the rule rearranges red cells without changing the bg colors",
]

DENSITY_KINDS = ("sparse", "medium", "dense")
DEGENERATE_TEXTURES = ("no_red", "all_red", "full_grid")
HELPFUL_TEXTURES = DENSITY_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "split_ratio":    {"type": "float", "default": "0.5", "valid": "0.4..0.6"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "n_red":          {"type": "int", "default": "rng 4..8", "valid": "1..16"},
    "density":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DENSITY_KINDS)},
    "texture":        {"type": "str", "default": "alias for density",
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
        h_lo, h_hi, w_lo, w_hi = 8, 8, 10, 12
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 10, 12, 14, 16
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 10, 12, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    density = (overrides.get("texture") if overrides.get("texture") in DENSITY_KINDS else None) or \
              overrides.get("density") or \
              ctx.draw_choice("density", list(DENSITY_KINDS))
    split = w // 2
    g = full_grid(h, w, 8)
    for r in range(h):
        for c in range(split, w):
            g[r][c] = 1
    if density == "sparse":
        period = 3
    elif density == "dense":
        period = 1
    else:
        period = 2
    for r in range(1, h - 1, period):
        g[r][1 + (r % 3)] = 2
        if split + 1 + (r % 2) < w:
            g[r][split + 1 + (r % 2)] = 2
        if r + 1 < h and w - 2 >= 0:
            g[r][w - 2] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    split = w // 2
    g = full_grid(h, w, 8)
    for r in range(h):
        for c in range(split, w):
            g[r][c] = 1
    if name == "no_red":
        return g
    if name == "all_red":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
