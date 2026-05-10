"""Generator for 13b:m85 — scale keyed object 2x.

Rule: a single-cell marker names a color C. The multi-cell shape of
color C gets cropped and upscaled 2x. Output is that.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, marker_color_missing, multiple_keyed_shapes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a70a4fc336b9"
VERSION = "1.1.0"
TASK_ID = "a70a4fc336b9"
SUMMARY = "1 single-cell marker (color C) + 2-3 multi-cell shapes, one matching C."

INVARIANTS = [
    "background is 0",
    "exactly one isolated single-cell marker",
    "2-3 multi-cell shapes, distinct colors; one matches marker color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "marker_color_missing", "multiple_keyed_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "marker_with_shapes",
                       "valid": "marker_with_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_shapes = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
        n_shapes = 3
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 11, 14)
        n_shapes = None
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    if n_shapes is None:
        n_shapes = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_shapes)
    keyed_color = palette[0]
    g[0][0] = keyed_color
    for color in palette:
        _place(g, rng, rng.choice(_SHAPES), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # no marker at corner → rule has no key color, undefined behavior
        _place(g, type("R", (), {"randint": lambda *a: 3, "choice": lambda x, y=None: y or x})(), _SHAPES[0], 4)
        for (dr, dc) in _SHAPES[0]: g[3 + dr][3 + dc] = 4
        for (dr, dc) in _SHAPES[1]: g[7 + dr][7 + dc] = 6
        return g
    if name == "marker_color_missing":
        # marker present but no shape of that color → rule has nothing to scale
        g[0][0] = 4   # key=4
        for (dr, dc) in _SHAPES[0]: g[3 + dr][3 + dc] = 6   # only 6-shape
        for (dr, dc) in _SHAPES[1]: g[7 + dr][7 + dc] = 8
        return g
    if name == "multiple_keyed_shapes":
        # multiple shapes share the keyed color → which one to scale?
        g[0][0] = 4   # key=4
        for (dr, dc) in _SHAPES[0]: g[3 + dr][3 + dc] = 4
        for (dr, dc) in _SHAPES[1]: g[7 + dr][7 + dc] = 4   # also 4
        return g
    return g
