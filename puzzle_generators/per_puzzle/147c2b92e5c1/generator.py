"""Generator for 14b:hard_95 — select holed object, rotate, scale 2x.

Rule: code value at row 0 (some non-bg cell). Body has multiple
shapes, exactly one with 1 hole. Output: that shape cropped, transformed
by code, scaled 2x.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_code, no_holed_object, multiple_holed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "147c2b92e5c1"
VERSION = "1.1.0"
TASK_ID = "147c2b92e5c1"
SUMMARY = "Code value in row 0 + 1 single-holed shape + 1-2 solid shapes."

INVARIANTS = [
    "background is 0",
    "row 0 has exactly one non-bg cell (the code value, in {1..7})",
    "body has 2-3 shapes, exactly one with a single hole",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_code", "no_holed_object", "multiple_holed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "11..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "row0_code_with_holed",
                       "valid": "row0_code_with_holed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_HOLED = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
]
_SOLID = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color, r_min=2):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(r_min, h - sh); c0 = rng.randint(0, w - sw)
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 15)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    code = rng.randint(1, 5)
    g[0][rng.randint(0, w - 1)] = code
    palette = rng.sample([c for c in [2, 3, 4, 6, 7, 8, 9] if c != code], 3)
    _place(g, rng, _HOLED[0], palette[0])
    for color in palette[1:]:
        _place(g, rng, rng.choice(_SOLID), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_code":
        # Body shapes but row 0 empty — rule's transform code
        # lookup fails.
        for dr, dc in _HOLED[0]: g[2 + dr][2 + dc] = 4
        for r, c in [(8, 8), (8, 9), (9, 9)]: g[r][c] = 6
        return g
    if name == "no_holed_object":
        # Code present but no holed shape — rule's "single holed
        # object" filter excludes everything.
        g[0][3] = 2
        for r, c in [(3, 3), (3, 4), (4, 3), (4, 4)]: g[r][c] = 4
        for r, c in [(8, 8), (8, 9), (9, 9)]: g[r][c] = 6
        return g
    if name == "multiple_holed":
        # Two holed shapes — rule's "single holed" tie-break
        # ambiguous.
        g[0][3] = 2
        for dr, dc in _HOLED[0]: g[2 + dr][1 + dc] = 4
        for dr, dc in _HOLED[0]: g[7 + dr][8 + dc] = 6
        return g
    return g
