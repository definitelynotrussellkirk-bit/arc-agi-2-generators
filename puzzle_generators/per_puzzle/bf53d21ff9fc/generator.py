"""Generator for 182e5d0f.

Rule: a gray dot follows an adjacent green path and lands on the
second-to-last path cell.

Combinatorial axes (8): grid_h/w, path_len, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_path, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bf53d21ff9fc"
VERSION = "1.1.0"
TASK_ID = "bf53d21ff9fc"
SUMMARY = "Gray dot follows adjacent green path and lands on second-to-last path cell."

INVARIANTS = [
    "the background is orange",
    "a gray cell is adjacent to the first green path cell",
    "the green path is one-cell-wide and non-branching",
    "the final green cell remains green while the gray marker advances",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_path", "no_marker", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "8..12"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "10..14"},
    "path_len":       {"type": "int", "default": "rng 4..7", "valid": "2..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        path_len = ctx.draw_int("path_len", 3, 4)
    elif difficulty == "hard":
        path_len = ctx.draw_int("path_len", 7, 10)
    else:
        path_len = ctx.draw_int("path_len", 4, 7)
    h = rng.randint(8, 12)
    w = max(10, path_len + 4)
    g = full_grid(h, w, 7)
    r = rng.randint(2, h - 3)
    c0 = 2
    g[r][c0 - 1] = 5
    for i in range(path_len):
        g[r][c0 + i] = 3
    if rng.choice([True, False]):
        g[r + 1][c0 + path_len - 1] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 7)
    if name == "no_path":
        g[5][2] = 5
        return g
    if name == "no_marker":
        for c in range(2, 8):
            g[5][c] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
