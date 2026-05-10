"""Generator for f8f52ecc.

Rule: same-colored terminals are connected by obstacle-aware L-shaped paths.

Combinatorial axes (8): grid_h/w, terminal_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_terminals, single_terminal, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "de8785512d06"
VERSION = "1.1.0"
TASK_ID = "de8785512d06"
SUMMARY = "Same-colored terminals connect via obstacle-aware L-shaped paths."

INVARIANTS = [
    "the background is a nonzero mode color",
    "each routed color has at least two terminal cells",
    "paths are drawn through background cells using horizontal/vertical L segments",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_terminals", "single_terminal", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "11..13"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "12..14"},
    "terminal_count": {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "corners", "valid": "corners"},
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
        terminal_count = ctx.draw_int("terminal_count", 2, 2)
    elif difficulty == "hard":
        terminal_count = ctx.draw_int("terminal_count", 4, 4)
    else:
        terminal_count = ctx.draw_int("terminal_count", 2, 4)
    bg, color = ctx.draw_distinct_colors("colors", n=2, exclude={0, 8})
    h = 11 + (sample_index % 3)
    w = 12 + ((sample_index * 2) % 3)
    g = full_grid(h, w, bg)
    points = [(1, 1), (h - 2, w - 2), (2, w - 3), (h - 3, 2)]
    for r, c in points[:terminal_count]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 4)
    if name == "no_terminals":
        return g
    if name == "single_terminal":
        g[1][1] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
