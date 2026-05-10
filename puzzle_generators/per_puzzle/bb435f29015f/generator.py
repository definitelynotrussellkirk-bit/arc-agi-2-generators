"""Generator for arc_additional_puzzles_21_set21_bundle:E147 — Keep only largest object.

Rule: among all non-bg objects, keep the one with most cells (tie-break:
top-left). Erase everything else.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes (≥2 objects share max size → "largest" is
ambiguous, tie-break decides), single_object (only one object,
trivially largest → no candidate contrast), no_objects (grid is all
bg → rule's selector finds nothing, output equals input).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import RING_3X3

GENERATOR_ID = "bb435f29015f"
VERSION = "1.1.0"
TASK_ID = "bb435f29015f"
SUMMARY = "2-4 well-separated non-bg objects, with a unique largest."

INVARIANTS = [
    "2-4 distinct objects of different colors, each ≥3 cells",
    "exactly one object has the strictly largest cell count",
    "objects don't touch (separated by ≥1 bg cell on all sides)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_object", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "n_objs":            {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":     {"type": "str", "default": "ranked_objects_no_touch",
                          "valid": "ranked_objects_no_touch"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


SHAPES = [
    (5, [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]),  # T shape
    (5, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]),  # P shape
    (4, [(0, 0), (0, 1), (1, 0), (1, 1)]),          # 2x2
    (7, RING_3X3),
    (8, RING_3X3),
    (3, [(0, 0), (0, 1), (1, 0)]),
    (3, [(0, 0), (0, 1), (0, 2)]),
    (6, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]),
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_lo, n_hi = 2, 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_lo, n_hi = 3, 4
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_lo, n_hi = 2, 4
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_objs = rng.randint(n_lo, n_hi)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_objs)
    chosen = []
    sizes_used = set()
    while len(chosen) < n_objs:
        s, shape = rng.choice(SHAPES)
        if s in sizes_used:
            continue
        chosen.append((s, shape))
        sizes_used.add(s)
    occupied = [[False] * w for _ in range(h)]
    for (size, shape), color in zip(chosen, palette):
        sh = max(r for r, c in shape) + 1
        sw = max(c for r, c in shape) + 1
        placed = False
        for _ in range(60):
            r0 = rng.randint(1, h - sh - 1)
            c0 = rng.randint(1, w - sw - 1)
            if any(occupied[rr][cc]
                   for rr in range(r0 - 1, r0 + sh + 1)
                   for cc in range(c0 - 1, c0 + sw + 1)):
                continue
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
                occupied[r0 + dr][c0 + dc] = True
            for rr in range(r0 - 1, r0 + sh + 1):
                for cc in range(c0 - 1, c0 + sw + 1):
                    occupied[rr][cc] = True
            placed = True
            break
        if not placed:
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # Two objects share max size (4 cells each) — "largest" is
        # ambiguous; tie-break decides.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[1 + dr][1 + dc] = 3
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[6 + dr][6 + dc] = 6
        return g
    if name == "single_object":
        # Only one object — trivially largest, no contrast.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]:
            g[3 + dr][3 + dc] = 4
        return g
    if name == "no_objects":
        # No non-bg cells — rule's selector finds nothing.
        return g
    return g
