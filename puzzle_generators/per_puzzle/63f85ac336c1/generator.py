"""Generator for next_b:m09 — fill component bounding boxes.

Rule: each connected component is replaced with a solid rectangle
filling its bbox (same color).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_solid, single_component, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "63f85ac336c1"
VERSION = "1.1.0"
TASK_ID = "63f85ac336c1"
SUMMARY = "2-4 partial-bbox components in same color (4)."

INVARIANTS = [
    "background is 0",
    "2-4 connected components (4-conn), all in color 4",
    "each does NOT fill its own bbox (so input != output)",
    "components' bboxes do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_solid", "single_component", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "bbox_isolated",
                       "valid": "bbox_isolated"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_PARTIALS = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)],
]


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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 4)
    used: set[tuple[int, int]] = set()
    for _ in range(n):
        for _ in range(40):
            shape = rng.choice(_PARTIALS)
            sh = max(r for r, _ in shape) + 1
            sw = max(c for _, c in shape) + 1
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bad = False
            for r in range(max(0, r0 - 1), min(h, r0 + sh + 1)):
                for c in range(max(0, c0 - 1), min(w, c0 + sw + 1)):
                    if (r, c) in used: bad = True; break
                if bad: break
            if bad: continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = 4
            for r in range(r0, r0 + sh):
                for c in range(c0, c0 + sw):
                    used.add((r, c))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "all_solid":
        # all components already solid rectangles → bbox-fill = identity, no contrast
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 4
        for r in range(7, 9):
            for c in range(7, 10):
                g[r][c] = 4
        return g
    if name == "single_component":
        # one partial-bbox component → no comparison, rule still applies trivially
        for r, c in [(3, 3), (3, 4), (4, 3)]:
            g[r][c] = 4
        return g
    if name == "no_components":
        # empty grid → no objects to bbox-fill
        return g
    return g
