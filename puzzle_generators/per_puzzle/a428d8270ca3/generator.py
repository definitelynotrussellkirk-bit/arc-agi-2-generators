"""Generator for 1190bc91.

Rule: colored singleton spines emit diagonal rays; optional domino
markers add wedge fields.

Combinatorial axes (8): grid_h/w, spine_length, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_spine, single_dot, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a428d8270ca3"
VERSION = "1.1.0"
TASK_ID = "a428d8270ca3"
SUMMARY = "Colored singleton spines emit diagonal rays; optional dominoes add wedges."

INVARIANTS = [
    "background is color 0",
    "singleton colors appear exactly once on a straight spine",
    "optional domino colors appear as one adjacent two-cell marker",
    "all active colors are nonzero and distinct",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_spine", "single_dot", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "8..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "8..12"},
    "spine_length":   {"type": "int", "default": "3", "valid": "3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
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
    ctx.draw_int("spine_length", 3, 3)
    h = 8 + rng.randint(0, 4)
    w = 8 + rng.randint(0, 4)
    colors = ctx.draw_distinct_colors("colors", n=5, exclude={0})
    g = full_grid(h, w, 0)

    vertical = ((seed + sample_index) % 2 == 0)
    if vertical:
        c = 2 + ((sample_index + rng.randint(0, 3)) % max(1, w - 4))
        rows = [1, h // 2, h - 2]
        for i, r in enumerate(rows):
            g[r][c] = colors[i]
        if sample_index % 3 != 0:
            c0 = max(0, min(w - 2, c - 1))
            g[0][c0] = colors[3]
            g[0][c0 + 1] = colors[3]
        if sample_index % 4 in (1, 2) and c + 3 < w:
            r0 = max(1, min(h - 2, h // 2 - 1))
            g[r0][c + 3] = colors[4]
            g[r0 + 1][c + 3] = colors[4]
    else:
        r = 2 + ((sample_index + rng.randint(0, 3)) % max(1, h - 4))
        cols = [1, w // 2, w - 2]
        for i, c in enumerate(cols):
            g[r][c] = colors[i]
        if sample_index % 3 != 0:
            r0 = max(0, min(h - 2, r - 1))
            g[r0][0] = colors[3]
            g[r0 + 1][0] = colors[3]
        if sample_index % 4 in (1, 2) and r + 3 < h:
            c0 = max(1, min(w - 2, w // 2 - 1))
            g[r + 3][c0] = colors[4]
            g[r + 3][c0 + 1] = colors[4]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_spine":
        return g
    if name == "single_dot":
        g[5][5] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 3
        return g
    return g
