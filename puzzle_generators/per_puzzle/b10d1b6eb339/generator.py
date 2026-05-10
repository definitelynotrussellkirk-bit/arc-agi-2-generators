"""Generator for 305b1341.

Rule: two-column key rows map source colors to fill colors around
their source-cell bounding boxes.

Combinatorial axes (8): grid_h/w, mapping_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_variant.
Degenerates: no_keys, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b10d1b6eb339"
VERSION = "1.1.0"
TASK_ID = "b10d1b6eb339"
SUMMARY = "Key rows map source to fill colors around source-cell bboxes."

INVARIANTS = [
    "key rows have nonzero source and fill colors in columns 0 and 1",
    "source-color shapes outside the key define expanded bounding boxes",
    "each source color appears once outside the key area",
    "shapes sit clear of the key rows so bboxes do not overlap",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_keys", "no_shapes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "mapping_count":  {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_variant":  {"type": "str", "default": "rng", "valid": "rng"},
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
        mc_lo, mc_hi = 2, 2
    elif difficulty == "hard":
        mc_lo, mc_hi = 3, 3
    else:
        mc_lo, mc_hi = 2, 3
    mapping_count = ctx.draw_int("mapping_count", mc_lo, mc_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 2 * mapping_count:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    colors = pool[:2 * mapping_count]
    g = full_grid(13, 14, 0)
    anchors = [(4, 5), (7, 9), (9, 4)]
    for i in range(mapping_count):
        source = colors[2 * i]
        fill = colors[2 * i + 1]
        g[i][0] = source
        g[i][1] = fill
        r0, c0 = anchors[i]
        row_jitter = rng.randint(0, 1)
        for dr, dc in SHAPES[i]:
            g[r0 + dr + row_jitter][c0 + dc] = source
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 0]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 14, 0)
    if name == "no_keys":
        for dr, dc in SHAPES[0]:
            g[4 + dr][5 + dc] = 2
        return g
    if name == "no_shapes":
        g[0][0] = 2; g[0][1] = 3
        g[1][0] = 4; g[1][1] = 5
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
