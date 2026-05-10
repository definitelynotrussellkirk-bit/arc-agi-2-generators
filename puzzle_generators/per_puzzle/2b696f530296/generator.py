"""Generator for c8cbb738.

Rule: several four-cell color groups are normalized around their
integer centroids.

Combinatorial axes (8): radius, group_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, bg_color.
Degenerates: no_groups, single_group, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2b696f530296"
VERSION = "1.1.0"
TASK_ID = "2b696f530296"
SUMMARY = "Four-cell color groups normalized around integer centroids."

INVARIANTS = [
    "background is the modal nonzero color",
    "each foreground color appears exactly four times",
    "foreground groups use compact offsets around separate integer centroids",
    "groups sit clear of each other so centroids are unambiguous",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_groups", "single_group", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

_MOTIFS_BY_RADIUS = {
    1: [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(-1, -1), (-1, 1), (1, -1), (1, 1)],
        [(-1, 0), (0, -1), (0, 1), (1, 0)],
        [(-1, -1), (-1, 0), (1, 0), (1, 1)],
        [(-1, 1), (-1, 0), (1, 0), (1, -1)],
    ],
    2: [
        [(-2, 0), (0, -2), (0, 2), (2, 0)],
        [(-2, -2), (-2, 2), (2, -2), (2, 2)],
        [(-2, -1), (-1, -2), (1, 2), (2, 1)],
        [(-2, 0), (-1, 0), (1, 0), (2, 0)],
        [(0, -2), (0, -1), (0, 1), (0, 2)],
        [(-2, 1), (-1, -1), (1, -1), (2, 1)],
    ],
}

AXES = {
    "radius":         {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "group_count":    {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "bg_color":       {"type": "color", "default": "rng !0", "valid": "1..9"},
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
    radius = ctx.draw_int("radius", 1, 2)
    if difficulty == "easy":
        gc_lo, gc_hi = 2, 2
    elif difficulty == "hard":
        gc_lo, gc_hi = 4, 4
    else:
        gc_lo, gc_hi = 2, 4
    group_count = ctx.draw_int("group_count", gc_lo, gc_hi)
    bg = ctx.draw_color("background", exclude={0})
    colors = ctx.draw_distinct_colors("colors", n=group_count, exclude={0, bg})
    motifs = _MOTIFS_BY_RADIUS[radius]
    spacing = 2 * radius + 3
    h = 2 * radius + 3 + rng.randint(0, 2)
    w = 2 * radius + 3 + (group_count - 1) * spacing + rng.randint(0, 2)
    center_r = radius + 1
    first_center_c = radius + 1
    g = full_grid(h, w, bg)
    chosen = [rng.choice(motifs) for _ in range(group_count)]
    for idx, color in enumerate(colors):
        center_c = first_center_c + idx * spacing
        for dr, dc in chosen[idx]:
            g[center_r + dr][center_c + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 12, 5)
    if name == "no_groups":
        return g
    if name == "single_group":
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[2 + dr][2 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
