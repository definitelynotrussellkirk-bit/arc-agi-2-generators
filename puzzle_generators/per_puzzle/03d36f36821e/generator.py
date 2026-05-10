"""Generator for 10b:m69 — crop component with most holes.

Rule: of the connected components, exactly one has the maximum number
of bg cells inside its bbox (holes). Output is that component cropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components (no objects → rule has nothing to crop);
tied_holes (two components share max holes → rule's "exactly one
max" precondition fails, selector ambiguous); all_solid (all
components are solid rectangles, hole count = 0 across all →
selector returns whichever rng picks first, no clear pattern).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "03d36f36821e"
VERSION = "1.1.0"
TASK_ID = "03d36f36821e"
SUMMARY = "2-3 components; exactly one has strictly the most bbox-interior bg cells."

INVARIANTS = [
    "background is 0",
    "2-3 isolated 4-connected components, distinct colors",
    "exactly one has strictly the most bbox-interior bg cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "tied_holes", "all_solid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "grid_w":            {"type": "int", "default": "rng 12..15", "valid": "11..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":     {"type": "str", "default": "components_with_holes",
                          "valid": "components_with_holes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOST_HOLES = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
     (1, 0), (1, 4),
     (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
     (3, 0), (3, 4),
     (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],  # 5x5 with 6 holes
    [(0, 0), (0, 1), (0, 2), (0, 3),
     (1, 0), (1, 3),
     (2, 0), (2, 1), (2, 2), (2, 3),
     (3, 0), (3, 3),
     (4, 0), (4, 1), (4, 2), (4, 3)],  # 5x4 with 4 holes
]
_FEWER_HOLES = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],  # 3x3 ring (1 hole)
    [(0, 0), (1, 0), (1, 1)],                                          # solid
    [(0, 0), (0, 1), (1, 0), (1, 1)],                                  # 2x2
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_others = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 1 + n_others)
    _place(g, rng, rng.choice(_MOST_HOLES), palette[0])
    for color in palette[1:]:
        _place(g, rng, rng.choice(_FEWER_HOLES), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — no components, nothing to crop.
        return g
    if name == "tied_holes":
        # Two components both have 6 holes (same 5x5 ring) — selector ambiguous.
        for dr, dc in _MOST_HOLES[0]:
            g[1 + dr][1 + dc] = 1
        for dr, dc in _MOST_HOLES[0]:
            if 1 + dr < h and 7 + dc < w:
                g[1 + dr][7 + dc] = 2
        return g
    if name == "all_solid":
        # All components solid — every component has 0 holes, no max.
        for r in range(2):
            for c in range(2):
                g[1 + r][1 + c] = 1
        for r in range(3):
            for c in range(3):
                g[5 + r][5 + c] = 2
        for r in range(2):
            for c in range(2):
                g[7 + r][10 + c] = 3
        return g
    return g
