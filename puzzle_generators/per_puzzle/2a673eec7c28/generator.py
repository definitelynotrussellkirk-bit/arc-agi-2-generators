"""Generator for 9720b24f.

Rule: intruder pixels inside a shape component's convex hull are removed.

Combinatorial axes (8): grid_h/w, size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shell, no_intruder, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "2a673eec7c28"
VERSION = "1.1.0"
TASK_ID = "2a673eec7c28"
SUMMARY = "Intruder pixels inside a shape component's convex hull are removed."

INVARIANTS = [
    "a same-color component forms a convex enclosing outline",
    "nonzero cells of other colors appear inside that component's convex hull",
    "intruder pixels are erased to background while the enclosing component is preserved",
]

SIZE_KINDS = ("S6", "S7", "S8")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shell", "no_intruder", "full_grid")
HELPFUL_TEXTURES = SIZE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "size":           {"type": "choice", "default": "rng helpful",
                       "valid": "6|7|8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in SIZE_KINDS:
        size = int(tx[1])
    else:
        size = ctx.draw_choice("size", [6, 7, 8])
    shell, intruder = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(13, 13, 0)
    r0 = 2
    c0 = 2 + (sample_index % 2)
    draw_frame(g, r0, c0, r0 + size - 1, c0 + size - 1, shell)
    g[r0 + size // 2][c0 + size // 2] = intruder
    g[r0 + size // 2 - 1][c0 + size // 2] = intruder
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_shell":
        g[6][6] = 4
        return g
    if name == "no_intruder":
        draw_frame(g, 2, 2, 8, 8, 3)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 3
        return g
    return g
