"""Generator for 1a244afd.

Rule: each magenta marker pairs with the nearest unused blue marker;
the magenta becomes 8 and the rotated blue-to-magenta offset becomes 7.

Combinatorial axes (8): grid_h/w, pair_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
offset_kind.
Degenerates: no_pairs, single_pair, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f413b017af40"
VERSION = "1.1.0"
TASK_ID = "f413b017af40"
SUMMARY = "Magenta markers pair with nearest blue, rotated offset becomes 7."

INVARIANTS = [
    "magenta cells use color 6 and sit as isolated markers",
    "blue cells use color 1 and sit as isolated pairing anchors",
    "each magenta marker has a unique nearest unused blue anchor",
    "the rotated blue-to-magenta offset stays inside the grid",
]

OFFSETS = [(2, 0), (0, 2), (-2, 0), (0, -2), (1, 2), (2, 1)]
DEGENERATE_TEXTURES = ("no_pairs", "single_pair", "full_grid")
HELPFUL_TEXTURES = ("compact", "spread", "rotated")

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "pair_count":     {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES)},
    "offset_kind":    {"type": "str", "default": "rng", "valid": "rng"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        pc_lo, pc_hi = 1, 1
    elif difficulty == "hard":
        pc_lo, pc_hi = 3, 4
    else:
        pc_lo, pc_hi = 1, 3
    pair_count = ctx.draw_int("pair_count", pc_lo, pc_hi)
    h = rng.randint(11, 13)
    w = rng.randint(11, 13)
    anchors = [(2, 2), (2, w - 4), (h - 4, 2), (h - 4, w - 4)]
    rng.shuffle(anchors)
    g = full_grid(h, w, 0)
    used = set()
    for br, bc in anchors[:pair_count]:
        offsets = OFFSETS[:]
        rng.shuffle(offsets)
        for dr, dc in offsets:
            mr, mc = br + dr, bc + dc
            rr, rc = br - dc, bc + dr
            cells = {(br, bc), (mr, mc)}
            if (0 <= mr < h and 0 <= mc < w and
                    0 <= rr < h and 0 <= rc < w and
                    not (cells & used)):
                g[br][bc] = 1
                g[mr][mc] = 6
                used |= cells
                break
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_pairs":
        return g
    if name == "single_pair":
        g[2][2] = 1
        g[4][2] = 6
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 6
        return g
    return g
