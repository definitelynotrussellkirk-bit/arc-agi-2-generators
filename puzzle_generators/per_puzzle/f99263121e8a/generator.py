"""Generator for 12b:m82 — stack cropped objects by left-to-right order.

Rule: sort components by leftmost column, then vertically stack their
bbox-crops with 1-row gaps (center-aligned by width).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, equal_leftmosts, single_component.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f99263121e8a"
VERSION = "1.1.0"
TASK_ID = "f99263121e8a"
SUMMARY = "3 small shapes in distinct colors, distinct leftmost columns."

INVARIANTS = [
    "background is 0",
    "exactly 3 connected components",
    "each component has a strictly distinct leftmost column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "equal_leftmosts", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "distinct_leftmost_columns",
                       "valid": "distinct_leftmost_columns"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
]


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 12)
    rng = ctx.draw_rng("layout")
    for _ in range(40):
        g = full_grid(h, w, 0)
        palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
        leftmosts = []
        ok = True
        for color in palette:
            placed = False
            for _ in range(60):
                shape = rng.choice(_SHAPES)
                sh = max(r for r, _ in shape) + 1
                sw = max(c for _, c in shape) + 1
                r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
                if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
                shape_left = min(c for _, c in shape)
                lc = c0 + shape_left
                if lc in leftmosts: continue
                for dr, dc in shape:
                    g[r0 + dr][c0 + dc] = color
                leftmosts.append(lc)
                placed = True; break
            if not placed: ok = False; break
        if ok and len(set(leftmosts)) == 3:
            return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_components":
        return g
    if name == "equal_leftmosts":
        # All components share leftmost column — sort order is ambiguous.
        for dr, dc in _SHAPES[0]: g[1 + dr][2 + dc] = 4
        for dr, dc in _SHAPES[0]: g[5 + dr][2 + dc] = 5
        for dr, dc in _SHAPES[0]: g[8 + dr][2 + dc] = 6
        return g
    if name == "single_component":
        # Only one component — rule's stack operation is trivial.
        for dr, dc in _SHAPES[0]: g[2 + dr][3 + dc] = 4
        return g
    return g
