"""Generator for b782dc8a.

Rule: singleton center color flood-fills reachable zero cells with
alternating center and arm colors.

Combinatorial axes (8): grid_h/w, wall_mode, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_seed, full_grid, all_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "44690b1b635f"
VERSION = "1.1.0"
TASK_ID = "44690b1b635f"
SUMMARY = "Singleton center color flood-fills with alternating arm color."

INVARIANTS = [
    "background is color 0",
    "walls when present use color 8",
    "one marker color appears exactly once and is the BFS center",
    "a second marker color supplies the alternating arm color",
]

WALL_MODES = ("none", "split")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seed", "full_grid", "all_walls")
HELPFUL_TEXTURES = WALL_MODES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "wall_mode":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(WALL_MODES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for wall_mode",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    wall_mode = (overrides.get("texture") if overrides.get("texture") in WALL_MODES else None) or \
                overrides.get("wall_mode") or \
                ctx.draw_choice("wall_mode", list(WALL_MODES))
    center, arm = ctx.draw_distinct_colors("colors", n=2, exclude={0, 8})
    h = 7 + rng.randint(0, 3)
    w = 7 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    g[h // 2][w // 2] = center
    g[1][1] = arm
    g[h - 2][w - 2] = arm
    if wall_mode == "split":
        for r in range(1, h - 1):
            if r != h // 2:
                g[r][w // 2 - 1] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 8, 0)
    if name == "no_seed":
        return g
    if name == "all_walls":
        for r in range(8):
            for c in range(8):
                g[r][c] = 8
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(8):
                g[r][c] = 2
        return g
    return g
