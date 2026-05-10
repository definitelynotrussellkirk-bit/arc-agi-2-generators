"""Generator for 15b:hard_102 — select symmetric object, rotate, scale 2x.

Rule: code at (h-1, w-1). Among shapes whose crop is both LR- and UD-
symmetric, the largest is picked. Output: that crop transformed per
code, then upscaled 2x.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_symmetric (no LR+UD-symmetric component → rule's
selector finds nothing, output undefined), all_symmetric (every
component is symmetric → tie-break decides which is "largest"),
no_code (cell (h-1, w-1) is bg → transform is identity by default).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8801696784e1"
VERSION = "1.1.0"
TASK_ID = "8801696784e1"
SUMMARY = "Code at (h-1, w-1) + 1 4-fold-symmetric shape + 1 asymmetric shape."

INVARIANTS = [
    "background is 0",
    "cell (h-1, w-1) is a transform code in {1, 2, 3}",
    "exactly one component whose crop is both LR- and UD-symmetric",
    "1 other asymmetric component (smaller or non-symmetric)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_symmetric", "all_symmetric", "no_code")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "code_plus_sym_plus_asym",
                       "valid": "code_plus_sym_plus_asym"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SYMMETRIC = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
]
_ASYM = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
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
        r0 = rng.randint(0, h - sh - 1); c0 = rng.randint(0, w - sw - 1)
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([2, 4, 5, 6, 7, 8, 9], 2)
    code = rng.choice([1, 2, 3])
    g[h - 1][w - 1] = code
    _place(g, rng, rng.choice(_SYMMETRIC), palette[0])
    _place(g, rng, rng.choice(_ASYM), palette[1])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    g[h - 1][w - 1] = 1
    if name == "no_symmetric":
        # No LR+UD-symmetric component — rule's selector finds
        # nothing; output undefined.
        for dr, dc in _ASYM[0]: g[2 + dr][2 + dc] = 4
        for dr, dc in _ASYM[2]: g[2 + dr][7 + dc] = 6
        return g
    if name == "all_symmetric":
        # All components are LR+UD-symmetric — rule's "largest"
        # tie-break decides; selection ambiguous.
        for dr, dc in _SYMMETRIC[1]: g[2 + dr][2 + dc] = 4
        for dr, dc in _SYMMETRIC[2]: g[5 + dr][7 + dc] = 6
        return g
    if name == "no_code":
        # Cell (h-1, w-1) is bg — transform code missing; rule
        # defaults to identity transform.
        g[h - 1][w - 1] = 0
        for dr, dc in _SYMMETRIC[0]: g[2 + dr][2 + dc] = 4
        for dr, dc in _ASYM[1]: g[3 + dr][8 + dc] = 6
        return g
    return g
