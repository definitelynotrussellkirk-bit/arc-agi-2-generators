"""Generator for 17b:m119 — scale the only horizontally symmetric object.

Rule: of the connected components, exactly one's normalized binary
shape is left-right (horizontal) mirror symmetric. Output is that
shape scaled 2x in its color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_symmetric (no LR-symmetric component → rule's
selector finds nothing), all_symmetric (every component is LR-symmetric
→ "exactly one" precondition fails), single_motif (only one component
→ trivially the symmetric one, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "988bc6e81731"
VERSION = "1.1.0"
TASK_ID = "988bc6e81731"
SUMMARY = "2-3 components; exactly one is LR-mirror symmetric."

INVARIANTS = [
    "background is 0",
    "2-3 isolated 4-connected components, distinct colors",
    "exactly one's bbox-normalized binary shape is LR-mirror symmetric",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_symmetric", "all_symmetric", "single_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "one_sym_plus_distractors",
                       "valid": "one_sym_plus_distractors"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LR_SYM = [
    [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 3), (2, 0), (2, 3)],
]
_ASYM = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_asym = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 1 + n_asym)
    _place(g, rng, rng.choice(_LR_SYM), palette[0])
    for color in palette[1:]:
        _place(g, rng, rng.choice(_ASYM), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_symmetric":
        # No LR-symmetric component — rule's selector finds nothing.
        for dr, dc in _ASYM[0]: g[1 + dr][1 + dc] = 4
        for dr, dc in _ASYM[2]: g[5 + dr][7 + dc] = 6
        return g
    if name == "all_symmetric":
        # Every component is LR-symmetric → "exactly one" precondition
        # fails; rule's selector is ambiguous.
        for dr, dc in _LR_SYM[1]: g[1 + dr][1 + dc] = 4
        for dr, dc in _LR_SYM[2]: g[6 + dr][8 + dc] = 6
        return g
    if name == "single_motif":
        # Only one component — trivially the "the only" symmetric;
        # no contrast across candidates.
        for dr, dc in _LR_SYM[0]: g[3 + dr][5 + dc] = 7
        return g
    return g
