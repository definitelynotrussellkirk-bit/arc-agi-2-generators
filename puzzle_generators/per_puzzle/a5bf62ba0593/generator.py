"""Generator for 20b:hard_138 — select transform recolor and center stamp.

Rule: cells (0,0), (0,1), (0,2) hold selector color, transform code,
target color. Body has shapes; the shape with the selector color is
transformed by code, recolored to target, then center-stamped into a
7x7 canvas.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_header (cells (0,0..2) empty → rule has no
selector/code/target); selector_no_match (selector color refers to
no body shape → rule's lookup returns nothing); identity_transform
(transform code = 1 (identity) → output = recolored selector
shape only).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a5bf62ba0593"
VERSION = "1.1.0"
TASK_ID = "a5bf62ba0593"

SUMMARY = "Top row: selector + code + target color; body has 2-3 shapes incl. one matching selector."

INVARIANTS = [
    "background is 0",
    "cell (0,0) is the selector color (one of the body shape colors)",
    "cell (0,1) is the transform code (1-5)",
    "cell (0,2) is the target color (different from selector)",
    "body (rows 1-7) has 2-3 multi-cell shapes in distinct colors; one is selector color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_header", "selector_no_match", "identity_transform")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":            {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "header_with_body_shapes",
                          "valid": "header_with_body_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place_or_raise(g, rng, shape, color, label):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(60):
        r0 = rng.randint(1, min(7, h - sh)); c0 = rng.randint(0, w - sw)
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 4)
    selector, target_color = palette[0], palette[1]
    other_colors = palette[2:4]
    code = rng.randint(1, 5)
    g[0][0] = selector
    g[0][1] = code
    g[0][2] = target_color
    _place_or_raise(g, rng, rng.choice(_SHAPES), selector, f"selector ({selector})")
    for color in other_colors:
        _place_or_raise(g, rng, rng.choice(_SHAPES), color, f"other ({color})")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_header":
        # No header — rule has no selector/code/target.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[7 + dr][8 + dc] = 6
        return g
    if name == "selector_no_match":
        # Selector = 4 but body has no color-4 shape.
        g[0][0] = 4; g[0][1] = 2; g[0][2] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 7
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[7 + dr][8 + dc] = 8
        return g
    if name == "identity_transform":
        # Transform code = 1 — output is just the selector shape recolored.
        g[0][0] = 4; g[0][1] = 1; g[0][2] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[3 + dr][3 + dc] = 4
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[7 + dr][8 + dc] = 7
        return g
    return g
