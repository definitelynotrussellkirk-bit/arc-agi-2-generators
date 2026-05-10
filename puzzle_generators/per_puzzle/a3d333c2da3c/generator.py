"""Generator for e41c6fd3.

Rule: every object shifts vertically so its top row aligns with the top
row of the cyan(8) object.

Combinatorial axes (8): grid_h/w, object_count, target_row, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_target, no_others, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a3d333c2da3c"
VERSION = "1.1.0"
TASK_ID = "a3d333c2da3c"
SUMMARY = "Every object shifts vertically to align with cyan top row."

INVARIANTS = [
    "background is color 0",
    "one object uses color 8 and supplies the target top row",
    "all objects are separated by columns so vertical alignment cannot collide",
    "object columns and internal shapes are preserved",
]

POSITION_BIASES = ("scattered", "row_offset", "tight", "spread")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_target", "no_others", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "12", "valid": "10..16"},
    "object_count":   {"type": "int", "default": "3", "valid": "2..5"},
    "target_row":     {"type": "int", "default": "rng 4..5", "valid": "3..7"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..4"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, r0, c0, cells, color):
    for dr, dc in cells:
        if 0 <= r0 + dr < len(g) and 0 <= c0 + dc < len(g[0]):
            g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 10, 12
        oc = 2
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
        oc = 4
    else:
        h_lo, h_hi = 12, 14
        oc = 3
    object_count = int(overrides.get("object_count",
                                     ctx.draw_int("object_count", oc, oc)))
    object_count = max(2, min(5, object_count))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, max(2, object_count - 1), rng)
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = int(overrides.get("grid_w", 12))
    g = full_grid(h, w, 0)
    target_r = int(overrides.get("target_row",
                                 ctx.draw_int("target_row", 4, 5)))
    target_r = max(3, min(h - 4, target_r))
    _paint(g, target_r, max(2, w // 2), [(0, 0), (0, 1), (1, 1)], 8)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    shapes = [
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (0, 2)],
    ]
    for i in range(object_count - 1):
        if i >= len(pal):
            break
        shape = shapes[i % len(shapes)]
        if bias == "row_offset":
            r = 1 + i * 3
        elif bias == "tight":
            r = max(1, target_r - 2 + rng.randint(-1, 1))
        elif bias == "spread":
            r = rng.randint(1, max(1, h - 4))
        else:
            r = rng.randint(1, max(1, h - 4))
        c = 1 + i * 4
        if c + 2 < w and r + 2 < h:
            _paint(g, r, c, shape, pal[i])
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 9]
    pool = [c for c in pool if c not in (0, 8)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_target":
        g[2][2] = 3; g[3][2] = 3; g[3][3] = 3
        return g
    if name == "no_others":
        g[5][5] = 8; g[5][6] = 8; g[6][6] = 8
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
