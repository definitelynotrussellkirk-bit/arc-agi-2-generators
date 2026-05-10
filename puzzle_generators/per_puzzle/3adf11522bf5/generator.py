"""Generator for 31adaf00.

Rule: maximal all-zero square regions filled with color 1; obstacles
preserved.

Combinatorial axes (8): grid_size, n_obstacles, palette_kind, obstacle_color,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_obstacles, no_clean, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3adf11522bf5"
VERSION = "1.1.0"
TASK_ID = "3adf11522bf5"
SUMMARY = "Maximal all-zero squares filled with color 1; obstacles preserved."

INVARIANTS = [
    "the grid contains black zero regions interrupted by nonzero obstacles",
    "at least one all-zero square of side two or larger exists",
    "color 1 marks cells belonging to maximal zero squares selected by the rule",
    "nonzero obstacle cells remain unchanged",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_obstacles", "no_clean", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 8..13", "valid": "4..30"},
    "n_obstacles":    {"type": "int", "default": "rng 8..18", "valid": "1..30"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "obstacle_color": {"type": "color", "default": "rng !{0,1}",
                       "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
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
    h, w = ctx.draw_grid_size("grid_size", lo=(8, 8), hi=(13, 14))
    obstacle = ctx.draw_color("obstacle", exclude={0, 1})
    g = full_grid(h, w, 0)
    n_obs = int(overrides.get("n_obstacles",
                              rng.randint(8, 18)))
    n_obs = max(1, min(30, n_obs))
    for _ in range(n_obs):
        r = rng.randrange(h)
        c = rng.randrange(w)
        if not (1 <= r <= min(4, h - 2) and 1 <= c <= min(4, w - 2)):
            g[r][c] = obstacle
    for r in range(1, min(5, h)):
        for c in range(1, min(5, w)):
            g[r][c] = 0
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_obstacles":
        return g
    if name == "no_clean":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
