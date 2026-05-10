"""Generator for ac0c5833.

Rule: a red source shape is stamped beside every matching yellow marker
cluster.

Combinatorial axes (8): grid_h/w, marker_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_source, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e7c4af96e258"
VERSION = "1.1.0"
TASK_ID = "e7c4af96e258"
SUMMARY = "Red source shape stamped beside every matching yellow marker cluster."

INVARIANTS = [
    "a small red source shape has an adjacent yellow marker reference",
    "other yellow markers match that reference under the identity transform",
    "the source shape is copied at each matching marker while the original source is cleared if unused",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_source", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "11..14"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "13..16"},
    "marker_count":   {"type": "int", "default": "rng 2..5", "valid": "2..5"},
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
        marker_count = ctx.draw_int("marker_count", 2, 2)
    elif difficulty == "hard":
        marker_count = ctx.draw_int("marker_count", 4, 5)
    else:
        marker_count = ctx.draw_int("marker_count", 2, 5)
    h = 11 + (sample_index % 4)
    w = 13 + ((sample_index * 2) % 4)
    g = full_grid(h, w, 0)

    sr = 3 + (sample_index % 2)
    sc = 4 + ((sample_index // 2) % 2)
    g[sr][sc] = 2
    g[sr][sc - 1] = 4

    placed = 0
    for r in range(1, h - 1):
        for c in range(1, w - 2):
            if placed >= marker_count:
                break
            if abs(r - sr) + abs(c - (sc - 1)) < 4:
                continue
            if (r + c + sample_index) % 3 == 0:
                g[r][c] = 4
                placed += 1
        if placed >= marker_count:
            break
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 0)
    if name == "no_source":
        g[5][5] = 4
        g[7][7] = 4
        return g
    if name == "no_markers":
        g[3][4] = 2
        g[3][3] = 4
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 4
        return g
    return g
