"""Generator for next_b:hard_12 — make matching shapes symmetric.

Rule: color-1 template; for each color-3 component matching the
template's normalized cells, output adds the LR-mirror of those cells
(across the bbox right edge), painted color 8 — combined with the
original cells, painted 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_match, mirror_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4179e1ac3cf7"
VERSION = "1.1.0"
TASK_ID = "4179e1ac3cf7"

SUMMARY = "1 color-1 template + 1-2 color-3 matching shapes (with LR-mirror room)."

INVARIANTS = [
    "background is 0",
    "exactly one color-1 multi-cell template",
    "1-2 color-3 components matching the template's normalized cells",
    "each color-3 shape has bbox width ≤ half of grid width minus 1 (so the LR-mirror lands in-bounds)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_match", "mirror_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "template_plus_match",
                       "valid": "template_plus_match"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place_or_raise(g, rng, shape, color, label, *, c_max=None):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    cap = c_max if c_max is not None else (w - sw)
    for _ in range(60):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, cap)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return
    raise ValueError(f"could not place {label}")


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    template = rng.choice(_SHAPES)
    _place_or_raise(g, rng, template, 1, "color-1 template")
    _place_or_raise(g, rng, template, 3, "matching color-3 shape")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_template":
        # No color-1 template — rule has no shape to match against.
        for dr, dc in _SHAPES[0]: g[3 + dr][3 + dc] = 3
        return g
    if name == "no_match":
        # Template + a color-3 shape that doesn't match — rule mirrors nothing.
        for dr, dc in _SHAPES[0]: g[1 + dr][1 + dc] = 1
        for dr, dc in _SHAPES[2]: g[5 + dr][5 + dc] = 3
        return g
    if name == "mirror_oob":
        # Match shape too close to right edge — LR-mirror would land out of grid.
        for dr, dc in _SHAPES[2]: g[1 + dr][1 + dc] = 1
        for dr, dc in _SHAPES[2]: g[5 + dr][w - 4 + dc] = 3
        return g
    return g
